from datetime import datetime
from ftw.builder import Builder
from ftw.builder import create
from ftw.events.testing import FUNCTIONAL_TESTING
from ftw.events.tests import FunctionalTestCase
from ftw.testbrowser import browsing
from plone import api
import transaction

events_portlet_action = '/++contextportlets++plone.rightcolumn/+/eventsarchiveportlet'


class TestEventArchivePortlets(FunctionalTestCase):
    layer = FUNCTIONAL_TESTING

    def setUp(self):
        super(TestEventArchivePortlets, self).setUp()
        self.grant('Manager')

    def _add_portlet(self, browser, context=None):
        """
        This helper method adds a events archive portlet on the given context.
        If no context is provided then the portlet will be added on the
        Plone site.
        """
        context = context or self.portal
        browser.login().visit(context, view='@@manage-portlets')
        browser.css('#portletmanager-plone-rightcolumn form')[0].fill(
            {':action': events_portlet_action}).submit()
        browser.open(context)

    @browsing
    def test_archive_portlet_available_when_there_are_events(self, browser):
        events_folder = create(Builder('event folder').titled(u'Event Folder')
                               .with_property('layout', 'event_listing'))
        create(Builder('event page').titled(u'Event Entry').within(events_folder)
               .with_property('layout', 'event_listing'))

        self._add_portlet(browser, events_folder)

        self.assertIn('Archive', browser.css('.archive-portlet header h2').text,
                      'Archive portlet is not here but it should be.')

    @browsing
    def test_archive_portlet_not_available_when_empty(self, browser):
        events_folder = create(Builder('event folder').titled(u'Event Folder')
                               .with_property('layout', 'event_listing'))

        self._add_portlet(browser, events_folder)

        self.assertNotIn('Archive', browser.css('dt.portletHeader').text,
                         'Archive portlet is here but it should not be.')

    @browsing
    def test_archive_portlet_summary(self, browser):
        """
        This test makes sure the summary is correct.
        """
        events_folder = create(Builder('event folder').titled(u'Event Folder')
                               .with_property('layout', 'event_listing'))
        create(Builder('event page').titled(u'Event Entry 1').within(events_folder)
               .having(start=datetime(2013, 1, 1), end=datetime(2013, 1, 1)))
        create(Builder('event page').titled(u'Event Entry 2').within(events_folder)
               .having(start=datetime(2013, 1, 11), end=datetime(2013, 1, 11)))
        create(Builder('event page').titled(u'Event Entry 3').within(events_folder)
               .having(start=datetime(2013, 2, 2), end=datetime(2013, 2, 2)))

        self._add_portlet(browser, events_folder)

        self.assertEqual(
            ['http://nohost/plone/event-folder/event_listing?archive=2013/02/01',
                'http://nohost/plone/event-folder/event_listing?archive=2013/01/01'],
            map(lambda month: month.attrib['href'], browser.css('.month')))

    @browsing
    def test_archive_portlet_not_available_on_plone_site(self, browser):
        """
        The events archive portlet is only rendered on events listing views.
        """
        events_folder = create(Builder('event folder').titled(u'Event Folder')
                               .with_property('layout', 'event_listing'))
        create(Builder('event page').titled(u'Event Entry 1').within(events_folder))

        self._add_portlet(browser)
        self.assertNotIn('Archive', browser.css('dt.portletHeader').text,
                         'Archive portlet is here but it should not be.')

    @browsing
    def test_archive_portlet_not_available_on_content_page(self, browser):
        """
        The events archive portlet is only rendered on events listing views.
        """
        page = create(Builder('sl content page').titled(u'Content Page'))
        events_folder = create(Builder('event folder').titled(u'Event Folder')
                               .with_property('layout', 'event_listing'))
        create(Builder('event page').titled(u'Event Entry 1').within(events_folder))

        self._add_portlet(browser, page)
        self.assertNotIn('Archive', browser.css('dt.portletHeader').text,
                         'Archive portlet is here but it should not be.')

    @browsing
    def test_archive_portlet_link(self, browser):
        """
        This test makes sure the summary is correct.
        """
        events_folder = create(Builder('event folder').titled(u'Event Folder')
                               .with_property('layout', 'event_listing'))
        create(Builder('event page').titled(u'Event Entry 1').within(events_folder)
               .having(start=datetime(2013, 1, 1), end=datetime(2013, 1, 1)))
        create(Builder('event page').titled(u'Event Entry 2').within(events_folder)
               .having(start=datetime(2013, 1, 11), end=datetime(2013, 1, 11)))

        self._add_portlet(browser, events_folder)

        browser.css('.month').first.click()
        self.assertEqual(2, len(browser.css('.event-item')))

    @browsing
    def test_month_with_umlaut(self, browser):
        lang_tool = api.portal.get_tool('portal_languages')
        lang_tool.setDefaultLanguage('de')
        transaction.commit()

        events_folder = create(Builder('event folder').titled(u'Event Folder')
                               .with_property('layout', 'event_listing'))
        create(Builder('event page').titled(u'Event Entry 1').within(events_folder)
               .having(start=datetime(2013, 3, 1), end=datetime(2013, 3, 1)))

        self._add_portlet(browser, events_folder)

        browser.css('.month').first.click()
        self.assertEqual(1, len(browser.css('.event-item')))
