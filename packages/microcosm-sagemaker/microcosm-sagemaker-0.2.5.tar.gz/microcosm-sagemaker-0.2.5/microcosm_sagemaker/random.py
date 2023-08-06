from random import seed

from microcosm.api import defaults


@defaults(
    seed=42,
)
class Random:
    def __init__(self, graph):
        self.seed = graph.config.random.seed

        graph.training_initializers.register(self)

    def init(self):
        seed(self.seed)
