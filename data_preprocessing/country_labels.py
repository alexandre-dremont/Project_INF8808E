# Abréviation des noms de pays trop longs pour l'affichage des axes.
# Le nom complet reste la donnée (survol, clic, jointures), on ne touche qu'au libellé.

COUNTRY_ABBR = {
    "Falkland Islands (Islas Malvinas)": "Falkland Islands",
    "Saint Vincent and the Grenadines": "St Vincent & Gren.",
    "Federated States of Micronesia": "Micronesia (Fed.)",
    "Democratic Republic of Congo": "DR Congo",
    "Northern Mariana Islands": "N. Mariana Is.",
    "Bosnia and Herzegovina": "Bosnia & Herz.",
    "British Virgin Islands": "British Virgin Is.",
    "Caribbean Netherlands": "Caribbean Neth.",
    "Saint Kitts and Nevis": "St Kitts & Nevis",
    "Sao Tome and Principe": "Sao Tome & Pr.",
    "Canary Islands (Sp.)": "Canary Islands",
    "United Arab Emirates": "UAE",
    "Syrian Arab Republic": "Syria",
    "Trinidad and Tobago": "Trinidad & Tobago",
}


def short_name(name, limit=18):
    """Libellé court d'un pays : abréviation connue, sinon troncature avec « … »."""
    if name in COUNTRY_ABBR:
        return COUNTRY_ABBR[name]
    return name if len(name) <= limit else name[:limit - 1].rstrip() + "…"
