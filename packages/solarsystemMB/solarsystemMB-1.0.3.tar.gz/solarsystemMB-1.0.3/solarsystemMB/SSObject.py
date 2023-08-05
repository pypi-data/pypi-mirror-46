import os
import psycopg2
from astropy import constants as const
from astropy import units as u


class SSObject:
#    def __new__(cls, obj):
#        ''' Verify that valid object has been requested '''
#
#        with psycopg2.connect(database='thesolarsystemmb') as con:
#            cur = con.cursor()
#
#            # check if valid object
#            cur.execute('SELECT unnest(enum_range(NULL::SSObject))::text')
#            objects = [ob[0].title() for ob in cur.fetchall()]
#
#        if obj.title() in objects:
#            return super().__new__(cls)  # empty instance
#        else:
#            return None

    def __init__(self, obj):
        '''Create a SSObject'''

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
        out = '''Object: {}
    Type = {}
    Orbits {}
    Radius = {:0.2f} {}
    Mass = {:0.2e} {}
    a = {:0.2f} {}
    Eccentricity = {:0.2f}
    Tilt = {:0.2f} {}
    Rotation Period = {:0.2f} {}
    Orbital Period = {:0.2f} {}
    GM = {:0.2e} {} '''.format(self.object, self.type, self.orbits,
                               self.radius.value, self.radius.unit,
                               self.mass.value, self.mass.unit,
                               self.a.value, self.a.unit,
                               self.e,
                               self.tilt.value, self.tilt.unit,
                               self.rotperiod.value, self.rotperiod.unit,
                               self.orbperiod.value, self.orbperiod.unit,
                               self.GM.value, self.GM.unit)

        return(out)

    def get_moons(self):
        with psycopg2.connect(database='thesolarsystemmb') as con:
            cur = con.cursor()

            query = cur.execute('''SELECT object FROM SolarSystem
                                   WHERE orbits = %s''', (self.object, ))
            result = cur.fetchall()
            if len(result) == 0:
                moons = None
            else:
                moons = tuple(SSObject(m[0]) for m in result)

            return moons
