from ftw.builder import Builder
from ftw.builder import create
from ftw.events.tests import FunctionalTestCase
from ftw.testbrowser import browsing
from ftw.testbrowser.pages import factoriesmenu
from ftw.testbrowser.pages import statusmessages


class TestEventPage(FunctionalTestCase):

    @browsing
    def test_create_event_page(self, browser):
        self.grant('Manager')
        folder = create(Builder('events folder').titled(u'Activities'))
        browser.login().open(folder)
        factoriesmenu.add('Event Page')

        browser.fill({'Title': 'Jogging'}).save()
        statusmessages.assert_no_error_messages()
        self.assertEquals('http://nohost/plone/activities/jogging/view',
                          browser.url)
