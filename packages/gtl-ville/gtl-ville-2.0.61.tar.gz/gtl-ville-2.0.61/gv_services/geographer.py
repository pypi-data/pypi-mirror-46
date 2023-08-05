#!/usr/bin/env python3

import os
import traceback

from gv_services.proto.common_pb2 import Ack
from gv_services.storage.dbstorage.dbstorage import DbStorage
from gv_services.settings import SHAPEFILE_NAME
from gv_utils import datetime, enums, protobuf

DATAPOINTEID = enums.AttId.datapointeid
DATATYPEEID = enums.AttId.datatypeeid
EID = enums.AttId.eid
GEOM = enums.AttId.geom
ROADEID = enums.AttId.roadeid
VALIDFROM = enums.AttId.validfrom


class Geographer:

    def __init__(self, logger, basecartopath, *dbcredentials):
        super().__init__()
        self.logger = logger
        self.basecartopath = basecartopath
        self.dbstorage = DbStorage(*dbcredentials)

    async def async_init(self):
        await self.dbstorage.async_init()

    async def add_mapping_roads_data_points(self, pbmapping):
        success = False
        try:
            mapping, validat = await protobuf.decode_mapping(pbmapping)
            datapoints, mapping = await Geographer._get_data_point_from_mapping(mapping, validat)
            if datapoints:
                await self.dbstorage.insert_data_point(datapoints)
            if mapping:
                await self.dbstorage.insert_road_data_point(mapping)
            success = True
        except:
            self.logger.error('An error occurred while adding new road - data point mappings.')
            self.logger.error(traceback.format_exc())
        finally:
            return success

    @staticmethod
    async def _get_data_point_from_mapping(mapping, validat):
        datapoints = {}
        roadsdatapoints = []
        validfrom = datetime.from_timestamp(validat, True)
        for roadeid, locations in mapping.items():
            if not isinstance(locations, dict):
                for loceid in locations:
                    roadsdatapoints.append({DATAPOINTEID: loceid, ROADEID: roadeid, VALIDFROM: validfrom})
            else:
                for loceid, location in locations.items():
                    datapoints[loceid] = {EID: loceid, GEOM: location[GEOM], DATATYPEEID: location[DATATYPEEID]}
        return list(datapoints.values()), roadsdatapoints

    async def add_data_points(self, pbdata):
        success = False
        try:
            datapoints = await protobuf.decode_locations(pbdata)
            if datapoints:
                await self.dbstorage.insert_data_point(list(datapoints.values()))
            success = True
        except:
            status = False
            self.logger.error('An error occurred while adding new data points.')
            self.logger.error(traceback.format_exc())
        finally:
            return success

    async def import_shapefile_to_db(self, stream):
        status = True
        try:
            await self.dbstorage.import_shapefile(os.path.join(self.basecartopath, SHAPEFILE_NAME))
        except:
            status = False
        finally:
            await stream.send_message(Ack(success=status))

    async def get_data_points(self, stream):
        message = await stream.recv_message()
        eids, datatype = message.eids.eids, message.datatype
        datapoints = {}
        for v in (await self.dbstorage.get_data_points(eids, datatype)).values():
            datapoints.update(v)
        datapoints = await protobuf.encode_locations(datapoints)
        await stream.send_message(datapoints)

    async def get_roads(self, stream):
        message = await stream.recv_message()
        eids = message.eids.eids
        roads = await protobuf.encode_locations(await self.dbstorage.get_roads(eids))
        await stream.send_message(roads)

    async def get_zones(self, stream):
        message = await stream.recv_message()
        eids = message.eids.eids
        zones = await protobuf.encode_locations(await self.dbstorage.get_zones(eids))
        await stream.send_message(zones)

    async def get_mapping_roads_data_points(self, stream):
        message = await stream.recv_message()
        roadeids, dpeids, validat = message.fromeids.eids, message.toeids.eids, message.validat.ToSeconds()
        roadsdatapoints = await protobuf.encode_mapping(await self.dbstorage.get_mapping_roads_data_points(
            roadeids, dpeids, datetime.from_timestamp(validat, True)), validat)
        await stream.send_message(roadsdatapoints)

    async def get_mapping_zones_roads(self, stream):
        message = await stream.recv_message()
        zoneeids, roadeids, validat = message.fromeids.eids, message.toeids.eids, message.validat.ToSeconds()
        zonesroads = await protobuf.encode_mapping(await self.dbstorage.get_mapping_zones_roads(
            zoneeids, roadeids, datetime.from_timestamp(validat, True)), validat)
        await stream.send_message(zonesroads)

    async def update_roads_freeflow_speed(self, stream):
        status = True
        try:
            await self.dbstorage.updata_roads_ffspeed(await protobuf.decode_ffspeeds(await stream.recv_message()))
        except:
            status = False
        finally:
            await stream.send_message(Ack(success=status))

    async def update_zones_freeflow_speed(self, stream):
        pass
