from ftw.builder import Builder
from ftw.builder import create
from ftw.events.tests import FunctionalTestCase
from ftw.testbrowser import browsing
from ftw.testbrowser.pages import factoriesmenu
from ftw.testbrowser.pages import statusmessages
from Products.CMFPlone.interfaces.syndication import IFeedSettings
import transaction


class TestEventFolder(FunctionalTestCase):

    @browsing
    def test_create_event_folder(self, browser):
        self.grant('Manager')
        browser.login().open()
        factoriesmenu.add('Event Folder')

        browser.fill({'Title': 'Activities'}).save()
        statusmessages.assert_no_error_messages()
        self.assertEquals('http://nohost/plone/activities/view', browser.url)

    @browsing
    def test_event_folder_has_empty_listing_block(self, browser):
        self.grant('Manager')
        folder = create(Builder('event folder'))
        browser.login().visit(folder, view='@@simplelayout-view')
        self.assertEqual(
            ['No content available'],
            browser.css('.sl-layout .ftw-events-eventlistingblock').text
        )

    @browsing
    def test_event_folder_rss_feed_only_renders_event_pages(self, browser):
        self.grant('Manager')
        folder = create(Builder('event folder'))
        event1 = create(Builder('event page').titled(u'Event 1').within(folder))
        event2 = create(Builder('event page').titled(u'Event 2').within(folder))

        IFeedSettings(folder).enabled = True
        transaction.commit()

        # Make sure the event folder contains the event listing block
        # and two event pages.
        self.assertEqual(
            ['ftw.events.EventListingBlock', 'ftw.events.EventPage', 'ftw.events.EventPage'],
            [obj.portal_type for obj in folder.listFolderContents()]
        )

        # Make sure that the RSS feed only renders the event pages,
        # not the event listing block.
        browser.login().visit(folder, view='rss.xml')
        self.assertEqual(
            [event1.Title(), event2.Title()],
            browser.css('item title').text
        )
