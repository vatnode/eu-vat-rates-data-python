import re
import unittest

from eu_vat_rates_data import get_rate, get_all_rates, is_eu_member, data_version, validate_format


class SmokeTest(unittest.TestCase):
    def test_de_is_eu_member(self):
        self.assertTrue(is_eu_member('DE'))

    def test_gb_is_not_eu_member(self):
        self.assertFalse(is_eu_member('GB'))

    def test_no_is_not_eu_member(self):
        self.assertFalse(is_eu_member('NO'))

    def test_dataset_has_45_countries(self):
        self.assertEqual(len(get_all_rates()), 45)

    def test_all_standard_rates_positive(self):
        for code, rate in get_all_rates().items():
            self.assertGreater(rate['standard'], 0, f'{code}: standard rate is {rate["standard"]}')

    def test_eu_member_field_is_bool(self):
        for code, rate in get_all_rates().items():
            self.assertIsInstance(rate['eu_member'], bool, f'{code}: eu_member is not bool')

    def test_all_vat_names_non_empty(self):
        for code, rate in get_all_rates().items():
            self.assertIsInstance(rate['vat_name'], str, f'{code}: vat_name is not str')
            self.assertGreater(len(rate['vat_name']), 0, f'{code}: vat_name is empty')

    def test_data_version_format(self):
        self.assertRegex(data_version, r'^\d{4}-\d{2}-\d{2}$')

    def test_unknown_country_returns_none(self):
        self.assertIsNone(get_rate('XX'))


if __name__ == '__main__':
    unittest.main()

    def test_validate_format_accepts_well_formed_ids(self):
        self.assertTrue(validate_format('ATU12345678'))
        self.assertTrue(validate_format('DE123456789'))
        self.assertTrue(validate_format('atu12345678'))

    def test_validate_format_rejects_malformed_input(self):
        self.assertFalse(validate_format(''))
        self.assertFalse(validate_format('INVALID'))
        self.assertFalse(validate_format('DE12'))

    def test_validate_format_handles_greek_el_prefix(self):
        # Greek VAT numbers carry the VIES prefix EL while the dataset keys Greece as GR.
        self.assertTrue(validate_format('EL123456789'))
        self.assertTrue(validate_format('el123456789'))
        self.assertFalse(validate_format('EL12345678'))
