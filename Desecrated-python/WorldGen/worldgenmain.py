import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import random
import math
import numpy as np

RADIUS=6371 #Radius of earth km

def gen_lat():
	return random.uniform(0,180)

def gen_lon():
	return random.uniform(0,360)

def pt():
	return (lat(),lon())

class BoundingCircle(object):
	lat=0
	lon=0
	radius=0
	def __init__(self,lat,lon,radius):
		self.lat=lat
		self.lon=lon
		self.radius=radius

	def within(lat2,lon2):
		return within(self.lat,self.lon,self.radius,lat2,lon2)

def within(lat,lon,radius,lat2,lon2):
	distance=haversine(lat,lon,lat2,lon2)
	return distance<=radius

def to_geocentric(lat,lon):
	a=RADIUS
	lat=math.radians(lat)
	lon=math.radians(lon)
	x = a*math.cos(lon)* math.cos(lat)
	y = a*math.sin(lon)* math.cos(lat)
	z = a*math.sin(lat)
	return (x,y,z)

def to_geodetic(x,y,z):
	dis=math.sqrt(x**2+y**2+z**2)
	lon=math.atan2(y,x)
	lat=math.asin(z/dis)
	return math.degrees(lat),math.degrees(lon)

def antipode(lat,lon):
	x,y,z=to_geocentric(lat,lon)
	return to_geodetic(-x,-y,-z)

def midpoint(lat1,lon1,lat2,lon2):
	v1=np.array(to_geocentric(lat1,lon1))
	v3=np.array(to_geocentric(lat2,lon2))
	v2=(v1+v3)/2
	return to_geodetic(*v2)

def center(lat_lons):
	vs=map(lambda pt:np.array(to_geocentric(*pt)) , lat_lons)
	print(vs)

def norm(v,mag=1):
	return (v/np.linalg.norm(v))*mag

def intersection(lat1, lon1, lat2, lon2, lat3, lon3, lat4, lon4):
	a0=to_geocentric(lat1,lon1)
	a1=to_geocentric(lat2,lon2)
	b0=to_geocentric(lat3,lon3)
	b1=to_geocentric(lat4,lon4)
	nor1=np.cross(a0,a1)
	nor2=np.cross(b0,b1)
	sect1=np.cross(nor1,nor2)
	sect2=-sect1
	geosect_a=to_geodetic(*sect1)
	geosect_b=to_geodetic(*sect2)

	mid12=midpoint(lat1,lon1,lat2,lon2)
	mid34=midpoint(lat3,lon3,lat4,lon4)
	half_dis12=haversine(lat1,lon1,lat2,lon2)/2
	half_dis34=haversine(lat3,lon3,lat4,lon4)/2

	if (within(*mid12,half_dis12,*geosect_a) and within(*mid34,half_dis34,*geosect_a)):
		return geosect_a
	elif (within(*mid12,half_dis12,*geosect_b) and within(*mid34,half_dis34,*geosect_b)):	
		return geosect_b
	else:
		return (None,None)


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
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = RADIUS # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def heading(lat1,lon1,lat2,lon2):
	lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
	X=math.cos(lat2)*math.sin(lon1-lon2)
	Y=math.cos(lat1)*math.sin(lat2)-math.sin(lat1)*math.cos(lat2)*math.cos(lon1-lon2)
	brng= math.atan2(X,Y)
	brng=(brng+(math.pi*2))%(math.pi*2)
	return (2*math.pi)-brng 

def destination(lat,lon,heading,dis):
	a=RADIUS
	distRatio = dis / a;
	distRatioSine = math.sin(distRatio);
	distRatioCosine = math.cos(distRatio);

	startLatRad = math.radians(lat);
	startLonRad = math.radians(lon);

	startLatCos = math.cos(startLatRad);
	startLatSin = math.sin(startLatRad);

	endLatRads = math.asin((startLatSin * distRatioCosine) + (startLatCos * distRatioSine * math.cos(heading)));

	endLonRads = startLonRad + math.atan2(math.sin(heading) * distRatioSine * startLatCos, distRatioCosine - startLatSin * math.sin(endLatRads));

	newLat = math.degrees(endLatRads);
	newLong = math.degrees(endLonRads);
	return (newLat,newLong)

def full_circle(lat1,lon1,lat2,lon2):
	anti_lat,anti_lon=antipode(lat1,lon1)
	anti_lat2,anti_lon2=antipode(lat2,lon2)
	return ([lat1,lat2,anti_lat,anti_lat2,lat1],[lon1,lon2,anti_lon,anti_lon2,lon1])

	# plt.plot([lon1, lon2], [lat1, lat2],
 #         color='blue', linewidth=1, marker='o',
 #         transform=ccrs.Geodetic(),
 #         )


lons = 360 * np.random.rand(2)
lats = 180 * np.random.rand(2) - 90

lat1=87
lon1=65

lat2=-36
lon2=145

lat3=-30
lon3=10

lat4=40
lon4=150

sect=intersection(lat1,lon1,lat2,lon2,lat3,lon3,lat4,lon4)

lata,lona=(sect[0],sect[1])

# print(to_geodetic(*to_geocentric(lat1,lon1)))

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1,
                     projection=ccrs.PlateCarree())
ax.coastlines()

# flats,flons=full_circle(lat1,lon1,lat2,lon2)
# flats2,flons2=full_circle(lat3,lon3,lat4,lon4)

# ax.plot(flons,flats, transform=ccrs.Geodetic())
# ax.plot(flons2,flats2, transform=ccrs.Geodetic())

ax.plot([lon1,lon2],[lat1,lat2], transform=ccrs.Geodetic())
ax.plot([lon3,lon4],[lat3,lat4], transform=ccrs.Geodetic())

ax.scatter([lona],[lata])
ax.set_global()


plt.show()