from shapely.measurement import length

from Pt import Pt
from Trapezoid import Trapezoid
from Segment import Segment
from BNode import BNode

import pandas as pd

class TrapezoidalMap:

    def __init__(self, bounds):
        self.lower = bounds[0]
        self.upper = bounds[1]
        self.top = Segment(Pt(self.lower.x, self.upper.y), self.upper)
        self.bottom = Segment(self.lower, Pt(self.upper.x, self.lower.y))
        self.trapezoids = []
        self.segments = []
        self.bn = BNode(Trapezoid(self.top, self.bottom, self.lower, self.upper), bounds)

    def buildMap(self, segments: list[Segment]):
        '''
        Handles the process of adding points, segments, and trapezoids to trapezoid map
        :param segments: list of Segment objects containing two points
        :return: None
        '''
        self.segments = segments

        #add each segment to map
        for segment in self.segments:

            rightp = segment.rightp
            #insert segment and points
            self.bn.insert(segment)
            #find segment in map
            node = self.bn.find(rightp).left
            #divide the trapezoid the segment passes through
            node.horizontalDivide(segment)
        #save trapezoids to map
        #ordered from left to right, and up and down
        self.trapezoids = [x for x in self.bn.inorder() if isinstance(x, Trapezoid)]
        #build agaceny matrix and save it to output file
        self.getMatrix()

    def getMatrix(self):
        '''
        Builds agency matrix
        :return: None
        '''
        #get list of all nodes in map and name them
        trapDict, startDict, endDict, segDict = self.indices()

        #merge dicts into one large dictionary
        n = len(trapDict) + len(startDict) + len(endDict) + len(segDict)
        mergedDict = {**startDict, **endDict, **segDict, **trapDict}


        vals_list = list(mergedDict.values())
        keys_list = list(mergedDict.keys())

        cols, rows = (n, n)
        #create matrix
        matrix = [[0 for i in range(cols)] for j in range(rows)]
        #get preorder of all nodes in map
        map = self.bn.preorder()

        for node in map:
            #find the row index of current node value
            pos1 = None
            pos2 = None
            val = node.value
            col = vals_list.index(val)

            neigh1 = node.left
            neigh2 = node.right

            #if node has neighboring node, get column index of neighbor(s)
            #change the matrix entry to 1
            if not neigh1.isempty():
                pos1 = vals_list.index(neigh1.value)
                matrix[pos1][col] = 1
            if not neigh2.isempty():
                pos2 = vals_list.index(neigh2.value)
                matrix[pos2][col] = 1

            #check if which segments neighbor trapezoids if not direct child of segment
            if isinstance(val, Trapezoid):
                top = val.top
                bot = val.bottom
                leftx = val.leftp.x
                rightx = val.rightp.x

                if top in vals_list:
                    pos_t = vals_list.index(top)
                    matrix[col][pos_t] = 1
                if bot in vals_list:
                    pos_b = vals_list.index(bot)
                    matrix[col][pos_b] = 1

                points = [x.value for x in map if isinstance(x.value, Pt)]

                for point in points:
                    if point.inTrap(val):
                        pos_p = vals_list.index(point)
                        matrix[col][pos_p] = 1


        #create table and save matrix to file
        df = pd.DataFrame(matrix, index = keys_list, columns=keys_list)

        df.loc['Sum'] = df.sum(numeric_only=True, axis=0)
        df['Sum'] = df.sum(axis=1)

        df.to_csv("output.csv")

    def query_point(self, point):
        '''
        Find path to trapezoid containing point
        :param point: Point to be located
        :return: Returns a path referencing the point, segment, and trapezoid names
        '''
        path = self.bn.recordPath(point)

        return self.nameValue(path)

    def nameValue(self, path):
        '''
        apply names to nodes
        :param path: The path from a starting point to a trapezoid
        :return: Return a list of named nodes
        '''
        trapDict, startDict, endDict, segDict = self.indices()

        n = len(trapDict) + len(startDict) + len(endDict) + len(segDict)

        mergedDict = {**startDict, **endDict, **segDict, **trapDict}

        vals_list = list(mergedDict.values())
        keys_list = list(mergedDict.keys())

        val_idx = [vals_list.index(x) for x in path]

        named = [keys_list[x] for x in val_idx]

        return named

    def indices(self):
        '''
        Creates names for each node
        :return: Returns 4 dictionaries: dict{'name': node}
        '''
        trapDict = {}
        startDict = {}
        endDict = {}
        segDict = {}

        for i in range(len(self.segments)):
            start = self.segments[i].leftp
            end = self.segments[i].rightp
            segment = self.segments[i]

            startDict.update({f"P{i + 1}": start})
            endDict.update({f"Q{i + 1}": end})
            segDict.update({f"S{i + 1}": segment})

        for i in range(len(self.trapezoids)):
            trapDict.update({f"T{i + 1}": self.trapezoids[i]})


        return trapDict, startDict, endDict, segDict

def main():
    inputFile = "testData.txt"

    inputFile = open(inputFile, "r+")

    lines = [line.strip("\n") for line in inputFile.readlines()]
    inputFile.close()

    #number of segments
    n_segments = int(lines[0])

    # stores segments
    segments = []

    #bounding box
    box = [eval(x) for x in lines[1].split(" ")]
    bounds = [Pt(box[0], box[1]), Pt(box[2], box[3])]

    #build segments
    for line in lines[2:]:
        split = line.split(" ")
        if len(split) == 4:
            leftp = Pt(int(split[0]), int(split[1]))
            rightp = Pt(int(split[2]), int(split[3]))
            segment = Segment(leftp, rightp)
            segments.append(segment)

    #create empty trapezoidal map
    tmap = TrapezoidalMap(bounds)

    #build the map using the segments
    tmap.buildMap(segments)

    #enter desried quary point
    point = input("Enter point: ")

    point = [eval(x) for x in point.split(" ")]
    #query point and produce named path
    print(tmap.query_point(Pt(point[0], point[1])))


if __name__ == '__main__':
    main()


