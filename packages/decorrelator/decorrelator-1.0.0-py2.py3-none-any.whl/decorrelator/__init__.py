import theano
theano.config.compute_test_value = "ignore"

from .correlation import CorrelationModel
from .linear import LinearRelation