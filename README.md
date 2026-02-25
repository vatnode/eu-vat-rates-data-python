# eu-vat-rates-data · Python

[![PyPI version](https://img.shields.io/pypi/v/eu-vat-rates-data)](https://pypi.org/project/eu-vat-rates-data/)
[![Python versions](https://img.shields.io/pypi/pyversions/eu-vat-rates-data)](https://pypi.org/project/eu-vat-rates-data/)
[![Last updated](https://img.shields.io/github/last-commit/vatnode/eu-vat-rates-python?path=src%2Feu_vat_rates_data%2Feu_vat_rates.json&label=last%20updated)](https://github.com/vatnode/eu-vat-rates-python/commits/main)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

EU VAT rates for all **27 EU member states** plus the **United Kingdom**, sourced from the [European Commission TEDB](https://taxation-customs.ec.europa.eu/tedb/vatRates.html). Checked daily, published automatically when rates change.

- Standard, reduced, super-reduced, and parking rates
- Full type hints — works with mypy and pyright out of the box
- Data embedded in the package — works offline, no network calls
- Checked daily via GitHub Actions, new version published only when rates change

Also available in: [JavaScript/TypeScript (npm)](https://www.npmjs.com/package/eu-vat-rates-data) · [PHP (Packagist)](https://packagist.org/packages/vatnode/eu-vat-rates-data) · [Go](https://pkg.go.dev/github.com/vatnode/eu-vat-rates-go) · [Ruby (RubyGems)](https://rubygems.org/gems/eu_vat_rates_data)

---

## Installation

```bash
pip install eu-vat-rates-data
# or
uv add eu-vat-rates-data
# or
poetry add eu-vat-rates-data
```

---

## Usage

```python
from eu_vat_rates_data import get_rate, get_standard_rate, get_all_rates, is_eu_member, data_version

# Full rate object for a country
fi = get_rate("FI")
# {
#   "country": "Finland",
#   "currency": "EUR",
#   "standard": 25.5,
#   "reduced": [10.0, 13.5],
#   "super_reduced": None,
#   "parking": None
# }

# Just the standard rate
get_standard_rate("DE")   # → 19.0

# Type guard
if is_eu_member(user_input):
    rate = get_rate(user_input)   # always returns a dict here

# All 28 countries at once
all_rates = get_all_rates()
for code, rate in all_rates.items():
    print(f"{code}: {rate['standard']}%")

# When were these rates last fetched?
print(data_version)  # e.g. "2026-02-25"
```

---

## Type hints

```python
from eu_vat_rates_data import VatRate

rate: VatRate = get_rate("FI")  # type checker knows this is a TypedDict
```

```python
class VatRate(TypedDict):
    country: str
    currency: str
    standard: float
    reduced: list[float]
    super_reduced: float | None
    parking: float | None
```

---

## Data structure

`reduced` may contain rates for special territories (e.g. French DOM departments, Azores/Madeira for Portugal). All values come verbatim from EC TEDB.

Standard ISO 3166-1 alpha-2 country codes. Greece is `GR` (TEDB internally uses `EL`, which this package normalises).

### Example

```python
get_rate("PT")
# {
#   "country": "Portugal",
#   "currency": "EUR",
#   "standard": 23.0,
#   "reduced": [6.0, 13.0],   # mainland + Azores/Madeira variants
#   "super_reduced": None,
#   "parking": None
# }
```

---

## Data source & update frequency

Rates are fetched from the **European Commission Taxes in Europe Database (TEDB)**:

- Canonical data repo: **https://github.com/vatnode/eu-vat-rates-data**
- Refreshed: **daily at 08:00 UTC**
- Published to PyPI only when actual rates change (not on date-only updates)

---

## Covered countries

EU-27 member states + United Kingdom (28 countries total):

`AT BE BG CY CZ DE DK EE ES FI FR GB GR HR HU IE IT LT LU LV MT NL PL PT RO SE SI SK`

---

## License

MIT
