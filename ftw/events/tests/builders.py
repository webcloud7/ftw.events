from ftw.builder import builder_registry
from ftw.builder.dexterity import DexterityBuilder


class EventsFolderBuilder(DexterityBuilder):
    portal_type = 'ftw.events.EventsFolder'

builder_registry.register('events folder', EventsFolderBuilder)


class EventsBuilder(DexterityBuilder):
    portal_type = 'ftw.events.EventPage'

builder_registry.register('event page', EventsBuilder)
