from unittest import TestCase

from ems_client.service import Service


class ServiceTests(TestCase):

    def setUp(self):
        if not hasattr(self, '_api'):
            self._api = Service()

    def test_apiversion(self):
        version = self._api.get_api_version()
        self.assertGreaterEqual(version["Version"], "1.1.32.0", "API version")
        self.assertTrue(version["License"] in ["Basic", "Advanced"])

    def test_booking(self):
        booking = self._api.get_booking(8152)
        self.assertEquals(booking.event_name, 'Joe & Harold Wedding Reception')
        booking = self._api.get_booking(8806)
        self.assertEquals(booking.event_name, 'Test')

    def test_bookings(self):
        bookings = self._api.get_bookings('2016-01-01', '2016-01-01')
        self.assertGreaterEqual(len(bookings), 1)
        bookings = self._api.get_bookings('2016-01-02', '2016-01-02')
        self.assertGreaterEqual(len(bookings), 1)

    def test_buildings(self):
        buildings = self._api.get_buildings()
        self.assertGreaterEqual(len(buildings), 3)

    def test_event_types(self):
        event_types = self._api.get_event_types()
        self.assertGreaterEqual(len(event_types), 3)

    def test_rooms(self):
        rooms = self._api.get_all_rooms()
        self.assertGreaterEqual(len(rooms), 0)
        active_rooms = list(filter(lambda rm: rm.active, rooms))
        self.assertEqual(len(active_rooms), 53)

    def test_service_orders(self):
        service_orders = self._api.get_service_order_details('2016-01-01',
                                                             '2016-01-01')
        self.assertEqual(len(service_orders), 2)
        service_orders = self._api.get_service_order_details('2016-01-02',
                                                             '2016-01-02')
        self.assertEqual(len(service_orders), 4)

    def test_statuses(self):
        statuses = self._api.get_statuses()
        self.assertGreaterEqual(len(statuses), 16)
