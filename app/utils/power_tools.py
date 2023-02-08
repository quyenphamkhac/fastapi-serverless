from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.metrics import MetricUnit, single_metric

logger: Logger = Logger()
tracer: Tracer = Tracer()
metrics: Metrics = Metrics()
