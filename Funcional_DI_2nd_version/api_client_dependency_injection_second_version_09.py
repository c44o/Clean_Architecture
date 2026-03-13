from cleaner_api_dependency_injection_second_version_09 import api

api('move 100')
api('turn -90')
api('set soap')
api('start')
api('move 50')
s = api('stop')

print(s.x, s.y, s.angle, s.state)
