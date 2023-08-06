import argparse
import bottle
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
import time


class AuthExtension:
    """
    Contains a session info that is sweeped periodically
    Should be configurable externally
    Should add login callback to the server
    TODO: fill login and logout callback
    TODO: create default creds holder
    TODO: create constructor parameters

    TODO: use cherryPy server: https://github.com/tiagohillebrandt/bottle-ssl/blob/master/server.py
        to do HTTPS on this port
    """
    def __init__(self, server):
        self.server = server
        self.secret_holder = ...
        self.sessions = {}
        self.session_validity_period = 7200
        self.period = 60
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self.harvest)
        self.thread.daemon = True
        self.thread.start()
        self.server.internal_endpoints.append({
            "about": "Pass user and pwd to receive token to built-in Auth engine", 
            "route": "auth_login",
            "callback": self.login
        })
        self.server.internal_endpoints.append({
            "about": "Pass token to terminate session in the built-in Auth engine",
            "route": "auth_logout",
            "callback": self.logout
        })

    def login(self, epoint, page, data):
        pass

    def logout(self, epoint, page, data):
        pass

    def __call__(self, callback):
        def wrapped(epoint, page, data):
            token = data.get('token')
            if token is None:
                bottle.abort(401, "Authentication token not present")
            with self.lock:
                if token not in self.sessions.keys():
                    bottle.abort(403, "Your token either expired or is invalid; either way resource is unaccessible")
                data["user"] = self.sessions[token]["user"]
            del data["token"]
            callback(epoint, page, data)
        return wrapped

    def harvest(self):
        while True:
            time.sleep(self.period)
            with self.lock:
                now = time.time()
                self.sessions = {k: v for k, v in self.sessions.items() if v["expiration"] < now}            


class DropInServer:
    """
    Minimalistic server that given config will call proper subprocesses and get their input
    Should reload config dynamically whenever it is changed if file is given
    Should be installable and runnable via cli method

    TODO: autoparams (not handcrafted)
    """

    _default_cfg_path = os.path.join(os.path.expanduser("~"), ".local", ".syntax.dropin.json")
    _parser = argparse.ArgumentParser()
    _parser.add_argument("--run", nargs="?", default=True, help="Run the DropIn server with default or specified config")
    _parser.add_argument("--make_config", action="store_true", help="Build default config in your home")

    def __init__(self, config_path=None, config=None):
        if config:
            self.config = config
        else:
            if config_path is None:
                config_path = DropInServer._default_cfg_path
            with open(config_path, "r") as f:
                self.config = json.load(f)
        self.internal_endpoints = []  # used to ...
        self.extensions = {}
        if self.config.get("extensions"):
            for k, v in self.config.items():
                self.install_import_extension(k, v)
        self.endpoints = self.config["endpoints"]
        if not self.endpoints:
            raise RuntimeError("No endpoints - terminating")
        self.app = bottle.Bottle(__name__)

        @bottle.get('/')
        def all_methods():
            bottle.response.content_type="application/json"
            epoints = self.endpoints.copy()
            epoints.update(self.internal_endpoints)
            return json.dumps(epoints)

        @bottle.route('/<page>', method=["GET", "POST"])
        def index(page):
            paths = []
            for epoint in self.endpoints:
                if page.startswith(epoint["route"]):
                    break
            else:
                for epoint in self.internal_endpoints:
                    if page.startswith(epoint["route"]):
                        break
                else:
                    bottle.response.content_type = "text/plain; charset=utf-8"
                    bottle.abort(404, "No such method")
            if bottle.request.method == 'POST':
                if bottle.request.content_type.lower().startswith('application/json'):
                    data = bottle.request.json
                else:
                    data = bottle.request.form
                for fobj in bottle.request.files:
                    if fobj.filename:
                        path = tempfile.mkstemp()[1]
                        fobj.save(path)
            else:
                data = {}
            try:
                if epoint.get("executable") is not None:
                    this_call = self.call
                else:
                    this_call = epoint["callback"]
                if epoint.get("extensions"):
                    for extension in epoint["extensions"]:
                        this_call = self.extensions[extension](this_call)
                return this_call(epoint, page, data)
            finally:
                for path in paths:
                    os.remove(path)

        bottle.run(host=self.config["address"], port=self.config["port"])

    def call(self, epoint, page, data):
        call = []
        for bit in epoint["params"]:
            params = set(re.findall("\\$([A-Za-z]+|\\{w+?\\})", bit))
            if params:
                if all([x in data for x in params]):
                    for param in params:
                        bit = bit.replace("$" + param. data[param])
                    call.append(bit)
            else:
                call.append(bit)
        p = subprocess.Popen([epoint["executable"]] + call, stdout=subprocess.PIPE)
        response, error = p.communicate()
        if p.returncode != 0:
            bottle.response.content_type = "text/plain; charset=utf-8"
            bottle.abort(500, {'message': error})
        else:
            bottle.response.content_type = "text/plain; charset=utf-8"            
            return response

    def install_import_addon(self, key, path):
        """
        Import addon; if unavailable, get it from path. Paths may be interpreted
        as Python imports or installable snippets.
        """
        if path == "auth":
            self.extensions[key] = AuthExtension(self)
        elif isinstance(path, list) and path[0] == "auth":
            password_manager = path[1]
            password_file = path[2]
            self.extensions[key] = AuthExtension(self, pwd_mgr=password_manager, pwd_file=password_file)
        elif isinstance(path, str) or isinstance(path, list):
            if isinstance(path, list):
                path, args = path[0], path[1:]
            else:
                args = []
            try:
                path = path.split(".")
                path = ".".join(path[:-1]), path[-1]
                module = __import__(path[0])
                self.extensions[key] = module.__dict__[path[1]](self, *args)
            except:
                raise NotImplementedError("Remote import should be doable")
        else:
            raise ValueError("Incorrect path for an import")

    @classmethod
    def cli(cls, *args):
        args = cls._parser.parse_args(args)
        if args.run is not True:  # because default None is produced when it should be run
            if isinstance(args.run, str):
                return DropInServer(config_path=args.run)
            else:
                return DropInServer()
        if args.make_config:
            config = {
                "address": "0.0.0.0",
                "port": 2137,
                "extensions": {},
                "endpoints": [
                    {
                        "about": "Example service that can be served over this DropInServer",
                        "route": "hello",
                        "executable": "echo",
                        "params": ["Hello world!"],
                        "extensions": []
                    }
                ]
            }
            with open(cls._default_cfg_path, "w") as f:
                return json.dump(config, f)
        cls._parser.print_help()


if __name__ == "__main__":
    DropInServer.cli(*sys.argv[1:])
