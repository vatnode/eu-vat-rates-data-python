import re
import unittest

from eu_vat_rates_data import get_rate, get_standard_rate, get_all_rates, is_eu_member, data_version


class SmokeTest(unittest.TestCase):
    def test_de_standard_rate(self):
        self.assertEqual(get_standard_rate('DE'), 19.0)

    def test_ee_standard_rate(self):
        self.assertEqual(get_standard_rate('EE'), 24.0)

    def test_fr_is_eu_member(self):
        self.assertTrue(is_eu_member('FR'))

    def test_gb_is_not_eu_member(self):
        self.assertFalse(is_eu_member('GB'))

    def test_dataset_has_44_countries(self):
        self.assertEqual(len(get_all_rates()), 44)

    def test_eu_member_field_present(self):
        self.assertTrue(get_rate('DE')['eu_member'])
        self.assertFalse(get_rate('NO')['eu_member'])

    def test_data_version_format(self):
        self.assertRegex(data_version, r'^\d{4}-\d{2}-\d{2}$')


if __name__ == '__main__':
    unittest.main()
