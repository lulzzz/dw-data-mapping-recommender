from src.reader.NotMNISTReader import NotMNISTReader
from src.service.gateway.database_gateways.DatabaseGateway import DatabaseGateway


class NotMNISTGateway(DatabaseGateway):
    def __init__(self, dataset_dir):
        self.dataset_dir = dataset_dir

    def X_and_y(self):
        not_mnist_reader = NotMNISTReader()
        return not_mnist_reader.read(path=self.dataset_dir)
