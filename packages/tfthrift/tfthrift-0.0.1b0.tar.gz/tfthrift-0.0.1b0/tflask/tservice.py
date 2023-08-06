#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

from thrift.transport import TSocket
from thrift.protocol import TBinaryProtocol
from thrift.server import TNonblockingServer
from thrift.transport import TTransport
from thrift.server import TProcessPoolServer
import logging


class ThriftServer:
    def __init__(self, ip, port, handler_obj, service_module, num_workers=10):
        """

        @param ip:
        @param port:
        @param handler_obj:
        @param service_module: Thrift Service的模块py文件
        @param num_workers:  用多少个worker

        @return:
        """
        self._ip = ip
        self._port = port
        self._handler_obj = handler_obj
        self._service_module = service_module
        self._num_workers = num_workers

        self._processor = service_module.Processor(self._handler_obj)
        self._server_socket = TSocket.TServerSocket(
            host=self._ip, port=self._port)
        self._tfactory = TTransport.TBufferedTransportFactory()
        self._pfactory = TBinaryProtocol.TBinaryProtocolFactory()

        # 线程池Server
        # self._server = TServer.TThreadPoolServer(
        #     self._processor,
        #     self._server_socket,
        #     tfactory=self._tfactory,
        #     pfactory=self._pfactory,
        #
        #     daemon=True,
        # )
        # self._server.setNumThreads(self._num_threads)

        # # 非阻塞Server, 应该是Epoll这一套东西
        self._server = TNonblockingServer.TNonblockingServer(
            self._processor,
            self._server_socket,

            inputProtocolFactory=self._pfactory,
        )
        self._server.setNumThreads(self._num_workers)

        # 进程池
        self._server = TProcessPoolServer.TProcessPoolServer(self._processor, self._server_socket,
                                                             self._tfactory, self._pfactory)
        self._server.setPostForkCallback(self.processCallback)
        self._server.setNumWorkers(self._num_workers)

        # # 每一个请求, 一个线程
        # self._server = TServer.TThreadedServer(
        #     self._processor,
        #     self._server_socket,
        
        #     tfactory=self._tfactory,
        #     pfactory=self._pfactory,
        # )
    
    def processCallback(self):
        print("start new worker")

    def start(self):
        logging.info("start rpc server")
        self._server.serve()

# if __name__ == "__main__":
#     handler = Worker(None)
#     server = ThriftServer("0.0.0.0", 8088, handler, Rpc)
#     server.start()

