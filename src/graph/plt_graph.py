import numpy as np
import matplotlib.pyplot as plt


class plt_graph(object):
    # FIXME: THIS IS WRONG! JUST A BYPASS FOR TESTING
    def __init__(self, train_sizes, train_scores, test_scores):
        self.train_sizes = train_sizes
        self.train_scores = train_scores
        self.test_scores = test_scores

    def graph(self):
        train_scores_mean = np.mean(self.train_scores, axis=1)
        train_scores_std = np.std(self.train_scores, axis=1)
        test_scores_mean = np.mean(self.test_scores, axis=1)
        test_scores_std = np.std(self.test_scores, axis=1)
        plt.grid()

        plt.fill_between(self.train_sizes, train_scores_mean - train_scores_std,
                         train_scores_mean + train_scores_std, alpha=0.1,
                         color="r")
        plt.fill_between(self.train_sizes, test_scores_mean - test_scores_std,
                         test_scores_mean + test_scores_std, alpha=0.1, color="g")
        plt.plot(self.train_sizes, train_scores_mean, 'o-', color="r",
                 label="Training score")
        plt.plot(self.train_sizes, test_scores_mean, 'o-', color="g",
                 label="Test score")

        plt.legend(loc="best")
        plt.show()
