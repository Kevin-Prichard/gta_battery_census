# All field defs extracted from-
#   pl_all_4_2020_dar.r in https://www2.census.gov/programs-surveys/decennial/rdo/about/2020-census-program/Phase3/SupportMaterials/2020PL_R_import_scripts.zip
# Extracted by running this in shell, then pasting each section to stdin-
#   perl -ane 'BEGIN{$c=0} ($fn, $desc)=$_=~m|^\#  (\w+)\s+(.+)|;  push @a,sprintf("    %-18s  # %s",sprintf("\"%s\": %d,", $fn, $c++), $desc);  END{$"="\n"; print "@a\n"}' > defs/geofields.txt

from common import DictObj


geo = DictObj({
    "FILEID": 0,        # File Identification
    "STUSAB": 1,        # State/US-Abbreviation (USPS)
    "SUMLEV": 2,        # Summary Level
    "GEOVAR": 3,        # Geographic Variant
    "GEOCOMP": 4,       # Geographic Component
    "CHARITER": 5,      # Characteristic Iteration
    "CIFSN": 6,         # Characteristic Iteration File Sequence Number
    "LOGRECNO": 7,      # Logical Record Number
    "GEOID": 8,         # Geographic Record Identifier
    "GEOCODE": 9,       # Geographic Code Identifier
    "REGION": 10,       # Region
    "DIVISION": 11,     # Division
    "STATE": 12,        # State (FIPS)
    "STATENS": 13,      # State (NS)
    "COUNTY": 14,       # County (FIPS)
    "COUNTYCC": 15,     # FIPS County Class Code
    "COUNTYNS": 16,     # County (NS)
    "COUSUB": 17,       # County Subdivision (FIPS)
    "COUSUBCC": 18,     # FIPS County Subdivision Class Code
    "COUSUBNS": 19,     # County Subdivision (NS)
    "SUBMCD": 20,       # Subminor Civil Division (FIPS)
    "SUBMCDCC": 21,     # FIPS Subminor Civil Division Class Code
    "SUBMCDNS": 22,     # Subminor Civil Division (NS)
    "ESTATE": 23,       # Estate (FIPS)
    "ESTATECC": 24,     # FIPS Estate Class Code
    "ESTATENS": 25,     # Estate (NS)
    "CONCIT": 26,       # Consolidated City (FIPS)
    "CONCITCC": 27,     # FIPS Consolidated City Class Code
    "CONCITNS": 28,     # Consolidated City (NS)
    "PLACE": 29,        # Place (FIPS)
    "PLACECC": 30,      # FIPS Place Class Code
    "PLACENS": 31,      # Place (NS)
    "TRACT": 32,        # Census Tract
    "BLKGRP": 33,       # Block Group
    "BLOCK": 34,        # Block
    "AIANHH": 35,       # American Indian Area/Alaska Native Area/Hawaiian Home Land (Census)
    "AIHHTLI": 36,      # American Indian Trust Land/Hawaiian Home Land Indicator
    "AIANHHFP": 37,     # American Indian Area/Alaska Native Area/Hawaiian Home Land (FIPS)
    "AIANHHCC": 38,     # FIPS American Indian Area/Alaska Native Area/Hawaiian Home Land Class Code
    "AIANHHNS": 39,     # American Indian Area/Alaska Native Area/Hawaiian Home Land (NS)
    "AITS": 40,         # American Indian Tribal Subdivision (Census)
    "AITSFP": 41,       # American Indian Tribal Subdivision (FIPS)
    "AITSCC": 42,       # FIPS American Indian Tribal Subdivision Class Code
    "AITSNS": 43,       # American Indian Tribal Subdivision (NS)
    "TTRACT": 44,       # Tribal Census Tract
    "TBLKGRP": 45,      # Tribal Block Group
    "ANRC": 46,         # Alaska Native Regional Corporation (FIPS)
    "ANRCCC": 47,       # FIPS Alaska Native Regional Corporation Class Code
    "ANRCNS": 48,       # Alaska Native Regional Corporation (NS)
    "CBSA": 49,         # Metropolitan Statistical Area/Micropolitan Statistical Area
    "MEMI": 50,         # Metropolitan/Micropolitan Indicator
    "CSA": 51,          # Combined Statistical Area
    "METDIV": 52,       # Metropolitan Division
    "NECTA": 53,        # New England City and Town Area
    "NMEMI": 54,        # NECTA Metropolitan/Micropolitan Indicator
    "CNECTA": 55,       # Combined New England City and Town Area
    "NECTADIV": 56,     # New England City and Town Area Division
    "CBSAPCI": 57,      # Metropolitan Statistical Area/Micropolitan Statistical Area Principal City Indicator
    "NECTAPCI": 58,     # New England City and Town Area Principal City Indicator
    "UA": 59,           # Urban Area
    "UATYPE": 60,       # Urban Area Type
    "UR": 61,           # Urban/Rural
    "CD116": 62,        # Congressional District (116th)
    "CD118": 63,        # Congressional District (118th)
    "CD119": 64,        # Congressional District (119th)
    "CD120": 65,        # Congressional District (120th)
    "CD121": 66,        # Congressional District (121st)
    "SLDU18": 67,       # State Legislative District (Upper Chamber) (2018)
    "SLDU22": 68,       # State Legislative District (Upper Chamber) (2022)
    "SLDU24": 69,       # State Legislative District (Upper Chamber) (2024)
    "SLDU26": 70,       # State Legislative District (Upper Chamber) (2026)
    "SLDU28": 71,       # State Legislative District (Upper Chamber) (2028)
    "SLDL18": 72,       # State Legislative District (Lower Chamber) (2018)
    "SLDL22": 73,       # State Legislative District (Lower Chamber) (2022)
    "SLDL24": 74,       # State Legislative District (Lower Chamber) (2024)
    "SLDL26": 75,       # State Legislative District (Lower Chamber) (2026)
    "SLDL28": 76,       # State Legislative District (Lower Chamber) (2028)
    "VTD": 77,          # Voting District
    "VTDI": 78,         # Voting District Indicator
    "ZCTA": 79,         # ZIP Code Tabulation Area (5-Digit)
    "SDELM": 80,        # School District (Elementary)
    "SDSEC": 81,        # School District (Secondary)
    "SDUNI": 82,        # School District (Unified)
    "PUMA": 83,         # Public Use Microdata Area
    "AREALAND": 84,     # Area (Land)
    "AREAWATR": 85,     # Area (Water)
    "BASENAME": 86,     # Area Base Name
    "NAME": 87,         # Area Name-Legal/Statistical Area Description (LSAD) Term-Part Indicator
    "FUNCSTAT": 88,     # Functional Status Code
    "GCUNI": 89,        # Geographic Change User Note Indicator
    "POP100": 90,       # Population Count (100%)
    "HU100": 91,        # Housing Unit Count (100%)
    "INTPTLAT": 92,     # Internal Point (Latitude)
    "INTPTLON": 93,     # Internal Point (Longitude)
    "LSADC": 94,        # Legal/Statistical Area Description Code
    "PARTFLAG": 95,     # Part Flag
    "UGA": 96,          # Urban Growth Area
})

part1 = DictObj({
    "FILEID": 0,  # File Identification
    "STUSAB": 1,  # State/US-Abbreviation (USPS)
    "CHARITER": 2,  # Characteristic Iteration
    "CIFSN": 3,  # Characteristic Iteration File Sequence Number
    "LOGRECNO": 4,  # Logical Record Number
    "P0010001": 5,  # Total:
    "P0010002": 6,  # Population of one race:
    "P0010003": 7,  # White alone
    "P0010004": 8,  # Black or African American alone
    "P0010005": 9,  # American Indian and Alaska Native alone
    "P0010006": 10,  # Asian alone
    "P0010007": 11,  # Native Hawaiian and Other Pacific Islander alone
    "P0010008": 12,  # Some Other Race alone
    "P0010009": 13,  # Population of two or more races:
    "P0010010": 14,  # Population of two races:
    "P0010011": 15,  # White; Black or African American
    "P0010012": 16,  # White; American Indian and Alaska Native
    "P0010013": 17,  # White; Asian
    "P0010014": 18,  # White; Native Hawaiian and Other Pacific Islander
    "P0010015": 19,  # White; Some Other Race
    "P0010016": 20,  # Black or African American; American Indian and Alaska Native
    "P0010017": 21,  # Black or African American; Asian
    "P0010018": 22,  # Black or African American; Native Hawaiian and Other Pacific Islander
    "P0010019": 23,  # Black or African American; Some Other Race
    "P0010020": 24,  # American Indian and Alaska Native; Asian
    "P0010021": 25,  # American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander
    "P0010022": 26,  # American Indian and Alaska Native; Some Other Race
    "P0010023": 27,  # Asian; Native Hawaiian and Other Pacific Islander
    "P0010024": 28,  # Asian; Some Other Race
    "P0010025": 29,  # Native Hawaiian and Other Pacific Islander; Some Other Race
    "P0010026": 30,  # Population of three races:
    "P0010027": 31,  # White; Black or African American; American Indian and Alaska Native
    "P0010028": 32,  # White; Black or African American; Asian
    "P0010029": 33,  # White; Black or African American; Native Hawaiian and Other Pacific Islander
    "P0010030": 34,  # White; Black or African American; Some Other Race
    "P0010031": 35,  # White; American Indian and Alaska Native; Asian
    "P0010032": 36,  # White; American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander
    "P0010033": 37,  # White; American Indian and Alaska Native; Some Other Race
    "P0010034": 38,  # White; Asian; Native Hawaiian and Other Pacific Islander
    "P0010035": 39,  # White; Asian; Some Other Race
    "P0010036": 40,  # White; Native Hawaiian and Other Pacific Islander; Some Other Race
    "P0010037": 41,  # Black or African American; American Indian and Alaska Native; Asian
    "P0010038": 42,  # Black or African American; American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander
    "P0010039": 43,  # Black or African American; American Indian and Alaska Native; Some Other Race
    "P0010040": 44,  # Black or African American; Asian; Native Hawaiian and Other Pacific Islander
    "P0010041": 45,  # Black or African American; Asian; Some Other Race
    "P0010042": 46,  # Black or African American; Native Hawaiian and Other Pacific Islander; Some Other Race
    "P0010043": 47,  # American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander
    "P0010044": 48,  # American Indian and Alaska Native; Asian; Some Other Race
    "P0010045": 49,  # American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander; Some Other Race
    "P0010046": 50,  # Asian; Native Hawaiian and Other Pacific Islander; Some Other Race
    "P0010047": 51,  # Population of four races:
    "P0010048": 52,  # White; Black or African American; American Indian and Alaska Native; Asian
    "P0010049": 53,  # White; Black or African American; American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander
    "P0010050": 54,  # White; Black or African American; American Indian and Alaska Native; Some Other Race
    "P0010051": 55,  # White; Black or African American; Asian; Native Hawaiian and Other Pacific Islander
    "P0010052": 56,  # White; Black or African American; Asian; Some Other Race
    "P0010053": 57,  # White; Black or African American; Native Hawaiian and Other Pacific Islander; Some Other Race
    "P0010054": 58,  # White; American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander
    "P0010055": 59,  # White; American Indian and Alaska Native; Asian; Some Other Race
    "P0010056": 60,  # White; American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander; Some Other Race
    "P0010057": 61,  # White; Asian; Native Hawaiian and Other Pacific Islander; Some Other Race
    "P0010058": 62,  # Black or African American; American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander
    "P0010059": 63,  # Black or African American; American Indian and Alaska Native; Asian; Some Other Race
    "P0010060": 64,  # Black or African American; American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander; Some Other Race
    "P0010061": 65,  # Black or African American; Asian; Native Hawaiian and Other Pacific Islander; Some Other Race
    "P0010062": 66,  # American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander; Some Other Race
    "P0010063": 67,  # Population of five races:
    "P0010064": 68,  # White; Black or African American; American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander
    "P0010065": 69,  # White; Black or African American; American Indian and Alaska Native; Asian; Some Other Race
    "P0010066": 70,  # White; Black or African American; American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander; Some Other Race
    "P0010067": 71,  # White; Black or African American; Asian; Native Hawaiian and Other Pacific Islander; Some Other Race
    "P0010068": 72,  # White; American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander; Some Other Race
    "P0010069": 73,  # Black or African American; American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander; Some Other Race
    "P0010070": 74,  # Population of six races:
    "P0010071": 75,  # White; Black or African American; American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander; Some Other Race
    "P0020001": 76,  # Total:
    "P0020002": 77,  # Hispanic or Latino
    "P0020003": 78,  # Not Hispanic or Latino:
    "P0020004": 79,  # Population of one race:
    "P0020005": 80,  # White alone
    "P0020006": 81,  # Black or African American alone
    "P0020007": 82,  # American Indian and Alaska Native alone
    "P0020008": 83,  # Asian alone
    "P0020009": 84,  # Native Hawaiian and Other Pacific Islander alone
    "P0020010": 85,  # Some Other Race alone
    "P0020011": 86,  # Population of two or more races:
    "P0020012": 87,  # Population of two races:
    "P0020013": 88,  # White; Black or African American
    "P0020014": 89,  # White; American Indian and Alaska Native
    "P0020015": 90,  # White; Asian
    "P0020016": 91,  # White; Native Hawaiian and Other Pacific Islander
    "P0020017": 92,  # White; Some Other Race
    "P0020018": 93,  # Black or African American; American Indian and Alaska Native
    "P0020019": 94,  # Black or African American; Asian
    "P0020020": 95,  # Black or African American; Native Hawaiian and Other Pacific Islander
    "P0020021": 96,  # Black or African American; Some Other Race
    "P0020022": 97,  # American Indian and Alaska Native; Asian
    "P0020023": 98,  # American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander
    "P0020024": 99,  # American Indian and Alaska Native; Some Other Race
    "P0020025": 100,  # Asian; Native Hawaiian and Other Pacific Islander
    "P0020026": 101,  # Asian; Some Other Race
    "P0020027": 102,  # Native Hawaiian and Other Pacific Islander; Some Other Race
    "P0020028": 103,  # Population of three races:
    "P0020029": 104,  # White; Black or African American; American Indian and Alaska Native
    "P0020030": 105,  # White; Black or African American; Asian
    "P0020031": 106,  # White; Black or African American; Native Hawaiian and Other Pacific Islander
    "P0020032": 107,  # White; Black or African American; Some Other Race
    "P0020033": 108,  # White; American Indian and Alaska Native; Asian
    "P0020034": 109,  # White; American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander
    "P0020035": 110,  # White; American Indian and Alaska Native; Some Other Race
    "P0020036": 111,  # White; Asian; Native Hawaiian and Other Pacific Islander
    "P0020037": 112,  # White; Asian; Some Other Race
    "P0020038": 113,  # White; Native Hawaiian and Other Pacific Islander; Some Other Race
    "P0020039": 114,  # Black or African American; American Indian and Alaska Native; Asian
    "P0020040": 115,  # Black or African American; American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander
    "P0020041": 116,  # Black or African American; American Indian and Alaska Native; Some Other Race
    "P0020042": 117,  # Black or African American; Asian; Native Hawaiian and Other Pacific Islander
    "P0020043": 118,  # Black or African American; Asian; Some Other Race
    "P0020044": 119,  # Black or African American; Native Hawaiian and Other Pacific Islander; Some Other Race
    "P0020045": 120,  # American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander
    "P0020046": 121,  # American Indian and Alaska Native; Asian; Some Other Race
    "P0020047": 122,  # American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander; Some Other Race
    "P0020048": 123,  # Asian; Native Hawaiian and Other Pacific Islander; Some Other Race
    "P0020049": 124,  # Population of four races:
    "P0020050": 125,  # White; Black or African American; American Indian and Alaska Native; Asian
    "P0020051": 126,  # White; Black or African American; American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander
    "P0020052": 127,  # White; Black or African American; American Indian and Alaska Native; Some Other Race
    "P0020053": 128,  # White; Black or African American; Asian; Native Hawaiian and Other Pacific Islander
    "P0020054": 129,  # White; Black or African American; Asian; Some Other Race
    "P0020055": 130,  # White; Black or African American; Native Hawaiian and Other Pacific Islander; Some Other Race
    "P0020056": 131,  # White; American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander
    "P0020057": 132,  # White; American Indian and Alaska Native; Asian; Some Other Race
    "P0020058": 133,  # White; American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander; Some Other Race
    "P0020059": 134,  # White; Asian; Native Hawaiian and Other Pacific Islander; Some Other Race
    "P0020060": 135,  # Black or African American; American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander
    "P0020061": 136,  # Black or African American; American Indian and Alaska Native; Asian; Some Other Race
    "P0020062": 137,  # Black or African American; American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander; Some Other Race
    "P0020063": 138,  # Black or African American; Asian; Native Hawaiian and Other Pacific Islander; Some Other Race
    "P0020064": 139,  # American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander; Some Other Race
    "P0020065": 140,  # Population of five races:
    "P0020066": 141,  # White; Black or African American; American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander
    "P0020067": 142,  # White; Black or African American; American Indian and Alaska Native; Asian; Some Other Race
    "P0020068": 143,  # White; Black or African American; American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander; Some Other Race
    "P0020069": 144,  # White; Black or African American; Asian; Native Hawaiian and Other Pacific Islander; Some Other Race
    "P0020070": 145,  # White; American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander; Some Other Race
    "P0020071": 146,  # Black or African American; American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander; Some Other Race
    "P0020072": 147,  # Population of six races:
    "P0020073": 148,  # White; Black or African American; American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander; Some Other Race
})

part2 = DictObj({
    "FILEID": 0,  # File Identification
    "STUSAB": 1,  # State/US-Abbreviation (USPS)
    "CHARITER": 2,  # Characteristic Iteration
    "CIFSN": 3,  # Characteristic Iteration File Sequence Number
    "LOGRECNO": 4,  # Logical Record Number
    "P0030001": 5,  # P3-1: Total
    "P0030002": 6,  # P3-2: Population of one race
    "P0030003": 7,  # P3-3: White alone
    "P0030004": 8,  # P3-4: Black or African American alone
    "P0030005": 9,  # P3-5: American Indian and Alaska Native alone
    "P0030006": 10,  # P3-6: Asian alone
    "P0030007": 11,  # P3-7: Native Hawaiian and Other Pacific Islander alone
    "P0030008": 12,  # P3-8: Some other race alone
    "P0030009": 13,  # P3-9: Population of two or more races
    "P0030010": 14,  # P3-10: Population of two races
    "P0030011": 15,  # P3-11: White; Black or African American
    "P0030012": 16,  # P3-12: White; American Indian and Alaska Native
    "P0030013": 17,  # P3-13: White; Asian
    "P0030014": 18,  # P3-14: White; Native Hawaiian and Other Pacific Islander
    "P0030015": 19,  # P3-15: White; Some other race
    "P0030016": 20,  # P3-16: Black or African American; American Indian and Alaska Native
    "P0030017": 21,  # P3-17: Black or African American; Asian
    "P0030018": 22,  # P3-18: Black or African American; Native Hawaiian and Other Pacific Islander
    "P0030019": 23,  # P3-19: Black or African American; Some other race
    "P0030020": 24,  # P3-20: American Indian and Alaska Native; Asian
    "P0030021": 25,  # P3-21: American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander
    "P0030022": 26,  # P3-22: American Indian and Alaska Native; Some other race
    "P0030023": 27,  # P3-23: Asian; Native Hawaiian and Other Pacific Islander
    "P0030024": 28,  # P3-24: Asian; Some other race
    "P0030025": 29,  # P3-25: Native Hawaiian and Other Pacific Islander; Some other race
    "P0030026": 30,  # P3-26: Population of three races
    "P0030027": 31,  # P3-27: White; Black or African American; American Indian and Alaska Native
    "P0030028": 32,  # P3-28: White; Black or African American; Asian
    "P0030029": 33,  # P3-29: White; Black or African American; Native Hawaiian and Other Pacific Islander
    "P0030030": 34,  # P3-30: White; Black or African American; Some other race
    "P0030031": 35,  # P3-31: White; American Indian and Alaska Native; Asian
    "P0030032": 36,  # P3-32: White; American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander
    "P0030033": 37,  # P3-33: White; American Indian and Alaska Native; Some other race
    "P0030034": 38,  # P3-34: White; Asian; Native Hawaiian and Other Pacific Islander
    "P0030035": 39,  # P3-35: White; Asian; Some other race
    "P0030036": 40,  # P3-36: White; Native Hawaiian and Other Pacific Islander; Some other race
    "P0030037": 41,  # P3-37: Black or African American; American Indian and Alaska Native; Asian
    "P0030038": 42,  # P3-38: Black or African American; American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander
    "P0030039": 43,  # P3-39: Black or African American; American Indian and Alaska Native; Some other race
    "P0030040": 44,  # P3-40: Black or African American; Asian; Native Hawaiian and Other Pacific Islander
    "P0030041": 45,  # P3-41: Black or African American; Asian; Some other race
    "P0030042": 46,  # P3-42: Black or African American; Native Hawaiian and Other Pacific Islander; Some other race
    "P0030043": 47,  # P3-43: American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander
    "P0030044": 48,  # P3-44: American Indian and Alaska Native; Asian; Some other race
    "P0030045": 49,  # P3-45: American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander; Some other race
    "P0030046": 50,  # P3-46: Asian; Native Hawaiian and Other Pacific Islander; Some other race
    "P0030047": 51,  # P3-47: Population of four races
    "P0030048": 52,  # P3-48: White; Black or African American; American Indian and Alaska Native; Asian
    "P0030049": 53,  # P3-49: White; Black or African American; American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander
    "P0030050": 54,  # P3-50: White; Black or African American; American Indian and Alaska Native; Some other race
    "P0030051": 55,  # P3-51: White; Black or African American; Asian; Native Hawaiian and Other Pacific Islander
    "P0030052": 56,  # P3-52: White; Black or African American; Asian; Some other race
    "P0030053": 57,  # P3-53: White; Black or African American; Native Hawaiian and Other Pacific Islander; Some other race
    "P0030054": 58,  # P3-54: White; American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander
    "P0030055": 59,  # P3-55: White; American Indian and Alaska Native; Asian; Some other race
    "P0030056": 60,  # P3-56: White; American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander; Some other race
    "P0030057": 61,  # P3-57: White; Asian; Native Hawaiian and Other Pacific Islander; Some other race
    "P0030058": 62,  # P3-58: Black or African American; American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander
    "P0030059": 63,  # P3-59: Black or African American; American Indian and Alaska Native; Asian; Some other race
    "P0030060": 64,  # P3-60: Black or African American; American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander; Some other race
    "P0030061": 65,  # P3-61: Black or African American; Asian; Native Hawaiian and Other Pacific Islander; Some other race
    "P0030062": 66,  # P3-62: American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander; Some other race
    "P0030063": 67,  # P3-63: Population of five races
    "P0030064": 68,  # P3-64: White; Black or African American; American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander
    "P0030065": 69,  # P3-65: White; Black or African American; American Indian and Alaska Native; Asian; Some other race
    "P0030066": 70,  # P3-66: White; Black or African American; American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander; Some other race
    "P0030067": 71,  # P3-67: White; Black or African American; Asian; Native Hawaiian and Other Pacific Islander; Some other race
    "P0030068": 72,  # P3-68: White; American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander; Some other race
    "P0030069": 73,  # P3-69: Black or African American; American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander; Some other race
    "P0030070": 74,  # P3-70: Population of six races
    "P0030071": 75,  # P3-71: White; Black or African American; American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander; Some other race
    "P0040001": 76,  # P4-1: Total
    "P0040002": 77,  # P4-2: Hispanic or Latino
    "P0040003": 78,  # P4-3: Not Hispanic or Latino
    "P0040004": 79,  # P4-4: Population of one race
    "P0040005": 80,  # P4-5: White alone
    "P0040006": 81,  # P4-6: Black or African American alone
    "P0040007": 82,  # P4-7: American Indian and Alaska Native alone
    "P0040008": 83,  # P4-8: Asian alone
    "P0040009": 84,  # P4-9: Native Hawaiian and Other Pacific Islander alone
    "P0040010": 85,  # P4-10: Some other race alone
    "P0040011": 86,  # P4-11: Population of two or more races
    "P0040012": 87,  # P4-12: Population of two races
    "P0040013": 88,  # P4-13: White; Black or African American
    "P0040014": 89,  # P4-14: White; American Indian and Alaska Native
    "P0040015": 90,  # P4-15: White; Asian
    "P0040016": 91,  # P4-16: White; Native Hawaiian and Other Pacific Islander
    "P0040017": 92,  # P4-17: White; Some other race
    "P0040018": 93,  # P4-18: Black or African American; American Indian and Alaska Native
    "P0040019": 94,  # P4-19: Black or African American; Asian
    "P0040020": 95,  # P4-20: Black or African American; Native Hawaiian and Other Pacific Islander
    "P0040021": 96,  # P4-21: Black or African American; Some other race
    "P0040022": 97,  # P4-22: American Indian and Alaska Native; Asian
    "P0040023": 98,  # P4-23: American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander
    "P0040024": 99,  # P4-24: American Indian and Alaska Native; Some other race
    "P0040025": 100,  # P4-25: Asian; Native Hawaiian and Other Pacific Islander
    "P0040026": 101,  # P4-26: Asian; Some other race
    "P0040027": 102,  # P4-27: Native Hawaiian and Other Pacific Islander; Some other race
    "P0040028": 103,  # P4-28: Population of three races
    "P0040029": 104,  # P4-29: White; Black or African American; American Indian and Alaska Native
    "P0040030": 105,  # P4-30: White; Black or African American; Asian
    "P0040031": 106,  # P4-31: White; Black or African American; Native Hawaiian and Other Pacific Islander
    "P0040032": 107,  # P4-32: White; Black or African American; Some other race
    "P0040033": 108,  # P4-33: White; American Indian and Alaska Native; Asian
    "P0040034": 109,  # P4-34: White; American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander
    "P0040035": 110,  # P4-35: White; American Indian and Alaska Native; Some other race
    "P0040036": 111,  # P4-36: White; Asian; Native Hawaiian and Other Pacific Islander
    "P0040037": 112,  # P4-37: White; Asian; Some other race
    "P0040038": 113,  # P4-38: White; Native Hawaiian and Other Pacific Islander; Some other race
    "P0040039": 114,  # P4-39: Black or African American; American Indian and Alaska Native; Asian
    "P0040040": 115,  # P4-40: Black or African American; American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander
    "P0040041": 116,  # P4-41: Black or African American; American Indian and Alaska Native; Some other race
    "P0040042": 117,  # P4-42: Black or African American; Asian; Native Hawaiian and Other Pacific Islander
    "P0040043": 118,  # P4-43: Black or African American; Asian; Some other race
    "P0040044": 119,  # P4-44: Black or African American; Native Hawaiian and Other Pacific Islander; Some other race
    "P0040045": 120,  # P4-45: American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander
    "P0040046": 121,  # P4-46: American Indian and Alaska Native; Asian; Some other race
    "P0040047": 122,  # P4-47: American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander; Some other race
    "P0040048": 123,  # P4-48: Asian; Native Hawaiian and Other Pacific Islander; Some other race
    "P0040049": 124,  # P4-49: Population of four races
    "P0040050": 125,  # P4-50: White; Black or African American; American Indian and Alaska Native; Asian
    "P0040051": 126,  # P4-51: White; Black or African American; American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander
    "P0040052": 127,  # P4-52: White; Black or African American; American Indian and Alaska Native; Some other race
    "P0040053": 128,  # P4-53: White; Black or African American; Asian; Native Hawaiian and Other Pacific Islander
    "P0040054": 129,  # P4-54: White; Black or African American; Asian; Some other race
    "P0040055": 130,  # P4-55: White; Black or African American; Native Hawaiian and Other Pacific Islander; Some other race
    "P0040056": 131,  # P4-56: White; American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander
    "P0040057": 132,  # P4-57: White; American Indian and Alaska Native; Asian; Some other race
    "P0040058": 133,  # P4-58: White; American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander; Some other race
    "P0040059": 134,  # P4-59: White; Asian; Native Hawaiian and Other Pacific Islander; Some other race
    "P0040060": 135,  # P4-60: Black or African American; American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander
    "P0040061": 136,  # P4-61: Black or African American; American Indian and Alaska Native; Asian; Some other race
    "P0040062": 137,  # P4-62: Black or African American; American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander; Some other race
    "P0040063": 138,  # P4-63: Black or African American; Asian; Native Hawaiian and Other Pacific Islander; Some other race
    "P0040064": 139,  # P4-64: American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander; Some other race
    "P0040065": 140,  # P4-65: Population of five races
    "P0040066": 141,  # P4-66: White; Black or African American; American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander
    "P0040067": 142,  # P4-67: White; Black or African American; American Indian and Alaska Native; Asian; Some other race
    "P0040068": 143,  # P4-68: White; Black or African American; American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander; Some other race
    "P0040069": 144,  # P4-69: White; Black or African American; Asian; Native Hawaiian and Other Pacific Islander; Some other race
    "P0040070": 145,  # P4-70: White; American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander; Some other race
    "P0040071": 146,  # P4-71: Black or African American; American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander; Some other race
    "P0040072": 147,  # P4-72: Population of six races
    "P0040073": 148,  # P4-73: White; Black or African American; American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander; Some other race
    "H0010001": 149,  # H1-1: Total
    "H0010002": 150,  # H1-2: Occupied
    "H0010003": 151,  # H1-3: Vacant
})

part3 = DictObj({
    "FILEID": 0,  # File Identification
    "STUSAB": 1,  # State/US-Abbreviation (USPS)
    "CHARITER": 2,  # Characteristic Iteration
    "CIFSN": 3,  # Characteristic Iteration File Sequence Number
    "LOGRECNO": 4,  # Logical Record Number
    "P0050001": 5,  # Total:
    "P0050002": 6,  # Institutionalized population:
    "P0050003": 7,  # Correctional facilities for adults
    "P0050004": 8,  # Juvenile facilities
    "P0050005": 9,  # Nursing facilities/Skilled-nursing facilities
    "P0050006": 10,  # Other institutional facilities
    "P0050007": 11,  # Noninstitutionalized population:
    "P0050008": 12,  # College/University student housing
    "P0050009": 13,  # Military quarters
    "P0050010": 14,  # Other noninstitutional facilities
})
