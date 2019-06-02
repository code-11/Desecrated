import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random
import math
import numpy as np

RADIUS = 6371  # Radius of earth km
CIRCUM = 2 * math.pi * RADIUS


def gen_lat():
    return random.uniform(0, 180)


def gen_lon():
    return random.uniform(0, 360)

class BoundingCircle(object):
    lat = 0
    lon = 0
    radius = 0
    PRINT_RESOLUTION = 100

    @classmethod
    def three_point(cls, lat1, lon1, lat2, lon2, lat3, lon3):
        a = to_geocentric(lat1, lon1)
        b = to_geocentric(lat2, lon2)
        c = to_geocentric(lat3, lon3)

        alph = np.subtract(a, b)
        beta = np.subtract(c, b)
        phi = np.cross(alph, beta)

        center_pt = to_geodetic(*phi)
        the_radius = haversine(*center_pt, lat1, lon1)

        # Order of points given can sometimes give the inside out bounding circle!
        if the_radius > CIRCUM/4.0:
            center_pt=antipode(*center_pt)
            the_radius=haversine(*center_pt, lat1, lon1)

        circle = cls(*center_pt, the_radius)
        return circle

    def __init__(self, lat, lon, radius):
        self.lat = lat
        self.lon = lon
        self.radius = radius

    def __repr__(self):
        return "<BC " + str((self.lat, self.lon)) + " " + str(self.radius) + " >"

    def within(self, lat2, lon2):
        return within(self.lat, self.lon, self.radius, lat2, lon2)

    def print(self, ax):
        pts = []
        for rad_angle in np.linspace(0, 2 * math.pi, self.PRINT_RESOLUTION):
            pts.append(destination(self.lat, self.lon, rad_angle, self.radius))

        lats, lons = zip(*pts)
        ax.plot(lons, lats, transform=ccrs.Geodetic(), color="black")

    # This should work but I can't get the transform right
    # ax.add_patch(mpatches.Rectangle(xy=[70, -45], width=90, height=90, facecolor='red', alpha=0.2, transform=ccrs.Geodetic()))
    # ax.add_patch(mpatches.Circle(xy=[self.lon, self.lat], radius=50, transform=ccrs.Geodetic(), color='red', alpha=0.3, zorder=30))


def within(lat, lon, radius, lat2, lon2):
    distance = haversine(lat, lon, lat2, lon2)
    return distance <= radius


def to_geocentric(lat, lon):
    a = RADIUS
    lat = math.radians(lat)
    lon = math.radians(lon)
    x = a * math.cos(lon) * math.cos(lat)
    y = a * math.sin(lon) * math.cos(lat)
    z = a * math.sin(lat)
    return (x, y, z)


def to_geodetic(x, y, z):
    dis = math.sqrt(x ** 2 + y ** 2 + z ** 2)
    lon = math.atan2(y, x)
    lat = math.asin(z / dis)
    return math.degrees(lat), math.degrees(lon)


def antipode(lat, lon):
    x, y, z = to_geocentric(lat, lon)
    return to_geodetic(-x, -y, -z)


def midpoint(lat1, lon1, lat2, lon2):
    v1 = np.array(to_geocentric(lat1, lon1))
    v3 = np.array(to_geocentric(lat2, lon2))
    v2 = (v1 + v3) / 2
    return to_geodetic(*v2)


def center(lat_lons):
    vs = map(lambda pt: to_geocentric(*pt), lat_lons)
    np_vs = np.array(list(vs))
    vs_len = np_vs.shape[0]
    vs_sum = np.sum(np_vs, axis=0)
    return to_geodetic(*(vs_sum / vs_len))


def norm(v, mag=1):
    return (v / np.linalg.norm(v)) * mag


def intersection(lat1, lon1, lat2, lon2, lat3, lon3, lat4, lon4):
    a0 = to_geocentric(lat1, lon1)
    a1 = to_geocentric(lat2, lon2)
    b0 = to_geocentric(lat3, lon3)
    b1 = to_geocentric(lat4, lon4)
    nor1 = np.cross(a0, a1)
    nor2 = np.cross(b0, b1)
    sect1 = np.cross(nor1, nor2)
    sect2 = -sect1
    geosect_a = to_geodetic(*sect1)
    geosect_b = to_geodetic(*sect2)

    mid12 = midpoint(lat1, lon1, lat2, lon2)
    mid34 = midpoint(lat3, lon3, lat4, lon4)
    half_dis12 = haversine(lat1, lon1, lat2, lon2) / 2
    half_dis34 = haversine(lat3, lon3, lat4, lon4) / 2

    if (within(*mid12, half_dis12, *geosect_a) and within(*mid34, half_dis34, *geosect_a)):
        return geosect_a
    elif (within(*mid12, half_dis12, *geosect_b) and within(*mid34, half_dis34, *geosect_b)):
        return geosect_b
    else:
        return (None, None)


def line_distance(lat1, lon1, lat2, lon2, lat, lon):
    a = to_geocentric(lat1, lon1)
    b = to_geocentric(lat2, lon2)
    c = to_geocentric(lat, lon)

    nor1 = np.cross(a, b)
    nor2 = np.cross(c, nor1)
    d = np.cross(nor1, nor2)
    return haversine(lat, lon, *to_geodetic(*d))


def haversine(lat1, lon1, lat2, lon2):
    """
	Calculate the great circle distance (km) between two points 
	on the earth (specified in decimal degrees)
	"""
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = RADIUS  # Radius of earth in kilometers. Use 3956 for miles
    return c * r


"""
Calculate a starting heading defined from lat1,lon1, between 0 and 2*pi
"""


def heading(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    X = math.cos(lat2) * math.sin(lon1 - lon2)
    Y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(lon1 - lon2)
    brng = math.atan2(X, Y)
    brng = (brng + (math.pi * 2)) % (math.pi * 2)
    return (2 * math.pi) - brng

"""
How much angle a will have to spin clockwise to get to b
"""


def angle_dist(a,b):
    if b < a:
        b += math.pi * 2
    return b-a


"""
Given a point and a heading, determine the focus of that great circle
"""


def focus(lat, lon, heading):
    lat2, lon2 = destination(lat, lon, heading, 10)

    v1 = to_geocentric(lat, lon)
    v2 = to_geocentric(lat2, lon2)
    nor = np.cross(v1, v2)

    return to_geodetic(*nor)


"""
Given a starting point in lat lon (degrees), and a heading (radians), and a distance (km), find the end point
"""


def destination(lat, lon, heading, dis):
    a = RADIUS
    distRatio = dis / a
    distRatioSine = math.sin(distRatio)
    distRatioCosine = math.cos(distRatio)

    startLatRad = math.radians(lat)
    startLonRad = math.radians(lon)

    startLatCos = math.cos(startLatRad)
    startLatSin = math.sin(startLatRad)

    endLatRads = math.asin((startLatSin * distRatioCosine) + (startLatCos * distRatioSine * math.cos(heading)))

    endLonRads = startLonRad + math.atan2(math.sin(heading) * distRatioSine * startLatCos,
                                          distRatioCosine - startLatSin * math.sin(endLatRads))

    newLat = math.degrees(endLatRads)
    newLong = math.degrees(endLonRads)
    return (newLat, newLong)


def full_circle(lat1, lon1, lat2, lon2):
    anti_lat, anti_lon = antipode(lat1, lon1)
    anti_lat2, anti_lon2 = antipode(lat2, lon2)
    return ([lat1, lat2, anti_lat, anti_lat2, lat1], [lon1, lon2, anti_lon, anti_lon2, lon1])


def full_circle_hd(lat1, lon1, heading):
    lat2, lon2 = destination(lat1, lon1, heading, 10)
    return full_circle(lat1, lon1, lat2, lon2)


def full_circle_focus(lat, lon):
    pt_on_circle = destination(lat, lon, 0, CIRCUM / 4)
    pt_on_circle2 = destination(lat, lon, 10, CIRCUM / 4)

    return full_circle(*pt_on_circle, *pt_on_circle2)


def gen_rnd_pts(n=20):
    xs = 200 * np.random.rand(n) - 100
    ys = 200 * np.random.rand(n) - 100
    zs = 200 * np.random.rand(n) - 100

    pts = []
    for (x, y, z) in zip(xs, ys, zs):
        pts.append(to_geodetic(x, y, z))
    return pts


def gen_rnd_color():
    return list(np.random.random(size=3))


def bin_partition(pts, heading):
    if len(pts) > 3:
        lats, lons = zip(*pts)

        lata, lona = center(zip(lats, lons))
        focus_pt = focus(lata, lona, heading)

        far_pts = []
        near_pts = []
        for pt in pts:
            if within(*focus_pt, CIRCUM / 4, *pt):
                near_pts.append(pt)
            else:
                far_pts.append(pt)

        return (
            bin_partition(near_pts, heading + math.pi / 2), bin_partition(far_pts, heading + math.pi / 2), (lata, lona),
            heading, focus_pt)
    else:
        return voronoi_cluster(pts)


def calc_baseline_angles(cluster, near, far, is_right):
    near_lat, near_lon = near
    far_lat, far_lon = far
    baseline_heading = heading(near_lat, near_lon, far_lat, far_lon)

    def angle_from_baseline(lat, lon):
        potential_heading = heading(near_lat, near_lon, lat, lon)
        # print("candidate heading: "+str(potential_heading))
        if is_right:
            return angle_dist(baseline_heading, potential_heading)
        else:
            return angle_dist(potential_heading,baseline_heading)
    #
    # print("near: "+str(near))
    # print("far: "+str(far))
    # print("heading: "+str(baseline_heading))

    angles = []
    for pt in cluster.pts:
        if pt != near:
            angle=angle_from_baseline(*pt)
            # print("candidate: "+str(pt))
            angles.append((pt, angle))
    angles.sort(key=lambda ang_pair: ang_pair[1])
    return angles


def find_candidate(cluster, angles, baseline_near, baseline_far):
    filtered = []
    for i, angle_pair in enumerate(angles):
        pt, angle = angle_pair
        angle_met = False
        circle_met = False

        if angle <= math.pi:
            angle_met = True

        if i+1 < len(angles):
            next_point, next_angle = angles[i+1]
            bc = BoundingCircle.three_point(*baseline_near, *baseline_far, *pt)
            # Circle made by baseline and candidate may not contain next candidate
            circle_met = not bc.within(*next_point)

        else:
            circle_met = True

        if angle_met:
            if circle_met:
                return pt
            else:
                cluster.remove_edge(*baseline_near, *pt)
    return None


def merge(left_cluster, right_cluster, center, heading, focus):
    # centerline
    center_b = destination(*center, heading, 10)

    left_base = left_cluster.lowest()
    right_base = right_cluster.lowest()

    left_angles = calc_baseline_angles(left_cluster, left_base, right_base, False)
    left_candidate=find_candidate(left_cluster, left_angles, left_base, right_base)

    right_angles = calc_baseline_angles(right_cluster, right_base, left_base, True)
    right_candidate=find_candidate(right_cluster, right_angles, right_base, left_base)
    print(left_candidate,right_candidate)
    return (left_base, right_base, right_cluster, left_angles+right_angles)


def print_partition(ax, stuff):
    try:
        left, right, focus = stuff
        print_partition(ax, left)
        print_partition(ax, right)

        part_lats, part_lons = full_circle_focus(*focus)
        ax.plot(part_lons, part_lats, color="red", transform=ccrs.Geodetic())
    except:
        lats, lons = zip(*stuff)
        ax.scatter(lons, lats, color=gen_rnd_color())


def print_clusters(ax, stuff):
    try:
        left, right, center, heading, focus = stuff
        print_clusters(ax, left)
        print_clusters(ax, right)
    except:
        stuff.print(ax)


class voronoi_cluster(object):
    edges = []
    pts = []
    color = None

    def __init__(self, pts, edges = []):
        self.edges = edges
        self.pts = pts
        self.color = gen_rnd_color()
        self.initial_merge()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "[" + str(len(self.pts)) + "]"

    def remove_edge(self, lat1, lon1, lat2, lon2):
        pt1 = (lat1, lon1)
        pt2 = (lat2, lon2)
        tup1 = (pt1, pt2)
        tup2 = (pt2, pt1)
        if tup1 in self.edges:
            self.edges.remove(tup1)
        if tup2 in self.edges:
            self.edges.remove(tup2)

    def initial_merge(self):
        pts = self.pts
        edges = self.edges

        if len(pts) > 1:
            edges.append((pts[0], pts[1]))
        if len(pts) > 2:
            edges.append((pts[1], pts[2]))
            edges.append((pts[0], pts[2]))

    """
	Returns the closest point in this cluster to the given line
	"""

    def closest_to_line(self, lat1, lon1, lat2, lon2):
        return min(self.pts, key=lambda pt: line_distance(lat1, lon1, lat2, lon2, *pt))

    def lowest(self):
        return min(self.pts, key=lambda pt: pt[0])

    def print(self, ax):
        lats, lons = zip(*self.pts)

        for edge in self.edges:
            ax.plot((edge[0][1], edge[1][1]), (edge[0][0], edge[1][0]), linewidth=1, color="black",
                    transform=ccrs.Geodetic())

        ax.scatter(lons, lats, color=self.color)


def voronoi():
    # pts = gen_rnd_pts(5)
    # stuff = bin_partition(pts, 0)
# return stuff
    a=(1,-3)
    b=(0,-2)
    c=(2,-2)
    d=(3,-2)
    e=(1,-1)
    f=(3,1)
    g=(3,3)
    h=(2,2)
    i=(1,3)
    j=(0,3)
    pts1=[a,b,c,d,e]
    pts2=[f,h,g,i,j]
    edges1=[(a,b),(b,e),(a,c),(c,e),(b,c),(a,d),(c,d),(e,d)]
    edges2=[(f,g),(f,h),(f,j),(h,g),(h,i),(h,j),(g,i),(i,j)]
    left=voronoi_cluster(pts1,edges1)
    right=voronoi_cluster(pts2,edges2)

    return (left,right,(0,0),0,(0,180))


# near_lats,near_lons=zip(*near_pts)
# far_lats,far_lons=zip(*far_pts)

# ax.scatter(near_lons,near_lats)
# ax.scatter(far_lons,far_lats,color="green")


# # sect=intersection(lat1,lon1,lat2,lon2,lat3,lon3,lat4,lon4)

# # lata,lona=(sect[0],sect[1])

# # print(to_geodetic(*to_geocentric(lat1,lon1)))


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1,
                     # projection=ccrs.Orthographic(30,-85))
                     projection=ccrs.PlateCarree())
ax.coastlines()

# flats,flons=full_circle(lat1,lon1,lat2,lon2)
# flats2,flons2=full_circle(lat3,lon3,lat4,lon4)

# ax.plot(flons,flats, transform=ccrs.Geodetic())
# ax.plot(flons2,flats2, transform=ccrs.Geodetic())

# ax.plot([lon1,lon2],[lat1,lat2], transform=ccrs.Geodetic())
# ax.plot([lon3,lon4],[lat3,lat4], transform=ccrs.Geodetic())


# lata,lona=center(zip([lat1,lat2,lat3,lat4],[lon1,lon2,lon3,lon4]))


# ax.plot(plot_lons,plot_lats,color="red",transform=ccrs.Geodetic())
# ax.scatter(lons_a,lats_a)
# ax.scatter(lons_b,lats_b,color="green")


stuff = voronoi()
# circ_pts=full_circle_hd(stuff[2][0],stuff[2][1],stuff[3])
# circ_lats,circ_lons=circ_pts	
# for lpt in stuff[0].pts:
# 	for rpt in stuff[1].pts:
# 		sect_lat1,sect_lon1=intersection(circ_lats[0],circ_lons[0],circ_lats[1],circ_lons[1],*lpt,*rpt)
# 		sect_lat2,sect_lon2=intersection(circ_lats[1],circ_lons[1],circ_lats[2],circ_lons[2],*lpt,*rpt)
# 		sect_lat3,sect_lon3=intersection(circ_lats[2],circ_lons[2],circ_lats[3],circ_lons[3],*lpt,*rpt)
# 		sect_lat4,sect_lon4=intersection(circ_lats[3],circ_lons[3],circ_lats[0],circ_lons[0],*lpt,*rpt)
# 		print(sect_lat1,sect_lat2,sect_lat3,sect_lat4)
# 		if sect_lat1!=None:
# 			sect_lat=sect_lat1
# 			sect_lon=sect_lon1
# 		if sect_lat2!=None:
# 			sect_lat=sect_lat2
# 			sect_lon=sect_lon2
# 		if sect_lat3!=None:
# 			sect_lat=sect_lat3
# 			sect_lon=sect_lon3
# 		if sect_lat4!=None:
# 			sect_lat=sect_lat4
# 			sect_lon=sect_lon4

# 		r_dis=haversine(*rpt,sect_lat,sect_lon)
# 		l_dis=haversine(*lpt,sect_lat,sect_lon)
# 		plt.text(*rpt, str(round(r_dis,3)),
# 	         horizontalalignment='right',
# 	         transform=ccrs.Geodetic())
# 		plt.text(*lpt, str(round(l_dis,3)),
# 	         horizontalalignment='right',
# 	         transform=ccrs.Geodetic())	         
# 		ax.scatter([sect_lon],[sect_lat],color="black",transform=ccrs.Geodetic())
# 		ax.plot([lpt[1],rpt[1]],[lpt[0],rpt[0]],color="red",transform=ccrs.Geodetic())
# ax.plot(circ_lons,circ_lats,color="blue",transform=ccrs.Geodetic())

# circ=BoundingCircle(1.5,-179.99999999,19690.957)
# circ.print(ax)
# print(circ.within(20,20))

a, b, right_cluster, angles = merge(*stuff)
lata, lona = a
latb, lonb = b
print_clusters(ax, stuff)

flats, flons = full_circle_hd(stuff[2][0], stuff[2][1], stuff[3])
ax.plot(flons, flats, color="blue", transform=ccrs.Geodetic())
ax.plot([lona, lonb], [lata, latb], color="red", transform=ccrs.Geodetic())
for angle_pair in angles:
    pt = angle_pair[0]
    angle = angle_pair[1]
    plt.text(pt[1], pt[0], str(round(angle, 3)),
             horizontalalignment='right',
             transform=ccrs.Geodetic())

ax.scatter([lona, lonb], [lata, latb], color="red", transform=ccrs.Geodetic())

# heading_pts = []
# for heading in np.linspace(0, 2*math.pi, 16):
#     heading_pt = destination(latb, lonb, heading, 30)
#     ax.plot([lonb, heading_pt[1]], [latb, heading_pt[0]], color="blue", transform=ccrs.Geodetic())
#     ax.text(heading_pt[1], heading_pt[0], str(round(heading, 3)))


# pts=gen_rnd_pts(5)

pt1=(-15,20)
pt2=(32,0)
pt3=(5,5)

lat1,lon1=pt1
lat2,lon2=pt2
lat3,lon3=pt3

ax.scatter([lon1,lon2,lon3],[lat1,lat2,lat3],color="black")

in_pts=[]
out_pts=[]
circ=BoundingCircle.three_point(*pt1,*pt2,*pt3)

circ.print(ax)

ax.set_global()

plt.show()
