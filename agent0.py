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
import field_calculator
from field import Field
from bzrc import *

class Agent(object):
    """Class handles all command and control logic for a teams tanks."""

    def __init__(self, bzrc, color):
        self.bzrc = bzrc
        self.color = color
        self.constants = self.bzrc.get_constants()
        self.commands = []
        self.base = self.get_own_base(self.color, self.bzrc.get_bases())
        self.enemy = self.pick_enemy(self.color)
        print("enemy is %s" % self.enemy)
        # How to tell what color I am?

    def get_own_base(self, own_color, bases):
        for base in bases:
            if base.color == own_color:
                return base

    def pick_enemy(self, own_color):
        colors = ['red', 'blue', 'green', 'purple']
        colors.remove(own_color)
        return colors[random.randint(0, 2)]

    def tick(self, time_diff):
        """Some time has passed; decide what to do next."""
        mytanks, othertanks, flags, shots = self.bzrc.get_lots_o_stuff()
        self.mytanks = mytanks
        self.flags = flags
        # We only care about our enemy's flag
        enemy_flag = None
        for flag in self.flags:
            # print("flag color: %s x: %f y: %f" % (flag.color, flag.x, flag.y))
            if flag.color == self.enemy:
                # print("enemy found, and it is %s" % flag.color)
                enemy_flag = flag

        # Flag is the goal, so it creates an attractive field
        obstacles = self.bzrc.get_obstacles()
        fields = self.repulsive_and_tangential_fields_from_obstacles(obstacles)
        attractive_field = Field(enemy_flag.x, enemy_flag.y, 5, 300)
        attractive_field.kind = 'attractive'

        for tank in self.mytanks:
            print("tank angle is %f x is %f y is %f" % (tank.angle, tank.x, tank.y))
            #if this tank has the flag, then its attractive field is the home base
            if tank.flag == self.enemy:
                attractive_field = Field((self.base.corner1_x + self.base.corner3_x) / 2.0, (self.base.corner1_y + self.base.corner3_y) / 2.0, 5, 300)
                attractive_field.kind = 'attractive'
            fields.append(attractive_field)
            self.bzrc.angvel(tank.index, self.calculate_angvel(tank, fields))
            #speed depends on how far away we are?
            #just ignore that for now, see if it works.
            self.bzrc.speed(tank.index, self.calculate_speed(tank, fields))
            self.bzrc.shoot(tank.index)

    def calculate_centroid(self, obstacle):
        x = 0.0
        y = 0.0
        for point in obstacle:
            x += point[0]
            y += point[1]
        return { 'x': x / float(len(obstacle)), 'y': y / float(len(obstacle)) }

    def calculate_radius_from_centroid(self, centroid, obstacle):
        return math.sqrt((centroid['x'] - obstacle[0][0]) ** 2 + (centroid['y'] - obstacle[0][1]) ** 2)


    def repulsive_and_tangential_fields_from_obstacles(self, obstacles):
        fields = []
        for obstacle in obstacles:
            centroid = self.calculate_centroid(obstacle)
            radius = self.calculate_radius_from_centroid(centroid, obstacle)
            field = Field(centroid['x'], centroid['y'], radius, 100)
            field.kind = 'repulsive'
            fields.append(field)
            tan_field = Field(centroid['x'], centroid['y'], radius, 100)
            tan_field.kind = 'tangential'
            fields.append(tan_field)
        return fields


    def calculate_speed(self, tank, fields):
        return 1.0

    def calculate_angvel(self, tank, fields):
        x = 0.0
        y = 0.0
        for field in fields:
            res = field_calculator.calculate_field_to_goal({'x': tank.x, 'y': tank.y}, {'x': field.x, 'y': field.y}, field.r, field.s)
            dx = tank.x-res['x'];
            dy = tank.y-res['y'];
            tanRadius = 100;
            repRadius = 100;

            dist = math.sqrt(dx*dx + dy*dy);
            if field.kind == 'attractive':
                x += res['x']
                y += res['y']
            elif field.kind == 'repulsive':
                if repRadius <= dist:
                    x -= res['x']
                    y -= res['y']
            elif field.kind == 'tangential':
                if tanRadius <= dist:
                    x -= res['y']
                    y += res['x']

        target_angle = math.atan2(y, x)

        # res = field_calculator.calculate_field_to_goal({'x': tank.x, 'y': tank.y}, {'x': fields.x, 'y': fields.y}, fields.r, fields.s)
        # print("res is x: %f, y: %f" % (res['x'], res['y']))
        # Res is a vector. now compare the angle of the vector to our angle.
        # target_angle = math.atan2(res['y'], res['x'])
        print("target angle is %f, my angle is %f" % (target_angle, tank.angle))
        tank_angle = tank.angle
        direction = field_calculator.determine_turn_direction(tank_angle, target_angle)
        if direction == "clockwise":
            return 0.4
        else:
            return -0.4

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
