from ftw.builder import Builder
from ftw.builder import create
from ftw.events.restapi.content import SerializeEventListingBlockToJson
from ftw.events.testing import FUNCTIONAL_TESTING
from ftw.events.tests import FunctionalTestCase
from ftw.testbrowser import browsing


class TestRestApiIntegration(FunctionalTestCase):

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        super(TestRestApiIntegration, self).setUp()
        self.grant('Manager', 'Site Administrator')

        self.layer['portal'].manage_permission(
            'plone.restapi: Use REST API',
            roles=['Anonymous']
        )

        self.eventfolder = create(Builder('event folder'))
        self.eventlistingblock = self.eventfolder.objectValues()[0]
        self.event = create(Builder('event page')
                            .within(self.eventfolder)
                            .titled(u'Some Event'))

    def test_query_is_from_event_listing_block(self):
        self.assertDictEqual(
            self.eventlistingblock.restrictedTraverse('@@events').get_query(),
            SerializeEventListingBlockToJson(self.eventlistingblock, self.eventlistingblock.REQUEST).get_query()
        )

    @browsing
    def test_do_not_serialize_events_by_default_on_block(self, browser):
        browser.open(self.eventlistingblock.absolute_url(), method='GET',
                     headers={'Accept': 'application/json'})
        self.assertNotIn('items', browser.json)

    @browsing
    def test_eventlistingblock_has_block_configuration(self, browser):
        browser.open(self.eventlistingblock.absolute_url(), method='GET',
                     headers={'Accept': 'application/json'})
        self.assertIn('block-configuration', browser.json)

    @browsing
    def test_include_events(self, browser):
        browser.open(self.eventlistingblock.absolute_url() + '?include_items=true', method='GET',
                     headers={'Accept': 'application/json'})
        self.assertIn('items', browser.json)

        event = browser.json['items'][0]
        self.assertEquals(self.event.Title().decode('utf-8'), event['title'])

    @browsing
    def test_pagination(self, browser):

        for number in range(0, 5):
            create(Builder('event page')
                   .within(self.eventfolder)
                   .titled(u'Event Nr. {}'.format(number)))
        browser.open(self.eventlistingblock.absolute_url() + '?include_items=true&b_size=2', method='GET',
                     headers={'Accept': 'application/json'})

        self.assertEquals(6, browser.json['items_total'])
        self.assertIn('batching', browser.json)

    @browsing
    def test_serialize_event_by_default_on_eventfolder(self, browser):
        browser.open(self.eventfolder.absolute_url(), method='GET',
                     headers={'Accept': 'application/json'})
        self.assertIn('items', browser.json)
