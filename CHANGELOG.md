# Changelog

Rate changes themselves are not listed here — they land automatically whenever the
European Commission TEDB publishes them, and every change is visible in the commit
history of [`src/eu_vat_rates_data/eu_vat_rates_data.json`](https://github.com/vatnode/eu-vat-rates-data-python/commits/main/src/eu_vat_rates_data/eu_vat_rates_data.json).
This file records changes to the package API, the data format, and corrections to
hand-maintained fields.

## 2026-09-29

- **added:** `identifiers` on every country — `registry_authority_name`, `registry_name`, `registry_code_name`, `tax_id_name` and `vat_id_name`, keyed by language (every official language plus `en`), the name as the value. Names only, never numbers; `null` where no official name could be confirmed. TypedDict `Identifiers` and alias `LocalizedName` added.

## 2026-04-25

- **fix:** Corrected Sweden (SE) VAT number regex — was `^SE\d{12}$`, now correctly requires the mandatory `01` suffix: `^SE\d{10}01$`.
