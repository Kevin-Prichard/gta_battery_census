import csv
import gzip
import json
import os
import pickle
import sys
import time
from collections import namedtuple
from io import TextIOWrapper

import simplekml as K
from pyproj import Geod
from shapely.geometry import Polygon
from simplekml import StyleMap

geod = Geod(ellps="WGS84")
sqkm2sqmi = 0.386102


def load_boundary_file(fname, pruncate=0) -> Polygon:
    with open(fname, "r") as f:
        all = f.read()
    obj = json.loads(all[all.find("{"):])
    return Polygon(shell=[(p[0], p[1]) for p in obj["coordinates"][0][pruncate:]])


def get_area2(poly):
    # https://stackoverflow.com/a/64165076/604811
    return abs(geod.geometry_area_perimeter(poly)[0])


def load_tsv(fname: str, delim="\t"):
    c = 0
    if fname.lower().endswith(".tsv.gz"):
        fh = TextIOWrapper(gzip.open(filename=fname, mode="rb"), encoding="utf-8")
    elif fname.lower().endswith(".tsv"):
        fh = open(fname, "r")
    else:
        raise Exception(f"Don't know what to do with this pathname: {fname}")
    try:
        fields_line = fh.readline().strip()
        p = 0
        while ord(fields_line[p]) >= 128:
            p += 1
        fields = fields_line[p:].strip().split(delim)
        reader = csv.DictReader(fh, fields, delimiter=delim)
        for row in reader:
            c += 1
            yield row, c
    finally:
        fh.close()


def load_csv_indexed(csv_file, idx_colno, val_colnos, verbose=False):
    timest = time.time()
    indexed_data = dict()
    rowno = 0
    with open(csv_file, "r", encoding="latin1") as csv_fh:
        try:
            reader = csv.reader(csv_fh, delimiter=r"|")
            for r in reader:
                indexed_data[r[idx_colno]] = {colno: r[colno] for colno in val_colnos}
                rowno += 1
        except Exception as eee:
            print(f"{csv_file}\n{str(r)}\n{eee}\n")
            exit()

    if verbose:
        print(f"dur: {time.time() - timest} -- {csv_file}")
    return indexed_data


def put_data_snapshot(pathname, data):
    with open(pathname, "wb") as pfh:
        pickle.dump(data, pfh)
        print(f"Saved {pathname}")


def get_data_snapshot(pathname):
    if os.path.exists(pathname):
        with open(pathname, "rb") as pfh:
            print(f"Loaded {pathname}")
            return pickle.load(pfh)


def kml_abgr_pct(abgr_min: str, abgr_max: str, pct: float, color_els_aff: tuple, main_color_field):
    # print(abgr_min, abgr_max, pct, color_els_aff, main_color_field)
    els_min = [int(abgr_min[ptr:ptr + 2], 16)
               if ptr / 2 in color_els_aff else abgr_min[ptr:ptr + 2]
               for ptr in range(0, len(abgr_min), 2)]
    els_max = [int(abgr_max[ptr:ptr + 2], 16)
               if ptr / 2 in color_els_aff else abgr_max[ptr:ptr + 2]
               for ptr in range(0, len(abgr_max), 2)]
    for col_el in color_els_aff:
        els_min[col_el] = ('00' if int(pct * 100) <= 1 and col_el != main_color_field else hex(int(pct * (els_max[col_el] - els_min[col_el]) + els_min[col_el]))[2:].upper().zfill(2))
    return ''.join(els_min)


def make_stylemap_colorprop(width_norm, width_hilite, color_min, color_max, pct, color_fields, main_color_field):  # norm_col, norm_width, hi_col, hi_width
    color = kml_abgr_pct(color_min, color_max, pct, color_fields, main_color_field)
    # print(f"{color_min}..{color_max} * {pct} = {color}")
    sm = K.StyleMap()
    norm = K.Style()
    norm.linestyle.color = color
    norm.linestyle.width = width_norm
    norm.polystyle.color = color
    norm.polystyle.fill = 1
    norm.polystyle.outline = 1
    sm.normalstyle = norm
    hilite = K.Style()
    hilite.linestyle.color = color
    hilite.linestyle.width = width_hilite
    hilite.polystyle.color = color
    hilite.polystyle.fill = 1
    hilite.polystyle.outline = 1
    sm.highlightstyle = hilite
    return sm


def make_stylemap(cols_widths: dict):  # norm_col, norm_width, hi_col, hi_width
    sm = K.StyleMap()
    norm = K.Style()
    norm.linestyle.color = cols_widths["ncol"]
    norm.linestyle.width = cols_widths["nwidth"]
    norm.polystyle.color = cols_widths["ncol"]
    norm.polystyle.fill = 1
    norm.polystyle.outline = 1
    sm.normalstyle = norm
    hilite = K.Style()
    hilite.linestyle.color = cols_widths["hcol"]
    hilite.linestyle.width = cols_widths["hwidth"]
    hilite.polystyle.color = cols_widths["hcol"]
    hilite.polystyle.fill = 1
    hilite.polystyle.outline = 1
    sm.highlightstyle = hilite
    return sm


def add_polyline(doc, boundary, altitude: float = None):
    poly = doc.newpolygon(name=boundary.n, description=boundary.n)
    poly.outerboundaryis = list(boundary.b.exterior.coords)
    poly.placemark.geometry.outerboundaryis.gxaltitudeoffset = boundary.a or altitude
    poly.stylemap = boundary.c


class Boundary:
    b: Polygon = None
    n: str = None
    c: StyleMap = None
    a: float = None

    def __init__(self, b: Polygon, n: str, c: StyleMap, a: float = 0.0):
        self.b = b
        self.n = n
        self.c = c
        self.a = a


def printe(s, stream=sys.stderr):
    stream.write(s)
    stream.write("\n")


class DictObj(dict):
    def __init__(self, d=None):
        super().__init__(d)

    def __getattr__(self, item):
        if item in self:
            return self[item]


# KML color order: AaBbGgRr
Styleset = namedtuple('Styleset', ['width_norm', 'width_hilite', 'color_min', 'color_max', 'color_fields', 'main_color_field'])
Shapeset = namedtuple('AreaStyleset', ['boundary', 'styleset', 'cache_pathname'])
ShapesetConditional = namedtuple('AreaStyleset', ['boundary', 'styleset', 'cache_pathname', 'inclusion_fn', 'incl_styleset', 'excl_styleset'])
