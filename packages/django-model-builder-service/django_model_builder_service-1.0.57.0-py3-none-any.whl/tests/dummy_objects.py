class DummyBuilderService:
    def build_model(self):
        pass

    def get_model_data(self):
        pass


class DummyWrapper:
    def build(self):
        pass


class DummyMetricsRegistrar:
    def counter(self):
        pass

    def gauge(self):
        pass


class DummyJob:
    def remove(self):
        pass

    def pause(self):
        pass

    def resume(self):
        pass


class DummyScheduler:
    def start(self):
        pass

    def shutdown(self, wait):
        pass

    def add_job(self, *args, **kwargs):
        pass
