import pytest
from frontier_experiment_lite import FrontierExperimentLite

def test_measure_transcendence_depth():
    fe = FrontierExperimentLite()
    samples = [
        "We seek to transcend the limitations of matter and become infinite.",
        "Beyond the physical, there is an ultimate pure essence.",
        "This absolute consciousness is boundless and eternal.",
    ]
    for text in samples:
        assert fe._measure_transcendence_depth(text) > 0

