from geopy import distance
mydolgota = float(input())
myshirota = float(input())
clubdolgota = float(input())
clubshirota = float(input())
mylocation = (myshirota, mydolgota)
clublocation = (clubshirota, clubdolgota)
print(distance.distance(mylocation, clublocation).km)