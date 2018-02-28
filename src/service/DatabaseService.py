class DatabaseService(object):
    def __init__(self, gateway):
        self.database_gateway = gateway

    def X_and_y(self):
        return self.database_gateway.X_and_y()

    def split_into_train_and_test(self, X, y):
        return self.database_gateway.split_into_train_and_test(X=X, y=y)


