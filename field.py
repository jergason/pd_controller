class Field(object):
    def __init__(self, x, y, r, s):
        """The field has a location, a radius, and a strength of field."""
        self.x = x
        self.y = y
        self.r = r
        self.s = s

    def __str__(self):
        return "x: %f y: %f r: %f s: %f" % (self.x, self.y, self.r, self.s)
