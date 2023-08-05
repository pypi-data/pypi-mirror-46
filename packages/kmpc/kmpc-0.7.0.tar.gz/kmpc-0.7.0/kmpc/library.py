from copy import deepcopy
from functools import partial
import os

from twisted.internet.defer import Deferred, DeferredList
import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.logger import Logger
from twisted.internet.defer import inlineCallbacks
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.factory import Factory

from kmpc.extra import KmpcHelpers
from kmpc.widgets import BaseLabel

# make sure we are on updated version of kivy
kivy.require('1.10.0')

Helpers = KmpcHelpers()


class LibraryScreen(Screen):
    """The Library screen, for browsing through mpd's library."""

    # set some initial variables
    current_view = {
            'value': 'root',
            'base': '/',
            'info': {'type': 'uri'}}
    library_selection = {}

    def enter_screen(self, *args):
        ss = self.ids.ss
        ss.ids.librarybutton.state = 'down'
        ss.ids.librarybutton.disabled = True

    def change_view_type(self, value):
        """Callback when user presses one of the Library view buttons."""
        Logger.info("Library: View changed to "+value)
        app = App.get_running_app().root
        # make sure nothing is selected in the recyclebox
        self.rbl.clear_selection()
        # the button state things sort of implement a tabbed view without it
        # being a tabbedview so there doesn't have to be a separate recyclebox
        # for each view type
        # probably a more elegant way of doing this
        if value == 'Files':
            self.current_view = {
                    'value': 'root',
                    'base': '/',
                    'info': {'type': 'uri'}}
            (app.mpdconnection.protocol.
                lsinfo(self.current_view['base']).
                addCallback(self.reload_view).
                addErrback(app.mpdconnection.handle_mpd_error))
        elif value == 'Albums':
            self.current_view = {
                    'value': 'All Album Artists',
                    'base': 'All Album Artists',
                    'info': {'type': 'rootalbums'}}
            (app.mpdconnection.protocol.
                list('albumartistsort').
                addCallback(self.reload_view).
                addErrback(app.mpdconnection.handle_mpd_error))
        elif value == 'Tracks':
            self.current_view = {
                    'value': 'All Track Artists',
                    'base': 'All Track Artists',
                    'info': {'type': 'roottracks'}}
            (app.mpdconnection.protocol.
                list('artistsort').
                addCallback(self.reload_view).
                addErrback(app.mpdconnection.handle_mpd_error))
        elif value == 'Playlists':
            self.current_view = {
                    'value': 'All Playlists',
                    'base': 'All Playlists',
                    'info': {'type': 'playlist'}}
            (app.mpdconnection.protocol.
                listplaylists().
                addCallback(self.reload_view).
                addErrback(app.mpdconnection.handle_mpd_error))

    def render_row(self, r, has_sticker, result):
        rr = deepcopy(r)
        if has_sticker:
            rr['copy_flag'] = str(result)
        else:
            rr['copy_flag'] = ''
        (App.get_running_app().root.mpdconnection.protocol.
            sticker_get('song', rr['base'], 'rating').
            addCallback(partial(self.render_row2, rr, True)).
            addErrback(partial(self.render_row2, rr, False)))

    def render_row2(self, r, has_sticker, result):
        rr = deepcopy(r)
        if has_sticker:
            rr['rating'] = str(result)
        else:
            rr['rating'] = ''
        self.rv.data.append(rr)

    def reload_view(self, result):
        """Callback that loads library data from mpd into the recyclebox."""
        Logger.info("Library: reload_view() current type: "
                    + self.current_view['info']['type'])
        # clear all current recycleview data
        self.rv.data = []
        if self.current_view['info']['type'] == 'uri':
            # file-based browsing uses uri types
            if self.current_view['base'] != '/':
                # if we aren't at the base of the filesystem, allow browsing to
                # parent folder
                hbase, tbase = os.path.split(self.current_view['base'])
                b1, b2 = os.path.split(hbase)
                if b2 == '':
                    b2 = 'root'
                upbase = os.path.normpath(
                        os.path.join(self.current_view['base'], '..'))
                if upbase == '.':
                    upbase = '/'
                r = {'value': "up to "+b2,
                     'base': upbase,
                     'info': {'type': 'uri'},
                     'copy_flag': '',
                     'rating': ''}
                self.rv.data.append(r)
                self.current_header.text = tbase
            else:
                # at filesystem base
                self.current_header.text = 'All Files'
        elif self.current_view['info']['type'] == 'albumartistsort':
            # inside a particular album artist, allow browsing to root
            r = {'value': 'up to All Album Artists',
                 'base': 'All Album Artists',
                 'info': {'type': 'rootalbums'},
                 'copy_flag': '',
                 'rating': ''}
            self.rv.data.append(r)
            self.current_header.text = self.current_view['base']
        elif self.current_view['info']['type'] == 'album':
            # inside a particular album, allow browsing to album artist
            v = self.current_view['info']['albumartistsort']
            r = {'value': v,
                 'base': self.current_view['info']['albumartistsort'],
                 'info': {'type': 'albumartistsort'},
                 'copy_flag': '',
                 'rating': ''}
            self.rv.data.append(r)
            self.current_header.text = self.current_view['base']
        elif self.current_view['info']['type'] == 'artistsort':
            # inside a particular artist, allow browsing to root
            r = {'value': 'up to All Track Artists',
                 'base': 'All Track Artists',
                 'info': {'type': 'roottracks'},
                 'copy_flag': '',
                 'rating': ''}
            self.rv.data.append(r)
            self.current_header.text = self.current_view['base']
        else:
            # something else?
            self.current_header.text = self.current_view['base']
        # loop through the rows mpd returned and add them to the recycleview
        for row in result:
            if 'playlist' in row:
                # we found a playlist, display it
                if self.current_view['info']['type'] != 'uri':
                    Logger.debug("Library: playlist found = "+row['playlist'])
                    r = {'value': row['playlist'],
                         'base': row['playlist'],
                         'info': {'type': 'playlist'},
                         'copy_flag': '',
                         'rating': ''}
                    self.rv.data.append(r)
            elif 'directory' in row:
                # we found a directory, format and display it
                Logger.debug(
                        "Library: directory found: ["+row['directory']+"]")
                b1, b2 = os.path.split(row['directory'])
                r = {'value': b2,
                     'base': row['directory'],
                     'info': {'type': 'uri'},
                     'copy_flag': '',
                     'rating': ''}
                self.rv.data.append(r)
            elif 'file' in row:
                # we found a song, format and display it
                Logger.debug("FileBrowser: file found: ["+row['file']+"]")
                r = {'value': Helpers.formatsong(row),
                     'base': row['file'],
                     'info': {'type': 'file'}}
                (App.get_running_app().root.mpdconnection.protocol.
                    sticker_get('song', row['file'], 'copy_flag').
                    addCallback(partial(self.render_row, r, True)).
                    addErrback(partial(self.render_row, r, False)))
            else:
                # we found something else, figure out what it is based on our
                # current view type
                if self.current_view['info']['type'] == 'rootalbums':
                    # we found an album artist, display it
                    Logger.debug("Library: album artist found: ["+row+"]")
                    r = {'value': row,
                         'base': row,
                         'info': {'type': 'albumartistsort'},
                         'copy_flag': '',
                         'rating': ''}
                    self.rv.data.append(r)
                elif self.current_view['info']['type'] == 'albumartistsort':
                    # we found an album, display it
                    Logger.debug("Library: album found: ["+row+"]")
                    v = self.current_view['base']
                    r = {'value': row,
                         'base': row,
                         'info': {'type': 'album',
                                  'albumartistsort': v},
                         'copy_flag': '',
                         'rating': ''}
                    self.rv.data.append(r)
                elif self.current_view['info']['type'] == 'roottracks':
                    # we found an artist, display it
                    Logger.debug("Library: track artist found: ["+row+"]")
                    r = {'value': row,
                         'base': row,
                         'info': {'type': 'artistsort'},
                         'copy_flag': '',
                         'rating': ''}
                    self.rv.data.append(r)
                elif self.current_view['info']['type'] == 'artistsort':
                    # we found a track, display it
                    # note that tracks are not parsed by Helpers.formatsong
                    # like filenames are; mpd formats a track itself
                    Logger.debug("Library: track found: ["+row+"]")
                    r = {'value': row,
                         'base': row,
                         'info': {'type': 'track',
                                  'artistsort': self.current_view['base']},
                         'copy_flag': '',
                         'rating': ''}
                    self.rv.data.append(r)
                else:
                    # shouldn't ever see this, but y'know, whatever
                    Logger.warn("Library: "
                                + "not sure what to do with ["+format(row)+"]")

    def handle_long_touch(self, row, index):
        """Callback for handling long touches in the recycleview."""
        Logger.debug("Library: handle_long_touch("+format(row)+")")
        app = App.get_running_app().root
        # load up the selected row as the current view, then display it
        self.current_view = deepcopy(row)
        if row['info']['type'] == 'uri':
            # selected a directory
            (app.mpdconnection.protocol.
                lsinfo(row['base']).
                addCallback(self.reload_view).
                addErrback(app.mpdconnection.handle_mpd_error))
        elif row['info']['type'] == 'rootalbums':
            # selected an album artist
            (app.mpdconnection.protocol.
                list('albumartistsort').
                addCallback(self.reload_view).
                addErrback(app.mpdconnection.handle_mpd_error))
        elif row['info']['type'] == 'albumartistsort':
            # selected an album
            (app.mpdconnection.protocol.
                list('album', 'albumartistsort', row['base']).
                addCallback(self.reload_view).
                addErrback(app.mpdconnection.handle_mpd_error))
        elif row['info']['type'] == 'album':
            # selected an album track
            (app.mpdconnection.protocol.
                find('album',
                     row['base'],
                     'albumartistsort',
                     row['info']['albumartistsort']).
                addCallback(self.reload_view).
                addErrback(app.mpdconnection.handle_mpd_error))
        elif row['info']['type'] == 'roottracks':
            # selected an artist
            (app.mpdconnection.protocol.
                list('artistsort').
                addCallback(self.reload_view).
                addErrback(app.mpdconnection.handle_mpd_error))
        elif row['info']['type'] == 'artistsort':
            # selected a track
            (app.mpdconnection.protocol.
                list('title', 'artistsort', row['base']).
                addCallback(self.reload_view).
                addErrback(app.mpdconnection.handle_mpd_error))
        elif row['info']['type'] == 'playlist':
            # selected a playlist, go ahead and load it up and play it
            app.mpdconnection.protocol.clear()
            app.mpdconnection.protocol.load(row['base'])
            app.mpdconnection.protocol.play('0')
        elif row['info']['type'] == 'file':
            # selected a file, append it to the queue and play from there
            app.mpdconnection.protocol.clear()
            a, b = os.path.split(row['base'])
            app.mpdconnection.protocol.add(a)
            (app.mpdconnection.protocol.
                play(str(int(index)-1)))
        else:
            # should never see this
            Logger.warn("Library: long-touch for ["
                        + format(row)+"] not implemented")

    def browser_queue_popup(self):
        """Callback when user presses the 'Q' button."""
        browserQueuePopup = Factory.BrowserQueuePopup()
        browserQueuePopup.open()

    def browser_add_find(self, result):
        """Callback for appending a bunch of tracks to the queue."""
        for rrow in result:
            App.get_running_app().root.mpdconnection.protocol.add(rrow['file'])

    def browser_add_find_one(self, result):
        """Callback for appending one track to the queue."""
        # since mpd always returns a list, just do the first one then break
        for rrow in result:
            App.get_running_app().root.mpdconnection.protocol.add(rrow['file'])
            break

    def browser_add(self, clearfirst, insert, p):
        """Callback when user appends to/inserts into/replaces the queue."""
        Logger.info('Library: browser_add('+str(clearfirst)+')')
        app = App.get_running_app().root
        # if !, clear the queue
        if clearfirst:
            Logger.info('Library: Clearing queue')
            App.get_running_app().root.mpdconnection.protocol.clear()
        # loop through the recyclebox and add each selected node
        for index in self.rbl.selected_nodes:
            row = self.rv.data[index]
            mtype = row['info']['type']
            Logger.info("Library: Adding "+mtype+" '"
                        + row['base']+"' to current queue")
            if mtype == 'uri' or mtype == 'file':
                if insert and app.currsong:
                    # if >, insert the song/directory after the currently
                    # playing song
                    app.mpdconnection.protocol.addid(
                            row['base'],
                            str(int(app.currsong)+1))
                    app.mpdconnection.protocol.prio(
                            '5',
                            str(int(app.currsong)+1),
                            str(int(app.currsong)+1))
                else:
                    # append the song/directory to the queue
                    (app.mpdconnection.protocol.
                        add(row['base']))
            elif mtype == 'albumartistsort':
                # append all tracks by a particular album artist
                (app.mpdconnection.protocol.
                    find(mtype, row['base']).
                    addCallback(self.browser_add_find).
                    addErrback(app.mpdconnection.handle_mpd_error))
            elif mtype == 'album':
                # append all tracks on a particular album
                (app.mpdconnection.protocol.
                    find(mtype,
                         row['base'],
                         'albumartistsort',
                         row['info']['albumartistsort']).
                    addCallback(self.browser_add_find).
                    addErrback(app.mpdconnection.handle_mpd_error))
            elif mtype == 'artistsort':
                # append all tracks by a particular artist
                (app.mpdconnection.protocol.
                    find(mtype, row['base']).
                    addCallback(self.browser_add_find).
                    addErrback(app.mpdconnection.handle_mpd_error))
            elif mtype == 'track':
                # append a particular artist's specific track
                # currently just adds the first match that mpd finds
                (app.root.mpdconnection.protocol.
                    find('artistsort',
                         row['info']['artistsort'],
                         'title',
                         row['base']).
                    addCallback(self.browser_add_find_one).
                    addErrback(app.mpdconnection.handle_mpd_error))
            elif mtype == 'playlist':
                # append a playlist
                (app.mpdconnection.protocol.
                    load(row['base']))
            else:
                # should never see this
                Logger.warning("Library: "+mtype+' not implemented')
        # clear the currently selected rows after doing the above work
        self.rbl.clear_selection()
        # close the popup
        p.dismiss()

    def browser_delete(self):
        """Callback when user presses the delete playlist button."""
        app = App.get_running_app().root
        for index in self.rbl.selected_nodes:
            plname = self.rv.data[index]['base']
            Logger.info("Library: deleting playlist "+plname)
            (app.mpdconnection.protocol.
                rm(plname).
                addErrback(app.mpdconnection.handle_mpd_error))
            self.current_view = {
                    'value': 'All Playlists',
                    'base': 'All Playlists',
                    'info': {'type': 'playlist'}}
            (app.mpdconnection.protocol.
                listplaylists().
                addCallback(self.reload_view).
                addErrback(app.mpdconnection.handle_mpd_error))
        self.rbl.clear_selection()

    def popup_generate(self):
        """Callback when user presses the Generate button."""
        generatePopup = Factory.GeneratePopup()
        generatePopup.open()

    def update_generate_text(self, p):
        """Callback when user changes the generate spinners."""
        stars = p.ids.ratings_spinner.text
        op = p.ids.operation_spinner.text
        if stars == 'None':
            p.ids.playlist_name.text = 'No Stars'
        elif op == '<':
            p.ids.playlist_name.text = 'Less Than '+stars+'-Star'
        elif op == '<=':
            p.ids.playlist_name.text = stars+'-Star or Less'
        elif op == '=':
            p.ids.playlist_name.text = stars+'-Star'
        elif op == '>=':
            p.ids.playlist_name.text = stars+'-Star or More'
        elif op == '>':
            p.ids.playlist_name.text = 'More Than '+stars+'-Star'

    def generate_list(self, ltype, p):
        """Callback when user presses Generate Synclist or Generate Playlist."""
        stars = p.ids.ratings_spinner.text
        op = p.ids.operation_spinner.text
        pname = p.ids.playlist_name.text
        Logger.info('Library: generating list with stars '+op+' '+str(stars))
        app = App.get_running_app().root
        self.tlist = {}
        if p.ids.ratings_spinner.text != 'None':
            (app.mpdconnection.protocol.
                sticker_find('song', '', 'rating').
                addCallback(partial(self.generate_play_list, ltype, p)).
                addErrback(app.mpdconnection.handle_mpd_error))
        else:
            Logger.info('Library: cannot generate when stars = None')
            p.dismiss()

    def generate_play_list(self, ltype, p, result):
        """Second part of generate list callback."""
        Logger.debug("Library: generate_play_list: generating list "+ltype)
        app = App.get_running_app().root
        stars = p.ids.ratings_spinner.text
        op = p.ids.operation_spinner.text
        pname = p.ids.playlist_name.text
        for row in result:
            rating = row['sticker'].split('=')[1]
            uri = row['file']
            if ((op == '<' and int(rating) < int(stars)) or
                    (op == '<=' and int(rating) <= int(stars)) or
                    (op == '=' and int(rating) == int(stars)) or
                    (op == '>=' and int(rating) >= int(stars)) or
                    (op == '>' and int(rating) > int(stars))):
                Logger.debug("generate_play_list: rating ["
                             + rating+"] file ["+uri+"]")
                self.tlist[uri] = 1
        if ltype == 'playlist':
            Logger.info("Library: writing to playlist ["+pname+"]")
            cb = []
            cb.append(app.mpdconnection.protocol.playlistclear(pname))
            for k in sorted(self.tlist.keys()):
                cb.append(app.mpdconnection.protocol.playlistadd(pname, k))
            dl = DeferredList(cb, consumeErrors=True)
            dl.addCallback(partial(self.dismiss_generate_popup, p))
        elif ltype == 'synclist':
            (app.mpdconnection.protocol.
                sticker_find('song', '', 'copy_flag').
                addCallback(partial(self.generate_sync_list, p)).
                addErrback(app.mpdconnection.handle_mpd_error))

    def generate_sync_list(self, p, result):
        """Callback when generating synclist."""
        for row in result:
            uri = row['file']
            if row['sticker'] == 'copy_flag=Y':
                Logger.debug("Library: generate_sync_list: copy flag adding "
                        + uri)
                self.tlist[uri] = 1
            else:
                Logger.debug("Library: generate_sync_list: copy flag removing "
                        +uri)
                try:
                    del self.tlist[uri]
                except KeyError:
                    pass
        cb = []
        aroot = App.get_running_app().root
        pl = aroot.config.get('sync','syncplaylist')
        Logger.info("Library: generate_sync_list: writing to playlist ["
                    + pl + "]")
        cb.append(aroot.mpdconnection.protocol.playlistclear(pl))
        for k in sorted(self.tlist.keys()):
            cb.append(aroot.mpdconnection.protocol.playlistadd(pl, k))
        dl = DeferredList(cb, consumeErrors=True)
        dl.addCallback(partial(self.dismiss_generate_popup, p))

    def dismiss_generate_popup(self, p, result):
        p.dismiss()

    def browser_sticker_popup(self):
        """Callback when user presses the 'S' button."""
        browserStickerPopup = Factory.BrowserStickerPopup()
        browserStickerPopup.open()

    def library_rating_popup(self, instance, p):
        """Popup for setting song rating."""
        Logger.debug('Library: library_rating_popup()')
        p.dismiss()
        popup = Factory.RatingPopup(
                rating_set=self.library_rating_set,
                robject=self.rbl.selected_nodes)
        popup.open()

    def library_rating_set(self, robject, rating, popup):
        """Method that sets an objects's rating."""
        Logger.debug('Library: library_rating_set('+rating+')')
        popup.dismiss()
        for index in robject:
            rtype = self.rv.data[index]['info']['type']
            if rtype == 'file':
                if rating:
                    (App.get_running_app().root.mpdconnection.protocol.
                        sticker_set('song',
                                    self.rv.data[index]['base'],
                                    'rating',
                                    rating).
                        addCallback(partial(self.handle_rating_set,
                                            index,
                                            rating,
                                            True)).
                        addErrback(partial(self.handle_rating_set,
                                           index,
                                           rating,
                                           False)))
                    (App.get_running_app().root.mpdconnection.protocol.
                            sendmessage("ratingchange",
                                    self.rv.data[index]['base']))
                else:
                    (App.get_running_app().root.mpdconnection.protocol.
                        sticker_delete('song',
                                       self.rv.data[index]['base'],
                                       'rating').
                        addCallback(partial(self.handle_rating_set,
                                            index,
                                            rating,
                                            True)).
                        addErrback(partial(self.handle_rating_set,
                                           index,
                                           rating,
                                           False)))
            else:
                Logger.debug('Library: cannot setting rating on rtype ' + rtype)

    def handle_rating_set(self, index, rating, succ, result):
        if succ:
            Logger.info("Library: successfully set song rating for "
                        + self.rv.data[index]['base'])
            self.rv.data[index]['rating'] = rating
            self.rv.refresh_from_data()
        else:
            Logger.info("Library: could not set song rating for "
                        + self.rv.data[index]['base'])

    def reload_row_after_sticker(self, copy_flag, index, result):
        self.rv.data[index]['copy_flag'] = copy_flag
        self.rv.refresh_from_data()

    def set_copy_flag_find(self, copy_flag, index, result):
        app = App.get_running_app().root
        for rrow in result:
            if copy_flag:
                Logger.debug("set_copy_flag_find: setting copy_flag to "
                             + copy_flag+" for file "+rrow['file'])
                (app.mpdconnection.protocol.
                    sticker_set('song', rrow['file'], 'copy_flag', copy_flag).
                    addCallback(partial(self.reload_row_after_sticker,
                                        copy_flag,
                                        index)).
                    addErrback(app.mpdconnection.handle_mpd_error))
            else:
                Logger.debug("set_copy_flag_find: clearing copy_flag for file "
                             + rrow['file'])
                (app.mpdconnection.protocol.
                    sticker_delete('song', rrow['file'], 'copy_flag').
                    addCallback(partial(self.reload_row_after_sticker,
                                        '',
                                        index)).
                    addErrback(app.mpdconnection.handle_mpd_error))

    def set_copy_flag_find_one(self, copy_flag, index, result):
        app = App.get_running_app().root
        for rrow in result:
            if copy_flag:
                Logger.debug("set_copy_flag_find_one: setting copy_flag to "
                             + copy_flag+" for file "+rrow['file'])
                (app.mpdconnection.protocol.
                    sticker_set('song', rrow['file'], 'copy_flag', copy_flag).
                    addCallback(partial(self.reload_row_after_sticker,
                                        copy_flag,
                                        index)).
                    addErrback(app.mpdconnection.handle_mpd_error))
            else:
                Logger.debug("set_copy_flag_find_one: clearing copy_flag "
                             + "for file "+rrow['file'])
                (app.mpdconnection.protocol.
                    sticker_delete('song', rrow['file'], 'copy_flag').
                    addCallback(partial(self.reload_row_after_sticker,
                                        '',
                                        index)).
                    addErrback(app.mpdconnection.handle_mpd_error))
            break

    def set_copy_flag(self, copy_flag, p):
        Logger.info('Library: set_copy_flag('+str(copy_flag)+')')
        app = App.get_running_app().root
        p.dismiss()
        for index in self.rbl.selected_nodes:
            row = self.rv.data[index]
            mtype = row['info']['type']
            Logger.info("Library: Setting copy_flag for "+mtype+" '"
                        + row['base']+"' to "+copy_flag)
            if mtype == 'file':
                Logger.debug("set_copy_flag: adding uri or file")
                if copy_flag:
                    Logger.debug("set_copy_flag: setting copy_flag to "
                                 + copy_flag+" for file "+row['base'])
                    (app.mpdconnection.protocol.
                        sticker_set('song',
                                    row['base'],
                                    'copy_flag',
                                    copy_flag).
                        addCallback(partial(self.reload_row_after_sticker,
                                            copy_flag,
                                            index)).
                        addErrback(app.mpdconnection.handle_mpd_error))
                else:
                    Logger.debug("set_copy_flag: clearing copy_flag for file "
                                 + row['base'])
                    (app.mpdconnection.protocol.
                        sticker_delete('song', row['base'], 'copy_flag').
                        addCallback(partial(self.reload_row_after_sticker,
                                            '',
                                            index)).
                        addErrback(app.mpdconnection.handle_mpd_error))
            elif mtype == 'albumartistsort':
                (app.mpdconnection.protocol.
                    find(mtype, row['base']).
                    addCallback(partial(self.set_copy_flag_find,
                                        copy_flag,
                                        index)).
                    addErrback(app.mpdconnection.handle_mpd_error))
            elif mtype == 'album':
                (app.mpdconnection.protocol.
                    find(mtype,
                         row['base'],
                         'albumartistsort',
                         row['info']['albumartistsort']).
                    addCallback(partial(self.set_copy_flag_find,
                                        copy_flag,
                                        index)).
                    addErrback(app.mpdconnection.handle_mpd_error))
            elif mtype == 'artistsort':
                (app.mpdconnection.protocol.
                    find(mtype, row['base']).
                    addCallback(partial(self.set_copy_flag_find,
                                        copy_flag,
                                        index)).
                    addErrback(app.mpdconnection.handle_mpd_error))
            elif mtype == 'track':
                (app.mpdconnection.protocol.
                    find('artistsort',
                         row['info']['artistsort'],
                         'title',
                         row['base']).
                    addCallback(partial(self.set_copy_flag_find_one,
                                        copy_flag,
                                        index)).
                    addErrback(app.mpdconnection.handle_mpd_error))
            elif mtype == 'uri':
                (app.mpdconnection.protocol.
                    find('base', row['base']).
                    addCallback(partial(self.set_copy_flag_find,
                                        copy_flag,
                                        index)).
                    addErrback(app.mpdconnection.handle_mpd_error))
            elif mtype == 'playlist':
                Logger.info("Library: "+mtype+" copy_flag not implemented")
            else:
                Logger.warning("Library: "+mtype+' copy_flag not implemented')
        self.rbl.clear_selection()


class LibraryRecycleBoxLayout(LayoutSelectionBehavior, RecycleBoxLayout):
    """Adds selection and focus behaviour to a recyclebox."""


class LibraryRow(RecycleDataViewBehavior, BoxLayout):
    """Adds selection support to a row in a recycleview."""
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def long_touch(self, touch, index, *args):
        """Callback when user long-presses on a row."""
        Logger.debug("Library: long-touch on "+str(index))
        app = App.get_running_app().root
        app.library.rbl.clear_selection()
        app.library.handle_long_touch(
                app.library.rv.data[index],
                index)

    def refresh_view_attrs(self, rv, index, data):
        """Catch and handle the view changes."""
        self.index = index
        return (RecycleDataViewBehavior.
                refresh_view_attrs(self, rv, index, data))

    def on_touch_down(self, touch):
        """Adds selection, long-press/double-click handling on touch down."""
        app = App.get_running_app().root
        if BoxLayout.on_touch_down(self, touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            # these lines start a 1 second clock to detect long-presses
            callback = partial(self.long_touch, touch, self.index)
            Clock.schedule_once(callback, 1)
            touch.ud['event'] = callback
            if touch.is_double_tap:
                Logger.debug("Library: double-click on "+str(self.index))
                app.library.rbl.clear_selection()
                app.library.handle_long_touch(
                        app.library.rv.data[self.index],
                        self.index)
            else:
                return self.parent.select_with_touch(self.index, touch)

    def on_touch_up(self, touch):
        """Clean up long-press handling on touch up."""
        if BoxLayout.on_touch_up(self, touch):
            return True
        # if i don't check for this, the app crashes when things scroll off
        # screen
        if 'event' in touch.ud:
            Clock.unschedule(touch.ud['event'])

    def apply_selection(self, rv, index, is_selected):
        """Respond to the selection of items in the view."""
        self.selected = is_selected
        lt = App.get_running_app().root.library
        if is_selected:
            lt.library_selection[index] = True
        else:
            if index in lt.library_selection:
                del lt.library_selection[index]
