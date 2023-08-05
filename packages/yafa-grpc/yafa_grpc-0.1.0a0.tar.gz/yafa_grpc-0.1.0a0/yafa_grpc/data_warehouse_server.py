from concurrent import futures
import time
import logging

import grpc

from yafa_grpc import data_warehouse_pb2
from yafa_grpc import data_warehouse_pb2_grpc
from yafa_grpc import LOGGING_VERBOSITY

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class StockPrice(data_warehouse_pb2_grpc.StockPriceServicer):

    def get_price(self, request, context):
        logging.debug("Data warehouse server received request:\n%s", request)
        return data_warehouse_pb2.DOHLC(
            symbol="response_symbol",
            date="response_date",
            open=12.3,
            high=12.3,
            low=12.3,
            close=12.3)


def serve():
    logging.info("Starting data warehouse server...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    data_warehouse_pb2_grpc.add_StockPriceServicer_to_server(StockPrice(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


def main():
    logging.basicConfig(level=LOGGING_VERBOSITY)
    serve()


if __name__ == '__main__':
    main()
