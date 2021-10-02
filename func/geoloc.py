from geopy import distance


def distance_calc(myshirota, mydolgota, clubshirota, clubdolgota):
    mylocation = (myshirota, mydolgota)
    clublocation = (clubshirota, clubdolgota)
    dist = distance.distance(mylocation, clublocation).km
    if dist < 1:
        return dist*1000
    else:
        return round(dist,2)