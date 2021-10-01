from geopy import distance
def distance_calc(myshirota, mydolgota, clubshirota, clubdolgota):
    mylocation = (myshirota, mydolgota)
    clublocation = (clubshirota, clubdolgota)
    return(distance.distance(mylocation, clublocation).km)
