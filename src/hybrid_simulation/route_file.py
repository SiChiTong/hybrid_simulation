#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function
from rospy import has_param, get_param
import random


def generate_route_file(route_file_path, max_steps, p_we, p_ew, p_ns):
    """
    Generates and stores the route file. (.rou.xml)

    :route_file_path: Absolute path to the file
    :max_steps: Maximum number of steps
    :p_we: Probability of having a car in the we init point
    :p_ew: Probability of having a car in the ew init point
    :p_ns: Probability of having a car in the ns init point
    """

    random.seed(42)  # make tests reproducible

    with open(route_file_path, "w") as routes:

        print("""<routes>
        
        <vType accel="2.0" decel="6.0" id="Car1" length="5.0" minGap="2.5" maxSpeed="10.0" sigma="0.9"
        lcStrategic="0.0" lcSpeedGain="0.9" lcKeepRight="100.01" />
        <vType accel="2.0" decel="6.0" id="ego-vehicle" length="4.1" minGap="2.0" maxSpeed="10.0" sigma="0.9"
        lcStrategic="0.0" lcSpeedGain="0.9" lcKeepRight="100.01"/>
        <route id="route01" edges="D8 L8 L9 L11 L1 D1"/>
        <route id="route02" edges="D6 L6 L17 L11 L1 D1"/>
        <route id="routeZoe" edges="D10 D6 L6 L17 L11 L1 D1"/>
        <route id="route03" edges="N1 N2"/> """, file=routes)
        veh_nr = 0
        for i in range(max_steps):
            if random.uniform(0, 1) < p_we:
                print('    <vehicle id="right_%i" type="Car1" route="route01" depart="%i" />'
                      % (veh_nr, i), file=routes)
                veh_nr += 1
            if random.uniform(0, 1) < p_ew:
                print('    <vehicle id="left_%i" type="Car1" route="route02" depart="%i" />'
                      % (veh_nr, i), file=routes)
                veh_nr += 1
            if random.uniform(0, 1) < p_ns:
                print('    <vehicle id="down_%i" type="Car1" route="route03" depart="%i" />'
                      % (veh_nr, i), file=routes)
                veh_nr += 1

            # Add broken vehicle after 30? steps

            if i in [10, 17, 24, 31]:
                print('    <vehicle id="broken_%i" type="Car1" route="route0%i" depart="%i"/>'
                      % (veh_nr, (i % 2)+1, i), file=routes)
                veh_nr += 1

            # if i == 45:
            if has_param("/ego_vehicle_name"):
                ego_vehicle_id = get_param("/ego_vehicle_name")
            else:
                ego_vehicle_id = "prius"

            if i == 5:
                    print('    <vehicle id="%s" type="ego-vehicle" route="routeZoe" depart="%i" color="1,1,1"/>'
                          % (ego_vehicle_id, i), file=routes)
                    veh_nr += 1

        print("</routes>", file=routes)