"""Test for the Queensland Bushfire Alert feed."""
import datetime
import unittest
from unittest import mock

from georss_client import UPDATE_OK
from georss_qld_bushfire_alert_client import \
    QldBushfireAlertFeed, QldBushfireAlertFeedManager
from tests import load_fixture

HOME_COORDINATES = (-31.0, 151.0)


class TestQldBushfireAlertFeed(unittest.TestCase):
    """Test the Qld Bushfire Alert feed."""

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_update_ok(self, mock_session, mock_request):
        """Test updating feed is ok."""
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = \
            load_fixture('qld_bushfire_alert_feed.xml')

        feed = QldBushfireAlertFeed(HOME_COORDINATES)
        assert repr(feed) == "<QldBushfireAlertFeed(home=(-31.0, 151.0), " \
                             "url=https://www.qfes.qld.gov.au/data/alerts/" \
                             "bushfireAlert.xml, radius=None, categories=" \
                             "None)>"
        status, entries = feed.update()
        assert status == UPDATE_OK
        self.assertIsNotNone(entries)
        assert len(entries) == 2

        feed_entry = entries[0]
        assert feed_entry.title == "Title 1"
        assert feed_entry.external_id == "1234"
        assert feed_entry.coordinates == (-32.2345, 149.1234)
        self.assertAlmostEqual(feed_entry.distance_to_home, 224.5, 1)
        assert feed_entry.published == datetime.datetime(2018, 9, 27, 8, 0)
        assert feed_entry.updated == datetime.datetime(2018, 9, 27, 8, 30)
        assert feed_entry.status == "Status 1"
        assert feed_entry.attribution == "Author 1"
        assert repr(feed_entry) == "<QldBushfireAlertFeedEntry(id=1234)>"

        feed_entry = entries[1]
        assert feed_entry.title == "Title 2"
        self.assertIsNone(feed_entry.published)
        self.assertIsNone(feed_entry.updated)

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_update_ok_with_category(self, mock_session, mock_request):
        """Test updating feed is ok."""
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = \
            load_fixture('qld_bushfire_alert_feed.xml')

        feed = QldBushfireAlertFeed(
            HOME_COORDINATES,
            filter_categories=['Category 1'])
        status, entries = feed.update()
        assert status == UPDATE_OK
        self.assertIsNotNone(entries)
        assert len(entries) == 1

        feed_entry = entries[0]
        assert feed_entry.title == "Title 1"
        assert feed_entry.external_id == "1234"

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_feed_manager(self, mock_session, mock_request):
        """Test the feed manager."""
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = load_fixture(
                'qld_bushfire_alert_feed.xml')

        # This will just record calls and keep track of external ids.
        generated_entity_external_ids = []
        updated_entity_external_ids = []
        removed_entity_external_ids = []

        def _generate_entity(external_id):
            """Generate new entity."""
            generated_entity_external_ids.append(external_id)

        def _update_entity(external_id):
            """Update entity."""
            updated_entity_external_ids.append(external_id)

        def _remove_entity(external_id):
            """Remove entity."""
            removed_entity_external_ids.append(external_id)

        feed_manager = QldBushfireAlertFeedManager(
            _generate_entity,
            _update_entity,
            _remove_entity,
            HOME_COORDINATES)
        assert repr(feed_manager) == "<QldBushfireAlertFeedManager(" \
                                     "feed=<QldBushfireAlertFeed(home=" \
                                     "(-31.0, 151.0), url=https://www." \
                                     "qfes.qld.gov.au/data/alerts/" \
                                     "bushfireAlert.xml, " \
                                     "radius=None, categories=None)>)>"
        feed_manager.update()
        entries = feed_manager.feed_entries
        self.assertIsNotNone(entries)
        assert len(entries) == 2
        assert feed_manager.last_timestamp \
            == datetime.datetime(2018, 9, 27, 8, 0)
        assert len(generated_entity_external_ids) == 2
        assert len(updated_entity_external_ids) == 0
        assert len(removed_entity_external_ids) == 0
