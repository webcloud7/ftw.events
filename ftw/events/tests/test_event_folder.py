from ftw.events.tests import FunctionalTestCase
from ftw.testbrowser import browsing
from ftw.testbrowser.pages import factoriesmenu
from ftw.testbrowser.pages import statusmessages


class TestEventFolder(FunctionalTestCase):

    @browsing
    def test_create_event_folder(self, browser):
        self.grant('Manager')
        browser.login().open()
        factoriesmenu.add('Events Folder')

        browser.fill({'Title': 'Activities'}).save()
        statusmessages.assert_no_error_messages()
        self.assertEquals('http://nohost/plone/activities/view', browser.url)
