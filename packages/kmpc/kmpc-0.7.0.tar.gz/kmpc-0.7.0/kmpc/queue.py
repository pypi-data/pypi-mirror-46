from functools import partial

import kivy
from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.logger import Logger
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.vkeyboard import VKeyboard
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.screenmanager import Screen
from kivy.factory import Factory
from kivy.clock import Clock

from kmpc.widgets import BaseLabel

# make sure we are on updated version of kivy
kivy.require('1.10.0')


class QueueScreen(Screen):
    """The Queue screen, shows the current queue and allows interacting with
    it."""
    queue_selection = {}

    def enter_screen(self, *args):
        ss = self.ids.ss
        ss.ids.queuebutton.state = 'down'
        ss.ids.queuebutton.disabled = True
        app = App.get_running_app().root
        # switching to the queue tab repopulates it if it is empty
        if len(self.rv.data) == 0:
            (app.mpdconnection.protocol.playlistinfo().
                addCallback(self.populate_queue).
                addErrback(app.mpdconnection.handle_mpd_error))

    def queue_clear_pressed(self):
        """Callback for queue clear button."""
        Logger.info("Queue: clear")
        App.get_running_app().root.mpdconnection.protocol.clear()

    def queue_delete_pressed(self):
        """Callback for queue delete button."""
        Logger.info("Queue: delete")
        # loop through all selected tracks and remove each one from the
        # queue
        for pos in self.queue_selection:
            songid = str(self.rv.data[pos]['songid'])
            Logger.debug("Queue: deleting songid "+songid)
            App.get_running_app().root.mpdconnection.protocol.deleteid(songid)
        self.rbl.clear_selection()

    def queue_move_pressed(self):
        """Callback for queue move button."""
        # TODO: implement this
        Logger.info("Queue: move")
        Logger.warn("Queue: move not implemented")
        self.rbl.clear_selection()

    def queue_shuffle_pressed(self):
        """Callback for queue shuffle button."""
        Logger.info("Queue: shuffle")
        # shuffle the queue. note that this is different from toggling
        # random playback, as it actually reorders the queue randomly rather
        # than just playing in random order
        App.get_running_app().root.mpdconnection.protocol.shuffle()
        self.rbl.clear_selection()

    def queue_swap_pressed(self):
        """Callback for queue swap button."""
        Logger.info("Queue: swap")
        app = App.get_running_app().root
        # if exactly 2 tracks are selected, swap them
        if len(self.queue_selection) != 2:
            Logger.warn("Queue: swap only works with two rows selected")
        else:
            s1 = self.queue_selection.keys()[0]
            s2 = self.queue_selection.keys()[1]
            (app.mpdconnection.protocol.
                swap(str(s1), str(s2)).
                addErrback(app.mpdconnection.handle_mpd_error))
        self.rbl.clear_selection()

    def queue_save_pressed(self):
        """Callback for queue save button."""
        Logger.info("Queue: save")
        self.rbl.clear_selection()
        popup = Factory.PlaylistSavePopup()
        popup.ids.ok_button.bind(on_press=partial(self.save_playlist,popup))
        popup.open()

    def save_playlist(self, popup, instance):
        """Tell mpd to save the current playlist with the name that was
        input."""
        app = App.get_running_app().root
        t = popup.ids.playlist_name.text
        Logger.info("Queue: save_playlist("+t+")")
        (app.mpdconnection.protocol.
            save(t).
            addErrback(app.mpdconnection.handle_mpd_error))
        popup.dismiss()

    def populate_queue(self, result):
        """Callback for mpd playlist info."""
        Logger.info("Queue: populate_queue()")
        app = App.get_running_app().root
        self.rv.data = []
        # loop through mpd playlist info and add to the recycleview
        for row in result:
            Logger.debug("Queue: row "+row['pos']+" found = "+row['title'])
            r = {'plpos': row['pos'],
                 'rownum': str(int(row['pos'])+1),
                 'artist': format(row['artist']),
                 'title': format(row['title']),
                 'songid': format(row['id'])}
            self.rv.data.append(r)
        # when queue is populated, also ask mpd for current status to
        # highlight current track
        (app.mpdconnection.protocol.
            status().
            addCallback(self.update_mpd_status).
            addErrback(app.mpdconnection.handle_mpd_error))

    def update_mpd_status(self, result):
        """Callback for mpd status about current track."""
        Logger.debug('Queue: update_mpd_status()')
        # TODO: pretty sure this is what crashes the player on super-long
        # queues
        if result['state'] == 'stop':
            # if stopped, there's no current track
            self.currsong = None
            # loop through recycleview, unhighlight all tracks
            for r in self.rv.data:
                r['iscurrent'] = False
        else:
            self.currsong = result['song']
            # loop through recycleview, highlight current track and unhighlight
            # all others
            for r in self.rv.data:
                if r['plpos'] == result['song']:
                    r['iscurrent'] = True
                else:
                    r['iscurrent'] = False
        # tell the recycleview to refresh itself from the changed data
        self.rv.refresh_from_layout()


class QueueRecycleBoxLayout(LayoutSelectionBehavior, RecycleBoxLayout):
    """Adds selection and focus behaviour to the recyclebox."""


class QueueRow(RecycleDataViewBehavior, BoxLayout):
    """Adds selection and long-press support to the recycleview."""
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def playfrom(self, touch, index, *args):
        """Handle long-press on a queue row."""
        Logger.debug("Queue: long-touch playfrom "+str(index))
        app = App.get_running_app().root
        app.mpdconnection.protocol.play(str(index))
        app.queue.rbl.clear_selection()

    def refresh_view_attrs(self, rv, index, data):
        """Catch and handle the view changes."""
        self.index = index
        return super(self.__class__, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        """Adds selection and long-press on touch down."""
        if super(self.__class__, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            # these lines start a 1 second clock to detect long-presses
            callback = partial(self.playfrom, touch, self.index)
            Clock.schedule_once(callback, 1)
            touch.ud['event'] = callback
            return self.parent.select_with_touch(self.index, touch)

    def on_touch_up(self, touch):
        """Clean up long-press on touch up."""
        if super(QueueRow, self).on_touch_up(touch):
            return True
        # if i don't check for this, the app crashes when things scroll off
        # screen
        if 'event' in touch.ud:
            Clock.unschedule(touch.ud['event'])

    def apply_selection(self, rv, index, is_selected):
        """Respond to the selection of items in the view."""
        self.selected = is_selected
        pt = App.get_running_app().root.queue
        if is_selected:
            pt.queue_selection[index] = True
        else:
            if index in pt.queue_selection:
                del pt.queue_selection[index]


# class PlaylistSavePopup(Popup):
#     pass
