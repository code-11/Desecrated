import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import random
import math
import numpy as np


def lat():
	return random.uniform(0,180)

def lon():
	return random.uniform(0,360)

def pt():
	return (lat(),lon())

def to_geocentric(lat,lon):
	a=6371
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

def intersection(lon1, lat1, lon2, lat2):
	pass

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def heading(lat1,lon1,lat2,lon2):
	lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
	X=math.cos(lat2)*math.sin(lon1-lon2)
	Y=math.cos(lat1)*math.sin(lat2)-math.sin(lat1)*math.cos(lat2)*math.cos(lon1-lon2)
	brng= math.atan2(X,Y)
	brng=(brng+(math.pi*2))%(math.pi*2)
	return (2*math.pi)-brng 

def plot_great_circle(lat1,lon1,lat2,lon2):
	plt.plot([lon1, lon2], [lat1, lat2],
         color='blue', linewidth=1, marker='o',
         transform=ccrs.Geodetic(),
         )

# plt.plot([ny_lon, delhi_lon], [ny_lat, delhi_lat],
#          color='blue', linewidth=2, marker='o',
#          transform=ccrs.Geodetic(),
#          )



lons = 360 * np.random.rand(2)
lats = 180 * np.random.rand(2) - 90

lat1=87
lon1=65

lat2=-36
lon2=145

lat3=48.8567
lon3=2.3508

# print(to_geodetic(*to_geocentric(lat1,lon1)))

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1,
                     projection=ccrs.PlateCarree())
ax.coastlines()
# ax.scatter(lons,lats)
# ax.plot(lons, lats,transform=ccrs.Geodetic())
ax.set_global()
print(heading(0,0,1,1))

print(heading(1,1,30,30))

print(heading(30,30,1,1))

print(heading(-30,-30,10,10))


# plt.show()