"""
Consumer factories.

"""


def configure_active_bundle(graph):
    if not getattr(graph.config, "active_bundle", ""):
        return None
    return getattr(graph, graph.config.active_bundle)


def configure_active_evaluation(graph):
    if not getattr(graph.config, "active_evaluation", ""):
        return None
    return getattr(graph, graph.config.active_evaluation)


def configure_sagemaker(graph):
    """
    Instantiates all the necessary sagemaker factories.

    """
    graph.use(
        "active_bundle",
        "active_evaluation",
        "training_initializers",
        "random",
    )
