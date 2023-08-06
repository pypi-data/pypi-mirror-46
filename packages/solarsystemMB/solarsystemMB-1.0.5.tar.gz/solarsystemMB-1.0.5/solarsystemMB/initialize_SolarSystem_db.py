"""Populate the database with available solar system data.i
Tables are created for Solar System Objects and naif_ids.
A SSObject datatype is also created."""
import glob
import os, os.path
import psycopg2
from astropy.io import ascii


def initialize_SolarSystem_db(database='thesolarsystemmb', force=False):
    """Add Solar System information to the database
    Currently the solar system data is in a hand-made table, but it would
    be great to get this information directly from the SPICE kernels

    **Parameters**

    database
        Name of the PostgeSQL database to use. Default is 'thesolarsystemmb'
        and there should be no reason to change this. This database is used
        for all nexoclom modules.

    force
        By default, the database tables are only created if they do not already
        exist. Set force to True to force the tables to be remade. This would
        be necessary if there are updates to the atomic data.

    **Output**
    No output."""
    # Verify database is running
    status = os.popen('pg_ctl status').read()
    if 'no server running' in status:
        os.system('pg_ctl -D $HOME/.postgres/main/ -l '
                  '$HOME/.postgres/logfile start')
    else:
        pass

    # Create database if necessary
    with psycopg2.connect(host='localhost', database='postgres') as con:
        con.autocommit = True
        cur = con.cursor()
        cur.execute('select datname from pg_database')
        dbs = [r[0] for r in cur.fetchall()]

        if database not in dbs:
            print(f'Creating database {database}')
            cur.execute(f'create database {database}')
        else:
            pass

    # Populate the database tables
    with psycopg2.connect(host='localhost', database=database) as con:
        # Drop the old table (if necessary) and create a new one
        con.autocommit = True
        cur = con.cursor()
        cur.execute('select table_name from information_schema.tables')
        tables = [r[0] for r in cur.fetchall()]

        if ('solarsystem' in tables) and force:
            cur.execute('drop table solarsystem')
        else:
            pass

        if ('solarsystem' not in tables) or force:
            # Create SSObject datatype
            try:
                cur.execute('''CREATE TYPE SSObject
                               as ENUM (
                                    'Milky Way',
                                    'Sun',
                                    'Mercury',
                                    'Venus',
                                    'Earth',
                                    'Mars',
                                    'Jupiter',
                                    'Saturn',
                                    'Uranus',
                                    'Neptune',
                                    'Ceres',
                                    'Pluto',
                                    'Moon',
                                    'Phobos',
                                    'Deimos',
                                    'Io',
                                    'Europa',
                                    'Ganymede',
                                    'Callisto',
                                    'Mimas',
                                    'Enceladus',
                                    'Tethys',
                                    'Dione',
                                    'Rhea',
                                    'Titan',
                                    'Hyperion',
                                    'Iapetus',
                                    'Phoebe',
                                    'Charon',
                                    'Nix',
                                    'Hydra')''')
            except:
                pass

            # Create the database table
            print('Creating solarsystem table')
            cur.execute('''CREATE TABLE SolarSystem (
                             Object SSObject UNIQUE,
                             orbits SSObject,
                             radius float,
                             mass float,
                             a float,
                             e float,
                             tilt float,
                             rotperiod float,
                             orbperiod float)''')

            planfile = glob.glob(os.path.join(os.path.dirname(__file__),
                                              'data',
                                              'PlanetaryConstants.dat'))
            plantable = ascii.read(planfile[0], delimiter=':', comment='#')

            for row in plantable:
                cur.execute('''INSERT into SolarSystem VALUES
                                   (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                                   tuple(row))

        if ('naifids' in tables) and force:
            cur.execute('drop table naifids')
        else:
            pass

        if ('naifids' not in tables) or force:
            print('Creating naifids table')
            cur.execute('''CREATE table naifids (id int, object text)''')

            naifid_file = glob.glob(os.path.join(os.path.dirname(__file__),
                                                 'data', 'naif_ids.dat'))
            for line in open(naifid_file[0], 'r').readlines():
                if ':' in line:
                    line2 = line.split(':')
                    id = int(line2[0].strip())
                    object = line2[1].strip()
                    cur.execute(f"""INSERT into naifids values
                                  ({id}, '{object}')""")
