from .event import RemoteEvent
import inject
from applauncher.kernel import Configuration, InjectorReadyEvent, KernelShutdownEvent
import logging
import importlib


class RemoteEventBundle(object):

    def __init__(self):
        self.logger = logging.getLogger("remote-event")
        self.config_mapping = {
            "remote_event": {
                "group_id": "",
                "backend": "redis",
                "events": [{"name": {"type": "string"}}]
            }
        }

        self.event_listeners = [
            (InjectorReadyEvent, self.injector_ready),
            (RemoteEvent, self.propagate_remote_event),
            (KernelShutdownEvent, self.kernel_shutdown)
        ]

        self.run = True
        self.backend = None

    @inject.params(config=Configuration)
    def injector_ready(self, event, config):
        backend_name = config.remote_event.backend.strip(".")
        m = importlib.import_module(
            name="remote_event_bundle.backend.{backend}_backend".format(backend=backend_name)
        )
        backend = getattr(m, "{backend}Backend".format(backend=backend_name.capitalize()))
        self.backend = backend(group_id=config.remote_event.group_id)
        self.backend.register_events(config.remote_event.events)

    def propagate_remote_event(self, event):
        if self.backend:
            self.backend.propagate_remote_event(event)

    def kernel_shutdown(self, event):
        if self.backend:
            self.backend.shutdown()
