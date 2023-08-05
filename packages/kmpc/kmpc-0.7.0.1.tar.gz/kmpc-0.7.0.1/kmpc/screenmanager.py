from functools import partial

import kivy
from kivy.logger import Logger
from kivy.uix.screenmanager import ScreenManager, CardTransition
from kivy.app import App
from kivy.support import install_twisted_reactor
from kivy.properties import ObjectProperty

from kmpc.nowplaying import NowPlayingScreen
from kmpc.queue import QueueScreen
from kmpc.library import LibraryScreen
from kmpc.system import SystemScreen
from kmpc.mpdfactory import MpdConnection

# make sure we are on updated version of kivy
kivy.require('1.10.0')

class KmpcScreenManager(ScreenManager):
    """The main class that ties it all together."""

    mpdconnection = ObjectProperty(None)
    syncmpdconnection = ObjectProperty(None)
    nowplaying = ObjectProperty(None)
    queue = ObjectProperty(None)
    library = ObjectProperty(None)
    system = ObjectProperty(None)

    def __init__(self, config, *args, **kwargs):
        """Zero out variables, pull in config file, connect to mpd."""
        super(KmpcScreenManager, self).__init__(*args, **kwargs)
        self.transition = CardTransition(direction='down')
        self.config = config
        self.nowplaying = NowPlayingScreen()
        self.nowplaying.bind(on_enter=self.nowplaying.enter_screen)
        self.nowplaying.bind(on_leave=self.nowplaying.leave_screen)
        self.add_widget(self.nowplaying)
        self.queue = QueueScreen()
        self.queue.bind(on_enter=self.queue.enter_screen)
        self.add_widget(self.queue)
        self.library = LibraryScreen()
        self.library.bind(on_enter=self.library.enter_screen)
        self.add_widget(self.library)
        self.system = SystemScreen()
        self.system.bind(on_enter=self.system.enter_screen)
        self.add_widget(self.system)
        self.mpd_status = {'state': 'stop',
                           'repeat': 0,
                           'single': 0,
                           'random': 0,
                           'consume': 0,
                           'curpos': 0}
        self.currsong = None
        self.nextsong = None
        self.currfile = None
        self.do_idle_handler = True
        # install twisted reactor to interface with mpd
        install_twisted_reactor()
        # open mpd connection
        self.mpdconnection = MpdConnection(
                self.config.get('mpd', 'mpdhost'),
                self.config.get('mpd', 'mpdport'),
                self.mpd_idle_handler,
                [self.init_mpd],
                Logger.info)

    def init_mpd(self, instance):
        # get the initial mpd status
        (self.mpdconnection.protocol.status().
            addCallback(self.nowplaying.update_mpd_status).
            addErrback(self.mpdconnection.handle_mpd_error))
        # subscribe to 'kmpc' to check for messages from mpd
        self.mpdconnection.protocol.subscribe('kmpc')

    def mpd_idle_handler(self, result):
        # global flag for disabling during sync
        if self.do_idle_handler:
            # notify various subsystems based on what changed
            for s in result:
                Logger.info('mpd_idle_handler: Changed '+format(s))
                if format(s) == 'playlist':
                    # queue was changed, ask mpd for playlist info
                    (self.mpdconnection.protocol.playlistinfo().
                        addCallback(self.queue.populate_queue).
                        addErrback(self.mpdconnection.handle_mpd_error))
                    # force a reload of nextsong if queue changes
                    self.nextsong = None
                    (self.mpdconnection.protocol.status().
                        addCallback(self.nowplaying.update_mpd_status).
                        addErrback(self.mpdconnection.handle_mpd_error))
                elif format(s) == 'player':
                    # player was changed, ask mpd for player status
                    (self.mpdconnection.protocol.status().
                        addCallback(self.nowplaying.update_mpd_status).
                        addErrback(self.mpdconnection.handle_mpd_error))
                elif format(s) == 'sticker':
                    # song rating sticker was changed, ask mpd for current song
                    # rating
                    (self.mpdconnection.protocol.status().
                        addCallback(self.nowplaying.update_mpd_status).
                        addErrback(self.mpdconnection.handle_mpd_error))
                    (self.mpdconnection.protocol.
                        sticker_get('song', self.currfile, 'rating').
                        addCallback(self.nowplaying.update_mpd_sticker_rating).
                        addErrback(self.mpdconnection.handle_mpd_no_sticker))
                elif format(s) == 'options':
                    # some playback option was changed, ask mpd for player
                    # status
                    (self.mpdconnection.protocol.status().
                        addCallback(self.nowplaying.update_mpd_status).
                        addErrback(self.mpdconnection.handle_mpd_error))
                elif format(s) == 'message':
                    # an mpd message was received, ask mpd what it was
                    (self.mpdconnection.protocol.readmessages().
                        addCallback(self.handle_mpd_message).
                        addErrback(self.mpdconnecion.handle_mpd_error))
                else:
                    # default if none of the above, ask mpd for player status
                    (self.mpdconnection.protocol.status().
                        addCallback(self.nowplaying.update_mpd_status).
                        addErrback(self.mpdconnection.handle_mpd_error))

    def change_replaygain(self, v):
        Logger.debug("NowPlaying: change_replaygain to " + format(v))
        self.mpdconnection.protocol.replay_gain_mode(
                str(v)).addErrback(self.mpdconnection.handle_mpd_error)

    def change_crossfade(self, v):
        """Callback when user changes crossfade slider."""
        Logger.info('Settings: change_crossfade')
        self.mpdconnection.protocol.crossfade(
                str(v)).addErrback(self.mpdconnection.handle_mpd_error)

    def change_mixrampdb(self, v):
        """Callback when user changes mixrampdb slider."""
        Logger.info('Settings: change_mixrampdb')
        self.mpdconnection.protocol.mixrampdb(
                str(0.0-v)).addErrback(self.mpdconnection.handle_mpd_error)

    def change_mixrampdelay(self, v):
        """Callback when user changes mixrampdelay slider."""
        Logger.info('Settings: change_mixrampdelay')
        self.mpdconnection.protocol.mixrampdelay(
                str(v)).addErrback(self.mpdconnection.handle_mpd_error)

