from ftw.events.interfaces import IEventFolder
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.content import Container
from plone.directives import form
from zope.interface import alsoProvides
from zope.interface import implements


class IEventFolderSchema(form.Schema):
    pass

alsoProvides(IEventFolderSchema, IFormFieldProvider)


class EventFolder(Container):
    implements(IEventFolder)
