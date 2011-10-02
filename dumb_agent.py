class DumbTank(object):

    def __init__(self, bzrc, tank):
        self.tank = tank
        self.bzrc = bzrc
        self.constants = self.bzrc.get_constants()
        self.shoot_time_limit = random.uniform(1.5, 2.0)
        self.state = "not turning"
        self.last_shot_time = 0.0
        self.move_time_limit = 4.0
        self.last_turn_time = time.time() + self.move_time_limit
        self.time_to_turn_60_degrees = 1.5

    def tick(self, time_diff):
        """Some time has passed; decide what to do next."""


        current_time = time.time()
        self.bzrc.speed(self.tank.index, 1.0)
        # Check if we need to shoot
        if current_time > self.last_shot_time + self.shoot_time_limit:
            print("shooting")
            self.bzrc.shoot(self.tank.index)
            self.last_shot_time = time.time()
            self.shoot_time_limit = random.uniform(1.5, 2.0)

        # If we need to start turning
        if current_time > self.last_turn_time + self.time_to_turn_60_degrees + self.move_time_limit and self.state != "turning":
            self.last_turn_time = current_time
            print("turning")
            self.bzrc.angvel(self.tank.index, 1.0)
            self.state = "turning"
        elif self.state == "turning":
            # If we need to stop turning
            if current_time > self.last_turn_time + self.time_to_turn_60_degrees:
                self.bzrc.angvel(self.tank.index, 0.0)
                print("not turning")
                self.state = "not_turning"
