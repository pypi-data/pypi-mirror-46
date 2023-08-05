import yafa_grpc


def server():
    from yafa_grpc.data_warehouse_server import main
    main()


def client():
    from yafa_grpc.data_warehouse_client import main
    main()