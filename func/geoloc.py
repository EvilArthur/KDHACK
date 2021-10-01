from geopy import distance
def distance_calc(myshirota, mydolgota, clubshirota, clubdolgota):
    mylocation = (myshirota, mydolgota)
    clublocation = (clubshirota, clubdolgota)
    print(distance.distance(mylocation, clublocation).km)
