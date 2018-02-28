from sklearn.model_selection import train_test_split


class DatabaseGateway(object):
    def split_into_train_and_test(self, X, y):
        return train_test_split(X, y, test_size=0.33, random_state=42)
