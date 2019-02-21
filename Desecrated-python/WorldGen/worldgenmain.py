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

print(to_geodetic(*to_geocentric(lat1,lon1)))



# fig = plt.figure()
# ax = fig.add_subplot(1, 1, 1,
#                      projection=ccrs.PlateCarree())
# ax.coastlines()
# ax.scatter(lons,lats)
# ax.plot(lons, lats,transform=ccrs.Geodetic())
# ax.set_global()

# plt.show()