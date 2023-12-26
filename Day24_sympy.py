import numpy as np
from sympy import symbols, nonlinsolve

f = open("resources/day24_input.txt", "r")
lines = f.read().splitlines()
f.close()
data = []
for line in lines:
    line = line.split(" @ ")
    pos = [int(x) for x in line[0].split(", ")]
    speed = [int(x) for x in line[1].split(", ")]
    data.append((pos, speed))


def areParallel(a, b):
    p1 = a[1]
    p2 = b[1]
    if p1[0] == 0 and p2[0] == 0:
        return True
    if p1[0]/p2[0] == p1[1]/p2[1] and p1[0]/p2[0] == p1[2]/p2[2]:
        return True
    return False


def findIntersection(a, b):
    if areParallel(a, b):
        return None
    va = a[1][1]/a[1][0]
    vb = b[1][1]/b[1][0]
    ax = a[0][0]
    ay = a[0][1]
    bx = b[0][0]
    by = b[0][1]
    x = (va*ax - vb*bx - (ay - by)) / (va-vb)
    y = va * (x - ax) + ay
    return x, y


def findIntersection3(a, b):
    if areParallel(a, b):
        return None
    eq = np.array([[a[1][0], -b[1][0]],
                   [a[1][1], -b[1][1]]])
    val = np.array([b[0][0]-a[0][0],
                    b[0][1]-a[0][1]])
    try:
        res = np.linalg.solve(eq, val)
    except:
        print("No intersection: lines ", a, b, " exception! matrix is", eq, val)
        return None
        eq = np.array([[a[1][0], -b[1][0]], [a[1][2], -b[1][2]]])
        val = np.array([b[0][0]-a[0][0], b[0][2]-a[0][2]])
        res = np.linalg.solve(eq, val)
    #print(a, b, res)
    coorda = (a[0][0] + a[1][0]*res[0], a[0][1] + a[1][1]*res[0], a[0][2] + a[1][2]*res[0])
    coordb = (b[0][0] + b[1][0]*res[1], b[0][1] + b[1][1]*res[1], b[0][2] + b[1][2]*res[1])
    #if coorda[2] != coordb[2]:
    epsilon=1e-6
    #epsilon=1
    if abs(coorda[2] - coordb[2]) > epsilon:
        #print("No intersection: lines ", a, b, "check not passed")
        return None
    else:
        return coorda

def timeToPoint(a, pos):
    return (pos[0] - a[0][0]) / a[1][0]

def inFuture(a, pos):
    return timeToPoint(a, pos) > 0


def findNormalVector(a, b, c):
    ab = (b[0]-a[0], b[1]-a[1], b[2]-a[2])
    ac = (c[0]-a[0], c[1]-a[1], c[2]-a[2])
    n = (ab[1]*ac[2] - ac[1]*ab[2], -ab[0]*ac[2] + ac[0]*ab[2], ab[0]*ac[1] - ac[0]*ab[1])
    return n

# generic math functions

def add_v3v3(v0, v1):
    return (
        v0[0] + v1[0],
        v0[1] + v1[1],
        v0[2] + v1[2],
    )


def sub_v3v3(v0, v1):
    return (
        v0[0] - v1[0],
        v0[1] - v1[1],
        v0[2] - v1[2],
    )


def dot_v3v3(v0, v1):
    return (
            (v0[0] * v1[0]) +
            (v0[1] * v1[1]) +
            (v0[2] * v1[2])
    )


def len_squared_v3(v0):
    return dot_v3v3(v0, v0)


def mul_v3_fl(v0, f):
    return (
        v0[0] * f,
        v0[1] * f,
        v0[2] * f,
    )

# intersection function
def isect_line_plane_v3(p0, p1, p_co, p_no, epsilon=1e-6):
    """
    p0, p1: Define the line.
    p_co, p_no: define the plane:
        p_co Is a point on the plane (plane coordinate).
        p_no Is a normal vector defining the plane direction;
             (does not need to be normalized).

    Return a Vector or None (when the intersection can't be found).
    """

    u = sub_v3v3(p1, p0)
    dot = dot_v3v3(p_no, u)

    if abs(dot) > epsilon:
        # The factor of the point between p0 -> p1 (0 - 1)
        # if 'fac' is between (0 - 1) the point intersects with the segment.
        # Otherwise:
        #  < 0.0: behind p0.
        #  > 1.0: infront of p1.
        w = sub_v3v3(p0, p_co)
        fac = -dot_v3v3(p_no, w) / dot
        u = mul_v3_fl(u, fac)
        return add_v3v3(p0, u)

    # The segment is parallel to plane.
    return None

# ---


def trySolve3(a, b, c):
    px, py, pz, vx, vy, vz, t1, t2, t3 = symbols('px, py, pz, vx, vy, vz, t1, t2, t3', real=True)
    eq1 = a[1][0]*t1 + a[0][0] - vx*t1 - px
    eq2 = a[1][1]*t1 + a[0][1] - vy*t1 - py
    eq3 = a[1][2]*t1 + a[0][2] - vz*t1 - pz
    eq4 = b[1][0]*t2 + b[0][0] - vx*t2 - px
    eq5 = b[1][1]*t2 + b[0][1] - vy*t2 - py
    eq6 = b[1][2]*t2 + b[0][2] - vz*t2 - pz
    eq7 = c[1][0]*t3 + c[0][0] - vx*t3 - px
    eq8 = c[1][1]*t3 + c[0][1] - vy*t3 - py
    eq9 = c[1][2]*t3 + c[0][2] - vz*t3 - pz
    eqsystem = [eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8, eq9]
    vars = [px, py, pz, vx, vy, vz, t1, t2, t3]
    res = list(nonlinsolve(eqsystem, vars))[0]
    print(res)
    print(res[0]+res[1]+res[2])



#testArea = (7, 27)
testArea = (200000000000000, 400000000000000)


def withinTestArea(pos):
    return testArea[0] <= pos[0] <= testArea[1] and testArea[0] <= pos[1] <= testArea[1]


def testBelongsToPlane(p0, p_co, p_no, epsilon=1e-6):
    d = dot_v3v3(p_no, p_co)
    res = dot_v3v3(p_no, p0)
    if abs(d - res) < epsilon:
        return True
    else:
        return False



if False:
    #if True:
    testA = ((-10, -20, -30), (10, 2, 3))
    testB = ((15, 3, 12), (5, 1, 4))
    intersection = findIntersection3(testA, testB)
    print(intersection)
    exit(0)


trySolve3(data[0], data[1], data[2])
exit(0)

numLines = len(data)
numIntersections = 0
found = None
for index, a in enumerate(data[:-1]):
    for b in data[index+1:]:
        #print("Testing ", a, b)
        if areParallel(a, b):
            normal = findNormalVector(a[0], add_v3v3(a[0], a[1]), b[0])
            found = a
            print(a, b, " are parallel! Normal: ", normal)
            #break
        intersection = findIntersection3(a, b)
        if intersection is not None:
            print(a, b, " intersection at ", intersection)
            if (intersection[0] - a[0][0]) * a[1][0] > 0:
                normal = findNormalVector(a[0], add_v3v3(a[0], a[1]), b[0])
            found = a
            print("Normal: ", normal)
            break
    #if found:
    #break

a = found
resPoints = []
for test in data:
    intersection = isect_line_plane_v3(test[0], add_v3v3(test[0], test[1]), a[0], normal)
    if intersection is None:
        timeToInstersection = None
    else:
        timeToInstersection = ((intersection[0]-test[0][0])/test[1][0], (intersection[1]-test[0][1])/test[1][1], (intersection[2]-test[0][2])/test[1][2])
        resPoints.append((intersection, timeToInstersection[0]))
        if len(resPoints) == 2:
            pos = [None]*3
            for i in range(3):
                eq = np.array([[resPoints[0][1], 1], [resPoints[1][1], 1]])
                val = np.array([resPoints[0][0][i], resPoints[1][0][i]])
                res = np.linalg.solve(eq, val)
                pos[i] = round(res[1])
            print("Start position: ", pos, "sum = ", sum(pos))
            exit(0)


    print(test, intersection, timeToInstersection)


exit(0)


if False:
    for index, a in enumerate(data[:-1]):
        for b in data[index+1:]:
            intersection = findIntersection(a, b)
            if intersection is not None:
                #print(a, b, " intersect at ", intersection, inFuture(a, intersection), inFuture(b, intersection))
                if withinTestArea(intersection) and inFuture(a, intersection) and inFuture(b, intersection):
                    numIntersections += 1
    print("Result: ", numIntersections)
