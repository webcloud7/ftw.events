from ftw.events.interfaces import IEventPage
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.content import Container
from plone.directives import form
from zope.interface import alsoProvides
from zope.interface import implements


class IEventPageSchema(form.Schema):
    pass

alsoProvides(IEventPageSchema, IFormFieldProvider)


class EventPage(Container):
    implements(IEventPage)
