import QLines

from time import sleep



def main():
    LA = QLines.LineArrangement(None)
    LA.boundingBox(10, 40, 30, 0)
    e = LA.bbVertex.incEdge.twin
    for i in range(5):
        v = e.origin
        print("Origin: ", e.origin.coord, "Dest: ", e.dest.coord, "Twin: ", e.twin, "Next:", e.next, "Prev: ", e.prev)
        e = e.next


if __name__ == "__main__":
    main()