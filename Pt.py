class Pt:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def inTrap(self, trapezoid):
        top = trapezoid.top
        bot = trapezoid.bottom
        leftp = trapezoid.leftp
        rightp = trapezoid.rightp

        if (self < leftp or self > rightp) or (self.isAbove(top) or self.isBelow(bot)):
            return False
        else:
            return True

    def isAbove(self, segment):

        slope = segment.getSlope()
        x1 = self.x
        y1 = self.y
        x = segment.leftp.x
        y = segment.leftp.y

        # find y intercept of segment
        # y = mx + b
        # b (y intercept) = -(mx-y) = -mx + y
        b = -(slope * x) + y

        # find y value for if x were on line
        y_exp = slope * x1 + b

        # if y is greater than the expected y, return True
        if y1 > y_exp:
            return True

    def isBelow(self, segment):

        slope = segment.getSlope()
        x1 = self.x
        y1 = self.y
        x = segment.leftp.x
        y = segment.leftp.y

        # find y intercept of segment
        # y = mx + b
        # b (y intercept) = -(mx-y) = -mx + y
        b = -(slope * x) + y

        # find y value for if x were on line
        y_exp = slope * x1 + b

        # if y is less than the expected y, return True
        if y1 < y_exp:
            return True

    def isLeftOf(self, segment):
        if self.x < segment.leftp.x:
            return True

    def isRightOf(self, segment):
        if self.x > segment.rightp.x:
            return True

    def isBetween(self, segment):
        if self.x > segment.leftp.x and self.x < segment.rightp.x:
            return True

    def __lt__(self, segment):
        return self.x < segment.x

    def __gt__(self, segment):
        return self.x > segment.x

    def __le__(self, segment):
        return self.x <= segment.x

    def __ge__(self, segment):

        return self.x >= segment.x


    def __repr__(self):
        return f"Point ({self.x}, {self.y})"
