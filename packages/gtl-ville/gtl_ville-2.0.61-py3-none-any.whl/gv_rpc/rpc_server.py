#!/usr/bin/env python3

import asyncio
import traceback

from grpclib.server import Server
from grpclib.reflection.service import ServerReflection

from gv_services.interface import Interface
from gv_utils.asyncio import check_event_loop


class RpcServer:

    def __init__(self, logger):
        self.logger = logger
        self.server = None

    def start(self, *credentials):
        check_event_loop()  # will create a new event loop if needed (if we are in a thread)
        self.logger.info('RPC server is starting.')
        try:
            asyncio.run(self._run(*credentials))
        except KeyboardInterrupt:
            pass
        self.logger.info('RPC server has stopped.')

    async def _run(self, *credentials):
        paths = credentials[:2]
        dbcredentials = credentials[2:-2]
        rpccredentials = credentials[-2:]
        try:
            interface = Interface(self.logger, *paths, *dbcredentials)
            await interface.async_init()
            services = [interface]
            services = ServerReflection.extend(services)
            self.server = Server(services, loop=asyncio.get_event_loop())
            await self._serve(*rpccredentials)
        except:
            self.logger.error(traceback.format_exc())

    async def _serve(self, *rpccredentials):
        await self.server.start(*rpccredentials)
        self.logger.info('RPC server is serving on {}:{}.'.format(*rpccredentials))
        try:
            self.logger.info('RPC server has started.')
            await self.server.wait_closed()  # block until an exception is raised
        except asyncio.CancelledError:
            await self._close()

    async def _close(self):
        if self.server is not None:
            self.server.close()
            self.logger.info('RPC server is closing.')
            await self.server.wait_closed()
            self.server = None


def start(Application, threaded=False):
    if threaded:
        import threading
        threading.Thread(target=start, args=(Application, False), daemon=True).start()
        print('Starting application in a background thread...')
    else:
        Application()
