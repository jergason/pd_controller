#!/usr/bin/python -tt
#################################################################
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

    def __init__(self, bzrc, color):
        self.bzrc = bzrc
        self.color = color
        self.constants = self.bzrc.get_constants()
        self.commands = []
        self.bases = self.bzrc.get_bases()
        self.enemy = self.pick_enemy(self.color)
        # How to tell what color I am?


    def pick_enemy(self, own_color):
        colors = ['red', 'blue', 'green', 'purple']
        colors.remove(own_color)
        return colors.[random.randint(0, 2)]

    def tick(self, time_diff):
        """Some time has passed; decide what to do next."""
        mytanks, othertanks, flags, shots = self.bzrc.get_lots_o_stuff()
        self.mytanks = mytanks
        self.flags = flags
        # We only care about our enemy's flag
        enemy_flag = None
        for flag in self.flags:
            if flag.color == self.enemy:
                enemy_flag = flag

        # Flag is the goal, so it creates an attractive field
        # Self.obstacles = self.bzrc.get_obstacles()
        self.commands = []
        field = Field(flag.x, flag.y, 5, 500)

        # Loop through each tank, calculating speed
        for tank in self.mytanks:
            self.bzrc.angvel(tank.index, self.calculate_angvel(tank, field))
            #speed depends on how far away we are?
            #just ignore that for now, see if it works.
            self.bzrc.speed(tank.index, self.calculate_speed(tank, field))

    def calculate_angvel(self, tank, fields):
        res = field_calculator.calcuate_field_to_goal({'x': tank.x, 'y': tank.y}, {'x': fields.x, 'y': fields.y}, fields.r, fields.s)
        # Res is a vector. now compare the angle of the vector to our angle.
        target_angle_in_radians = math.atan2(res['x'], res['y'])
        tank_angle = tank.angle
        direction = self.determine_turn_direction(tank_angle, target_angle)
        if direction == "clockwise":
            return 1
        else:
            return -1

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
        execname, host, port, color = sys.argv
    except ValueError:
        execname = sys.argv[0]
        print >>sys.stderr, '%s: incorrect number of arguments' % execname
        print >>sys.stderr, 'usage: %s hostname port' % sys.argv[0]
        sys.exit(-1)

    # Connect.
    #bzrc = BZRC(host, int(port), debug=True)
    bzrc = BZRC(host, int(port))

    agent = Agent(bzrc, color)

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
