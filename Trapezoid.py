class Trapezoid:
    def __init__(self, top, bottom, leftp, rightp):
        self.top = top
        self.bottom = bottom
        self.leftp = leftp
        self.rightp = rightp


    def __repr__(self):
        return (f"\nTrapezoid( Top Segment: {self.top}, Bottom Segment : {self.bottom},"
                f"Left Point: {self.leftp}, Right Point: {self.rightp})\n")