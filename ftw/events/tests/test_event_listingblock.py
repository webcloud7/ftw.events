import datetime
from ftw.builder import Builder
from ftw.builder import create
from ftw.events.tests import FunctionalTestCase
from ftw.testbrowser import browsing
from ftw.testbrowser.pages import factoriesmenu
from ftw.testbrowser.pages import statusmessages


class TestEventListingBlock(FunctionalTestCase):

    def setUp(self):
        super(TestEventListingBlock, self).setUp()
        self.grant('Manager')

    @browsing
    def test_event_listing_block_builder(self, browser):
        page = create(Builder('sl content page').titled(u'A page'))

        create(Builder('event listing block')
               .within(page)
               .titled(u'This block renders event pages'))

        browser.login().visit(page)
        self.assertEqual(
            ['This block renders event pages'],
            browser.css('.sl-block.ftw-events-eventlistingblock h2').text
        )

    @browsing
    def test_event_listing_block_can_be_added_on_contentpage(self, browser):
        page = create(Builder('sl content page').titled(u'A page'))
        browser.login().visit(page)

        factoriesmenu.add('EventListingBlock')
        browser.fill({
            'Title': u'This block renders event pages',
        }).save()

        browser.open(page)
        self.assertEqual(
            ['This block renders event pages'],
            browser.css('.sl-block.ftw-events-eventlistingblock h2').text
        )

    @browsing
    def test_event_listing_block_does_not_render_title(self, browser):
        page = create(Builder('sl content page').titled(u'A page'))

        block = create(Builder('event listing block')
                       .within(page)
                       .titled(u'This block renders event pages'))
        browser.login()

        # Make sure the title is rendered by default.
        browser.visit(page)
        self.assertEqual(
            ['This block renders event pages'],
            browser.css('.sl-block.ftw-events-eventlistingblock h2').text
        )

        # Tell the block to no longer display the title.
        browser.login().visit(block, view='edit.json')
        response = browser.json
        browser.open_html(response['content'])
        browser.fill({
            'Show title': False,
        })
        browser.find_button_by_label('Save').click()

        # Make sure the title is no longer rendered.
        browser.visit(page)
        self.assertEqual(
            [],
            browser.css('.sl-block.ftw-events-eventlistingblock h2')
        )

    @browsing
    def test_block_filters_by_path(self, browser):
        """
        This test makes sure that the block only renders items
        from the given path.
        """
        event_folder1 = create(Builder('event folder')
                               .titled(u'Event Folder 1')
                               .within(self.portal))
        create(Builder('event page').titled(u'Hello World 1').within(event_folder1))

        event_folder2 = create(Builder('event folder')
                               .titled(u'Event Folder 2')
                               .within(self.portal))
        create(Builder('event page').titled(u'Hello World 2').within(event_folder2))

        page = create(Builder('sl content page').titled(u'Content Page with Eventlistingblock'))
        block = create(Builder('event listing block')
                       .within(page)
                       .having(current_context=False)
                       .titled(u'Not relevant in this test'))
        browser.login().visit(block, view='edit.json')
        response = browser.json
        browser.open_html(response['content'])
        browser.fill({
            'Limit to path': event_folder2,
        })
        browser.find_button_by_label('Save').click()
        browser.visit(page)

        self.assertEqual(
            ['Hello World 2'],
            browser.css('.sl-block.ftw-events-eventlistingblock h3').text
        )

    @browsing
    def test_block_prevents_path_and_current_context(self, browser):
        """
        This test makes sure that a block cannot be configured to
        have a filter by path and a filter by current context at the
        same time.
        """
        event_folder = create(Builder('event folder').titled(u'Event Folder'))

        browser.login()
        browser.visit(event_folder, view='++add_block++ftw.events.EventListingBlock')
        response = browser.json
        browser.open_html(response['content'])
        browser.fill({
            'Title': u'Not relevant for this test',
            'Limit to path': '/'.join(event_folder.getPhysicalPath()),
            'Limit to current context': True,
        })
        browser.find_button_by_label('Save').click()
        response = browser.json
        browser.open_html(response['content'])

        self.assertEqual(
            ['There were some errors.'],
            statusmessages.error_messages()
        )
        self.assertIn(
            'You cannot filter by path and current context at the same time.',
            browser.css('.error').text
        )

    @browsing
    def test_block_filter_by_current_context(self, browser):
        """
        This test makes sure the block filters by the current context.
        """
        page1 = create(Builder('sl content page').titled(u'Content Page 1'))
        event_folder1 = create(Builder('event folder')
                               .titled(u'Event Folder 1')
                               .within(page1))
        create(Builder('event page').titled(u'Hello World 1').within(event_folder1))
    
        page2 = create(Builder('sl content page').titled(u'Content Page 2'))
        event_folder2 = create(Builder('event folder')
                               .titled(u'Event Folder 2')
                               .within(page2))
        create(Builder('event page').titled(u'Hello World 2').within(event_folder2))

        block = create(Builder('event listing block')
                       .within(page2)
                       .titled(u'Not relevant for this test'))

        browser.login()

        # Make sure that the filter by context is active by default.
        browser.visit(page2)
        self.assertEqual(
            ['Hello World 2'],
            browser.css('.sl-block.ftw-events-eventlistingblock h3').text
        )

        # Tell the block to no longer filter by the current context.
        browser.login().visit(block, view='edit.json')
        response = browser.json
        browser.open_html(response['content'])
        browser.fill({
            'Limit to current context': False,
        })
        browser.find_button_by_label('Save').click()

        # Make sure the title is no longer rendered.
        browser.visit(page2)
        self.assertEqual(
            ['Hello World 1', 'Hello World 2'],
            browser.css('.sl-block.ftw-events-eventlistingblock h3').text
        )

    @browsing
    def test_block_crops_description(self, browser):
        """
        This test makes sure that the block crops the description of the event
        page to the default length (note that the description is shown by default
        but can be disabled).
        """
        page = create(Builder('sl content page').titled(u'Content Page 1'))
        event_folder = create(Builder('event folder').titled(u'Event Folder 1').within(page))
        create(Builder('event page')
               .titled(u'Hello World 1')
               .having(description=u"This description must be longer than "
                                   u"50 characters so we are able to test "
                                   u"if it will be cropped.")
               .within(event_folder))
        create(Builder('event listing block')
               .within(page)
               .titled(u'This is a EventListingBlock'))

        browser.login().visit(page)
        self.assertEqual(
            ['This description must be longer than 50 ...'],
            browser.css('.sl-block.ftw-events-eventlistingblock .description').text
        )

    @browsing
    def test_block_renders_entire_description(self, browser):
        """
        This test makes sure that the block renders the entire description
        if configured to do so.
        """
        page = create(Builder('sl content page').titled(u'Content Page 1'))
        event_folder = create(Builder('event folder').titled(u'Event Folder 1').within(page))
        create(Builder('event page')
               .titled(u'Hello World 1')
               .having(description=u"This description must be longer than "
                                   u"50 characters so we are able to test "
                                   u"if it will be cropped.")
               .within(event_folder))
        create(Builder('event listing block')
               .within(page)
               .having(description_length=0)
               .titled(u'This is a EventListingBlock'))

        browser.login().visit(page)
        self.assertEqual(
            [
                'This description must be longer than 50 characters '
                'so we are able to test if it will be cropped.'
            ],
            browser.css('.sl-block.ftw-events-eventlistingblock .description').text
        )

    @browsing
    def test_block_does_not_render_description(self, browser):
        """
        This test makes sure that the block does not render the description
        if configured to do so.
        """
        page = create(Builder('sl content page').titled(u'Content Page'))
        event_folder = create(Builder('event folder').titled(u'Event Folder').within(page))
        create(Builder('event page')
               .titled(u'Hello World')
               .having(description=u"The description.")
               .within(event_folder))
        create(Builder('event listing block')
               .within(page)
               .having(show_description=False)
               .titled(u'This is a EventListingBlock'))

        browser.login().visit(page)
        self.assertEqual(
            [],
            browser.css('.sl-block.ftw-events-eventlistingblock .description').text
        )

    @browsing
    def test_block_filters_by_subject(self, browser):
        """
        This test makes sure that the block filters event pages by subject.
        """
        page = create(Builder('sl content page').titled(u'Content Page'))
        event_folder = create(Builder('event folder').titled(u'Event Folder').within(page))
        create(Builder('event page')
               .titled(u'Event of Hans')
               .having(subjects=['Hans'])
               .starting(datetime.datetime(2010, 1, 1, 14, 0, 0))
               .ending(datetime.datetime(2010, 1, 1, 15, 0, 0))
               .within(event_folder))
        create(Builder('event page')
               .titled(u'Event of Peter')
               .having(subjects=['Peter'])
               .starting(datetime.datetime(2010, 1, 2, 15, 0, 0))
               .ending(datetime.datetime(2010, 1, 2, 16, 0, 0))
               .within(event_folder))
        create(Builder('event listing block')
               .within(page)
               .having(subjects=['Hans'])
               .having(show_title=False)
               .titled(u'This is a EventListingBlock'))

        browser.login()
        browser.visit(page)
        self.assertEqual(
            ['Jan 01, 2010 from 02:00 PM to 03:00 PM Event of Hans'],
            browser.css('.sl-block.ftw-events-eventlistingblock').text
        )

    @browsing
    def test_block_limits_quantity(self, browser):
        page = create(Builder('sl content page').titled(u'Content Page'))
        event_folder = create(Builder('event folder').titled(u'Event Folder').within(page))
        create(Builder('event page')
               .titled(u'Event of Hans')
               .starting(datetime.datetime(2010, 1, 1, 15, 0, 0))
               .ending(datetime.datetime(2010, 1, 1, 16, 0, 0))
               .within(event_folder))
        create(Builder('event page')
               .titled(u'Event of Peter')
               .starting(datetime.datetime(2010, 1, 2, 14, 0, 0))
               .ending(datetime.datetime(2010, 1, 2, 15, 0, 0))
               .within(event_folder))
        create(Builder('event listing block')
               .within(page)
               .having(quantity=1)
               .having(show_title=False)
               .titled(u'This is a EventListingBlock'))

        browser.login()
        browser.visit(page)
        self.assertEqual(
            ['Jan 02, 2010 from 02:00 PM to 03:00 PM Event of Peter'],
            browser.css('.sl-block.ftw-events-eventlistingblock').text
        )

    @browsing
    def test_block_renders_link_to_more_items(self, browser):
        page = create(Builder('sl content page')
                      .titled(u'Content Page'))
        event_folder = create(Builder('event folder').
                              titled(u'Event Folder')
                              .within(page))
        create(Builder('event page')
               .titled(u'Event')
               .within(event_folder))
        block = create(Builder('event listing block')
                       .within(page)
                       .having(show_more_items_link=True)
                       .titled(u'This is a EventListingBlock'))

        browser.login()

        # Make sure the link is there.
        browser.visit(page)
        self.assertEqual(
            'http://nohost/plone/content-page/this-is-a-eventlistingblock/events',
            browser.find('More Items').attrib['href']
        )

        # Tell the block to no longer render the link
        browser.login().visit(block, view='edit.json')
        response = browser.json
        browser.open_html(response['content'])
        browser.fill({
            'Show link to more items': False,
        })
        browser.find_button_by_label('Save').click()

        # Make sure the link is no longer there.
        browser.visit(page)
        self.assertIsNone(browser.find('More Items'))

    @browsing
    def test_block_renders_link_to_more_items_with_custom_label(self, browser):
        """
        This test makes sure that the link to thew view which renders more items
        has a custom label.
        """
        page = create(Builder('sl content page')
                      .titled(u'Content Page'))
        event_folder = create(Builder('event folder').
                              titled(u'Event Folder')
                              .within(page))
        create(Builder('event page')
               .titled(u'Event')
               .within(event_folder))
        create(Builder('event listing block')
               .within(page)
               .having(show_more_items_link=True)
               .having(more_items_link_label=u'Show me more')
               .titled(u'This is a EventListingBlock'))

        browser.login()

        # Make sure the link is there.
        browser.visit(page)
        self.assertEqual(
            'http://nohost/plone/content-page/this-is-a-eventlistingblock/events',
            browser.find('Show me more').attrib['href']
        )
