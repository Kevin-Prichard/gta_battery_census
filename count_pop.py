#!/usr/bin/env python3.10

import os
import re
import sys
from collections import defaultdict as dd
from copy import deepcopy
from typing import Callable, List

import shapefile
import shapely
import simplekml
import simplekml as K
from dbfread import DBF
from rtree import index as rtree_index
from shapely.geometry import Point, Polygon

from common import (get_area2, sqkm2sqmi, load_tsv, load_csv_indexed, printe,
                    put_data_snapshot, get_data_snapshot, add_polyline,
                    make_stylemap_colorprop, Styleset, DictObj,
                    load_boundary_file, Shapeset, Boundary)
from defs.boundaries import (battery_east, battery_west,
                             battery_west_stockton, battery_west_powell,
                             battery_west_van_ness, boundaries)
from defs.fields import geo, part1, part2
from defs.stylesets import *
from kmlplus import paths

object_maker_fn: Callable
CENSUS_2020_SHAPEFILE = "data/tl_2020_06_tabblock/tl_2020_06_tabblock20.shp"


def find_block_shapes(shp_pathname, boundary_coords, verbose=False):
    boundaries = Polygon(shell=[(p[0], p[1]) for p in boundary_coords])
    shp = shapefile.Reader(shp_pathname)
    file_num = 0
    shape_num = 0
    for s in shp.shapes():
        shape_num += 1
        if verbose and shape_num / 1000 == int(shape_num / 1000):
            printe(f"At shape_num: {shape_num}")
        for p in range(0, len(s.bbox) - 1, 2):
            if boundaries.contains(Point(s.bbox[p], s.bbox[p + 1])):
                filename = f"found_obj_{file_num}.txt"
                with open(filename, "w") as fh:
                    fh.write("\n".join(f"{p[0]}, {p[1]}" for p in s.points))
                if verbose:
                    printe(f"\tWrote {len(s.points)} to {filename}")
                file_num += 1


def convert_found_objs_to_kml(bounds, stylemap):
    file_tmpl = "found_objs/found_obj_{n}.txt"
    doc = simplekml.Kml(name="Blocks from Van Ness to Embarcadero, Bay to Market")

    for n in range(*bounds):
        coords = []
        fn = file_tmpl.format(n=n)
        with open(fn, "r") as fh:
            for point_text in fh.readlines():
                coords.append(list(map(float, point_text.split(", "))))
        poly = doc.newpolygon(name=fn, description=fn)
        poly.outerboundaryis = coords
        poly.placemark.geometry.outerboundaryis.gxaltitudeoffset = 0
        poly.stylemap = stylemap
    doc.save("test.kml")


def read_recs(f, IDs):
    db = DBF(f)
    c = 0
    chkfld = "NAME20"  # "GEOID20"
    dupes = dict()
    dupe_cnt = 0
    geoid_min, geoid_max = "zzzzzzzzzzzzzzzzzzz", "0000000000000000000000"
    for r in db:
        chk = r[chkfld]
        if chk < geoid_min:
            geoid_min = chk
            printe(r)
        if chk > geoid_max:
            geoid_max = chk
            printe(r)
        if chk not in dupes:
            dupes[chk] = 1
            dupe_cnt += 1
        c += 1
    printe(f"{geoid_min}, {geoid_max}, {dupe_cnt}, {c}")


def get_shape_dbf_coords(dbfn, shfn, rowno):
    for idx, r in enumerate(DBF(dbfn)):
        if idx == rowno:
            printe(r)
            break

    shp = shapefile.Reader(shfn)
    for idx, s in enumerate(shp.shapes()):
        if idx == rowno:
            printe(s.bbox, s.oid)


def print_cap_dict(d, label=None, key_subst=None, skip_keys=None):
    if label:
        printe(label)
    tot = 0
    for k in sorted(d.keys(), key=lambda x: key_subst[x] if key_subst else x):
        if not skip_keys or k not in skip_keys:
            printe(f"{key_subst[k] if key_subst else k}\t{d[k]}")
            tot += d[k]
    printe(f"Total: {tot}")


def convert_geoids_to_oids(dbf_pathname, geoids_wanted) -> dict:
    # Translate LOGRECIDs to positional OIDs
    table = DBF(dbf_pathname)
    oids = dict()
    oid = 0
    for r in table:
        if info := geoids_wanted.get(r["GEOID20"]):
            oids[oid] = info
        oid += 1
    return oids


def make_kml_poly(doc, label, shape, styleset, scaling_coef=1.0, altitude: float = None):
    if isinstance(styleset, Styleset):
        stylemap = make_stylemap_colorprop(**styleset._asdict(), pct=scaling_coef)
    else:
        stylemap = make_stylemap_colorprop(**styleset, pct=scaling_coef)
    poly = doc.newpolygon(name=label, description=label)
    if getattr(shape, 'points'):
        poly.outerboundaryis = shape.points
    else:
        poly.outerboundaryis = shape
    altitude = 0.0 if altitude is None else altitude
    poly.placemark.geometry.outerboundaryis.gxaltitudeoffset = altitude
    poly.stylemap = stylemap

    return poly


def make_kml_poly_3d(doc, label, shape, styleset, scaling_coef, max_height=None):
    stylemap = make_stylemap_colorprop(**styleset, pct=scaling_coef)
    points = shape.points if hasattr(shape, 'points') else shape
    lower_layer, upper_layer, sides = paths.quick_polygon(
        points, lower_height=0, upper_height=int(scaling_coef * max_height))
    fol = doc.newfolder(name=f"Folder {label}")

    poly = fol.newpolygon(name=f"Lower layer label {label}", description=f"Lower layer desc {label}")
    poly.outerboundaryis = lower_layer.kml_coordinate_list
    poly.altitudemode = K.AltitudeMode.relativetoground
    poly.stylemap = stylemap

    poly = fol.newpolygon(name=f"Upper layer label {label}", description=f"Upper layer desc {label}")
    poly.outerboundaryis = upper_layer.kml_coordinate_list
    poly.altitudemode = K.AltitudeMode.relativetoground
    poly.stylemap = stylemap

    for idx, item in enumerate(sides):
        poly = fol.newpolygon(name=f"Side#{idx} label {label}", description=f"Side#{idx} desc {label}")
        poly.outerboundaryis = item
        poly.altitudemode = K.AltitudeMode.relativetoground
        poly.stylemap = stylemap

    return poly


def get_oid_mins_maxes(oids, field_num):
    val_min, val_max = float("inf"), float("-inf")
    for _, vals in oids.items():
        val = float(vals[field_num])
        if val < val_min:
            val_min = val
        if val > val_max:
            val_max = val
    return val_min, val_max


def convert_oids_to_shape_kml(oids, shp_pathname, boundaries, layer_name, styleset, max_height=100, verbose=False):
    doc = simplekml.Kml(name=layer_name)
    pop_min, pop_max = get_oid_mins_maxes(oids, "POP100")
    scaling_pct_denom = pop_max - pop_min  # absolute range of population values, minus smallest value, for scaling
    shp = shapefile.Reader(shp_pathname)
    shape_num = 0
    oids_in_bounds = 0
    total_pop = 0
    total_hou = 0
    for s in shp.shapes():
        if info := oids.get(s.oid):
            if boundaries.intersects(points_to_poly(s.points)):
                if float(info['HU100']) > 0 and float(info['POP100']) > 0:
                    scale_coef = (float(info['POP100']) - pop_min) / scaling_pct_denom
                else:
                    scale_coef = 0
                label = (
                    f"Population: {info['POP100'] if int(info['HU100']) > 0 else 0}, "
                    f"Housing Units: {info['HU100']}\n"
                    f"GeoID: {info['GEOID']}")
                object_maker_fn(doc, label, s, styleset, scale_coef, max_height=max_height)
                oids_in_bounds += 1
                if int(info['HU100']) > 0:
                    total_hou += int(info['HU100'])
                    total_pop += int(info['POP100'])
        shape_num += 1
        if verbose and shape_num / 1000 == int(shape_num / 1000):
            printe(f"At shape_num: {shape_num}, polys found in boundaries: {oids_in_bounds}/{len(oids)}")

    printe(f"Within boundaries: "
           f"population {total_pop}, "
           f"housing units {total_hou}, "
           f"census blocks {oids_in_bounds}/{len(oids)}")
    doc.description = f"Population: {total_pop}\n" \
                      f"Housing units {total_hou}\n" \
                      f"Census Blocks {oids_in_bounds}"
    return doc


def points_to_poly(points):
    return Polygon(shell=[(p[0], p[1]) for p in points])


csv_files = DictObj({
    "part1": "data/ca2020/ca000012020.pl",
    "part2": "data/ca2020/ca000022020.pl",
    "part3": "data/ca2020/ca000032020.pl",
    "geo": "data/ca2020/cageo2020.pl",
})


def get_geo_bounded_population_and_housing(boundaries, verbose=False):
    p1 = load_csv_indexed(csv_files.part1, part1.keys(), part1.LOGRECNO, (part1.P0010001, part1.P0010002))
    p2 = load_csv_indexed(csv_files.part2, part2.keys(), part2.LOGRECNO, (part2.P0030001, part2.P0030002))
    g1 = load_csv_indexed(csv_files.geo, geo.keys(), geo.LOGRECNO, (
        geo.GEOID, geo.GEOVAR, geo.GEOCOMP, geo.SUMLEV, geo.GEOCODE, geo.POP100, geo.HU100, geo.INTPTLAT, geo.INTPTLON))
    geo_pop = 0
    geo_hou = 0
    geo_recs = 0
    p1_pop1 = 0
    p1_pop2 = 0
    p2_pop1 = 0
    p2_pop2 = 0
    c = 0

    gv = dd(int)
    gc = dd(int)
    sl = dd(int)
    gvp = dd(int)
    gcp = dd(int)
    slp = dd(int)
    geoids = dict()
    try:
        p = None
        for logrecno, georec in g1.items():
            gv[georec[geo.GEOVAR]] += 1
            gc[georec[geo.GEOCOMP]] += 1
            sl[georec[geo.SUMLEV]] += 1
            if georec[geo.SUMLEV] == "750":
                if boundaries.contains(p := Point(float(georec[geo.INTPTLON]), float(georec[geo.INTPTLAT]))):
                    gvp[georec[geo.GEOVAR]] += int(georec[geo.POP100])
                    gcp[georec[geo.GEOCOMP]] += int(georec[geo.POP100])
                    slp[georec[geo.SUMLEV]] += int(georec[geo.POP100])
                    geo_pop += float(georec[geo.POP100])
                    geo_hou += float(georec[geo.HU100])
                    geo_recs += 1
                    p1_pop1 += float(p1[logrecno][part1.P0010001])
                    p1_pop2 += float(p1[logrecno][part1.P0010002])
                    p2_pop1 += float(p2[logrecno][part2.P0030001])
                    p2_pop2 += float(p2[logrecno][part2.P0030002])
                    geoids[georec[geo.GEOID][9:]] = {"GEOID": georec[geo.GEOID][9:], "POP100": georec[geo.POP100], "HU100": georec[geo.HU100]}
            if verbose and c / 10000 == int(c / 10000):
                printe(geo_recs, c)
            c += 1
    except Exception as ee:
        import pudb;
        pu.db
        x = 1

    if verbose:
        printe(f"total_pop: {geo_pop}, total_hou: {geo_hou}, total_recs: {geo_recs}")
        printe(f"p1_pop1: {p1_pop1}, p1_pop2: {p1_pop2}, p2_pop1: {p2_pop1}, p2_pop2: {p2_pop2}")
        print_cap_dict(gv, label="Geographic Variant")
        print_cap_dict(gc, label="Geographic Component")
        print_cap_dict(sl, label="Summary Level")
        printe("\n\n")
        print_cap_dict(gvp, label="Geographic Variant Population")
        print_cap_dict(gcp, label="Geographic Component Population")
        print_cap_dict(slp, label="Summary Level Population")
    return geoids


def gen_map_from_census_pop_and_blocks(
        boundary_file_or_points, pathname_prefix, project_title, styleset,
        sumlev=750, max_height=250, reset=False, produce_map=True, kml_suffix=".kml"):
    printe(project_title)
    if isinstance(boundary_file_or_points, str):
        boundaries = load_boundary_file(boundary_file_or_points)
    else:
        boundaries = points_to_poly(boundary_file_or_points)

    # Find GEOIDs for SUMLEV=sumlev (typically 750, block-level)
    geoids_pathname = f"{pathname_prefix}geoids.pkl"
    if reset or not (geoids_within := get_data_snapshot(geoids_pathname)):
        geoids_within = get_geo_bounded_population_and_housing(boundaries)
        put_data_snapshot(geoids_pathname, geoids_within)

    # Convert (or lookup) GEOIDs to OIDs;
    #     .oid is the unique ID for shapefile objects, corresponds to rowno in the .dbf
    oids_pathname = f"{pathname_prefix}oids.pkl"
    if reset or not (oids_within := get_data_snapshot(oids_pathname)):
        oids_within = convert_geoids_to_oids(
            "data/tl_2020_06_tabblock/tl_2020_06_tabblock20.dbf",
            geoids_within)
        put_data_snapshot(oids_pathname, oids_within)

    # Lookup shapes for the oids found within boundaries
    if produce_map:
        kml = convert_oids_to_shape_kml(
            oids_within,
            "data/tl_2020_06_tabblock/tl_2020_06_tabblock20.shp",
            boundaries,
            project_title,
            styleset,
            max_height=max_height,
        )
        kml.save(save_path := f"{pathname_prefix}sumlev-{sumlev}{kml_suffix}")
        printe(f"Saved {save_path}")

    return {"geoids": geoids_within, "oids": oids_within}


POINT_WKT_RX = re.compile(r"^\s*POINT\s*\((\S+)\s*(\S+)\)\s*$")


def wkt_point_to_polyline(wkt):
    parts = POINT_WKT_RX.match(wkt).groups()
    xy = float(parts[0]), float(parts[1])
    return points_to_poly([xy, xy, xy])


def get_included_businesses(boundaries, business_census_csv_file):
    #  list(boundaries.boundary.array_interface()['data'])
    discarded_empty = 0
    businesses_within = []
    addresses_seen = dd(int)
    for biz, cnt in load_tsv(business_census_csv_file, '\t'):
        if biz['Location End Date']:
            if biz['Business Location']:
                poly = wkt_point_to_polyline(biz['Business Location'])
                if boundaries.contains(p := Point(poly.exterior.coords[0])):
                    if biz['Street Address'] not in addresses_seen:
                        addresses_seen[biz['Street Address']] = 1
                        biz['point'] = p
                        biz['poly'] = p
                        businesses_within.append(biz)
            else:
                discarded_empty += 1
    printe(f"discarded_empty: {discarded_empty}")
    return businesses_within


def sort_businesses_by_census_block(biz_within, shape_records):
    biz_by_block = dd(list)
    block_min, block_max = sys.float_info.max, sys.float_info.min
    rtree = rtree_index.Index()
    for ptr, biz in enumerate(biz_within):
        rtree.insert(ptr, biz['poly'].bounds, biz)

    for shaperec in shape_records:
        bizzes = rtree.intersection(shaperec.shape.bbox)
        bizzes_this_block = []
        for biz in bizzes:
            if biz_within[biz]['poly'].intersects(Polygon(shell=shaperec.shape.points)):
                bizzes_this_block.append(biz_within[biz])
                # biz_by_block[shaperec].append(biz_within[biz])
        block_count = len(bizzes_this_block)
        block_min = block_count if block_count < block_min else block_min
        block_max = block_count if block_count > block_max else block_max
        biz_by_block[shaperec] = bizzes_this_block
    return biz_by_block, {"block_min": block_min, "block_max": block_max}


def get_shapes_within_boundaries(boundaries, census_shapefile_pathname, found_shapes_pathname, reset=False):
    if reset or not os.path.exists(found_shapes_pathname):
        writer = shapefile.Writer(found_shapes_pathname)
        reader = shapefile.Reader(census_shapefile_pathname)
        data_dictionary = dict()
        for field_no, field in enumerate(reader.fields):
            writer.field(*field)
            data_dictionary[field[0]] = field_no

        for shp in reader:
            if boundaries.intersects(Polygon(shell=shp.shape.points)):
                setattr(shp.shape, "geoid", shp.record[data_dictionary["BLOCKCE20"]])
                writer.record(*shp.record)
                writer.shape(shp.shape)
        writer.close()

    shapes_within = shapefile.Reader(found_shapes_pathname).shapeRecords()
    return shapes_within


def gen_business_census_3d_map(bizzes_by_block, label, block_min, block_max, styleset, max_height, verbose=False):
    doc = simplekml.Kml(name=label)
    scaling_pct_denom = block_max - block_min  # absolute range of population values, minus smallest value, for scaling

    shape_num = 0
    total_biz = 0
    for shape, bizzes in bizzes_by_block.items():
        biz_pop = len(bizzes)
        total_biz += biz_pop
        shape_num += 1
        scale_coef = (float(biz_pop) - block_min) / scaling_pct_denom if biz_pop > 0 else 0.0
        label = f"Business pop: {biz_pop}"
        object_maker_fn(doc, label, shape.shape, styleset, scale_coef, max_height=max_height)
        if verbose and shape_num / 10 == int(shape_num / 10):
            printe(f"At shape_num: {shape_num}, polys found in boundaries: {biz_pop}")

    printe(f"Total biz pop within boundaries {total_biz}")
    doc.description = f"Population: {total_biz}"
    return doc


def gen_3d_map_from_business_pop_and_blocks(
        boundary_file_or_points,
        business_census_csv_file,
        census_shapefile_pathname,
        pathname_prefix, project_title, styleset,
        max_height=250, reset=False, kml_suffix=".kml"):
    global object_maker_fn
    object_maker_fn = make_kml_poly_3d

    if not os.path.exists(pathname_prefix):
        os.mkdir(pathname_prefix)

    printe(project_title)
    if isinstance(boundary_file_or_points, str):
        boundaries = load_boundary_file(boundary_file_or_points)
    else:
        boundaries = points_to_poly(boundary_file_or_points)

    biz_within_pathname = f"{pathname_prefix}biz_within.pkl"
    if reset or not (biz_within := get_data_snapshot(biz_within_pathname)):
        biz_within = get_included_businesses(boundaries, business_census_csv_file)
        put_data_snapshot(biz_within_pathname, biz_within)

    shapes_within_pathname = f"{pathname_prefix}shapes_within.shp"
    shapes_within = get_shapes_within_boundaries(boundaries, census_shapefile_pathname, shapes_within_pathname, reset)

    bizzes_by_block, min_max = sort_businesses_by_census_block(biz_within, shapes_within)
    # import pudb; pu.db
    kml = gen_business_census_3d_map(bizzes_by_block, **min_max, label=project_title, max_height=max_height, styleset=styleset, verbose=True)
    kml.save(f"{pathname_prefix}map{kml_suffix}")


def gen_biz_maps():
    global object_maker_fn
    object_maker_fn = make_kml_poly_3d
    kml_suffix = "-3D.kml"

    west_styleset = {'width_norm': 4, 'width_hilite': 16, 'color_min': '4064F0A9', 'color_max': '8064F0A9', 'color_fields': [0, 1, 2, 3], 'main_color_field': 2}
    east_styleset = {'width_norm': 4, 'width_hilite': 16, 'color_min': '40F0A064', 'color_max': '80F0A064', 'color_fields': [0, 1, 2, 3], 'main_color_field': 1}
    sfcc_styleset = {'width_norm': 4, 'width_hilite': 16, 'color_min': '4078DC78', 'color_max': '8078DC78', 'color_fields': [0, 1, 2, 3], 'main_color_field': 1}
    census_areas = [
        # ("census_battery_east.json.poly", "biz_battery_east", "Battery East", east_styleset),
        # ("census_battery_west.json.poly", "biz_battery_west", "Battery West to Kearny", west_styleset),
        # ("census_battery_west-stockton.json.poly", "biz_battery_west-stockton", "Battery West to Stockton", west_styleset),
        # ("census_battery_west-powell.json.poly", "biz_battery_west-powell", "Battery West to Powell", west_styleset),
        # ("census_battery_west-van_ness.json.poly", "biz_battery_west-van_ness", "Battery West to Van Ness", west_styleset),
        ("sf_commercial_core-east.json.poly", "biz_sfcc-east", "SF Commercial Core East", sfcc_styleset),
        # ("sf_commercial_core-west.json.poly", "biz_sfcc-west", "SF Commercial Core West", sfcc_styleset),
        # ("sf_commercial_core.json.poly", "biz_sfcc-all", "SF Commercial Core", sfcc_styleset),
    ]

    for area in census_areas:
        printe(f"\nWorking on {area[2]}")
        gen_3d_map_from_business_pop_and_blocks(
            f"defs/{area[0]}",
            "/Users/kev/projs/gta_battery_parking/data/Registered_Business_Locations_-_San_Francisco.tsv.gz",
            CENSUS_2020_SHAPEFILE,
            f"projects/{area[1]}/",
            project_title=f"{area[2]}: SF Business Census",
            styleset=area[3],
            max_height=250,
            kml_suffix=kml_suffix,
            reset=False,
        )


def gen_maps():
    global object_maker_fn
    object_maker_fn = make_kml_poly_3d
    kml_suffix = "-3D.kml"

    # west_styleset = {'width_norm': 4, 'width_hilite': 16, 'color_min': '50171f1f', 'color_max': '5064F0A9', 'color_fields': [1, 2, 3], 'main_color_field': 2}
    # east_styleset = {'width_norm': 4, 'width_hilite': 16, 'color_min': '501F1f14', 'color_max': '50F0A064', 'color_fields': [1, 2, 3], 'main_color_field': 1}
    west_styleset = {'width_norm': 4, 'width_hilite': 16, 'color_min': '4064F0A9', 'color_max': '8064F0A9', 'color_fields': [0, 1, 2, 3], 'main_color_field': 2}
    east_styleset = {'width_norm': 4, 'width_hilite': 16, 'color_min': '40F0A064', 'color_max': '80F0A064', 'color_fields': [0, 1, 2, 3], 'main_color_field': 1}

    gen_map_from_census_pop_and_blocks(
        battery_east,
        "projects/battery_east/", "Battery to Embarcadero, Census 2020",
        sumlev=750, styleset=east_styleset, kml_suffix=kml_suffix, reset=False)

    gen_map_from_census_pop_and_blocks(
        battery_west,
        "projects/battery_west/", "Battery to Kearny, Census 2020",
        sumlev=750, styleset=west_styleset, kml_suffix=kml_suffix, reset=False)

    gen_map_from_census_pop_and_blocks(
        battery_west_stockton,
        "projects/battery_west-stockton/", "Battery to Stockton, Census 2020",
        sumlev=750, styleset=west_styleset, kml_suffix=kml_suffix, reset=False)

    gen_map_from_census_pop_and_blocks(
        battery_west_powell,
        "projects/battery_west-powell/", "Battery to Powell, Census 2020",
        sumlev=750, styleset=west_styleset, kml_suffix=kml_suffix, reset=False)

    gen_map_from_census_pop_and_blocks(
        battery_west_van_ness,
        "projects/battery_west-van_ness/", "Battery to Van Ness, Census 2020",
        sumlev=750, styleset=west_styleset, kml_suffix=kml_suffix, reset=False)

    sfcore = load_boundary_file("defs/sf_commercial_core.json.poly")
    gen_map_from_census_pop_and_blocks(
        sfcore.boundary.coords,
        "projects/sf_commercial_core/", "SF Commercial Core, Census 2020",
        sumlev=750, styleset=west_styleset, kml_suffix=kml_suffix, reset=False)

    sfcore_west = load_boundary_file("defs/sf_commercial_core-west.json.poly")
    gen_map_from_census_pop_and_blocks(
        sfcore_west.boundary.coords,
        "projects/sf_commercial_core-west/", "SF Commercial Core West of Battery, Census 2020",
        sumlev=750, styleset=west_styleset, kml_suffix=kml_suffix, reset=False)

    sfcore_east = sfcore - sfcore_west
    gen_map_from_census_pop_and_blocks(
        sfcore_east.boundary.coords,
        "projects/sf_commercial_core-east/", "SF Commercial Core East of Battery, Census 2020",
        sumlev=750, styleset=east_styleset, kml_suffix=kml_suffix, reset=False)


def get_sqkm(boundary):
    return get_area2(boundary) / 1e6


def get_sqmi(boundary):
    return get_sqkm(boundary) * sqkm2sqmi


def print_sqmi(title, bdy_points):
    if isinstance(bdy_points, str):
        bdy_points = load_boundary_file(bdy_points)
    sqmi = get_sqmi(bdy_points)
    printe(f"{title}: {round(sqmi, 2)} sqmi, {round(sqmi / 0.15, 1)} times Battery to Embarcadero")
    return bdy_points


def land_area_analysis():
    print_sqmi("Battery to Embarcadero", "defs/census_battery_east.json.poly")
    print_sqmi("Battery to Kearny", "defs/census_battery_west.json.poly")
    print_sqmi("Battery to Stockton", "defs/census_battery_west-stockton.json.poly")
    print_sqmi("Battery to Powell", "defs/census_battery_west-powell.json.poly")
    print_sqmi("Battery to Van Ness", "defs/census_battery_west-van_ness.json.poly")
    sfcore_bdy = print_sqmi("SF Commercial Core", "defs/sf_commercial_core.json.poly")
    sfcore_west_bdy = print_sqmi("SF Commercial Core, West of Battery", "defs/sf_commercial_core-west.json.poly")
    sfcore_east_bdy = sfcore_bdy - sfcore_west_bdy
    print_sqmi("SF Commercial Core, East of Battery", sfcore_east_bdy)


def test_3d():
    west_styleset = {'width_norm': 4, 'width_hilite': 16, 'color_min': '50171f1f', 'color_max': '5064F0A9', 'color_fields': [1, 2, 3], 'main_color_field': 2}

    points = [
        (-122.3901093, 37.7907861),
        (-122.4094105, 37.7820018),
        (-122.3976088, 37.7832653),
        (-122.3901093, 37.7907861)]
    doc = simplekml.Kml(name="test_3d")
    make_kml_poly_3d(
        doc,
        label="test_3ddd", shape=points, styleset=west_styleset, scaling_coef=0.50)
    doc.save("test3d222.kml")


def intersect_two_boundaries(f1, f2, outfile):
    b1, b2 = load_boundary_file(f1), load_boundary_file(f2)
    b3 = b1.intersection(b2)
    with open(outfile, "w") as fh3:
        fh3.write("\n".join(f"{p[0]}, {p[1]}" for p in b3.boundary.coords))


def generate_adjacent_area_maps_2d(shapesets: List[Shapeset], reset=False):
    doc = K.Kml()
    prev_boundary = None
    temp_boundary = None
    for ssidx, shapeset in enumerate(shapesets):
        printe(f"Processing {shapeset.boundary} -> {shapeset.cache_pathname}")
        boundary = load_boundary_file(shapeset.boundary)
        if ssidx > 1:
            temp_boundary = deepcopy(boundary)
            if prev_boundary:
                boundary = boundary - prev_boundary
        shapes_found = get_shapes_within_boundaries(
            boundary, CENSUS_2020_SHAPEFILE, found_shapes_pathname=shapeset.cache_pathname, reset=reset)
        sys.stdout.write(f"\tFound {len(shapes_found)}, generating kml\n")
        for shape in shapes_found:
            make_kml_poly(doc, "", shape.shape, shapeset.styleset, 1.0)
        if ssidx > 1:
            prev_boundary = temp_boundary
    return doc


def apply_census_maps_2d(
        shapesets: List[Shapeset],
        doc: K.Kml = None,
        altitude: float = None,
        inclusion_fn: Callable = None,
        inclusion_styleset: Styleset = None,
        exclusion_styleset: Styleset = None,
        reset=False):
    doc = K.Kml() if doc is None else doc
    for ssidx, shapeset in enumerate(shapesets):
        printe(f"Processing {shapeset.boundary} -> {shapeset.cache_pathname}")
        boundary = load_boundary_file(shapeset.boundary)
        shapes_found = get_shapes_within_boundaries(
            boundary, CENSUS_2020_SHAPEFILE, found_shapes_pathname=shapeset.cache_pathname, reset=reset)
        printe(f"\tFound {len(shapes_found)}, generating kml")
        for shape in shapes_found:
            if inclusion_fn:
                if inclusion_fn(shape):
                    make_kml_poly(doc, "", shape=shape.shape, styleset=inclusion_styleset, scaling_coef=1.0)
                else:
                    make_kml_poly(doc, "", shape=shape.shape, styleset=exclusion_styleset, scaling_coef=1.0)
            else:
                make_kml_poly(doc, "", shape=shape.shape, styleset=shapeset.styleset, scaling_coef=1.0)

    return doc


def apply_boundary_maps(boundaryset: List[Boundary], doc: K.Kml = None):
    doc = K.Kml() if doc is None else doc
    for boundary in boundaryset:
        add_polyline(doc, boundary)
    return doc


def generate_hybrid_census_with_area_map_2d(
        boundaries: List[Boundary],
        census_maps: List[Shapeset],
        census_map_altitude: float = None,
        inclusion_fn: Callable = None,
        inclusion_styleset: Styleset = None,
        exclusion_styleset: Styleset = None):
    doc = apply_boundary_maps(boundaryset=boundaries)
    apply_census_maps_2d(census_maps,
                         doc,
                         altitude=census_map_altitude,
                         inclusion_fn=inclusion_fn,
                         inclusion_styleset=inclusion_styleset,
                         exclusion_styleset=exclusion_styleset,
                         reset=False)

    return doc


class PathFollower:
    def __init__(self, path: Boundary, repeat_n: int):
        self._path = path
        self._repeat_n = repeat_n
        self._position = None
        self._next_coords = None
        self.reset()

    def reset(self):
        self._position = 0
        self._next_coords = list(self._path.b.exterior.coords)[0:2]

    def offset(self, offset_x, offset_y):
        slope_points = list(self._path.b.exterior.coords)[0:2]
        lon_delta_x = slope_points[0][0] - slope_points[1][0] + offset_x
        lat_delta_y = slope_points[0][1] - slope_points[1][1] + offset_y
        return lon_delta_x, lat_delta_y

    def next(self) -> List[tuple]:
        pass


def repeat_object_along_path(boundary: Boundary,
                             path: Boundary,
                             times: int,
                             doc: K.Kml,
                             offset_x: float = 0.0,
                             offset_y: float = 0.0):
    slope_points = list(path.b.exterior.coords)[0:2]
    lon_delta_x = slope_points[0][0] - slope_points[1][0] + offset_x
    lat_delta_y = slope_points[0][1] - slope_points[1][1] + offset_y

    # printe(f"{slope_points[0]}, {slope_points[1]}, {lon_delta_x}, {lat_delta_y}")

    poly = deepcopy(boundary.b)
    while times >= 0:
        p = doc.newpolygon()
        p.outerboundaryis = poly.exterior.coords
        p.stylemap = boundary.c
        poly = shapely.affinity.translate(poly, xoff=lon_delta_x, yoff=lat_delta_y)
        times -= 1

    return list(path.b.exterior.coords)[0]


def plot_shapes_from_oids(oids: List[int], project_title, styleset):
    kml = convert_oids_to_shape_kml(
        oids,
        "data/tl_2020_06_tabblock/tl_2020_06_tabblock20.shp",
        boundaries,
        layer_name=project_title,
        styleset=styleset,
        max_height=100)
    return kml


def sidney_walkton_pop_emphasis():
    ids = DictObj(gen_map_from_census_pop_and_blocks(
        boundaries.battery_embarcadero_market.b.exterior.coords,
        "projects/sidney_walton_adjacent", "Sidney Walton", SS_DIST3_SIDNEY,
        produce_map=False))
    doc = plot_shapes_from_oids(
        oids=ids.oids,
        boundaries=boundaries.battery_embarcadero_market.b,
        project_title="oids from bat-emb-market",
        styleset=SS_DIST3_SIDNEY)

    def sidney_pop_incl(shp):
        if ids["oids"].get(shp.record.GEOID20):
            printe(f'sidney_pop_incl FOUND {ids["geoids"][shp.record.GEOID20][part1.P0010001]}')
            return ids["oids"][shp.record.GEOID20][part1.P0010001] > 40
        else:
            printe(f'sidney_pop_incl GNF: {shp.record.GEOID20}')

    # import pudb; pu.db
    doc = generate_hybrid_census_with_area_map_2d(
        boundaries=[boundaries.district_3, boundaries.battery_embarcadero_market],
        census_maps=[Shapeset("defs/battery_sidney_walton_census_inclusion_area.json.poly", SS_DIST3_SIDNEY, "projects/sidney_walton_adjacent.shp")],
        # census_maps=[],
        repeat_boundary=boundaries.battery_fat_dash,
        repeat_path=boundaries.battery_fat_dash_path,
        repeat_n=7,
        inclusion_fn=sidney_pop_incl,
        # inclusion_fn=lambda shp: ids["oids"][shp.record.GEOID20][part1.P0010001] > 40 if ids["oids"].get(shp.record.GEOID20) else False,
        inclusion_styleset=SS_DIST3_SIDNEY,
        exclusion_styleset=SS_DIST3_SIDNEY_LOLIT)
    return doc


if __name__ == '__main__':
    # test_3d()
    # gen_maps()
    # main()
    # gen_biz_maps()

    # doc = sidney_walkton_pop_emphasis()
    # doc.save("/dev/stdout")

    doc = generate_hybrid_census_with_area_map_2d(
        boundaries=[boundaries.district_3, boundaries.battery_embarcadero_market],
        census_maps=[Shapeset("defs/battery_sidney_walton_census_inclusion_area.json.poly", SS_DIST3_SIDNEY, "projects/sidney_walton_adjacent.shp")],
        # census_maps=[],
        census_map_altitude=75.0,
        repeat_boundary=boundaries.battery_fat_dash,
        repeat_path=boundaries.battery_fat_dash_path,
        repeat_n=7)
    doc.save("hybrid.kml")

    # doc = generate_area_maps_2d([
    #         Shapeset("defs/census_battery_east.json.poly", SS_RED_OPQFF, "projects/east_west/battery_east.shp"),
    #         Shapeset("defs/census_battery_west.json.poly", SS_GREEN_SIDES7F_OPQFF, "projects/east_west/battery_west_zone1.shp"),
    #         Shapeset("defs/census_battery_west-stockton.json.poly", SS_GREEN_SIDES9F_OPQFF, "projects/east_west/battery_west_zone2.shp"),
    #         Shapeset("defs/census_battery_west-powell.json.poly", SS_GREEN_SIDESBF_OPQFF, "projects/east_west/battery_west_zone3.shp"),
    #         Shapeset("defs/census_battery_west-van_ness.json.poly", SS_GREEN_SIDESDF_OPQFF, "projects/east_west/battery_west_zone4.shp"),
    #     ],
    #     "east_west.kml",
    #     reset=True
    # )
    # doc.save("map.kml")

    # intersect_two_boundaries(
    #     "defs/sf_commercial_core.json.poly",
    #     "defs/sf_commercial_core-EAST_INTERSECTION.json.poly",
    #     outfile="defs/sf_commercial_core-east2.json.poly")

    # get_geo_bounded_population_and_housing()

    # read_groups("data/tl_2020_06_tabblock/tl_2020_06_tabblock20.dbf")

    # convert_found_objs_to_kml([0, 1105])
    # read_groups('data/tl_2021_06_tabblock20/tl_2021_06_tabblock20.dbf')
    # read_polys('data/tl_2021_06_tabblock20/tl_2021_06_tabblock20.shp')
    # read_polys('data/tl_2021_06_tabblock20/tl_2021_06_tabblock20.shx')
    # # read_groups('data/cb_2018_06_bg_500k/cb_2018_06_bg_500k.dbf')
    # read_polys('data/cb_2018_06_bg_500k/cb_2018_06_bg_500k.shp')

    # read_recs('data/tl_2021_06_tabblock20/tl_2021_06_tabblock20.dbf', [21, 176])
    # get_shape_dbf_coords(f, rowno)

    """
    LINKING THE PLST FILES
    0669169 is a logical record number. It ties together all records from the four files.
    $ grep 0669169 *.pl
    ca000012020.pl:PLST|CA|000|01|0669169|9658|8025|4947|83|275|321|15|2384|1633|1507|32|152|102|20|1093|9|3|1|4|2|1|59|6|21|2|116|12|0|0|3|9|0|66|10|14|0|0|0|0|0|0|0|1|1|0|0|9|0|0|8|0|0|0|0|1|0|0|0|0|0|0|0|1|1|0|0|0|0|0|0|0|9658|4645|5013|4653|4146|70|32|284|9|112|360|333|30|102|79|14|85|8|3|1|0|1|1|0|5|3|1|26|10|0|0|0|4|0|0|9|2|0|0|0|0|0|0|0|1|0|0|0|1|0|0|1|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0
    ca000022020.pl:PLST|CA|000|02|0669169|7727|6553|4276|72|206|273|12|1714|1174|1096|25|119|56|15|799|8|3|1|4|2|1|48|6|9|0|73|5|0|0|2|4|0|45|8|8|0|0|0|0|0|0|0|0|1|0|0|5|0|0|5|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|7727|3324|4403|4123|3682|63|25|251|9|93|280|268|23|88|48|12|76|8|3|1|0|1|1|0|5|2|0|12|4|0|0|0|0|0|0|8|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|3508|3240|268
    ca000032020.pl:PLST|CA|000|03|0669169|51|0|0|0|0|0|51|0|0|51
    cageo2020.pl:PLST|CA|970|00|00|000|00|0669169|9700000US0691136|0691136|4|9|06|01779778|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||91136||262323819|694382|Aromas-San Juan Unified School District|Aromas-San Juan Unified School District|E||9658|3508|+36.8536061|-121.5554558|00||

    061150411021048 is a geoid.  It occurs only in cageo2020.pl, and in the TIGER dbf as ('GEOID20', '060450107007032')
    The geoid is composed of-
    06      State ID
    115     County ID
    041102  Tract ID
    1048    Block ID

    The STgeoYYYY.pl file serves to link a lat/lon to a geoid, where the LOGRECNO is obtained.
    $ grep 061150411021048 *.pl
    cageo2020.pl:PLST|CA|750|00|00|000|00|0668188|7500000US061150411021048|061150411021048|4|9|06|01779778|115|H1|00277322|93830|Z5|01935389|||||||99999|99|99999999|99999|99|99999999|041102|1|1048|9999|9|99999|99|99999999|999|99999|99|99999999|999999|9|99999|99|99999999|49700|1|472|99999|99999|9|999|99999|9|9||||03|||||004|||||003||||||||99999|99999|24090||28771|0|1048|Block 1048|S||0|0|+39.3733791|-121.2659154|BK||99999
    """

    """
    Strategy for counting population within geographical boundaries
    
    Wanted sums:
        H1. OCCUPANCY STATUS [3]
            Universe: Housing units
                Total: H0010001
                    Occupied: H0010002
                    Vacant: H0010003

        P1. P0010001
        
    Load part1: data/ca2020/ca000012020.pl, index by part1.LOGRECNO, extract part1.P0010001
    Load part2: index by part2.LOGRECNO, extract part2.P0030001 
    Load cageo2020.pl and iterate:
        if INTPTLAT, INTPTLON within boundaries:
            write to file
            get:
                population, housing = part1.POP100, part1.HU100
            compare population with part1.P0010001
    """

    """
    060014001001000
    061150411021048
    find_block_shapes(
        'data/tl_2021_06_tabblock20/tl_2021_06_tabblock20.shp',
        [[-122.4255466, 37.8063255], [-122.4191523, 37.7748533],
         [-122.3942184, 37.7948302], [-122.4033594, 37.8050371],
         [-122.4061489, 37.8066985], [-122.4091959, 37.8081904],
         [-122.412715, 37.8088346], [-122.4219847, 37.8076479],
         [-122.4234867, 37.8067663], [-122.425375, 37.8063594]])
    """
