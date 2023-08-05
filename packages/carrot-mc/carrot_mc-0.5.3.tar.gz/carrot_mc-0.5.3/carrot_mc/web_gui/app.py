from argparse import Namespace
from functools import wraps

import eventlet
from eventlet.semaphore import Semaphore
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO

from carrot_mc.backend import BackendService
from carrot_mc.carrot import CarrotService, InstallationManager
from carrot_mc.cli_printer import CliEventPrinter
from carrot_mc.data import Automappable

app = Flask(__name__, static_url_path='')
socketio = SocketIO(app)


class CompositePrinter:
    def __init__(self, printers):
        self.printers = printers

    def handle(self, event: str, payload=None):
        for printer in self.printers:
            printer.handle(event, payload)


class SocketEventRouter:
    def handle(self, event: str, payload=None):
        if not payload:
            socketio.emit(event, {})
            return

        if isinstance(payload, str):
            socketio.emit(event, payload)
            return

        if isinstance(payload, Namespace):
            payload = vars(payload)

        converted = dict()
        for k, v in payload.items():
            if isinstance(v, Automappable):
                converted[k] = v.to_dict()
            else:
                converted[k] = v

        socketio.emit(event, converted)
        eventlet.sleep(0) # Force flush


cli_printer = CliEventPrinter()
socket_router = SocketEventRouter()
composite_printer = CompositePrinter([cli_printer, socket_router])

backend_service = BackendService()
installation_manager = InstallationManager(backend_service, composite_printer)
carrot_service = CarrotService(backend_service, installation_manager, composite_printer)


class RequestQueue:
    semaphores = dict()

    def __init__(self, name):
        self.name = name
        if name not in self.semaphores:
            self.semaphores[name] = Semaphore()

    def __call__(self, func):
        @wraps(func)
        def semaphore_wrapper(*args, **kwargs):
            sema = self.semaphores[self.name]
            sema.acquire()

            try:
                func(*args, **kwargs)

            finally:
                sema.release()

        return semaphore_wrapper


def get_carrot_status():
    carrot = carrot_service.get_status()

    if carrot:
        carrot = carrot.to_dict()

    socketio.emit('carrot status', carrot)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path, cache_timeout=-1)


@socketio.on('carrot metadata')
def handle_metadata():
    result = backend_service.metadata()

    socketio.emit('carrot metadata', result)


@socketio.on('carrot search')
def handle_search(event):
    def do_search(event):
        result = carrot_service.search(Namespace(**event))
        socketio.emit('carrot search', [r.to_dict() for r in result])

    socketio.start_background_task(target=do_search, event=event)


@socketio.on('carrot init')
def handle_init(event):
    carrot_service.initialize(event)

    socketio.start_background_task(target=get_carrot_status)


@socketio.on('carrot install')
@RequestQueue('install')
def handle_install(event):
    carrot_service.install(Namespace(**event, channel=None))

    socketio.start_background_task(target=get_carrot_status)


@socketio.on('carrot status')
def handle_carrot_status():
    socketio.start_background_task(target=get_carrot_status)


@socketio.on('carrot enable')
def handle_carrot_enable(event):
    carrot_service.enable(Namespace(**event))


@socketio.on('carrot disable')
def handle_carrot_enable(event):
    carrot_service.disable(Namespace(**event))


def run_socket_app(args):
    socketio.run(app, host=args.host, port= args.port)
