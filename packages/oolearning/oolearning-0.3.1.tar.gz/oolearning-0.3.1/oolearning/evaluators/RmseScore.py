import numpy as np

from oolearning.enums.Metric import Metric
from oolearning.evaluators.CostFunctionMixin import CostFunctionMixin
from oolearning.evaluators.ScoreActualPredictedBase import ScoreActualPredictedBase


class RmseScore(CostFunctionMixin, ScoreActualPredictedBase):
    @property
    def name(self) -> str:
        return Metric.ROOT_MEAN_SQUARE_ERROR.value

    def _calculate(self, actual_values: np.ndarray, predicted_values: np.ndarray) -> float:
        return np.sqrt(np.mean(np.square(actual_values - predicted_values)))
