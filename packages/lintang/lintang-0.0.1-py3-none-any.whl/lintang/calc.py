from math import radians, cos, sin, asin, sqrt

class Haversine():

    def get_distance(lat1, lon1, lat2, lon2, type='kilometers'):

        if type=='miles':
            R = 3959.87433 # this is in miles.  For Earth radius in kilometers use 6372.8 km
        elif type=='kilometers':
            R = 6372.8
        else:
            return "wrong parameter 'type'."

        dLat = radians(lat2 - lat1)
        dLon = radians(lon2 - lon1)
        lat1 = radians(lat1)
        lat2 = radians(lat2)

        a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
        c = 2*asin(sqrt(a))

        return R * c


"""
    Usage:

    lon1 = -103.548851
    lat1 = 32.0004311
    lon2 = -103.6041946
    lat2 = 33.374939
    
    print(Haversine.get_distance(lat1, lon1, lat2, lon2))
"""