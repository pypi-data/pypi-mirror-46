"""
Main evaluation CLI

"""
from click import command
from microcosm.object_graph import ObjectGraph

from microcosm_sagemaker.app_hooks import create_evaluate_app
from microcosm_sagemaker.artifact import InputArtifact
from microcosm_sagemaker.commands.options import input_artifact_option, input_data_option
from microcosm_sagemaker.input_data import InputData


@command()
@input_data_option()
@input_artifact_option()
def main(input_data, input_artifact):
    graph = create_evaluate_app(
        loaders=[input_artifact.load_config],
    )

    run_evaluate(graph, input_data, input_artifact)


def run_evaluate(
    graph: ObjectGraph,
    input_data: InputData,
    input_artifact: InputArtifact,
) -> None:
    # Load the saved artifact
    graph.active_bundle.load(input_artifact)

    # Evaluate
    graph.active_evaluation(graph.active_bundle, input_data)
