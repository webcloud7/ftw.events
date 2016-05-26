from ftw.builder import Builder
from ftw.builder import create
from ftw.events.tests import FunctionalTestCase
from ftw.testbrowser import browsing
from ftw.testbrowser.pages import factoriesmenu
from ftw.testbrowser.pages import statusmessages


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
