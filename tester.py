import


def void():
    return random.choice(range(1, 10))


import main as wb

if __name__ == '__main__':
    actors = wb.Data(wb.Actor(name="Pumpe 2", unit="time/on/off", get_f=void, do_f=void), wb.Actor(name="Pumpe 1", unit="on/off", get_f=void, do_f=void))
    sensors = wb.Data(wb.Sensor(name="Regenmesser", unit="l", get_f=void), wb.Sensor(name="Feuchtigkeitssensor", unit="%", get_f=void))
    data = wb.Data(sensors=sensors, actors=actors)
#    saves = wb.Data(file="saves.dbin")
#    saves._args = {}
#    rule1 = wb.Rule(sensor="Feuchtigkeitssensor 1", operator="sa", sensor_value="25", actor="Pumpe 1", actor_value="20")
#    rule2 = wb.Rule(sensor="Feuchtigkeitssensor 1", operator="la", sensor_value="20", actor="Pumpe 1",actor_value="230")
#    saves.config("rules", wb.Data(rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2, rule2))
#    saves.config("rules", wb.Data())
#    saves.save(file="saves.dbin")
    s = wb.Server(host="localhost", port=80, thread=True, data=data, file="saves.dbin")
    s.run()
