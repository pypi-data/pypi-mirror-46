import sys
import os
import argparse
import json
import musicbrainzngs
import re
import errno
import io
import urllib
from twisted.internet import reactor, protocol, threads, defer, task
from twisted.web import client, http, error as weberror
from twisted.python import log
from mpd import MPDProtocol
from functools import partial
from kmpc.mpdfactory import MpdConnection
from kmpc.extra import KmpcHelpers
from kmpc.version import VERSION_STR

Helpers = KmpcHelpers()
client.HTTPClientFactory.noisy = False

class MpdParser(object):
    """The main class which queries mpd and dispatches events."""
    def __init__(self, args):
        self.mode = []
        # check what modes were specified, if none then do everything
        if (not args.artists and not args.releases and not args.recordings
                and not args.symlinks and not args.artistart):
            self.mode = ['artists','releases',
                    'recordings','symlinks','artistart']
        else:
            if args.artists:
                self.mode.append('artists')
            if args.releases:
                self.mode.append('releases')
            if args.recordings:
                self.mode.append('recordings')
            if args.symlinks:
                self.mode.append('symlinks')
            if args.artistart:
                self.mode.append('artistart')
        # these variables track what uuids we need to operate on
        self.queue = {}
        self.queue['artist'] = {}
        self.queue['release'] = {}
        self.queue['recording'] = {}
        self.queue['artistsymlink'] = {}
        self.queue['artistart'] = {}
        self.args = args
        # seconds to wait before next http query (so we don't get blocked)
        self.waittime = 0
        # how many tasks are left to wait on
        self.waitleft = 0
        # how many mpd queries are left to wait on
        self.mpdqueries = 0
        log.startLogging(sys.stdout)
        log.msg("Starting MpdParser with mode "+format(self.mode))
        musicbrainzngs.set_useragent(
                "kmpc",
                VERSION_STR,
                'https://gitlab.com/eratosthene/kmpc')
        self.mpdconnection = MpdConnection(
                args.ip, args.port,
                None, [self.dispatch], True, False)

    def dispatch(self, conn):
        """Start the callback chain for each mode."""
        if 'artists' in self.mode:
            Helpers.mkdir_p(os.path.join(self.args.cachepath,'artist'))
            # if --artistid specified, operate only on that list
            if self.args.artistid:
                d = defer.Deferred()
                d.addCallback(partial(self.handle_list,'artist'))
                d.addErrback(log.err)
                d.callback(self.args.artistid.split(','))
            else:
                (self.mpdconnection.protocol.
                        list('musicbrainz_artistid').
                        addCallback(partial(self.handle_list,'artist')).
                        addErrback(self.mpdconnection.handle_mpd_error))
                self.mpdqueries += 1
        if 'releases' in self.mode:
            Helpers.mkdir_p(os.path.join(self.args.cachepath,'release'))
            # if --releaseid specified, operate only on that list
            if self.args.releaseid:
                d = defer.Deferred()
                d.addCallback(partial(self.handle_list,'release'))
                d.addErrback(log.err)
                d.callback(self.args.releaseid.split(','))
            else:
                (self.mpdconnection.protocol.
                        list('musicbrainz_albumid').
                        addCallback(partial(self.handle_list,'release')).
                        addErrback(self.mpdconnection.handle_mpd_error))
                self.mpdqueries += 1
        if 'recordings' in self.mode:
            Helpers.mkdir_p(os.path.join(self.args.cachepath,'recording'))
            # if --recordingid specified, operate only on that list
            if self.args.recordingid:
                d = defer.Deferred()
                d.addCallback(partial(self.handle_list,'recording'))
                d.addErrback(log.err)
                d.callback(self.args.recordingid.split(','))
            else:
                (self.mpdconnection.protocol.
                        list('musicbrainz_trackid').
                        addCallback(partial(self.handle_list,'recording')).
                        addErrback(self.mpdconnection.handle_mpd_error))
                self.mpdqueries += 1
        if 'symlinks' in self.mode:
            Helpers.mkdir_p(os.path.join(self.args.cachepath,'artist_by_name'))
            # if --artistid specified, operate only on that list
            if self.args.artistid:
                d = defer.Deferred()
                d.addCallback(self.handle_symlink_list)
                d.addErrback(log.err)
                d.callback(self.args.artistid.split(','))
            else:
                (self.mpdconnection.protocol.
                        list('musicbrainz_artistid').
                        addCallback(self.handle_symlink_list).
                        addErrback(self.mpdconnection.handle_mpd_error))
                self.mpdqueries += 1
            self.waitleft += 1
        if 'artistart' in self.mode:
            Helpers.mkdir_p(os.path.join(self.args.cachepath,'artist'))
            # if --artistid specified, operate only on that list
            if self.args.artistid:
                d = defer.Deferred()
                d.addCallback(self.handle_art_list)
                d.addErrback(log.err)
                d.callback(self.args.artistid.split(','))
            else:
                (self.mpdconnection.protocol.
                        list('musicbrainz_artistid').
                        addCallback(self.handle_art_list).
                        addErrback(self.mpdconnection.handle_mpd_error))
                self.mpdqueries += 1

    def check_exit(self, *args):
        """Decrements the task counter, then exits if 0."""
        self.waitleft -= 1;
        log.msg("check_exit: "+str(self.waitleft)+" tasks left")
        if self.waitleft < 1:
            reactor.stop()

    def handle_list(self, qtype, result):
        """Parses the results of an mpd query and acts on it."""
        for row in result:
            # MB tags can have more than one uuid separated by /
            for uuid in str(row).split('/'):
                if len(uuid) > 0 and uuid not in self.queue[qtype]:
                    checkpath = Helpers.jpath(self.args.cachepath, uuid, qtype)
                    # only query if file doesn't exist or we are ignoring it
                    if self.args.ignorecache or not os.path.isfile(checkpath):
                        # add uuid to the queue so it only gets scheduled once
                        self.queue[qtype][uuid] = 1
                        log.msg("Scheduling MB query for "+qtype+" "+uuid+
                                " in "+str(self.waittime)+" seconds")
                        reactor.callLater(self.waittime, self.query_mb,
                                uuid, qtype)
                        self.waittime += 1
                        self.waitleft += 1
        # disconnect mpd after all queries are complete
        self.mpdqueries -= 1
        if self.mpdqueries < 1:
            self.mpdconnection.reactor.disconnect()
        # if we got all the way here and didn't do anything, we're done
        if self.waitleft == 0:
            self.check_exit()

    def handle_symlink_list(self, result):
        """Creates symlinks from an artist's readable name to their artistid."""
        for row in result:
            # MB tags can have more than one uuid separated by /
            for uuid in str(row).split('/'):
                checkpath = Helpers.jpath(self.args.cachepath, uuid, 'artist')
                if len(uuid) > 0 and os.path.isfile(checkpath):
                    # open the artist json file and parse it
                    with open(checkpath, 'r') as infile:
                        data = json.load(infile)
                        # create a UTF-8, os-safe name/sort_name to symlink to
                        name = (u''.join(data['artist']['name'])
                                .encode('utf-8').strip().replace(os.sep, '_'))
                        sort_name = (u''.join(data['artist']['sort-name'])
                                .encode('utf-8').strip().replace(os.sep, '_'))
                        if uuid not in self.queue['artistsymlink']:
                            # add uuid to the queue so it only gets scheduled
                            # once
                            self.queue['artistsymlink'][uuid] = 1
                            log.msg(u"Creating symlink for ["+
                                    name+"] ["+sort_name+"]")
                            try:
                                # symlink to name, ignoring errors
                                os.symlink(
                                        os.path.join('..', 
                                                'artist',
                                                Helpers.upath(uuid)),
                                        os.path.join(self.args.cachepath,
                                                'artist_by_name',
                                                name))
                            except OSError:
                                pass
                            try:
                                # symlink to sort_name, ignoring errors
                                os.symlink(
                                        os.path.join('..',
                                                'artist',
                                                Helpers.upath(uuid)),
                                        os.path.join(self.args.cachepath,
                                                'artist_by_name',
                                                sort_name))
                            except OSError:
                                pass
        # disconnect mpd after all queries are complete
        self.mpdqueries -= 1
        if self.mpdqueries < 1:
            self.mpdconnection.reactor.disconnect()
        self.check_exit()

    def query_mb(self, uuid, qtype, *args):
        """Query musicbrainz in a separate thread."""
        if qtype == 'artist':
            d = threads.deferToThread(musicbrainzngs.get_artist_by_id, uuid)
            d.addCallback(partial(self.handle_query_mb_artist, uuid))
        elif qtype == 'release':
            d = threads.deferToThread(musicbrainzngs.get_release_by_id, uuid,
                    includes=["recordings","release-groups","artists"])
            d.addCallback(partial(self.handle_query_mb_release, uuid))
        elif qtype == 'recording':
            d = threads.deferToThread(musicbrainzngs.get_recording_by_id, uuid, 
                    includes=["artists","releases"])
            d.addCallback(partial(self.handle_query_mb_recording, uuid))
        self.waittime -= 1

    def handle_query_mb_artist(self, artist_id, mbres):
        """Write the artist data to a json file."""
        name = u''.join(mbres['artist']['name']).encode('utf-8').strip()
        sort_name = (u''.join(mbres['artist']['sort-name'])
                .encode('utf-8').strip())
        # TODO: for some reason we still get ascii exceptions sometimes
        log.msg(u"Found artist ["+name+"] ["+
                sort_name+"]")
        Helpers.mkdir_p(Helpers.expath(self.args.cachepath,
                artist_id, 'artist'))
        with open(Helpers.jpath(self.args.cachepath,
                artist_id, 'artist'), 'w') as outfile:
            json.dump(mbres, outfile)
        self.check_exit()

    def handle_query_mb_release(self, release_id, mbres):
        """Write the release data to a json file."""
        title = u''.join(mbres['release']['title']).encode('utf-8').strip()
        # TODO: for some reason we still get ascii exceptions sometimes
        log.msg(u"Found release ["+title+"] "+str(self.waitleft-1)+"}")
        Helpers.mkdir_p(Helpers.expath(self.args.cachepath,
                release_id, 'release'))
        with open(Helpers.jpath(self.args.cachepath,
                release_id, 'release'), 'w') as outfile:
            json.dump(mbres, outfile)
        self.check_exit()

    def handle_query_mb_recording(self, recording_id, mbres):
        """Write the recording data to a json file."""
        title = u''.join(mbres['recording']['title']).encode('utf-8').strip()
        # TODO: for some reason we still get ascii exceptions sometimes
        log.msg(u"Found recording ["+title+"] "+str(self.waitleft-1)+"}")
        Helpers.mkdir_p(Helpers.expath(self.args.cachepath,
                recording_id, 'recording'))
        with open(Helpers.jpath(self.args.cachepath,
                recording_id, 'recording'), 'w') as outfile:
            json.dump(mbres, outfile)
        self.check_exit()

    def handle_art_list(self, result):
        """Download artwork for all artists."""
        self.mpdqueries -= 1
        if self.mpdqueries < 1:
            self.mpdconnection.reactor.disconnect()
        for row in result:
            for uuid in str(row).split('/'):
                if len(uuid) > 0:
                    # add to queue so it only gets scheduled once
                    self.queue['artistart'][uuid] = 1
        artists = self.queue['artistart'].keys()
        artists.sort()
        log.msg("Downloading art for "+str(len(artists))+" artists")
        fanarturl = "http://webservice.fanart.tv/v3/music/"
        apikey = "406b2a5af85c14b819c1c6332354b313"
        for uuid in artists:
            self.waitleft += 1
            furl = fanarturl+uuid+"?api_key="+apikey
            log.msg("scheduling fanart.tv query for "+uuid+" in "+
                    str(self.waittime)+" seconds")
            d = task.deferLater(reactor, self.waittime, client.getPage, furl)
            self.waittime += 1
            d.addCallback(partial(self.handle_agent_response, uuid))
            # trap 404 errors so they don't get displayed
            d.addErrback(self.ignore_404).addErrback(log.err)
        # if we got all the way here and didn't do anything, we're done
        if self.waitleft == 0:
            self.check_exit()

    def ignore_404(self, f):
        """Ignores 404 errors and decrements the task counter."""
        r = f.trap(weberror.Error)
        self.waittime -= 1
        self.check_exit()
        if f.value.status != '404':
            return f

    def handle_agent_response(self, uuid, body):
        """Parses json response from fanart.tv."""
        d = json.loads(body)
        log.msg(u"Found artist "+d['name'])
        if 'hdmusiclogo' in d:
            for idx, img in enumerate(d['hdmusiclogo']):
                self.check_file_download(uuid, img,
                        'logo', 'png')
        if 'musiclogo' in d:
            for idx, img in enumerate(d['musiclogo']):
                self.check_file_download(uuid, img,
                        'logo', 'png')
        if 'artistbackground' in d:
            for idx, img in enumerate(d['artistbackground']):
                self.check_file_download(uuid, img,
                        'artistbackground', 'jpg')
        self.waittime -= 1
        self.check_exit()

    def handle_download_file_response(self, filepath, trim, body):
        """Writes downloaded image to disk."""
        log.msg("Writing to "+filepath)
        file = open(filepath, "wb")
        file.write(body)
        file.close()
        # if this is an artist logo, trim any extra transparent space
        if trim:
            log.msg("trimming file")
            Helpers.trim_image(filepath)
        self.waittime -= 1
        self.check_exit()

    def check_file_download(self, uuid, img, arttype, ext):
        """Checks for an existing image file, downloading it if necessary."""
        fp = os.path.join(Helpers.artexpath(uuid, self.args.cachepath, arttype),
                img['id']+"."+ext)
        log.msg("Checking for "+fp)
        self.waitleft += 1
        Helpers.mkdir_p(Helpers.artexpath(uuid, self.args.cachepath, arttype))
        # only download if file doesn't exist or we are ignoring cache
        if self.args.ignorecache or not os.path.isfile(fp):
            log.msg("Scheduling download of "+arttype+" "+img['id']+
                    " in "+str(self.waittime)+" seconds")
            log.msg("from "+str(img['url']))
            d = task.deferLater(reactor, self.waittime, client.getPage,
                    str(img['url']))
            self.waittime += 1
            d.addCallback(partial(self.handle_download_file_response,
                    fp, (arttype == 'logo')))
            # trap 404 errors so they don't get displayed
            d.addErrback(self.ignore_404).addErrback(log.err)


def main_app():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip",
            help="ip address or hostname of mpd server (default 127.0.0.1)",
            default="127.0.0.1")
    parser.add_argument("-p", "--port",
            help="port of mpd server (default 6600)",
            default="6600")
    parser.add_argument("-c", "--cachepath",
            help="directory to save mb cach (default ~/.kmpc/mb-cache)",
            default=os.path.expanduser('~/.kmpc/mb-cache'))
    parser.add_argument("--artists",
            help="scan artists", action="store_true")
    parser.add_argument("--releases",
            help="scan releases", action="store_true")
    parser.add_argument("--recordings",
            help="scan recordings", action="store_true")
    parser.add_argument("--symlinks",
            help="create artist symlinks", action="store_true")
    parser.add_argument("--artistart",
            help="download artist backgrounds and logos", action="store_true")
    parser.add_argument("--ignorecache",
            help="ignore existing cache, rescan everything",
            action="store_true")
    parser.add_argument("--artistid",
            help="comma-delimited list of artistids to operate on")
    parser.add_argument("--releaseid",
            help="comma-delimited list of releaseids to operate on")
    parser.add_argument("--recordingid",
            help="comma-delimited list of recordingids to operate on")
    args = parser.parse_args()
    print format(args)
    mpdparser = MpdParser(args)
    reactor.run()

if __name__ == "__main__":
    main_app()
