# eu-vat-rates-data · Python

[![PyPI version](https://img.shields.io/pypi/v/eu-vat-rates-data)](https://pypi.org/project/eu-vat-rates-data/)
[![Python versions](https://img.shields.io/pypi/pyversions/eu-vat-rates-data)](https://pypi.org/project/eu-vat-rates-data/)
[![Last updated](https://img.shields.io/github/last-commit/vatnode/eu-vat-rates-data-python?path=src%2Feu_vat_rates_data%2Feu_vat_rates_data.json&label=last%20updated)](https://github.com/vatnode/eu-vat-rates-data-python/commits/main)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

VAT rates for **44 European countries** — EU-27 plus Norway, Switzerland, UK, and more. EU rates sourced from the European Commission TEDB and checked daily. Non-EU rates maintained manually.

- Standard, reduced, super-reduced, and parking rates
- `eu_member` flag on every country — `True` for EU-27, `False` for non-EU
- `vat_name` — official name of the VAT tax in the country's primary official language
- `vat_abbr` — short abbreviation used locally (e.g. "ALV", "MwSt", "TVA")
- Full type hints — works with mypy and pyright out of the box
- Data embedded in the package — works offline, no network calls
- EU rates checked daily via GitHub Actions, new version published only when rates change

Also available in: [JavaScript/TypeScript (npm)](https://www.npmjs.com/package/eu-vat-rates-data) · [PHP (Packagist)](https://packagist.org/packages/vatnode/eu-vat-rates-data) · [Go](https://pkg.go.dev/github.com/vatnode/eu-vat-rates-data-go) · [Ruby (RubyGems)](https://rubygems.org/gems/eu_vat_rates_data)

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
from eu_vat_rates_data import get_rate, get_standard_rate, get_all_rates, is_eu_member, has_rate, data_version

# Full rate object for a country
fi = get_rate("FI")
# {
#   "country": "Finland",
#   "currency": "EUR",
#   "eu_member": True,
#   "vat_name": "Arvonlisävero",
#   "vat_abbr": "ALV",
#   "standard": 25.5,
#   "reduced": [10.0, 13.5],
#   "super_reduced": None,
#   "parking": None
# }

# Just the standard rate
get_standard_rate("DE")   # → 19.0

# EU membership check — False for non-EU countries (GB, NO, CH, ...)
if is_eu_member(user_input):
    rate = get_rate(user_input)

# Dataset membership check (all 44 countries)
if has_rate(user_input):
    rate = get_rate(user_input)

# All 44 countries at once
all_rates = get_all_rates()
for code, rate in all_rates.items():
    print(f"{code}: {rate['standard']}%")

# When were EU rates last fetched?
print(data_version)  # e.g. "2026-03-27"
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
    eu_member: bool
    vat_name: str
    vat_abbr: str
    standard: float
    reduced: list[float]
    super_reduced: float | None
    parking: float | None
```

---

## Data structure

`reduced` may contain rates for special territories (e.g. French DOM departments, Azores/Madeira for Portugal). For EU countries, all values come from EC TEDB.

Standard ISO 3166-1 alpha-2 country codes. Greece is `GR` (TEDB internally uses `EL`, which this package normalises).

### Example

```python
get_rate("NO")
# {
#   "country": "Norway",
#   "currency": "NOK",
#   "eu_member": False,
#   "vat_name": "Merverdiavgift",
#   "vat_abbr": "MVA",
#   "standard": 25.0,
#   "reduced": [12.0, 15.0],
#   "super_reduced": None,
#   "parking": None
# }
```

---

## Data source & update frequency

- EU-27 rates: **European Commission TEDB**, refreshed **daily at 07:00 UTC**
- Non-EU rates: maintained manually, updated on official rate changes
- Published to PyPI only when actual rates change (not on date-only updates)

---


## Keeping rates current

Rates are bundled at install time. A new package version is published automatically whenever rates change — but your installed version will not update itself.

**Recommended:** add [Renovate](https://renovatebot.com) or [Dependabot](https://docs.github.com/en/code-security/dependabot) to your repo. They detect new versions and open a PR automatically whenever rates change — no manual update commands needed.

**Need real-time accuracy?** Fetch the always-current JSON directly:

```
https://cdn.jsdelivr.net/gh/vatnode/eu-vat-rates-data@main/data/eu-vat-rates-data.json
```

No package needed — parse it with a single `fetch()` / `http.get()` / `file_get_contents()` call and cache locally.

---

## Covered countries

**EU-27** (daily auto-updates via EC TEDB):

`AT` `BE` `BG` `CY` `CZ` `DE` `DK` `EE` `ES` `FI` `FR` `GR` `HR` `HU` `IE` `IT` `LT` `LU` `LV` `MT` `NL` `PL` `PT` `RO` `SE` `SI` `SK`

**Non-EU Europe** (manually maintained):

`AD` `AL` `BA` `CH` `GB` `GE` `IS` `LI` `MC` `MD` `ME` `MK` `NO` `RS` `TR` `UA` `XK`

---

## Need to validate VAT numbers?

This package provides **VAT rates** only. If you also need to **validate EU VAT numbers** against the official VIES database — confirming a business is VAT-registered — check out [vatnode.dev](https://vatnode.dev), a simple REST API with a free tier.

```bash
curl https://api.vatnode.dev/v1/vat/FI17156132 \
  -H "Authorization: Bearer vat_live_..."
# → { "valid": true, "companyName": "Suomen Pehmeä Ikkuna Oy" }
```

---

## License

MIT

If you find this useful, a ⭐ on GitHub is appreciated.
