import pickle
import functools


def void(*args, **kwargs):
    pass


def getfunction(arg):
    if type(arg) == type(""):
        return functools.partial(exec, arg)
    if type(arg) == type(void):
        return functools.partial(arg)


class _MainClass:
    def _init_(self, kwargs):
        self._args = kwargs

    def config(self, *args, **kwargs):
        try:
            intit = kwargs["tc"]
            if intit == 'correct-type':
                intit = True
        except KeyError:
            intit = False
        try:
            v1 = args[0]
        except IndexError:
            try:
                v1 = kwargs["key"]
            except KeyError:
                v1 = None
        try:
            v2 = args[1]
        except IndexError:
            try:
                v2 = kwargs["value"]
            except KeyError:
                v2 = None
        if v2 is None:
            if intit is True:
                try:
                    return self._args[int(v1)]
                except:
                    return self._args[str(v1)]
            else:
                return self._args[v1]
        else:
            self._args[v1] = v2
            return self.config(v1)

    def toDict(self):
        rd = {}
        for i in self._args:
            if type(self._args[i]) is type(void):
                continue
            try:
                rd.update({i: self._args[i].toDict()})
            except:
                rd.update({i: self._args[i]})
        return rd


class Data(_MainClass):
    def __init__(self, *args, **kwargs):
        c = -1
        for arg in args:
            c += 1
            kwargs[c] = arg
        self._init_(kwargs)
        try:
            if not self._args["nal"]:
                self.load(file=self._args["file"])
        except KeyError:
            pass

    def load(self, **kwargs):
        args = self._args
        for arg in kwargs:
            args[arg] = kwargs[arg]
        with open(args["file"], "rb") as file:
            p = pickle.load(file)
            td = Data()
            td._args = p
            return td

    def save(self, **kwargs):
        args = self._args
        for arg in kwargs:
            args[arg] = kwargs[arg]
        with open(args["file"], "wb") as file:
            pickle.dump(self._args, file)

    def toList(self):
        rl = []
        for i in self._args:
            rl.append(self._args[i])
        return rl


class Unit(_MainClass):
    def __init__(self, **kwargs):
        self._init_(kwargs)
        self.str = self._args["str"]


class Server(_MainClass):
    def __init__(self, **kwargs):
        self._init_(kwargs)
        self._server = server

    def run(self, **kwargs):
        args = self._args
        for arg in kwargs:
            args[arg] = kwargs[arg]
        try:
            args["thread"]
        except KeyError:
            args["thread"] = False
        self._server.run(args["host"], args["port"], args["data"], args["file"], args["thread"])


class Sensor(_MainClass):
    def __init__(self, **kwargs):
        self._init_(kwargs)
        self.name = self._args["name"]
        self.unit = self._args["unit"]
        self.get_f = self._args["get_f"]
        if not isinstance(self.unit, Unit):
            self.unit = Unit(str=self.unit)


class Actor(_MainClass):
    def __init__(self, **kwargs):
        self._init_(kwargs)
        self.name = self._args["name"]
        self.unit = self._args["unit"]
        self.get_f = self._args["get_f"]
        self.do_f = self._args["do_f"]
        if not isinstance(self.unit, Unit):
            self.unit = Unit(str=self.unit)


class Rule(_MainClass):
    def __init__(self, **kwargs):
        self._init_(kwargs)
        self.sensor = self._args["sensor"]
        self.operator = self._args["operator"]
        self.sensor_value = self._args["sensor_value"]
        self.actor = self._args["actor"]
        self.actor_value = self._args["actor_value"]

import server