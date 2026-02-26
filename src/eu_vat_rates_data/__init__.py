"""EU VAT rates for all 27 member states + UK.

Data sourced from the European Commission TEDB (Taxes in Europe Database).
Updated daily, published automatically when rates change.

Usage::

    from eu_vat_rates_data import get_rate, get_standard_rate, is_eu_member, data_version

    rate = get_rate("FI")
    # VatRate(country='Finland', currency='EUR', standard=25.5,
    #         reduced=[10.0, 13.5], super_reduced=None, parking=None)

    get_standard_rate("DE")   # 19.0
    is_eu_member("FR")        # True
    print(data_version)       # "2026-02-25"
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
    "data_version",
    "dataset",
]


class VatRate(TypedDict):
    country: str
    currency: str
    standard: float
    reduced: list[float]
    super_reduced: Optional[float]
    parking: Optional[float]


def _load() -> dict:
    raw = files("eu_vat_rates_data").joinpath("eu_vat_rates_data.json").read_text(encoding="utf-8")
    return json.loads(raw)


_dataset: dict = _load()

#: The full dataset dict (version, source, url, rates).
dataset: dict = _dataset

#: ISO 8601 date string indicating when the data was last fetched from EC TEDB.
data_version: str = _dataset["version"]

_rates: dict[str, VatRate] = _dataset["rates"]


def get_rate(country_code: str) -> Optional[VatRate]:
    """Return the full VAT rate object for *country_code*, or None if not found.

    Args:
        country_code: ISO 3166-1 alpha-2 code (e.g. ``"FI"``, ``"DE"``, ``"GB"``).

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
    """Return all 28 country rate objects keyed by ISO country code.

    Returns:
        Dict mapping country code → :class:`VatRate`.
    """
    return dict(_rates)


def is_eu_member(country_code: str) -> bool:
    """Return True if *country_code* is in the dataset (EU-27 + GB).

    Args:
        country_code: ISO 3166-1 alpha-2 code.

    Returns:
        ``True`` if the country is covered, ``False`` otherwise.
    """
    return country_code.upper() in _rates
