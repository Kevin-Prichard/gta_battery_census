A very quick census block custom map generation effort.

### Summary-

- generates 2D and 3D KML map overlays of census blocks within a specified geo region
- sums population and housing units within a geo area
- also sums San Francisco business counts within a geo area

### Details-

- key dependencies --
  - [shapely](https://github.com/shapely/shapely) (geometry binary operations: intersection, contains)
  - [simplekml](https://github.com/eisoldt/simplekml) (KML generation)
  - [kmlplus](https://github.com/MHenderson1988/kmlplus) (KML polygon 2D to 3D extrusion), simplified by me to support specific parameters instead of func(*args, **kwargs) which were causing numerous issues, just (long,lat) parameters now
  - [rtree](https://github.com/Toblerity/rtree) - similar to k-d trees, allows binary and coordinate range selection of objects within a bounding box.  Addresses a weakness of Shapefile, which has a `.shapes()` method that accepts a bounding box parameter, but it fails
  - [Keene U's map-based lon-lat polygon definition tool](https://www.keene.edu/campus/maps/tool/) - useful for defining geo regions within which various operations are performed
- internal primitive operations (common.py) --
  - `load_boundary_file`: parses the `*.json.poly` format produced by Keene's map tool, returns a `shapely.geometry.Polygon` object
  - `get_area2`: returns m² of a shapely polygon
  - `load_tsv`: dict generator for CSV, TSV, PSV files
  - `load_csv_indexed`: returns a dict of a delimited file, where key is a particular column of unique values
  - `get_data_snapshot`, `put_data_snapshot`: pickling wrappers for klunky memoization so I could get runtime flush control, which typically isn't offered by memoization decorators
  - `kml_abgr_pct`: scale a KML AaBbGgRr color value according to `pct`.  Enables intensifying color bands and opacity according to the value represented by the object being colored
  - `make_stylemap_colorprop`: generate a KML StyleMap, normal color based on kml_abgr_pct ("color proportional")
  - `make_stylemap`: generate a KML StyleMap based on a dict of colors and widths
  - `add_polyline`: adds a polyline to a `simplekml.Kml` doc
  - class `Boundary`: represent a shapely polygon (`.b`), with additional name (`.n`), color (`.c`), and altitude (`.a`) for various uses incl simplekml ingestion
  - class `DictObj`: wraps a python `dict` so that keys can be accessed as attributes, e.g. `mydict.asdf` returns `mydict["asdf"]`. Python dicts are tedious to type for read access, this cleans it up a bit
- files & folders --
  - `defs`: contains `*.json.poly` files from Keene U's map tool
  - `defs/fields.py` contains U.S. Census PL field defs, extracted and pythonized from [their R source]( https://www2.census.gov/programs-surveys/decennial/rdo/about/2020-census-program/Phase3/SupportMaterials/2020PL_R_import_scripts.zip) - hat tip to @mcastillon for this link
  - `defs/boundaries.py`: contains an ugly mix of geo boundaries scraped and presented as Python arrays for conversion to shapely.geometry.Polygon; and also the ubiquitous `boundaries` dict, which more properly defines boundaries via `load_boundary_file` from [Keene U's map tool](https://www.keene.edu/campus/maps/tool/)
  - `data/data_sources.md`: tells where to get Census 2020, and to which subfolders it should be unzipped
  - `defs/stylesets.py`: predefines some simplekml style map objects
  - `tools` contains a copy of Keene U's map tool, on the off change it should one day vanish from the web.  It's based on a widely-used [leafletjs](https://leafletjs.com/) map project
  - `docs` currently hasn't got anything of interest, just a copy of a bunch of images for the presentation, which really shouldn't be on github

### Tests
No tests, this was a quick one-off.  There were many interim sanity check tests performed, to determine whether valid results were being produced.  _Next time I'll capture those as actual pytests, which I've never done before._
