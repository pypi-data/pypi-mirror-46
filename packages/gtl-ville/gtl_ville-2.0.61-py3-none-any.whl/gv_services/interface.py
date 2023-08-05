#!/usr/bin/env python3

import asyncio

from gv_rpc.utils import TRAFFIC_DATA_TYPES
from gv_services.proto.common_pb2 import Ack, TrafficData
from gv_services.proto.geographer_pb2 import Locations, Mapping
from gv_services.proto.interface_grpc import InterfaceBase
from gv_services.archivist import Archivist
from gv_services.broadcaster import Broadcaster
from gv_services.geographer import Geographer
from gv_utils import enums


DATA_POINTS = enums.DataTypeId.datapoints
MAPPING_ROADS_DATA_POINTS = enums.DataTypeId.mappingroadsdatapoints


class Interface(InterfaceBase):

    def __init__(self, logger, basedatapath, basecartopath, *dbcredentials):
        super().__init__()
        self.logger = logger
        self.archivist = Archivist(logger, basedatapath)
        self.broadcaster = Broadcaster(logger)
        self.geographer = Geographer(logger, basecartopath, *dbcredentials)

    async def async_init(self):
        await self.geographer.async_init()

    async def publish(self, stream):
        message = await stream.recv_message()
        coros = [self.broadcaster.publish(message), ]
        datatype = message.datatype.split('-')[0]
        if datatype in TRAFFIC_DATA_TYPES:
            pbdata = TrafficData()
            message.data.Unpack(pbdata)
            coros.append(self.archivist.store_data(pbdata, datatype, message.timestamp))
        elif datatype == DATA_POINTS:
            pbdata = Locations()
            message.data.Unpack(pbdata)
            coros.append(self.geographer.add_data_points(pbdata))
        elif datatype == MAPPING_ROADS_DATA_POINTS:
            pbdata = Mapping()
            message.data.Unpack(pbdata)
            coros.append(self.geographer.add_mapping_roads_data_points(pbdata))
        status = await asyncio.gather(*coros)
        await stream.send_message(Ack(success=bool(int(sum(status)/len(status)))))

    async def subscribe(self, stream):
        await self.broadcaster.subscribe(stream)

    async def get_data(self, stream):
        await self.archivist.get_data(stream)

    async def add_mapping_roads_data_points(self, stream):
        message = await stream.recv_message()
        pbdata = Mapping()
        message.data.Unpack(pbdata)
        await self.geographer.add_mapping_roads_data_points(pbdata)

    async def add_data_points(self, stream):
        message = await stream.recv_message()
        pbdata = Locations()
        message.data.Unpack(pbdata)
        await self.geographer.add_data_points(pbdata)

    async def import_shapefile_to_db(self, stream):
        await self.geographer.import_shapefile_to_db(stream)

    async def get_data_points(self, stream):
        await self.geographer.get_data_points(stream)

    async def get_roads(self, stream):
        await self.geographer.get_roads(stream)

    async def get_zones(self, stream):
        await self.geographer.get_zones(stream)

    async def get_mapping_roads_data_points(self, stream):
        await self.geographer.get_mapping_roads_data_points(stream)

    async def get_mapping_zones_roads(self, stream):
        await self.geographer.get_mapping_zones_roads(stream)

    async def update_roads_freeflow_speed(self, stream):
        await self.geographer.update_roads_freeflow_speed(stream)

    async def update_zones_freeflow_speed(self, stream):
        await self.geographer.update_zones_freeflow_speed(stream)
