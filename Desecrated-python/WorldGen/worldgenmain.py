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

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1,
                     projection=ccrs.PlateCarree())
ax.coastlines()
ax.scatter(lons,lats)
ax.plot(lons, lats,transform=ccrs.Geodetic())
ax.set_global()

plt.show()