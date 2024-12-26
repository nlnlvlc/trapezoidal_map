from Pt import Pt
import shapely
from shapely.geometry import LineString, Point

class Segment:
    def __init__(self,leftp: Pt, rightp: Pt):
        self.leftp = leftp
        self.rightp = rightp

    def intersects(self, segment):
        '''
        Finds an intersection between two segments
        :param segment1: two endpoints (x, y) representing a line segment
        :param segment2: two endpoints (x, y) representing a line segment
        :return: if an intersecting point is found, returns the x, y pair. otherwise, returns False
        '''

        leftp = (self.leftp.x, self.leftp.y)
        rightp = (self.rightp.x, self.rightp.y)

        leftp2 = (segment.leftp.x, segment.leftp.y)
        rightp2 = (segment.rightp.x, segment.rightp.y)

        line1 = LineString([leftp, rightp])
        line2 = LineString([leftp2, rightp2])

        int_pt = line1.intersection(line2)
        if int_pt:
            point_of_intersection = Pt(int_pt.x, int_pt.y)

            return point_of_intersection
        else:
            return False

    def getSlope(self):
        return (self.rightp.y - self.leftp.y)/(self.rightp.x - self.leftp.x)

    def __repr__(self):
        return f"Segment({self.leftp}, {self.rightp})"