from unittest import TestCase

from prometheus_client import Counter, Gauge

from django_model_builder_service.metrics.metrics import MetricsRegistrar


class TestMetricsRegistrar(TestCase):

    def setUp(self):
        self.target = MetricsRegistrar()

    def test_registrar_metric_type(self):
        counter = self.target.counter(name='test_counter', documentation='test_counter_documentation')
        self.assertTrue(isinstance(counter, Counter))

        gauge = self.target.gauge(name='test_gauge', documentation='test_gauge_documentation')
        self.assertTrue(isinstance(gauge, Gauge))

    def test_registrar_lazy_initialization(self):
        counter1 = self.target.counter(name='test_counter_with_some_unique_name',
                                       documentation='test_counter_documentation')
        counter2 = self.target.counter(name='test_counter_with_some_unique_name',
                                       documentation='different documentation should not matter. Already created counter should be retrieved')
        self.assertTrue(counter1 is counter2)
