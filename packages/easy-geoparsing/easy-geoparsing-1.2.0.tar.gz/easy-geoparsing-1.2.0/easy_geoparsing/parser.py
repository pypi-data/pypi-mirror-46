import pandas as pd
from geotext import GeoText


class EasyCountryParser:

    """
    EasyCountryParser

    This class provides utilities, based on the data from the
    RESTcountries API and the GeoText natural-language parser library,
    for easily extracting and handling country names and codes.

    PROPERTIES:
        .data       - pandas DataFrame containing RESTcountries data
        .tld_to_a2c - python dict, maps TLDs to 2-character ISO codes
        .tld_to_a3c - python dict, maps TLDs to 3-character ISO codes
        .iso2to3    - python dict, maps 2-character ISO codes to 3
        .iso3to2    - python dict, maps 3-character ISO codes to 2
        .a2c_map    - python dict, maps 2-char ISO codes to full names
        .a3c_map    - python dict, maps 3-char ISO codes to full names

    METHODS:
        .retrieve_country - parses plaintext for extractable 2-character
                            ISO codes for countries (which can then be
                            manipulated using the mappers above)

    """

    def __init__(self, altnames=True):

        """
        __init__ for RESTcountries

        Downloads RESTcountries from V2 /all endpoint into a pandas
        DataFrame (RESTcountries.data)

        KEYWORDS:
            altnames = True - use alternative names for certain
                              countries (see get_countrymaps DocString)

        """

        self.data = pd.read_json("https://restcountries.eu/rest/v2/all")
        self.altnames = altnames

        self.get_codemaps()
        self.get_countrymaps()
        self.get_tld_maps()

    @staticmethod
    def retrieve_country(location_description):

        """
        retrieve_country

        This static method consumes a plain-text description of a
        location and uses the geotext library to match it to a country.
        The best match is returned, if there were any (may return None).

        INPUTS:
            location_description

        OUTPUTS:
            country_code - 2-character ISO-Geocode

        """

        if location_description in ["", None]:
            return None

        cdict = GeoText(location_description).country_mentions

        country_codes = list(cdict.keys())

        return country_codes[0] if len(country_codes) > 0 else None

    def get_codemaps(self):

        """
        get_codemaps

        Sets up two python dictionaries, iso2to3 and iso3to2. These map
        2-character ISO codes to 3-character codes and vice-versa.

        """

        self.iso2to3 = self.data.set_index("alpha2Code").alpha3Code.to_dict()
        self.iso3to2 = self.data.set_index("alpha3Code").alpha2Code.to_dict()

    def get_countrymaps(self):

        """
        get_countrymaps

        Generates mapping dictionaries for 2/3-character ISO codes to
        full names for display. If the altnames property of the class
        is set to True, these names will not all be the ones from the
        RESTcountries API (this alternate set are included for reasons of
        compatibility with other sources). The altnames flag is set to
        True by default and is set when the class is initialised.

        """

        self.a2c_map = self.data.set_index("alpha2Code").name.to_dict()
        self.a3c_map = self.data.set_index("alpha3Code").name.to_dict()

        if self.altnames:  # then reassign names to some countries

            alternates = (
                ("BO", "Bolivia"),
                ("VG", "British Virgin Islands"),
                ("VI", "United States Virgin Islands"),
                ("CV", "Cape Verde"),
                ("CD", "Congo"),
                ("FJ", "Fiji Fiji Islands"),
                ("VA", "Holy See (Vatican City State)"),
                ("CI", "Cote DIvoire"),
                ("IR", "Iran"),
                ("KG", "Kyrgyz Republic"),
                ("LA", "Lao"),
                ("LY", "Libyan Arab Jamahiriya"),
                ("MK", "Macedonia"),
                ("FM", "Micronesia"),
                ("MD", "Moldova"),
                ("PS", "Palestinian Territory"),
                ("RE", "Reunion"),
                ("VC", "Saint Vincent and Grenadines"),
                ("KR", "Korea"),
                ("TZ", "Tanzania"),
                ("GB", "United Kingdom"),
                ("UY", "Uruguay, Eastern Republic of"),
                ("VE", "Venezuela"),
                ("VN", "Vietnam"),
            )

            for iso2, aname in alternates:
                iso3 = self.iso2to3[iso2]
                self.a2c_map[iso2] = aname
                self.a3c_map[iso3] = aname

    def get_tld_maps(self):

        """
        get_tld_maps

        Uses RESTcountries.data to set up two dictionaries that map the
        top-level domains (TLDs) of countries to their 2/3-character
        ISO codes.

        These are set at RESTcountries.tld_to_a2c [_a3c]

        """

        self.tld_to_a2c = (
            self.data.set_index("alpha2Code")
            .topLevelDomain.map(lambda L: L[-1])
            .reset_index()
            .set_index("topLevelDomain")
            .alpha2Code.to_dict()
        )

        self.tld_to_a3c = (
            self.data.set_index("alpha3Code")
            .topLevelDomain.map(lambda L: L[-1])
            .reset_index()
            .set_index("topLevelDomain")
            .alpha3Code.to_dict()
        )

        self.tld_to_a2c[".gov"] = "US"
        self.tld_to_a2c[".wales"] = "GB"
        self.tld_to_a2c[".scot"] = "GB"

        self.tld_to_a3c[".gov"] = "USA"
        self.tld_to_a3c[".wales"] = "GBR"
        self.tld_to_a3c[".scot"] = "GBR"
