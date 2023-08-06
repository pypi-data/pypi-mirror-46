import abc


class Layer(abc.ABC):
    @abc.abstractmethod
    def load(self):
        pass

    @abc.abstractmethod
    @property
    def all(self):
        pass


class YamlLayer:
    def __init__(self, fname):
        self.fname = fname
        self.data = None

    def load(self):
        with open(self.fname, "r") as g:
            self.data = yaml.load(f)

    @property
    def all(self):
        return list(self.data.keys())

    def __getattr__(self, v):
        return self.data[v]


class ConfigManager:
    def __init__(self, *layers):
        self.config = {}
        for layer in layers:
            self.add_layer(layer)

    def add_layer(self, layer):
        layer.load()
        for key in layer.all:
            self.config[key] = self.layer[key]

    def __getattr__(self, v):
        return self.config[v]
