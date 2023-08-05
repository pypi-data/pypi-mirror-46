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


class DummyModel:
    pass


class DummyWrapper:
    def build(self):
        pass

    def get_prediction(self):
        pass


class DummyScheduler:
    def start(self):
        pass

    def shutdown(self, wait):
        pass

    def add_job(self, *args, **kwargs):
        pass
