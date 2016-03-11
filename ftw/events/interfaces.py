from zope.interface import Interface


class IFTWEventsLayer(Interface):
    """Request layer for ftw.events"""


class IEventsFolder(Interface):
    """Events folder marker interface.
    """


class IEventPage(Interface):
    """Event page folder marker interface.
    """
