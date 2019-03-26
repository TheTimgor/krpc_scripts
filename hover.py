import krpc
from time import sleep
import numpy

conn = krpc.connect()
earth = conn.space_center.bodies['Earth']
vessel = conn.space_center.active_vessel
srf_frame = earth.reference_frame
starting_pos = (vessel.flight().latitude,vessel.flight().longitude)
vessel.auto_pilot.target_pitch_and_heading(85, 90)
vessel.auto_pilot.engage()
vessel.control.throttle = 1
vessel.control.rcs = True
vessel.control.activate_next_stage()
sleep(2)
vessel.control.activate_next_stage()
sleep(10)

while True:
	r = earth.equatorial_radius + vessel.flight().mean_altitude
	f_g = vessel.mass * (earth.gravitational_parameter / r**2)
	m = vessel.mass 
	f_m = vessel.max_thrust
	spd = vessel.flight(reference_frame = srf_frame).vertical_speed
	diff = numpy.subtract(starting_pos, (vessel.flight().latitude,vessel.flight().longitude))	
	comp = spd
	throttle = (f_g / f_m) - comp - .36
	if(throttle < 0):
		throttle = 0
	vessel.control.throttle = throttle + 0.01