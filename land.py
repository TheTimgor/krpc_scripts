import krpc
from time import sleep
import numpy

conn = krpc.connect()
vessel = conn.space_center.active_vessel
ref = conn.space_center.ReferenceFrame.create_hybrid(
    position=vessel.orbit.body.reference_frame,
    rotation=vessel.surface_reference_frame)


alt = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
spd = conn.add_stream(getattr, vessel.flight(ref), 'speed')
v_spd = conn.add_stream(getattr, vessel.flight(ref), 'vertical_speed')
thr = conn.add_stream(getattr, vessel, 'available_thrust')
mass = conn.add_stream(getattr, vessel, 'mass')
q = conn.add_stream(getattr, vessel.flight(), 'dynamic_pressure')


# vessel.control.throttle = 1.0

print(v_spd())

while True:
	if q() > 7000:
		break

print('entry burn')
conn.space_center.physics_warp_factor = 0
vessel.control.sas = True
vessel.control.sas_mode = vessel.control.sas_mode.retrograde
vessel.control.throttle = 0.01


while True:
	if spd() < 300:
		break

while True:
	acc = thr()/mass() - 9.806
	time = spd() / acc
	dist = spd() + 0.5 * acc * (time**2)
	# print(dist)
	if alt() < 1000:
		vessel.control.gear = True
	if alt() < dist:	
		break

print('landing burn')
conn.space_center.physics_warp_factor = 0
vessel.control.sas_mode = vessel.control.sas_mode.retrograde
while True:
	vessel.control.throttle = 1
	if alt() < 1000:
		vessel.control.gear = True
	if v_spd() > -80:
		print(v_spd())
		break
while True:
	acc = (spd()**2) / (2*(alt()))
	thr_r = (acc+9.8) * mass()
	vessel.control.throttle = thr_r/thr() - .36
	if alt() < 1000:
		vessel.control.gear = True
	if v_spd() > -5:
		print(v_spd())
		break
print('landing burn end')


vessel.control.throttle = 0