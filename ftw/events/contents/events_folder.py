from ftw.events.interfaces import IEventsFolder
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.content import Container
from plone.directives import form
from zope.interface import alsoProvides
from zope.interface import implements


class IEventsFolderSchema(form.Schema):
    pass

alsoProvides(IEventsFolderSchema, IFormFieldProvider)


class EventsFolder(Container):
    implements(IEventsFolder)
