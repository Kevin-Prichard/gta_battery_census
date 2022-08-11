
## Files relied on by the messy code of this repo

### Public Law Census records for 2020: data/ca2020/*.pl
Contains summarized census records, for California, at various summary levels.

(The summary level we utilize is the most discrete, SUMLEV==750, which is the "census block" level.)

Within a census block record, we'll find both the census count and the housing unit count.

This directory contains the unzipped contents of [data/ca2020.pl.zip](https://www2.census.gov/programs-surveys/decennial/2020/data/01-Redistricting_File--PL_94-171/California/ca2020.pl.zip).

```
gta_battery_census kev$ ls -l data/ca2020
total 1427176
-rw-rw-r--@ 1 kev  staff  219677245 Jul 26  2021 ca000012020.pl
-rw-rw-r--@ 1 kev  staff  223866202 Jul 26  2021 ca000022020.pl
-rw-rw-r--@ 1 kev  staff   29177851 Jul 26  2021 ca000032020.pl
-rw-rw-r--@ 1 kev  staff  256684567 Jul 26  2021 cageo2020.pl
```

### Geographical Area Shapefiles: data/tl_2020_06_tabblock
Contains the shapefiles, for California (the "06" part), for Census 2020, for census blocks.

A "census block" is the finest grouping level of census counts from housing units.

This directory contains the unzipped contents of [data/tl_2020_06_tabblock20.zip](https://www2.census.gov/geo/tiger/TIGER2020/TABBLOCK20/tl_2020_06_tabblock20.zip).

```
gta_battery_census kev$ ls -l data/tl_2020_06_tabblock
total 2741000
-rwxrwxr-x@ 1 kev  staff          5 Dec 21  2020 tl_2020_06_tabblock20.cpg
-rwxrwxr-x@ 1 kev  staff   54571429 Dec 21  2020 tl_2020_06_tabblock20.dbf
-rwxrwxr-x@ 1 kev  staff        165 Dec 21  2020 tl_2020_06_tabblock20.prj
-rwxrwxr-x@ 1 kev  staff  578271364 Dec 21  2020 tl_2020_06_tabblock20.shp
-rwxrwxr-x@ 1 kev  staff      26729 Dec 21  2020 tl_2020_06_tabblock20.shp.ea.iso.xml
-rwxrwxr-x@ 1 kev  staff      38435 Dec 21  2020 tl_2020_06_tabblock20.shp.iso.xml
-rwxrwxr-x@ 1 kev  staff    4157884 Dec 21  2020 tl_2020_06_tabblock20.shx
```

At some point, these files can be superseded by subsequent year versions, i.e.
https://www2.census.gov/geo/tiger/TIGER2021/TABBLOCK20/

Unclear whether there are in-between deccennial census for ca2020.pl.zip.  Haven't found one, circa Aug 2022.
