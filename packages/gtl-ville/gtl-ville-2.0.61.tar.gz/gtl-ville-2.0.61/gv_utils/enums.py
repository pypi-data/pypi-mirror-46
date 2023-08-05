#!/usr/bin/env python3


class CsvData:
    samples = 'samples'
    timestamp = 'timestamp'

    confidence = 'confidence'
    density = 'density'
    flow = 'flow'
    fluidity = 'fluidity'
    occupancy = 'occupancy'
    speed = 'speed'
    status = 'status'
    traveltime = 'traveltime'


class DataTypeId:
    metropme = 'metropme'
    roads = 'roads'
    tomtomfcd = 'tomtomfcd'
    zones = 'zones'

    datapoints = 'datapoints'
    mappingroadsdatapoints = 'mappingroadsdatapoints'


class AttId:
    att = 'att'
    datapointseids = 'datapointseids'
    datatypeeid = 'datatypeeid'
    eid = 'eid'
    ffspeed = 'ffspeed'
    fow = 'fow'
    frc = 'frc'
    fromno = 'fromno'
    geom = 'geom'
    geomxy = 'geomxy'
    length = 'length'
    maxspeed = 'maxspeed'
    name = 'name'
    nlanes = 'nlanes'
    no = 'no'
    tono = 'tono'
    webatt = 'webatt'

    datapointeid = 'datapointeid'
    roadeid = 'roadeid'
    validfrom = 'validfrom'
    validto = 'validto'
    zoneeid = 'zoneeid'


class NetworkObjId:
    convexhull = 'convexhull'
    coordsnodesmap = 'coordsnodesmap'
    datapointsroadsmap = 'datapointsroadsmap'
    frcroadsmap = 'frcroadsmap'
    lonlatnodesmatrix = 'lonlatnodesmatrix'
    newdpmappings = 'newdpmappings'
    newzonemappings = 'newzonemappings'
    omiteddatapoints = 'omiteddatapoints'
    roadsdatamap = 'roadsdatamap'
    roadsffspeedmap = 'roadsffspeedmap'
    roadszonesmap = 'roadszonesmap'
    vordiag = 'vordiag'
    zonesdatamap = 'zonesdatamap'
