import copy


class ConfigParser(object):

    def parse_directories(self, config):
        """

        :param config: the configuration json.
        :type config: dict.
        :return: load all directories paths.
        :rtype: dict.
        @IMPORTANT: it doesn't change the original config file.
        """
        new_config = copy.deepcopy(config)
        # TODO: GENERALIZE IT
        directories = {'rootDirectory': new_config['rootDirectory'], 'datasetDirectory': new_config['datasetDirectory']}
        return directories

    def parse_classifiers(self, config):
        """

        :param config: the configuration json.
        :type config: dict.
        :return: load machine learning algorithms label from the configuration file.
        :rtype: dict.
        @IMPORTANT: it doesn't change the original config file.
        """

        new_config = copy.deepcopy(config)
        extracted = new_config['classifiers']
        return extracted

    def parse_plotly_graphs(self, config):
        """

        :param config: the configuration json.
        :type config: dict.
        :return: load all plotly visualizations from the configuration file.
        :rtype: dict.
        @IMPORTANT: it doesn't change the original config file.
        """

        new_config = copy.deepcopy(config)
        extracted_graphs = new_config['graphs']
        # TODO: IS THERE A BETTER WAY OF DOING THIS?
        plotly_graphs = []
        for graph in extracted_graphs:
            plotly_graphs.extend([graph for graph_key, graph_value in graph.items() if graph_key == 'plotly_graph'])

        return plotly_graphs

    def parse_visualizations(self, graph_json):

        new_config = copy.deepcopy(graph_json)
        extracted = new_config['visualizations']
        return extracted

    def parse_feature_extractors(self, config):
        """

        :param config: the configuration json.
        :type config: dict.
        :return: Load the feature extractors label from the configuration file.
        :rtype: dict
        @IMPORTANT: it doesn't change the original config file.
        """
        new_config = copy.deepcopy(config)
        extracted = new_config['featureExtractors']
        return extracted

    def parse_classes(self, json):
        classes = []

        for klasses in json:
            classes.extend(list(klasses))
        return classes

    # TODO: REFACTOR MODULE DIR
    def parse_module_dir(self, json):
        modules_dir = []

        for klass in json:
            for value in klass.values():
                modules_dir.append(value['moduleDir'])
        return modules_dir

    def parse_traces_module_dir(self, json):
        modules_dir = []

        for klass in json:
            for value in klass.values():
                modules_dir.append(value['tracesModuleDir'])
        return modules_dir

    def parse_traces_parameters(self, json, dataframe):
        print('hola')

    def parse_plt_graphs(self, config):
        """

        :param config: the configuration json.
        :type config: dict.
        :return: load all matplotlib visualizations from the configuration file.
        :rtype: dict.
        @IMPORTANT: it doesn't change the original config file.
        """

        new_config = copy.deepcopy(config)
        extracted_graphs = new_config['graphs']
        # TODO: IS THERE A BETTER WAY OF DOING THIS?
        plt_graphs = []
        for graph in extracted_graphs:
            plt_graphs.extend([graph for graph_key, graph_value in graph.items() if graph_key == 'plt_graph'])

        return plt_graphs

    def parse_space_transformers(self, config):
        """

        :param config: the configuration json.
        :type config: dict.
        :return: Load the space transformers label from the configuration file.
        :rtype: dict
        @IMPORTANT: it doesn't change the original config file.
        """
        new_config = copy.deepcopy(config)
        extracted = new_config['spaceTransformers']
        return extracted
