##### REFERENCE #####
# https://www.geeksforgeeks.org/closest-pair-of-points-onlogn-implementation/


import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def dist(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)


# Base case for 2 or 3 points using brute force
def baseCaseClosestPair(ptsX, ptsY):
    n = len(ptsX)
    if (n == 2):
        return ptsX[0], ptsX[1], dist(ptsX[0], ptsX[1])
    elif (n == 3):
        d_01 = dist(ptsX[0], ptsX[1])
        d_12 = dist(ptsX[1], ptsX[2])
        d_20 = dist(ptsX[2], ptsX[0])

        if (d_01 < d_12):
            p1, p2, d = ptsX[0], ptsX[1], d_01
        else:
            p1, p2, d = ptsX[1], ptsX[2], d_12

        if (d_20 < d):
            p1, p2, d = ptsX[2], ptsX[0], d_20

        return p1, p2, d
    else:
        print("ERROR: Got n > 3 for base case")
        exit()


# Return the closest pair across -
# 1. the strip, and
# 2. the closest pair from left & right halves
# Time Complexity = O(n)
def findClosestPair_strip(stripY, p1, p2, d):
    n = len(stripY)
    for i in range(n):
        j = i+1
        # Inner while loop runs atmost 6 times for each 'i', thus yielding the Time Complexity of the function as O(n)
        while (j < n) and (stripY[j].y - stripY[i].y <= d):     # Consider only those points whose Y-coord lies within a dist of 'd' from 'i'th point  -->  Atmost 6 such points exist for each 'i'
            d_curr = dist(stripY[j], stripY[i])
            if (d_curr < d):
                p1, p2, d = stripY[j], stripY[i], d_curr

            j += 1

    return p1, p2, d


# Find the closest pair of points using Divide & Conquer
def findClosestPair(ptsX, ptsY):
    n = len(ptsX)
    m = n//2

    # Base case
    if (n <= 1):
        print("ERROR: Can't find closest pair with less than 2 points")
        exit()
    elif (n <= 3):
        return baseCaseClosestPair(ptsX, ptsY)

    midPt = ptsX[m]     # Find the median point when points sorted acc. to X-coord
    ptsY_l = []     # Points in left & right regions will be sorted acc. to Y-coord
    ptsY_r = []     # since we are iterating through 'ptsY' in the below loop
    # Iterate through points sorted acc. to Y-coord and divide them into left and right.
    # Note that with the help of 'ptsX', we already know the median point (when points sorted acc. to X-coord).
    # So, splitting of points in left & right region can be done in O(n)
    for i in range(n):
        if (ptsY[i].x < midPt.x):
            ptsY_l.append(ptsY[i])
        else:
            ptsY_r.append(ptsY[i])

    p1_l, p2_l, d_l = findClosestPair(ptsX[:m], ptsY_l)
    p1_r, p2_r, d_r = findClosestPair(ptsX[m:], ptsY_r)
    if (d_l < d_r):
        p1, p2, d = p1_l, p2_l, d_l
    else:
        p1, p2, d = p1_r, p2_r, d_r

    stripY = []
    for i in range(n):
        if (abs(ptsY[i].x - midPt.x) <= d):
            stripY.append(ptsY[i])

    return findClosestPair_strip(stripY, p1, p2, d)


def closest_pair_points(pts):
    ptsX = pts[:]   # Used to find the median point when points sorted acc. to X-coord
    ptsY = pts[:]
    ptsX.sort(key=lambda pt: pt.x)
    ptsY.sort(key=lambda pt: pt.y)

    return findClosestPair(ptsX, ptsY)


if __name__ == "__main__":
    N = int(input())
    pts = []
    for n in range(N):
        x, y = map(float, input().split())
        pts.append(Point(x,y))

    p1, p2, d = closest_pair_points(pts)
    print("Closest pair of points - ", end='')
    print("(%.2f,%.2f) and (%.2f,%.2f)" % (p1.x, p1.y, p2.x, p2.y))
    print("Distance between closest pair = %.2f" % d)
