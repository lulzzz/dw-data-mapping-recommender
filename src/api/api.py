import gensim
import numpy as np
import pandas as pd

from builder.builder import ClassBuilder
from feature_extractors.shallow_extractors import ShallowExtractors
from parser.ConfigParser import ConfigParser
from reader.JsonReader import JsonReader
from service.DatabaseService import DatabaseService
from service.gateway.database_gateways.NotMNISTGateway import NotMNISTGateway
from src.classifiers.classifiers import MaximumProbabilityClassifier
from src.formatter.recommender_formatter import RecommenderFormatter
from src.parser.sample_pairs_parser import SamplePairsParser
from src.recommender.recommender import Recommender
from src.tokenizer.tokenizer import Tokenizer

from sklearn.model_selection import learning_curve
from sanic import Sanic
from sanic.response import json

# model = gensim.models.KeyedVectors.load_word2vec_format('datasets/wiki-news-300d-1M.vec')
# # self.model.init_sims(replace=True)
# shallow_extractors = ShallowExtractors(model=model)
# recommendation_metrics = [shallow_extractors.calculate_similarity_distance,
#                           shallow_extractors.edit_distance_partial_ratio,
#                           shallow_extractors.edit_distance_token_set_ratio,
#                           shallow_extractors.edit_distance_ratio]
# recommender = Recommender(recommendation_metrics=recommendation_metrics)
# recommender_formatter = RecommenderFormatter()
# maximum_probability_classifier = MaximumProbabilityClassifier()
# tokenizer = Tokenizer()

app = Sanic()


@app.route('/recommender', methods=['POST'])
async def recommend_papa_altoke(request):
    jsonn = request.json
    X = [jsonn['incoming']]
    y = [jsonn['expected']]

    recommended_words = maximum_probability_classifier.classify(X=X, y=y, recommender=recommender)

    # parsed_recommended_words = collections.defaultdict(dict)
    # i = 0
    # for s in recommended_words:
    #     for (key, value) in s.items():
    #         for (_key, _value) in value.items():
    #
    #             parsed_y = tokenizer.tokenize_by(sentences=y, method='cammel_case_words')
    #             processed_input_sentences_tokens = []
    #             for _y_p in parsed_y:
    #                 parsed_y = tokenizer.split_by(tokens=_y_p, delimiter="/")
    #                 parsed_y = tokenizer.normalize_tokens(tokens=parsed_y)
    #                 processed_input_sentences_tokens.append(parsed_y)
    #
    #             parsed_recommended_words[X[0][i]][_key] = _value
    #     i += 1

    return json(recommended_words)


@app.route('/compareAlgorithms', methods=['POST'])
async def xxx(request):
    sample_pairs_parser = SamplePairsParser()
    dataframe = sample_pairs_parser.parse(path='raw-datasets/sample_most_recent_pairs.xlsx')
    dataframe = dataframe[(dataframe.Feedback == 'OK')]
    number_of_dataweave_scripts = dataframe.block_num.nunique()

    X = []
    y = []
    for i in range(number_of_dataweave_scripts):
        if not dataframe[(dataframe.block_num == (i + 1))]['map_from'].empty:
            X.append(dataframe[(dataframe.block_num == (i + 1))]['map_from'])
            y.append(dataframe[(dataframe.block_num == (i + 1))]['map_to'])

    aux_X = []
    aux_y = []
    for _X, _y in zip(X, y):
        if len(_X) > 15:
            aux_X.append(_X[:15])
            aux_y.append(_y[:15])
        else:
            aux_X.append(_X)
            aux_y.append(_y)

    X = aux_X
    y = aux_y

    score = maximum_probability_classifier.score(X=X, y=y, recommender=recommender)

    mean = np.mean(score)
    std = np.std(score)

    return "Performance metric: Accuracy. Mean: {}, STD: {}".format(mean, std)


@app.route('/tesis', methods=['POST'])
async def yyy(request):
    json_reader = JsonReader()
    config_parser = ConfigParser()

    config = json_reader.read(path='configs/trust.config.json')

    directories = config_parser.parse_directories(config=config)
    # FIXME: this is redundant with the output of json_read.read() check if it's necesary to divide again
    feature_extractors = config_parser.parse_feature_extractors(config=config)
    space_transformers = config_parser.parse_space_transformers(config=config)
    classifiers = config_parser.parse_classifiers(config=config)

    class_builder = ClassBuilder()
    # Esto esta mal conceptualmente, ver de tener una config global
    not_mnist_gateway = NotMNISTGateway(dataset_dir=directories['datasetDirectory'])
    database_service = DatabaseService(gateway=not_mnist_gateway)

    feature_extractors_instances = class_builder.build(json=feature_extractors)
    space_transformers_instances = class_builder.build(json=space_transformers,
                                                       parameters=[space_transformers[0]['PCA']['parameters']])
    classifiers_instances = class_builder.build(json=classifiers)

    X, y = database_service.X_and_y()

    # features = feature_extraction(feature_extractors_instances=feature_extractors_instances)

    X_train, X_test, y_train, y_test = database_service.split_into_train_and_test(X=X, y=y)

    for space_transformers_instance in space_transformers_instances:
        space_transformers_instance = space_transformers_instance.fit(X_train)

    X_train = space_transform_(space_transformers_instances=space_transformers_instances, dataset=X_train)
    X_test = space_transform_(space_transformers_instances=space_transformers_instances, dataset=X_test)

    # It works!
    # plt.imshow(X=X[0], shape=(28, 28))

    # train
    for classifier_instance in classifiers_instances:
        classifier_instance.fit(X_train, y_train)

    predictions = []
    algorithms_names = []
    algorithms_training_sizes = []
    algorithms_trainin_scores = []
    algorithms_test_scores = []

    # predict
    for classifier_instance in classifiers_instances:
        algorithms_names.append(classifier_instance.__class__.__name__)
        predictions.append(classifier_instance.score(X=X_test, y=y_test))
        # predictions = classifier_instance.predict(X=X_test)
        train_sizes, train_scores, test_scores = learning_curve(classifier_instance, X_train, y_train,
                                                                train_sizes=[100, 500, 1000, 1500], cv=3)
        algorithms_training_sizes.append(train_sizes)
        algorithms_trainin_scores.append(train_scores)
        algorithms_test_scores.append(test_scores)

    dataframe0 = pd.DataFrame({'Algorithms': algorithms_names, 'TestScore': predictions})

    # visualizations
    plotly_graphs = config_parser.parse_plotly_graphs(config=config)
    plt_graphs = config_parser.parse_plt_graphs(config=config)

    # TODO: UP TO NOW IM NOT USING GRAPH TYPE, SHOULD BE GENERALIZATED
    # TODO: REFACTOR THIS LOOPS!!
    for plotly_graph in plotly_graphs:
        for graph_type, graph_values in plotly_graph.items():
            visualizations = graph_values['visualizations']

    traces_parameters_transformer = TracesParametersTransformer()

    transformed_traces_parameters = [
        traces_parameters_transformer.transform(traces=visualizations[0]['traces'], dataframe=dataframe0)]
    traces_instances = (class_builder.build(json=visualizations[0]['traces'], parameters=transformed_traces_parameters))

    # FIXME: HARDCODED VISUALIZATIONS
    plotly_graphs_parameters = [{'traces': traces_instances, 'layout': visualizations[0]['layout']}]
    plotly_graphs_instances = class_builder.build(json=plotly_graphs, parameters=plotly_graphs_parameters)

    # plt_graphs_parameters = [{'train_sizes': algorithms_training_sizes, 'train_scores': algorithms_trainin_scores,
    #                           'test_scores': algorithms_test_scores}]
    plt_graphs_parameters = [{'train_sizes': train_sizes, 'train_scores': train_scores,
                              'test_scores': test_scores}]
    plt_graphs_instances = class_builder.build(json=plt_graphs, parameters=plt_graphs_parameters)

    graphs_instances = plotly_graphs_instances + plt_graphs_instances

    for graph_instance in graphs_instances:
        graph_instance.graph()


def space_transform_(space_transformers_instances, dataset):
    # FIXME: JUST A TEST, USE AN ACTUAL LIST!!
    for space_transformer in space_transformers_instances:
        return space_transformer.transform(dataset)


class TracesParametersTransformer(object):
    def transform(self, traces, dataframe):
        transformed_parameters = {}
        for trace in traces:
            for trace_type, values in trace.items():
                for parameter, value in values['parameters'].items():
                    transformed_parameters[parameter] = dataframe[value].values

        return transformed_parameters


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
