import QLines

from time import sleep


def test_boundingBox(left, right, top, bottom):
    """Unit tests for bounding box"""
    test = QLines.LineArrangement(None)
    test.boundingBox(left, right, top, bottom)
    corners = [(left, top), (right, top), (right, bottom), (left, bottom)]
    unboundedFace = test.faceRecord[0]
    # if face is unbounded
    if unboundedFace.outComp is None:
        boundedFace = test.faceRecord[1]
    else:
        unboundedFace = test.faceRecord[1]
        boundedFace = test.faceRecord[0]

    # test bounded face by traversing its edges
    edge = boundedFace.outComp
    cur_coord = edge.origin.coord
    # find cur_coord in corners
    start = 0
    for i, coord in enumerate(corners):
        if cur_coord == coord:
            start = i
            break
    # make sure the traversak is correct
    for j in range(5):
        index = (start-j)%4  # subtract j as we want to go counter clockwise
        if cur_coord != corners[index]:
            print("Error in bounded face!")
            exit()
        edge = edge.next
        cur_coord = edge.origin.coord

    # test unbounded face by traversing its edges
    edge = unboundedFace.inComp[0]  # we know there should only be two faces
    cur_coord = edge.origin.coord
    # find cur_coord in corners
    start = 0
    for i, coord in enumerate(corners):
        if cur_coord == coord:
            start = i
            break
    # make sure the traversak is correct
    for j in range(5):
        index = (start+j)%4  # add j to move clockwise
        if cur_coord != corners[index]:
            print("Error in unbounded face!")
            exit()
        edge = edge.next
        cur_coord = edge.origin.coord








def main():
    test_boundingBox(10, 40, 30, 0)
    test_boundingBox(-100, 40.5, 36, -0.1)


if __name__ == "__main__":
    main()