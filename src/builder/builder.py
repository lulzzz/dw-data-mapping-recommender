import importlib

from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

from src.parser.ConfigParser import ConfigParser


class ClassBuilder(object):
    def build(self, json, parameters=None):
        config_parser = ConfigParser()
        classes = config_parser.parse_classes(json=json)
        modules_dir = config_parser.parse_module_dir(json=json)
        instances = self._initialize_classes(classes=classes, modules_dir=modules_dir, parameters=parameters)

        return instances

    def _initialize_classes(self, classes, modules_dir, parameters):
        instances = []

        # TODO: REFACTOR!
        if parameters is None:
            for klass, module_dir in zip(classes, modules_dir):
                my_module = importlib.import_module(module_dir)
                MyClass = getattr(my_module, klass)
                instances.append(MyClass())
        else:
            for klass, module_dir, parameter in zip(classes, modules_dir, parameters):
                my_module = importlib.import_module(module_dir)
                MyClass = getattr(my_module, klass)
                instances.append(MyClass(**parameter))

        return instances


class PipelineBuilder(object):
    def build(self, transformers, estimator):
        pipeline = Pipeline([transformer for transformer in transformers].append(estimator))
        return pipeline


class GridSearchBuilder(object):
    def build(self, param_grid, pipeline, cv):
        grid_search = GridSearchCV(pipeline, cv=cv, param_grid=param_grid)
        return grid_search

class DataframeBuilder(object):
    def build(self):
        pass