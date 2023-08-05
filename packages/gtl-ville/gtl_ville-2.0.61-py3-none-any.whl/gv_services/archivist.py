#!/usr/bin/env python3

import traceback

from gv_services.proto.common_pb2 import TrafficData
from gv_services.storage import filestorage
from gv_utils import datetime


class Archivist:

    def __init__(self, logger, basedatapath):
        super().__init__()
        self.logger = logger
        self.basedatapath = basedatapath

    async def store_data(self, pbtrafficdata, datatype, pbtimestamp):
        success = False
        try:
            datadate = datetime.from_timestamp(pbtimestamp.ToSeconds())
            await filestorage.write_data(self.basedatapath, pbtrafficdata.trafficdata, datatype, datadate)
            success = True
            self.logger.debug('Archivist stored {} data.'.format(datatype))
        except:
            self.logger.error(traceback.format_exc())
            self.logger.error('An error occurred while storing {} data.'.format(datatype))
        finally:
            return success

    async def get_data(self, stream):
        request = await stream.recv_message()
        datatype, datadate = request.datatype, datetime.from_timestamp(request.timestamp.ToSeconds())
        data = b''
        try:
            data = await filestorage.get_data(self.basedatapath, datatype, datadate)
        except:
            self.logger.error(traceback.format_exc())
            self.logger.error('An error occurred while getting {} data for {}.'.format(datatype,
                                                                                       datetime.to_string(datadate)))
        finally:
            await stream.send_message(TrafficData(trafficdata=data))
            self.logger.debug('Archivist served {} data.'.format(datatype))
