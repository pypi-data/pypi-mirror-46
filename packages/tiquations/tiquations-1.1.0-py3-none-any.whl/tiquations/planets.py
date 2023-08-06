
class Planets(object):
    def __init__(self,gravity,mass,radius,surface_area,sun_distance):
        self.gravity=gravity
        self.mass=mass
        self.radius=radius
        self.surface_area=surface_area
        self.sun_distance=sun_distance
        
earth=Planets(9.807,5.972e24,6371,510.1,149597870)
moon=Planets(1.62,7.34767309e22,1737.1,3.793e7,152503397)
mars=Planets(3.711,6.4171e23,3389.5,114.8,227940000)
jupiter=Planets(24.79,1.898e27,69911,61420,778300000)
neptune=Planets(11.15,1.024e26,24622,7618,4497100000)
mercury=Planets(3.7,3.285e23,2439.7,74.8,57900000)
saturn=Planets(10.44,5.683e26,58232,42700,1427000000)
uranus=Planets(8.87,8.681e25,25362,8083,2871000000)
venus=Planets(8.87,4.867e24,6051.8,460.2,108200000)
pluto=Planets(0.61,1.30900e22,1188.3,16647940,5913000000)
