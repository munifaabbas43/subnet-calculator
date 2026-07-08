"""
Unit tests for subnet_calc.py
Author: Munifa Abbas
"""

import unittest
from subnet_calc import get_network_info


class TestSubnetCalculator(unittest.TestCase):

    def test_class_c_slash_24(self):
        info = get_network_info("192.168.1.0/24")
        self.assertEqual(info["network_address"], "192.168.1.0")
        self.assertEqual(info["broadcast_address"], "192.168.1.255")
        self.assertEqual(info["usable_hosts"], 254)
        self.assertEqual(info["netmask"], "255.255.255.0")

    def test_slash_26(self):
        info = get_network_info("192.168.10.0/26")
        self.assertEqual(info["broadcast_address"], "192.168.10.63")
        self.assertEqual(info["usable_hosts"], 62)
        self.assertEqual(info["first_usable_host"], "192.168.10.1")
        self.assertEqual(info["last_usable_host"], "192.168.10.62")

    def test_slash_30_point_to_point(self):
        info = get_network_info("10.0.0.0/30")
        self.assertEqual(info["usable_hosts"], 2)

    def test_slash_31(self):
        info = get_network_info("10.0.0.0/31")
        self.assertEqual(info["total_addresses"], 2)
        self.assertEqual(info["usable_hosts"], 2)

    def test_private_address_detection(self):
        info = get_network_info("10.1.1.0/24")
        self.assertTrue(info["is_private"])

    def test_public_address_detection(self):
        info = get_network_info("8.8.8.0/24")
        self.assertFalse(info["is_private"])

    def test_wildcard_mask(self):
        info = get_network_info("172.16.0.0/22")
        self.assertEqual(info["wildcard_mask"], "0.0.3.255")

    def test_invalid_input_exits(self):
        with self.assertRaises(SystemExit):
            get_network_info("not.an.ip/24")


if __name__ == "__main__":
    unittest.main()
