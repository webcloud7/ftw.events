from Acquisition._Acquisition import aq_inner, aq_parent
from ftw.events import utils
from ftw.simplelayout.browser.blocks.base import BaseBlock
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter
from zope.contentprovider.interfaces import IContentProvider


class EventListingBlockView(BaseBlock):
    template = ViewPageTemplateFile('templates/eventlistingblock.pt')

    def get_block_info(self):
        """
        This method returns a dict containing information to be used in
        the block's template.
        """
        info = {
            'title': self.context.title,
            'show_title': self.context.show_title,
        }

        return info

    def get_items(self):
        """
        Returns a list of dicts where each dict contains the data of an
        event page. It is called from the template.
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog.searchResults(
            self.get_query()
        )

        if self.context.quantity:
            brains = brains[:self.context.quantity]

        items = [self.get_event_page_dict(brain) for brain in brains]

        return items

    def get_query(self):
        query = {
            'object_provides': {
                'query': ['ftw.events.interfaces.IEventPage'],
            },
            'sort_on': 'start',
            'sort_order': 'descending',
        }

        parent = aq_parent(aq_inner(self.context))
        if self.context.current_context:
            # `parent` is the object containing this block.
            path = '/'.join(parent.getPhysicalPath())
            query['path'] = {'query': path}
        elif self.context.filter_by_path:
            paths = ['/'.join(item.getPhysicalPath()) for item in self.context.filter_by_path]
            query['path'] = {'query': paths}

        if self.context.subjects:
            query['Subject'] = self.context.subjects

        return query

    def get_event_page_dict(self, brain):
        """
        Constructs a dict containing the data of the brain of an event page.
        """
        obj = brain.getObject()

        description = ''
        if self.context.show_description:
            description = brain.Description
        if self.context.description_length:
            description = utils.crop_text(
                description, self.context.description_length
            )

        # Copied from "plone.app.event.portlets.portlet_events.Renderer#formatted_date".
        provider = getMultiAdapter(
            (self.context, self.request, self),
            IContentProvider, name = 'formatted_date'
            )
        date_snippet = provider(obj)

        item = {
            'title': brain.Title,
            'description': description,
            'url': brain.getURL(),
            'brain': brain,
            'date_snippet': date_snippet,
        }
        return item
