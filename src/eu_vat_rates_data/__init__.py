"""VAT rates for 44 European countries (EU-27 + 17 non-EU).

EU rates sourced from the European Commission TEDB (Taxes in Europe Database),
checked daily. Non-EU rates maintained manually.

Usage::

    from eu_vat_rates_data import get_rate, get_standard_rate, is_eu_member, data_version

    rate = get_rate("FI")
    # VatRate(country='Finland', currency='EUR', eu_member=True,
    #         standard=25.5, reduced=[10.0, 13.5], super_reduced=None, parking=None)

    get_standard_rate("DE")   # 19.0
    is_eu_member("NO")        # False
    is_eu_member("FR")        # True
    print(data_version)       # "2026-03-18"
"""

from __future__ import annotations

import json
from importlib.resources import files
from typing import TypedDict, Optional

__all__ = [
    "VatRate",
    "get_rate",
    "get_standard_rate",
    "get_all_rates",
    "is_eu_member",
    "has_rate",
    "validate_format",
    "data_version",
    "dataset",
]


class VatRate(TypedDict):
    country: str
    currency: str
    eu_member: bool
    vat_name: str
    vat_abbr: str
    standard: float
    reduced: list[float]
    super_reduced: Optional[float]
    parking: Optional[float]
    format: str
    pattern: Optional[str]


def _load() -> dict:
    raw = files("eu_vat_rates_data").joinpath("eu_vat_rates_data.json").read_text(encoding="utf-8")
    return json.loads(raw)


_dataset: dict = _load()

#: The full dataset dict (version, source, url, rates).
dataset: dict = _dataset

#: ISO 8601 date string indicating when the EU data was last fetched from EC TEDB.
data_version: str = _dataset["version"]

_rates: dict[str, VatRate] = _dataset["rates"]


def get_rate(country_code: str) -> Optional[VatRate]:
    """Return the full VAT rate object for *country_code*, or None if not found.

    Args:
        country_code: ISO 3166-1 alpha-2 code (e.g. ``"FI"``, ``"DE"``, ``"NO"``).

    Returns:
        :class:`VatRate` dict or ``None``.
    """
    return _rates.get(country_code.upper())


def get_standard_rate(country_code: str) -> Optional[float]:
    """Return the standard VAT rate for *country_code*, or None if not found.

    Args:
        country_code: ISO 3166-1 alpha-2 code.

    Returns:
        Standard rate as a float (e.g. ``25.5``) or ``None``.
    """
    rate = get_rate(country_code)
    return rate["standard"] if rate else None


def get_all_rates() -> dict[str, VatRate]:
    """Return all 44 country rate objects keyed by ISO country code.

    Returns:
        Dict mapping country code → :class:`VatRate`.
    """
    return dict(_rates)


def is_eu_member(country_code: str) -> bool:
    """Return True if *country_code* is an EU-27 member state.

    Returns False for non-EU countries in the dataset (GB, NO, CH, etc.)
    and for unknown country codes.

    Args:
        country_code: ISO 3166-1 alpha-2 code.

    Returns:
        ``True`` for EU-27 member states, ``False`` otherwise.
    """
    rate = _rates.get(country_code.upper())
    return rate["eu_member"] if rate else False

def validate_format(vat_id: str) -> bool:
    """Return True if *vat_id* matches the expected format for its country.

    Input must include the country code prefix (e.g. ``"ATU12345678"``).
    Returns False when the country has no standardised format or the ID
    does not match.

    Note: Greece uses the ``"EL"`` prefix, not ``"GR"``.

    Args:
        vat_id: VAT number string including country code prefix.

    Returns:
        ``True`` if the format matches, ``False`` otherwise.
    """
    import re
    code = vat_id[:2].upper()
    rate = _rates.get(code)
    if not rate or not rate.get("pattern"):
        return False
    return bool(re.match(rate["pattern"], vat_id.upper()))


def has_rate(country_code: str) -> bool:
    """Return True if *country_code* is present in the dataset (all 44 countries).

    Use :func:`is_eu_member` to check EU membership specifically.

    Args:
        country_code: ISO 3166-1 alpha-2 code.

    Returns:
        ``True`` if the country is in the dataset, ``False`` otherwise.
    """
    return country_code.upper() in _rates
