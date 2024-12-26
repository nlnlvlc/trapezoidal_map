from shapely.measurement import bounds

from Trapezoid import Trapezoid
from Pt import Pt
from Segment import Segment
class BNode:

    def __init__(self, val=None, bounds=None):
        self.value = val
        if self.value:
            self.left = BNode()
            self.right = BNode()
        else:
            self.left = None
            self.right = None
        self.bound = bounds

    def isempty(self):
        return (self.value == None)

    def insert(self, data):
        if isinstance(data, Segment):
            self.addSegment(data)

        if isinstance(data, Pt):
            self.addPoint(data)

    def addPoint(self, data):
        # if both new data and self data are points
        if isinstance(self.value, Pt):

            if data < self.value:
                self.left.addPoint(data)
                return
            elif data >= self.value:

                self.right.addPoint(data)
                return
            elif data == self.value:

                return
            else:
                self.value = data

        if isinstance(self.value, Segment):

            if data == self.value.rightp:
                self.left = self.value
                self.value = data
            elif data.isAbove(self.value):
                self.left.insert(data)
                return
            else:
                self.right.insert(data)
                return
        if isinstance(self.value, Trapezoid):
            if data.inTrap(self.value):
                top = self.value.top
                bottom = self.value.bottom
                leftp = self.value.leftp
                rightp = self.value.rightp

                lower = self.bound[0]
                upper = self.bound[1]

                edge = Segment(Pt(data.x, lower.x), Pt(data.x, upper.x))

                # use as new point along edge separating both trapezoids
                inter = bottom.intersects(edge)

                trap1 = Trapezoid(top, bottom, leftp, inter)
                trap2 = Trapezoid(top, bottom, inter, rightp)

                self.value = data
                self.left = BNode(trap1, self.bound)
                self.right = BNode(trap2, self.bound)

    def addSegment(self, data: Segment):

        if not self.find(data.leftp):
            self.addPoint(data.leftp)
        if not self.find(data.rightp):
            self.addPoint(data.rightp)

        if isinstance(self.value, Pt):
            leftp = data.leftp
            rightp = data.rightp

            startNode = self.find(leftp)
            endNode = self.find(rightp)

            right = startNode.right

            left = endNode.left

            if isinstance(right, Trapezoid):
                right.horizontalDivide(data, "right")
            if isinstance(left, Trapezoid):
                left.horizontalDivide(data, "left")

    def horizontalDivide(self, seg: Segment, position=None):
        '''
        Divides a trapezoid with a segment passing thru it into a top and bottom trapezoid
        :param seg: segment passing through trapezoid
        :param position: Used to keep orientation for degenerating sides
        :return: 
        '''
        top = self.value.top
        bottom = self.value.bottom
        leftp = self.value.leftp
        rightp = self.value.rightp

        lower = self.bound[0]
        upper = self.bound[1]

        #left and right edges of trapezoid
        l_edge = Segment(Pt(leftp.x, lower.x), Pt(leftp.x, upper.x))
        r_edge = Segment(Pt(rightp.x, lower.x), Pt(rightp.x, upper.x))

        # use as new point along edge separating both trapezoids
        l_inter = seg.intersects(l_edge)
        r_inter = seg.intersects(r_edge)

        if l_inter == r_inter:
            if position == "left":
                self.left = BNode(self.value, self.bound)
            else:
                self.right = BNode(self.value, self.bound)

        else:
            trap1 = Trapezoid(top, seg, l_inter, r_inter)
            trap2 = Trapezoid(seg, bottom, l_inter, r_inter)

            self.left = BNode(trap1, self.bound)
            self.right = BNode(trap2, self.bound)

        self.value = seg

    def isleaf(self):
        if self.left.left == None and self.right.right == None:
            return True

    def find(self, value):
        '''
        Finds a point in the map
        :param value:
        :return:
        '''
        if self.isempty():
            return False
        if self.value == value:
            return self
        if isinstance(value, Pt):
            if isinstance(self.value, Pt):
                if value < self.value:
                    return self.left.find(value)
                else:
                    return self.right.find(value)
            if isinstance(self.value, Segment):
                if value.isAbove(self.value) or value.isLeftOf(self.value):
                    return self.left.find(value)
                else:
                    return self.right.find(value)

    def recordPath(self, value: Pt, path = []):
        if self.isempty():
            return False
        if isinstance(self.value, Trapezoid) and value.inTrap(self.value):
            path.append(self.value)
            return path
        if isinstance(self.value, Pt):
            if value < self.value:
                path.append(self.value)
                return self.left.recordPath(value, path)
            else:
                path.append(self.value)
                return self.right.recordPath(value, path)
        if isinstance(self.value, Segment):
            if value.isAbove(self.value) or value.isLeftOf(self.value):
                path.append(self.value)
                return self.left.recordPath(value, path)
            else:
                path.append(self.value)
                return self.right.recordPath(value, path)

    def preorder(self):
        if self.isempty():
            return []
        else:
            return [self] + self.left.preorder() +  self.right.preorder()

    def inorder(self):
        # Perform inorder traversal
        if self.isempty():
            return []
        else:
            return self.left.inorder() + [self.value] + self.right.inorder()

    def __repr__(self):
        return (f"Value: {"None" if self.value is None else self.value},\n "
                f"left: {"None" if self.left is None else self.left},\n "
                f"right: {"None" if self.right is None else self.right}\n")
