from __future__ import print_function
import logging

import grpc

from yafa_grpc import data_warehouse_pb2
from yafa_grpc import data_warehouse_pb2_grpc
from yafa_grpc import DATA_WAREHOUSE_HOST, LOGGING_VERBOSITY


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    channel = grpc.insecure_channel(f'{DATA_WAREHOUSE_HOST}:50051')
    stub = data_warehouse_pb2_grpc.StockPriceStub(channel)
    response = stub.get_price(
        data_warehouse_pb2.PriceRequest(symbol="request_symbol", date="request_date"))
    logging.debug("Data warehouse client received response:\n%s ", response)


def main():
    logging.basicConfig(level=LOGGING_VERBOSITY)
    run()


if __name__ == '__main__':
    main()
