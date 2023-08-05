from prometheus_client import Counter, Gauge


class MetricsRegistrar:
    COUNTERS = 'counters'
    GAUGES = 'gauges'

    def __init__(self):
        self.metrics_dict = {
            self.COUNTERS: {

            },
            self.GAUGES: {

            }
        }

    def counter(self, name, documentation=None, labels=None):
        if name not in self.metrics_dict[self.COUNTERS]:
            if not documentation:
                documentation = name

            if labels:
                self.metrics_dict[self.COUNTERS][name] = Counter(name, documentation, labels)
            else:
                self.metrics_dict[self.COUNTERS][name] = Counter(name, documentation)

        return self.metrics_dict[self.COUNTERS][name]

    def gauge(self, name, documentation=None, labels=None):
        if name not in self.metrics_dict[self.GAUGES]:
            if not documentation:
                documentation = name

            if labels:
                self.metrics_dict[self.GAUGES][name] = Gauge(name, documentation, labels)
            else:
                self.metrics_dict[self.GAUGES][name] = Gauge(name, documentation)

        return self.metrics_dict[self.GAUGES][name]
