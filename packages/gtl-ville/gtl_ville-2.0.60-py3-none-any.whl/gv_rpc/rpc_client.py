#!/usr/bin/env python3

import asyncio
import traceback

from grpclib.client import Channel

from gv_rpc.utils import TRAFFIC_DATA_TYPES
from gv_services.proto.broadcaster_pb2 import PubRequest, SubRequest
from gv_services.proto.common_pb2 import TrafficData
from gv_services.proto.geographer_pb2 import Locations, LocationsRequest, Mapping, MappingRequest
from gv_services.proto.interface_grpc import InterfaceStub
from gv_utils import enums, protobuf
from gv_utils.asyncio import check_event_loop


DATA_TYPE_EID = enums.AttId.datatypeeid

METRO_PME = enums.DataTypeId.metropme
TOMTOM_FCD = enums.DataTypeId.tomtomfcd
ROADS = enums.DataTypeId.roads
ZONES = enums.DataTypeId.zones

DATA_POINTS = enums.DataTypeId.datapoints
MAPPING_ROADS_DATA_POINTS = enums.DataTypeId.mappingroadsdatapoints


class RpcClient:
    samplings = {METRO_PME: 1*60, TOMTOM_FCD: 1*60}

    def __init__(self, logger, futures=None, callbacks=None):
        if futures is None:
            futures = []
        if callbacks is None:
            callbacks = {}

        self.logger = logger
        self.futures = futures
        self.callbacks = callbacks
        self.interface = None
        self._channel = None
        self._mainfut = None

    async def async_init(self):
        pass

    def start(self, rpchost, rpcport):
        check_event_loop()  # will create a new event loop if needed (if we are not in the main thread)
        self.logger.info('RPC client is starting.')
        try:
            asyncio.run(self._run(rpchost, rpcport))
        except KeyboardInterrupt:
            pass
        self.logger.info('RPC client has stopped.')

    async def _run(self, rpchost, rpcport):
        try:
            self._channel = Channel(rpchost, rpcport, loop=asyncio.get_event_loop())
            self.interface = InterfaceStub(self._channel)
            try:
                await self.async_init()
                self._mainfut = asyncio.gather(
                    *self.futures,
                    *[self._subscribe(datatype, callback) for datatype, callback in self.callbacks.items()]
                )
                self._mainfut.add_done_callback(self._close)
                self.logger.info('RPC client has started.')
                await self._mainfut
            finally:
                self._cancel()
        except:
            self._close()

    def _close(self, _=None):
        if self._channel is not None:
            self._channel.close()
            self._channel = None

    def _cancel(self):
        if self._mainfut is not None:
            self._mainfut.cancel()
            self._mainfut = None

    async def _subscribe(self, datatype, callback):
        async with self.interface.subscribe.open() as stream:
            await stream.send_message(SubRequest(datatype=datatype))
            self.logger.info('RPC client has subscribed to {} data.'.format(datatype))
            try:
                async for response in stream:
                    self.logger.debug('Got new {} data.'.format(datatype))
                    try:
                        if datatype in TRAFFIC_DATA_TYPES:
                            pbdata = TrafficData()
                            response.Unpack(pbdata)
                            data = await protobuf.decode_traffic_data(pbdata)
                        elif datatype == DATA_POINTS:
                            pbdata = Locations()
                            response.Unpack(pbdata)
                            data = await protobuf.decode_locations(pbdata)
                        elif datatype == MAPPING_ROADS_DATA_POINTS:
                            pbdata = Mapping()
                            response.Unpack(pbdata)
                            data = await protobuf.decode_mapping(pbdata)
                        else:
                            raise Exception
                    except:
                        self.logger.error(traceback.format_exc())
                        self.logger.error('An error occurred while decoding {} data.'.format(datatype))
                    else:
                        await callback(data)
            finally:
                await stream.end()
                self.logger.info('RPC client has unsubscribed from {} data.'.format(datatype))

    async def _publish(self, data, datatype, datatimestamp):
        success = False
        try:
            truedatatype = datatype.split('-')[0]
            if truedatatype in TRAFFIC_DATA_TYPES:
                pbdata = await protobuf.encode_traffic_data(data)
            elif truedatatype == DATA_POINTS:
                pbdata = await protobuf.encode_locations(data)
            elif truedatatype == MAPPING_ROADS_DATA_POINTS:
                pbdata = await protobuf.encode_mapping(data, datatimestamp)
            else:
                raise Exception
            request = PubRequest(datatype=datatype)
            request.data.Pack(pbdata)
            request.timestamp.FromSeconds(datatimestamp)
            response = await self.interface.publish(request)
            success = response.success
            if not success:
                self.logger.warning('Failed to publish {} data.'.format(datatype))
        except:
            self.logger.error(traceback.format_exc())
            self.logger.error('An error occurred while publishing {} data.'.format(datatype))
        finally:
            return success

    async def _get_data_points(self, datapointeids=None, datatypeeid=None):
        lr = LocationsRequest()
        if datapointeids is not None:
            lr.eids.eids.extend(datapointeids)
        if datatypeeid is not None:
            lr.datatype = datatypeeid
        return await protobuf.decode_locations(await self.interface.get_data_points(lr))

    async def _get_roads(self, roadeids=None):
        lr = LocationsRequest()
        if roadeids is not None:
            lr.eids.eids.extend(roadeids)
        return await protobuf.decode_locations(await self.interface.get_roads(lr))

    async def _get_zones(self, zoneeids=None):
        lr = LocationsRequest()
        if zoneeids is not None:
            lr.eids.eids.extend(zoneeids)
        return await protobuf.decode_locations(await self.interface.get_zones(lr))

    async def _get_mapping_roads_data_points(self):
        return (await protobuf.decode_mapping(await self.interface.get_mapping_roads_data_points(MappingRequest())))[0]

    async def _get_mapping_zones_roads(self):
        return (await protobuf.decode_mapping(await self.interface.get_mapping_zones_roads(MappingRequest())))[0]

    @staticmethod
    def _get_data_type_eid_from_data_points(datapoints):
        datapointeid, datapoint = datapoints.popitem()
        datatype = datapoint[DATA_TYPE_EID]
        datapoints[datapointeid] = datapoint
        return datatype


def start(Application, threaded=False):
    if threaded:
        import threading
        threading.Thread(target=start, args=(Application, False), daemon=True).start()
        print('Starting application in a background thread...')
    else:
        Application()
