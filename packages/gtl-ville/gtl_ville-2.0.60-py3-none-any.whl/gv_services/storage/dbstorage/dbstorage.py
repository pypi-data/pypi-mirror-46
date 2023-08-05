#!/usr/bin/env python3


import asyncio

import asyncpg
# IMPORTANT: ON OSX SHAPELY NEEDS TO BE IMPORTED BEFORE FIONA TO AVOID A CRASH IN GEOS LIBRARY
from shapely import geometry
import fiona

import gv_services.storage.dbstorage.dbrequest as dbrequest
import gv_services.storage.dbstorage.dbmapping as dbmapping
from gv_utils import enums


ATT = enums.AttId.att
DATAPOINTEID = enums.AttId.datapointeid
DATATYPEEID = enums.AttId.datatypeeid
EID = enums.AttId.eid
FFSPEED = enums.AttId.ffspeed
FOW = enums.AttId.fow
FRC = enums.AttId.frc
FROMNO = enums.AttId.fromno
GEOM = enums.AttId.geom
LENGTH = enums.AttId.length
MAXSPEED = enums.AttId.maxspeed
NAME = enums.AttId.name
NLANES = enums.AttId.nlanes
NO = enums.AttId.no
ROADEID = enums.AttId.roadeid
TONO = enums.AttId.tono
WEBATT = enums.AttId.webatt
ZONEEID = enums.AttId.zoneeid


class DbStorage:

    def __init__(self, *credentials):
        self.host, self.port, self.database, self.user, self.password = credentials
        self.dbpool = None
        self.datapoints = {}
        self.roads = {}
        self.zones = {}
        self.roadsdatapoints = {}
        self.zonesroads = {}

    def __del__(self):
        try:
            self.dbpool.terminate()
        except:
            pass

    async def async_init(self):
        self.dbpool = await asyncpg.create_pool(host=self.host, port=self.port, database=self.database,
                                                user=self.user, password=self.password)
        await self._init_cache()

    async def import_shapefile(self, shapefilepath):
        def get_roads():
            roads = []
            with fiona.open(shapefilepath, 'r', encoding='utf8') as features:
                for feature in features:
                    properties = feature['properties']
                    roads.append({
                        ATT: {
                            FOW: int(properties[FOW]),
                            FROMNO: int(properties[FROMNO]),
                            LENGTH: int(properties[LENGTH]),
                            NLANES: int(properties[NLANES]),
                            NO: int(properties[NO]),
                            TONO: int(properties[TONO])
                        },
                        EID: str(properties[EID]),
                        GEOM: geometry.shape(feature['geometry']),
                        WEBATT: {
                            FRC: int(properties[FRC]),
                            MAXSPEED: int(properties[MAXSPEED]),
                            NAME: str(properties[NAME])
                        }
                    })
            return roads
        await self.insert_road(await asyncio.get_event_loop().run_in_executor(None, get_roads))

    async def _init_cache(self):
        self.datapoints = {}
        self.roads = {}
        self.zones = {}
        self.roadsdatapoints = {}
        self.zonesroads = {}

        roadtask = asyncio.create_task(self._init_roads())

        async def _init_road_dp_map():
            await asyncio.gather(roadtask, self._init_data_points())
            await self._init_roads_data_points()

        async def _init_zone_road_map():
            await asyncio.gather(self._init_zones(), roadtask)
            await self._init_zones_roads()

        await asyncio.gather(_init_road_dp_map(), _init_zone_road_map())

    async def _init_data_points(self):
        async for datapoint in await dbrequest.get_data_points(self.dbpool):
            self._add_data_point(datapoint)

    async def _init_roads(self):
        async for road in await dbrequest.get_roads(self.dbpool):
            self._add_road(road)

    async def _init_zones(self):
        async for zone in await dbrequest.get_zones(self.dbpool):
            self._add_zone(zone)

    async def _init_roads_data_points(self):
        async for roaddatapoint in await dbrequest.get_roads_data_points(self.dbpool):
            self._add_road_data_point(roaddatapoint)

    async def _init_zones_roads(self):
        async for zoneroad in await dbrequest.get_zones_roads(self.dbpool):
            self._add_zone_road(zoneroad)

    def _add_data_point(self, datapoint):
        datatypeeid = datapoint[DATATYPEEID]
        if datatypeeid not in self.datapoints:
            self.datapoints[datatypeeid] = {}
        eid = datapoint[EID]
        self.datapoints[datatypeeid][eid] = datapoint

    def _add_road(self, road):
        eid = road[EID]
        self.roads[eid] = road

    def _add_zone(self, zone):
        eid = zone[EID]
        self.zones[eid] = zone

    def _add_road_data_point(self, roaddatapoint):
        roadeid = roaddatapoint[ROADEID]
        if roadeid not in self.roadsdatapoints:
            self.roadsdatapoints[roadeid] = set()
        self.roadsdatapoints[roadeid].add(roaddatapoint[DATAPOINTEID])

    def _add_zone_road(self, zoneroad):
        zoneeid = zoneroad[ZONEEID]
        if zoneeid not in self.zonesroads:
            self.zonesroads[zoneeid] = set()
        self.zonesroads[zoneeid].add(zoneroad[ROADEID])

    async def insert_data_point(self, datapoints):
        if isinstance(datapoints, dict):
            datapoints = [datapoints, ]

        newdatatypes = set()
        newdatapoints = list()
        for i in range(len(datapoints)):
            datapoint = datapoints[i]
            datatypeeid = datapoint[DATATYPEEID]
            eid = datapoint[EID]
            if datatypeeid not in self.datapoints:
                newdatatypes.add(datatypeeid)
            if eid not in self.datapoints.get(datatypeeid, {}):
                newdatapoints.append(datapoint)
            else:
                datapoints[i] = self.datapoints[datatypeeid][eid]

        await dbrequest.insert_data_type(self.dbpool, newdatatypes)
        for datapoint in await dbrequest.insert_data_point(self.dbpool, newdatapoints):
            self._add_data_point(datapoint)
        return datapoints

    async def insert_road(self, roads):
        if isinstance(roads, dict):
            roads = [roads, ]

        newroads = list()
        for i in range(len(roads)):
            road = roads[i]
            eid = road[EID]
            if eid not in self.roads:
                newroads.append(road)
            else:
                roads[i] = self.roads[eid]

        for road in await dbrequest.insert_road(self.dbpool, newroads):
            self._add_road(road)
        return roads

    async def insert_zone(self, zones):
        if isinstance(zones, dict):
            zones = [zones, ]

        newzones = list()
        for i in range(len(zones)):
            zone = zones[i]
            eid = zone[EID]
            if eid not in self.zones:
                newzones.append(zone)
            else:
                zones[i] = self.zones[eid]

        for zone in await dbrequest.insert_zone(self.dbpool, newzones):
            self._add_zone(zone)
        return zones

    async def insert_road_data_point(self, roaddatapoints):
        if isinstance(roaddatapoints, dict):
            roaddatapoints = [roaddatapoints, ]

        newroaddatapoints = list()
        for roaddatapoint in roaddatapoints:
            roadeid = roaddatapoint[ROADEID]
            if roadeid not in self.roadsdatapoints or roaddatapoint[DATAPOINTEID] not in self.roadsdatapoints[roadeid]:
                newroaddatapoints.append(roaddatapoint)

        for roaddatapoint in await dbrequest.insert_road_data_point(self.dbpool, newroaddatapoints):
            self._add_road_data_point(roaddatapoint)
        return roaddatapoints

    async def insert_zone_road(self, zoneroads):
        if isinstance(zoneroads, dict):
            zoneroads = [zoneroads, ]

        newzoneroads = list()
        for zoneroad in zoneroads:
            zoneeid = zoneroad[ZONEEID]
            if zoneeid not in self.zonesroads or zoneroad[ROADEID] not in self.zonesroads[zoneeid]:
                newzoneroads.append(zoneroad)

        for zoneroad in await dbrequest.insert_zone_road(self.dbpool, newzoneroads):
            self._add_zone_road(zoneroad)
        return zoneroads

    async def update_road(self, roads, fields):
        if isinstance(roads, dict):
            roads = [roads, ]
        if isinstance(fields, str):
            fields = [fields, ]

        modifiedroads = dict()
        for road in roads:
            eid = road[EID]
            if eid in self.roads:
                values = list()
                for field in fields:
                    value = road.get(field, self.roads[eid][field])
                    values.append(value)
                modifiedroads[eid] = values

        for roadeid in await dbrequest.update_road(self.dbpool, modifiedroads,
                                                [dbmapping.Road.invmapping[field] for field in fields]):
            values = modifiedroads[roadeid]
            for field in fields:
                self.roads[roadeid][field] = values.pop(0)

    async def updata_roads_ffspeed(self, eidsffspeeds):
        modifiedroads = dict()
        for eid, ffspeed in eidsffspeeds.items():
            if eid in self.roads:
                att = dict(self.roads[eid][ATT])
                att[FFSPEED] = int(ffspeed)
                modifiedroads[eid] = [att]

        for roadeid in await dbrequest.update_road(self.dbpool, modifiedroads,
                                                [dbmapping.Road.invmapping[ATT]]):
            self.roads[roadeid][ATT] = modifiedroads[roadeid][0]

    async def update_zone(self, zones, fields):
        if isinstance(zones, dict):
            zones = [zones, ]
        if isinstance(fields, str):
            fields = [fields, ]

        modifiedzones = dict()
        for zone in zones:
            eid = zone[EID]
            if eid in self.zones:
                values = list()
                for field in fields:
                    value = zone.get(field, self.zones[eid][field])
                    values.append(value)
                modifiedzones[eid] = values

        for zone in await dbrequest.update_zone(self.dbpool, modifiedzones,
                                                [dbmapping.Zone.invmapping[field] for field in fields]):
            for field in fields:
                if field in zone:
                    self.zones[zone[EID]][field] = zone[field]

    async def get_data_points(self, eids=None, datatype=None):
        if datatype and datatype in self.datapoints:
            datapoints = {datatype: self.datapoints[datatype]}
        else:
            datapoints = self.datapoints
        if eids:
            datapointsfiltered = dict()
            for datatype, v in datapoints.items():
                value = {eid: v[eid] for eid in eids if eid in v}
                if value:
                    datapointsfiltered[datatype] = value
            datapoints = datapointsfiltered
        return datapoints

    async def get_roads(self, eids=None):
        if eids:
            roads = dict([(k, v) for k, v in self.roads.items() if k in eids])
        else:
            roads = self.roads
        return roads

    async def get_zones(self, eids=None):
        if eids:
            zones = {eid: self.zones[eid] for eid in eids if eid in self.zones}
        else:
            zones = dict(self.zones.items())
        return zones

    # TODO: impl validat

    async def get_mapping_roads_data_points(self, roadeids=None, dpeids=None, validat=None):
        if roadeids:
            roadsdatapoints = {eid: self.roadsdatapoints[eid] for eid in roadeids if eid in self.roadsdatapoints}
        elif dpeids:
            roadsdatapoints = {}
            for k, v in self.roadsdatapoints.items():
                value = {eid for eid in v if eid in dpeids}
                if value:
                    roadsdatapoints[k] = value
        else:
            roadsdatapoints = self.roadsdatapoints
        return roadsdatapoints

    async def get_mapping_zones_roads(self, zoneids=None, roadeids=None, validat=None):
        if zoneids:
            zonesroads = {eid: self.zonesroads[eid] for eid in zoneids if eid in self.zonesroads}
        elif roadeids:
            zonesroads = {}
            for k, v in self.zonesroads.items():
                value = {eid for eid in v if eid in roadeids}
                if value:
                    zonesroads[k] = value
        else:
            zonesroads = self.zonesroads
        return zonesroads
