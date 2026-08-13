# Changelog

Rate changes themselves are not listed here — they land automatically whenever the
European Commission TEDB publishes them, and every change is visible in the commit
history of [`src/eu_vat_rates_data/eu_vat_rates_data.json`](https://github.com/vatnode/eu-vat-rates-data-python/commits/main/src/eu_vat_rates_data/eu_vat_rates_data.json).
This file records changes to the package API, the data format, and corrections to
hand-maintained fields.

## 2026-04-25

- **fix:** Corrected Sweden (SE) VAT number regex — was `^SE\d{12}$`, now correctly requires the mandatory `01` suffix: `^SE\d{10}01$`.
