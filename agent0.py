#!/usr/bin/python -tt

# An incredibly simple agent.  All we do is find the closest enemy tank, drive
# towards it, and shoot.  Note that if friendly fire is allowed, you will very
# often kill your own tanks with this code.

#################################################################
# NOTE TO STUDENTS
# This is a starting point for you.  You will need to greatly
# modify this code if you want to do anything useful.  But this
# should help you to know how to interact with BZRC in order to
# get the information you need.
#
# After starting the bzrflag server, this is one way to start
# this code:
# python agent0.py [hostname] [port]
#
# Often this translates to something like the following (with the
# port name being printed out by the bzrflag server):
# python agent0.py localhost 49857
#################################################################

import sys
import math
import time
import random

from bzrc import *

class Agent(object):
    """Class handles all command and control logic for a teams tanks."""

    def __init__(self, bzrc):
        self.bzrc = bzrc
        self.constants = self.bzrc.get_constants()
        self.commands = []
        self.shoot_time_limit = random.uniform(1.5, 2.0)
        self.state = "not turning"
        self.last_shot_time = 0.0
        self.move_time_limit = 4.0
        self.last_turn_time = time.time() + self.move_time_limit
        self.time_to_turn_60_degrees = 1.5

    def tick(self, time_diff):
        """Some time has passed; decide what to do next."""
        #loop through each tank
        #calculate field to goal
        #move tank towards goal
        mytanks, othertanks, flags, shots = self.bzrc.get_lots_o_stuff()
        #create tank objects
        #calculate environment
        #pass to react to get commands back from tanks
        #then do commands
        self.mytanks = mytanks
        self.flags = flags

        self.commands = []

        current_time = time.time()
        # self.commands.append(SpeedCommand(self.mytanks[0].index, 1.0))
        self.bzrc.speed(self.mytanks[0].index, 1.0)
        # Check if we need to shoot
        if current_time > self.last_shot_time + self.shoot_time_limit:
            # self.commands.append(ShootCommand(self.mytanks[0].index))
            print("shooting")
            self.bzrc.shoot(self.mytanks[0].index)
            self.last_shot_time = time.time()
            self.shoot_time_limit = random.uniform(1.5, 2.0)

        # If we need to start turning
        if current_time > self.last_turn_time + self.time_to_turn_60_degrees + self.move_time_limit and self.state != "turning":
            self.last_turn_time = current_time
            # self.commands.append(AngvelCommand(self.mytanks[0].index, 1))
            print("turning")
            self.bzrc.angvel(self.mytanks[0].index, 1.0)
            self.state = "turning"
        elif self.state == "turning":
            # If we need to stop turning
            if current_time > self.last_turn_time + self.time_to_turn_60_degrees:
                self.bzrc.angvel(self.mytanks[0].index, 0.0)
                print("not turning")
                # self.commands.append(AngvelCommand(self.mytanks[0].index, 0))
                self.state = "not_turning"



        # for tank in mytanks:
        #     self.attack_enemies(tank)

        # results = self.bzrc.do_commands(self.commands)

    def attack_enemies(self, tank):
        """Find the closest enemy and chase it, shooting as you go."""
        best_enemy = None
        best_dist = 2 * float(self.constants['worldsize'])
        for enemy in self.enemies:
            if enemy.status != 'alive':
                continue
            dist = math.sqrt((enemy.x - tank.x)**2 + (enemy.y - tank.y)**2)
            if dist < best_dist:
                best_dist = dist
                best_enemy = enemy
        if best_enemy is None:
            command = Command(tank.index, 0, 0, False)
            self.commands.append(command)
        else:
            self.move_to_position(tank, best_enemy.x, best_enemy.y)

    def move_to_position(self, tank, target_x, target_y):
        """Set command to move to given coordinates."""
        target_angle = math.atan2(target_y - tank.y,
                                  target_x - tank.x)
        relative_angle = self.normalize_angle(target_angle - tank.angle)
        command = Command(tank.index, 1, 2 * relative_angle, True)
        self.commands.append(command)

    def normalize_angle(self, angle):
        """Make any angle be between +/- pi."""

        angle -= 2 * math.pi * int (angle / (2 * math.pi))
        if angle <= -math.pi:
            angle += 2 * math.pi
        elif angle > math.pi:
            angle -= 2 * math.pi
        return angle


def main():
    # Process CLI arguments.
    try:
        execname, host, port = sys.argv
    except ValueError:
        execname = sys.argv[0]
        print >>sys.stderr, '%s: incorrect number of arguments' % execname
        print >>sys.stderr, 'usage: %s hostname port' % sys.argv[0]
        sys.exit(-1)

    # Connect.
    #bzrc = BZRC(host, int(port), debug=True)
    bzrc = BZRC(host, int(port))

    agent = Agent(bzrc)

    prev_time = time.time()

    # Run the agent
    try:
        while True:
            time_diff = time.time() - prev_time
            agent.tick(time_diff)
    except KeyboardInterrupt:
        print "Exiting due to keyboard interrupt."
        bzrc.close()


if __name__ == '__main__':
    main()

# vim: et sw=4 sts=4
