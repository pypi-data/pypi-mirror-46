from pathlib import Path

import click
import gevent
import zmq.green as zmq
from loguru import logger
from playhouse.apsw_ext import APSWDatabase, CharField, IntegerField
from reprobench.console.decorators import common, server_info
from reprobench.core.bootstrap.server import bootstrap
from reprobench.core.db import Observer, db
from reprobench.core.events import BOOTSTRAP
from reprobench.core.observers import CoreObserver
from reprobench.executors.db import BaseModel
from reprobench.utils import decode_message, get_db_path, import_class


class EventLog(BaseModel):
    event = CharField(primary_key=True)
    count = IntegerField()
    payload_size = IntegerField()


class BenchmarkServer(object):
    BACKEND_ADDRESS = "inproc://backend"

    def __init__(self, output_dir, frontend_address, **kwargs):
        db_path = get_db_path(output_dir)
        db.initialize(APSWDatabase(db_path))
        self.bootstrapped = Path(db_path).exists()
        self.frontend_address = frontend_address
        self.observers = [CoreObserver]

    def wait_for_bootstrap(self):
        while True:
            address, event_type, payload = self.frontend.recv_multipart()
            logger.trace((address, event_type, payload))
            if event_type == BOOTSTRAP:
                break

        payload = decode_message(payload)
        bootstrap(**payload)

        EventLog.create_table()

        event = EventLog.get_or_none(str(event_type))
        if event is None:
            event = EventLog(event=str(event_type), count=1, payload_size=len(payload))
        else:
            event.count += 1
            event.payload_size += len(payload)
        event.save()

        self.bootstrapped = True
        self.frontend.send_multipart([address, b"done"])

    def loop(self):
        while True:
            address, event_type, payload = self.frontend.recv_multipart()
            logger.trace((address, event_type, payload))

            event = EventLog.get_or_none(str(event_type))
            if event is None:
                event = EventLog(event=str(event_type), count=1, payload_size=len(payload))
            else:
                event.count += 1
                event.payload_size += len(payload)
            event.save()

            self.backend.send_multipart([event_type, payload, address])

    def run(self):
        self.context = zmq.Context()
        self.frontend = self.context.socket(zmq.ROUTER)
        self.frontend.bind(self.frontend_address)
        self.backend = self.context.socket(zmq.PUB)
        self.backend.bind(self.BACKEND_ADDRESS)

        logger.info(f"Listening on {self.frontend_address}...")

        if not self.bootstrapped:
            logger.info(f"Waiting for bootstrap event...")
            self.wait_for_bootstrap()

        self.observers += [
            import_class(o.module) for o in Observer.select(Observer.module)
        ]

        observer_greenlets = []
        for observer in self.observers:
            greenlet = gevent.spawn(
                observer.observe,
                self.context,
                backend_address=self.BACKEND_ADDRESS,
                reply=self.frontend,
            )
            observer_greenlets.append(greenlet)

        serverlet = gevent.spawn(self.loop)
        logger.info(f"Ready to receive events...")
        serverlet.join()

        gevent.killall(observer_greenlets)


@click.command(name="server")
@click.option(
    "-d", "--output-dir", type=click.Path(), default="./output", show_default=True
)
@server_info
@common
def cli(server_address, output_dir, **kwargs):
    server = BenchmarkServer(output_dir, server_address, **kwargs)
    server.run()


if __name__ == "__main__":
    cli()
