from abc import ABC, abstractmethod
from typing import Any

from microcosm_sagemaker.artifact import InputArtifact, OutputArtifact
from microcosm_sagemaker.input_data import InputData


class Bundle(ABC):
    @abstractmethod
    def fit(self, input_data: InputData) -> None:
        """
        Perform training

        """
        pass

    @abstractmethod
    def predict(self) -> Any:
        """
        Predict using the trained model

        Note that derived classes can define their own parameters and are
        expected to return something.

        """
        pass

    @abstractmethod
    def save(self, output_artifact: OutputArtifact) -> None:
        """
        Save the trained model

        """
        pass

    @abstractmethod
    def load(self, input_artifact: InputArtifact) -> None:
        """
        Load the trained model

        """
        pass
