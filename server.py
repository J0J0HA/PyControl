import time

import flask
import main
import json
from flask import Response, render_template

server = flask.Flask(__name__)
tdata = main.Data()


@server.route("/")
def index():
    global tdata
    return render_template("index.html")


@server.route("/exec/<string:command>")
def execc(command):
    return eval(command)


@server.route("/.get/<path:path>/")
def get(path):
    d = tdata
    for i in path.split("/"):
        try:
            d = d.config(int(i))
        except ValueError:
            d = d.config(str(i))
    return json.JSONEncoder().encode(d.toDict())


@server.route("/.get/")
def getfull():
    return json.JSONEncoder().encode(tdata.toDict())


@server.route("/.states/")
def getstate():
    result = {"actors": {}, "sensors": {}}
    actors = tdata.config("actors")
    sensors = tdata.config("sensors")
    for actor in actors.toDict():
        result["actors"].update({actors.config(actor).name: actors.config(actor).get_f()})
    for sensor in sensors.toDict():
        result["sensors"].update({sensors.config(sensor).name: sensors.config(sensor).get_f()})
    return json.JSONEncoder().encode(result)


@server.route("/_file/<path:path>.html")
def file(path):
    return render_template(path+".html")


@server.route("/.saves/")
def saves():
    global tfile
    return tfile.toDict()


@server.route("/.from/<path:path>/.set/<string:key>/.to/<string:value>/")
def update(path, key, value):
    global tfile
    exc = "tfile"
    for i in path.split("/"):
        exc += ".config('"+i+"', tc='correct-type')"
    exc += ".config('"+key+"', '"+value+"')"
    exec(exc)
    tfile.save()
    return "done"


@server.route("/.backup/")
def backup():
    tfile.save(file="backups/backup-"+(str(time.time()).split(".")[0])+"_(saves.dbin).backup")
    tfile.config("file", "saves.dbin")
    return "Backup done"

@server.route("/.movefrom/<string:fid>/.to/<string:tid>/")
def trans(fid, tid):
    global tfile
    #ntfile = main.Data(rules=main.Data(), file=tfile.config("file"))
    try:
        tfile.config('rules')._args[int(tid)] = tfile.config('rules')._args[int(fid)]
        del tfile.config('rules')._args[int(fid)]
    except:
        tfile.config('rules')._args[int(tid)] = tfile.config('rules')._args[str(fid)]
        del tfile.config('rules')._args[str(fid)]
    tfile.save()
    #tfile = ntfile
    time.sleep(2)
    return "done"


@server.route("/.addrule/<int:id>/")
def add(id):
    global tfile
    tfile.config("rules").config(id, main.Rule(sensor='null', operator='null', sensor_value='0', actor='null',actor_value='0'))
    tfile.save()
    return "added"


@server.route("/.subrule/<int:id>/")
def sub(id):
    global tfile
    del tfile.config("rules")._args[id]
    tfile.save()
    return "removed"


@server.route("/<path:path>")
def err404(path):
    return Response(render_template("404.html", path=path), 404)


def run(host, port, data, file, treading=None):
    global tdata, tfile
    tdata = data
    tfile = main.Data().load(file=file)
    if treading:
        import multiprocessing
        serverProcess = multiprocessing.Process(target=run, args=(host, port, data, file, None))
        serverProcess.start()
    else:
        server.run(host, port)
