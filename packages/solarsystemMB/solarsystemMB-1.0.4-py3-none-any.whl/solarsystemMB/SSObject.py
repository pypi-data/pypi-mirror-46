"""Create an object for each Solar System body containing basic information.
Information stored:
* object: Object name
* orbits: Body that the object orbits
* radius: in km
* mass: in kg
* a: orbital semi major axis. In AU if orbits the Sun; km
    if orbits a planet
* e: orbital eccentricity
* tilt: tilt of planetary axis in degrees
* rotperiod: rotation period in hours
* orbperiod: orbital period in days
* GM: mass * G in m**3/s**2
* moons: returned as a list of SSObjects

Values are astropy units quantities when appropriate.

"""
import os
import psycopg2
from astropy import constants as const
from astropy import units as u


class SSObject:
    """Creates Solar System object."""
    def __init__(self, obj):
        with psycopg2.connect(database='thesolarsystemmb') as con:
            cur = con.cursor()
            cur.execute('''SELECT * FROM SolarSystem
                           WHERE object = %s''', (obj.title(), ))
            result = cur.fetchone()

        self.object = result[0]
        self.orbits = result[1]
        self.radius = result[2] * u.km
        self.mass = result[3] * u.kg
        self.a = result[4]
        self.e = result[5]
        self.tilt = result[6] * u.deg
        self.rotperiod = result[7] * u.h
        self.orbperiod = result[8] * u.d
        self.GM = -self.mass * const.G
        self.moons = self.get_moons()

        if (self.orbits == 'Milky Way'):
            self.type = 'Star'
            self.a *= u.km
        elif (self.orbits == 'Sun'):
            self.type = 'Planet'
            self.a *= u.au
        else:
            self.type = 'Moon'
            self.a *= u.km

    def __len__(self):
        # Returns number of objects (e.g. Planet + moons) in the SSObeject
        return 1 if self.moons is None else len(self.moons)+1

    def __eq__(self, other):
        return self.object == other.object

    def __hash__(self):
        return hash((self.object, ))

    def __str__(self):
        out = (f'Object: {self.object}\n'
               f'Type = {self.type}\n'
               f'Orbits {self.orbits}\n'
               f'Radius = {self.radius:0.2f}\n'
               f'Mass = {self.mass:0.2e}\n'
               f'a = {self.a:0.2f}\n'
               f'Eccentricity = {self.e:0.2f}\n'
               f'Tilt = {self.tilt:0.2f}\n'
               f'Rotation Period = {self.rotperiod:0.2f}\n'
               f'Orbital Period = {self.orbperiod:0.2f}\n'
               f'GM = {self.GM:0.2e}')
        return(out)

    def get_moons(self):
        with psycopg2.connect(database='thesolarsystemmb') as con:
            cur = con.cursor()
            query = cur.execute('''SELECT object FROM SolarSystem
                                   WHERE orbits = %s''', (self.object, ))
            result = cur.fetchall()
            if len(result) == 0:
                return None
            else:
                return tuple(SSObject(m[0]) for m in result)
