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
import time
from dumb_agent import DumbTank
from bzrc import *

class Agent(object):
    """Class handles all command and control logic for a teams tanks."""

    def __init__(self, bzrc, number_of_agents):
        self.bzrc = bzrc
        self.constants = self.bzrc.get_constants()
        self.bzrc.sendline('mytanks')
        self.bzrc.read_ack()
        mytanks = self.bzrc.read_mytanks()
        self.mytanks = []
        self.number_of_agents = number_of_agents
        for tank in mytanks:
            self.mytanks.append(DumbTank(self.bzrc, tank))

    def tick(self, time_diff):
        """Some time has passed; decide what to do next."""
        for r in range(self.number_of_agents):
            self.mytanks[r].tick(time_diff)


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

    agent = Agent(bzrc, 2)

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
