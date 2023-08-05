#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import math

import shapely.geometry
import shapely.geos
import shapely.wkb


LONLAT_CENTER = (5.74626, 45.17475)
LONLAT_EXTEND = ((5.60268, 45.0821), (5.88934, 45.2674))
EXTEND_BBOX_XY = None
SRID = 4326


def lonlat_to_xy(lonlat, lonlatcenter=None):
    if lonlatcenter is None:
        lonlatcenter = LONLAT_CENTER

    return _to_xy(*lonlat, lonlatcenter)


def coords_to_xy(coords, lonlatcenter=None):
    if lonlatcenter is None:
        lonlatcenter = LONLAT_CENTER

    xys = []
    for lonlat in coords:
        xys.append(_to_xy(*lonlat, lonlatcenter))
    return xys


def _to_xy(lon, lat, lonlatcenter):
    lon = lon * math.pi / 180
    lat = lat * math.pi / 180
    loncenter = lonlatcenter[0] * math.pi / 180
    latcenter = lonlatcenter[1] * math.pi / 180

    r = 6371000  # earth radius in meters
    x = r * math.cos(lat) * math.sin(lon - loncenter)
    y = r * (math.cos(latcenter) * math.sin(lat) - math.sin(latcenter) * math.cos(lat) * math.cos(lon - loncenter))
    return x, y


def round_lonlat(lonlat):
    return round(lonlat[0] * 1000), round(lonlat[1] * 1000)


def is_inside_extend(geomxy):
    global EXTEND_BBOX_XY
    if EXTEND_BBOX_XY is None:
        coords = []
        for coord in coords_to_xy(LONLAT_EXTEND):
            coords.extend(coord)
        EXTEND_BBOX_XY = shapely.geometry.box(*coords)

    return EXTEND_BBOX_XY.intersects(geomxy)


def close_elems_it(lonlatrounded, lonlatmatrix, radius=1):
    if radius >= 1:
        lat, lon = lonlatrounded
        for i in _get_range(lat, radius):
            if i in lonlatmatrix:
                for j in _get_range(lon, radius):
                    if j in lonlatmatrix[i]:
                        for elem in lonlatmatrix[i][j]:
                            yield elem


def _get_range(i, radius):
    return sorted(range(i-radius, i+radius+1), key=lambda x: abs(x-i))


def encode_geometry(geometry):
    if not hasattr(geometry, '__geo_interface__'):
        raise TypeError('{g} does not conform to '
                        'the geo interface'.format(g=geometry))
    shape = shapely.geometry.asShape(geometry)
    shapely.geos.lgeos.GEOSSetSRID(shape._geom, SRID)
    return shapely.wkb.dumps(shape, include_srid=True)


def decode_geometry(wkb):
    return shapely.wkb.loads(wkb)
