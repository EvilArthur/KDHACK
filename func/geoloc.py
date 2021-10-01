from geopy import distance
myshirota = float(input())
mydolgota = float(input())
clubshirota = float(input())
clubdolgota = float(input())
mylocation = (myshirota, mydolgota)
clublocation = (clubshirota, clubdolgota)
print(distance.distance(mylocation, clublocation).km)
