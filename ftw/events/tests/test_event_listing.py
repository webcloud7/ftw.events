from ftw.builder import Builder
from ftw.builder import create
from ftw.events.tests import FunctionalTestCase
from ftw.testbrowser import browsing
from plone import api


class TestEventListing(FunctionalTestCase):

    def setUp(self):
        super(TestEventListing, self).setUp()
        self.grant('Manager')

    @browsing
    def test_event_listing(self, browser):
        """
        This test makes sure the event listing view renders the events.
        """
        event_folder = create(Builder('event folder')
                              .titled(u'Not relevant in this test'))
        create(Builder('event page')
               .titled(u'My Event')
               .within(event_folder))

        browser.login()

        # Get the event folder's event listing block which has been created automatically.
        block = api.content.find(portal_type='ftw.events.EventListingBlock')[0].getObject()

        # Make sure the view renders the events.
        browser.visit(block, view='@@events')
        self.assertEqual(
            ['My Event'],
            browser.css('.event-row .title').text
        )

    @browsing
    def test_custom_event_listing_title(self, browser):
        page = create(Builder('sl content page')
                      .titled(u'Not relevant in this test'))
        event_folder = create(Builder('event folder')
                              .titled(u'Not relevant in this test')
                              .within(page))
        create(Builder('event page')
               .titled(u'Not relevant in this test')
               .within(event_folder))
        block = create(Builder('event listing block')
                       .within(page)
                       .titled(u'Not relevant in this test'))

        browser.login()

        # A fallback title must be rendered on the view by default.
        browser.visit(block, view='@@events')
        self.assertEqual(
            ['Events'],
            browser.css('.documentFirstHeading').text
        )

        # Configure a custom title.
        browser.login().visit(block, view='edit.json')
        response = browser.json
        browser.open_html(response['content'])
        browser.fill({
            'Title of the view behind the "more items" link': u'All my events',
        })
        browser.find_button_by_label('Save').click()

        # Now the view must render the custom title.
        browser.visit(block, view='@@events')
        self.assertEqual(
            ['All my events'],
            browser.css('.documentFirstHeading').text
        )
