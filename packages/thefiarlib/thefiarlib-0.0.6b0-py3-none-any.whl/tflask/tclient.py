#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

from thrift import Thrift
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
from library.thrift_protocol import Rpc
from pprint import pprint

import logging
import json


class ThriftClient:
    def __init__(self, ip, port, module_file, timeout_ms=3 * 1000):
        """

        @param ip: 
        @param port: 
        @param module_file:  导向哪一个Service
        @param timeout_ms: socket的超时时间 
        @return: 
        """
        self._ip = ip
        self._port = port
        self._module_file = module_file
        self._timeout_ms = timeout_ms

        self._socket_obj = TSocket.TSocket(host=self._ip, port=self._port)
        self._socket_obj.setTimeout(self._timeout_ms)
        self._transport = TTransport.TBufferedTransport(
            self._socket_obj,
        )
        self._protocol = TBinaryProtocol.TBinaryProtocol(self._transport)

        self._client = self._module_file.Client(self._protocol)

    def __enter__(self):
        if not self._transport.isOpen():
            try:
                self._transport.open()
            except Thrift.TException as e:
                logging.error('ERROR')

                raise Exception(str(e))

            logging.info('ERROR')

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._transport.isOpen():
            self._transport.close()
            logging.info("connection conection")

    def request(self, method_name_str, *args):
        try:
            result = getattr(self._client, method_name_str)(*args)
        except Exception as e:
            logging.error('ERROR. %s' % [method_name_str, args])

            if self._transport.isOpen():
                self._transport.close()
                logging.warning("request:: is closed")

            raise Exception(str(e))
        else:
            return result


if __name__ == "__main__":
    with ThriftClient("127.0.0.1", 8088, Rpc) as client:
        # for index in range(1, 10):
        # $requestData = [
        #     'auth' => [
        #         'app_key' => $this->_config['app_key'],
        #         'app_secret' => $this->_config['app_secret'],
        #     ],
        #     'request_data' => [
        #         'url' => $url,
        #         'params' => $params,
        #     ],
        # ];

        t_rpc_request_data = {
            "auth":{
                "app_key": "key",
                "app_sec": "sec",
            },
            "request_data":{
                "url": "/",
                "params": {
                    "hello": "a"
                }
            }
        }

        resp = client.request("call", (json.dumps(t_rpc_request_data)))
        pprint(resp)
