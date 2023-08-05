import sys
import argparse
from twisted.internet import reactor,protocol
from twisted.python import log
from mpd import MPDProtocol
from kmpc.mpdfactory import MpdConnection

class MessageHandler(object):
    """Handles mpd messages."""
    def __init__(self, mpdconnection, error_handler):
        self.mpdconnection = mpdconnection
        self.handle_mpd_error = error_handler
        self.uri = None
        self.rating = None
        self.rid = None

    def handle_mpd_message(self, result):
        """Gets current rating and recordingid for a song."""
        for m in result:
            self.uri= m['message']
            log.msg("Rating changed for "+self.uri)
            (self.mpdconnection.protocol.sticker_get('song',self.uri,'rating').
                    addCallback(self.handle_sticker_get).
                    addErrback(self.handle_mpd_error))
            (self.mpdconnection.protocol.lsinfo(self.uri).
                    addCallback(self.handle_lsinfo).
                    addErrback(self.handle_mpd_error))

    def handle_lsinfo(self, result):
        """Finds all songs with the same recordingid."""
        for r in result:
            if 'musicbrainz_trackid' in r:
                self.rid=r['musicbrainz_trackid']
                log.msg('found recording id '+self.rid)
                (self.mpdconnection.protocol.find('MUSICBRAINZ_TRACKID',self.rid).
                        addCallback(self.handle_find).
                        addErrback(self.handle_mpd_error))

    def handle_find(self, result):
        """Sets rating for a song if it has the same recordingid."""
        for r in result:
            f = r['file']
            if f != self.uri:
                if self.rating is not None:
                    log.msg("Setting rating for "+f+" to "+self.rating)
                    self.mpdconnection.protocol.sticker_set('song',f,'rating',self.rating)
                else:
                    log.msg("Rating not yet set, debug race condition")

    def handle_sticker_get(self, result):
        """Stores rating for a song."""
        log.msg("found rating "+format(result))
        self.rating = format(result)

class MpdRatingSync(object):
    """Main application class."""
    def __init__(self, args):
        log.startLogging(sys.stdout)
        self.mpdconnection = MpdConnection(
                args.ip, args.port,
                self.mpd_idle_handler,
                [self.subscribe_to_channel],
                True,True)

    def mpd_idle_handler(self, result):
        """Dispatches MessageHandler on incoming messages."""
        for s in result:
            if format(s) == 'message':
                log.msg('Event on subsystem '+format(s))
                mh = MessageHandler(self.mpdconnection,
                        self.mpdconnection.handle_mpd_error)
                (self.mpdconnection.protocol.readmessages().
                        addCallback(mh.handle_mpd_message).
                        addErrback(self.mpdconnection.handle_mpd_error))

    def subscribe_to_channel(self, conn):
        """Subscribes to ratingchange channel."""
        log.msg("subscribing to ratingchange")
        self.mpdconnection.protocol.subscribe("ratingchange")

def main_app():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip",
            help="ip address or hostname of mpd server (default 127.0.0.1)",
            default='127.0.0.1')
    parser.add_argument("-p", "--port",
            help="port of mpd server (default 6600)",
            default='6600')
    args = parser.parse_args()
    mpdratingsync = MpdRatingSync(args)
    reactor.run()

if __name__ == "__main__":
    main_app()