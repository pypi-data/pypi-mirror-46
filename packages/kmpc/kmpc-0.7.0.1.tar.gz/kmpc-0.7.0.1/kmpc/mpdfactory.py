from twisted.internet import protocol
from mpd import MPDProtocol


class MPDFactoryProtocol(MPDProtocol):
    """Factory for MPDProtocol."""

    def connectionMade(self):
        """Call the connectionMade override."""
        if callable(self.factory.connectionMade):
            self.factory.connectionMade(self)

    def connectionLost(self, reason):
        """Call the connectionLost override."""
        if callable(self.factory.connectionLost):
            self.factory.connectionLost(self, reason)


class MPDClientFactory(protocol.ClientFactory):
    """Factory for MPDClient."""

    protocol = MPDFactoryProtocol
    connectionMade = None
    connectionLost = None

    def __init__(self, idlehandler=None, **kwargs):
        self.idlehandler = idlehandler

    def buildProtocol(self, addr):
        """Hook up protocol and idle handler."""
        protocol = self.protocol()
        protocol.factory = self
        if callable(self.idlehandler):
            protocol.idle_result = self.idlehandler
        return protocol


class MPDReconnectingClientFactory(protocol.ReconnectingClientFactory):
    """Factory for MPDClient."""

    protocol = MPDFactoryProtocol
    connectionMade = None
    connectionLost = None

    def __init__(self, idlehandler=None, **kwargs):
        self.idlehandler = idlehandler

    def buildProtocol(self, addr):
        """Hook up protocol and idle handler."""
        protocol = self.protocol()
        protocol.factory = self
        if callable(self.idlehandler):
            protocol.idle_result = self.idlehandler
        return protocol


class Dummy(object):
    """Wrapper class to handle calls to mpd before the connection is set up."""

    def __getattr__(self, attr):
        return self

    def __call__(self, *args):
        return self


class MpdConnection(object):

    def __init__(self, mpdhost, mpdport,
                 idlehandler=None, initconnections=[],
                 quiet=False, reconnect=True, logger=None):
        self.mpdhost = mpdhost
        self.mpdport = mpdport
        self.quiet = quiet
        if not logger:
            from twisted.python import log
            self.logger = log.msg
        else:
            self.logger = logger
        self.logger("MpdConnection: connecting to " + mpdhost + ":" + mpdport)
        # set up mpd connection
        self.initconnections = initconnections
        if reconnect:
            self.factory = MPDReconnectingClientFactory(idlehandler)
        else:
            self.factory = MPDClientFactory(idlehandler)
        self.factory.connectionMade = self.mpd_connectionMade
        self.factory.connectionLost = self.mpd_connectionLost
        from twisted.internet import reactor
        self.reactor = reactor.connectTCP(mpdhost, int(mpdport), self.factory)
        self.noprotocol = Dummy()

    # this part handles calls to protocol when it hasn't been set up yet or is
    # incorrectly specified in config
    @property
    def protocol(self):
        try:
            if self.realprotocol:
                return self.realprotocol
        except AttributeError:
            return self.noprotocol

    def mpd_connectionMade(self, protocol):
        """Callback when mpd is connected."""
        # copy the protocol to all the classes
        self.realprotocol = protocol
        if not self.quiet:
            self.logger('MpdConnection: Connected to mpd server host='
                        + self.mpdhost + ' port=' + self.mpdport)
        for ic in self.initconnections:
            if callable(ic):
                ic(self)

    def mpd_connectionLost(self, protocol, reason):
        """Callback when mpd connection is lost."""
        if not self.quiet:
            self.logger('MpdConnection: Connection lost: %s' % reason)

    def handle_mpd_error(self, result):
        """Prints handled errors to the error log."""
        if not self.quiet:
            self.logger('MpdConnection: mpd error ['
                        + format(result) + ']')
