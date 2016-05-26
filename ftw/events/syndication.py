from Products.CMFPlone.browser.syndication.adapters import FolderFeed
from plone import api
from ftw.events.interfaces import IEventPage


class EventFolderFeed(FolderFeed):

    def _brains(self):
        catalog = api.portal.get_tool('portal_catalog')
        query = {
            'object_provides': IEventPage.__identifier__,
            'path': {
                'query': '/'.join(self.context.getPhysicalPath()),
            },
            'sort_on': 'start',
            'sort_order': 'descending',
        }
        return catalog(**query)
