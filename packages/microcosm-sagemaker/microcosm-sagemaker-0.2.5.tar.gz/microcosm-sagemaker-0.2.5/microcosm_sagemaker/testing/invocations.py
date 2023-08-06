"""
Example CRUD routes tests.

Tests are sunny day cases under the assumption that framework conventions
handle most error conditions.

"""
from pathlib import Path

from hamcrest import (
    assert_that,
    equal_to,
    has_entries,
    is_,
)
from hamcrest.core.base_matcher import BaseMatcher

from microcosm_sagemaker.app_hooks import create_serve_app
from microcosm_sagemaker.artifact import InputArtifact
from microcosm_sagemaker.commands.config import load_default_runserver_config


class InvocationsRouteTestCase:
    """
    Helper base class for writing tests of the invocations route.

    """
    def setup(self, input_artifact_path: Path) -> None:
        self.input_artifact = InputArtifact(input_artifact_path)

        self.graph = create_serve_app(
            testing=True,
            loaders=[
                load_default_runserver_config,
                self.input_artifact.load_config,
            ],
        )

        self.client = self.graph.flask.test_client()

    def test_search(
        self,
        request_json: dict,
        response_items_matcher: BaseMatcher,
    ) -> None:
        """
        Invokes the invocations endpoint with `request_json`, and checks the
        `items` entry of the response against `response_items_matcher`.

        """
        self.graph.active_bundle.load(self.input_artifact)

        uri = "/invocations"

        response = self.client.post(
            uri,
            json=request_json,
        )

        assert_that(response.status_code, is_(equal_to(200)))
        assert_that(
            response.json,
            has_entries(
                items=response_items_matcher,
            ),
        )
