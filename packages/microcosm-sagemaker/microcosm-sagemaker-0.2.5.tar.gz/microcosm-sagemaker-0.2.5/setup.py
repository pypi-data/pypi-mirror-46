#!/usr/bin/env python
from setuptools import find_packages, setup

project = "microcosm-sagemaker"
version = "0.2.5"

setup(
    name=project,
    version=version,
    description="Opinionated machine learning organization and configuration",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Globality Engineering",
    author_email="engineering@globality.com",
    url="https://github.com/globality-corp/microcosm-sagemaker",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.6",
    keywords="microcosm",
    install_requires=[
        "boto3>=1.9.90",
        "click>=7.0",
        "microcosm>=2.0.0",
        "microcosm_flask[metrics,spooky]>=1.20.0",
    ],
    setup_requires=[
        "nose>=1.3.6",
    ],
    dependency_links=[
    ],
    entry_points={
        "console_scripts": [
            "train = microcosm_sagemaker.commands.train:main",
            "evaluate = microcosm_sagemaker.commands.evaluate:main",
            "runserver = microcosm_sagemaker.commands.runserver:main",
        ],
        "microcosm.factories": [
            "active_bundle = microcosm_sagemaker.factories:configure_active_bundle",
            "active_evaluation = microcosm_sagemaker.factories:configure_active_evaluation",
            "ping_convention = microcosm_sagemaker.conventions.ping:configure_ping",
            "random = microcosm_sagemaker.random:Random",
            "sagemaker = microcosm_sagemaker.factories:configure_sagemaker",
            "sagemaker_metrics = microcosm_sagemaker.metrics.store:SageMakerMetrics",
            "training_initializers = microcosm_sagemaker.training_initializer_registry:TrainingInitializerRegistry",
        ],
    },
    tests_require=[
        "coverage>=3.7.1",
        "PyHamcrest>=1.9.0",
    ],
)
