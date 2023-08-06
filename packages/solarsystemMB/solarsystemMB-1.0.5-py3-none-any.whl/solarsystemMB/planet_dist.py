'''Determine distance and radial velocity relative to Sun.'''
import os
import numpy as np
from scipy.misc import derivative
import astropy.units as u
from . import SSObject


def planet_dist(planet_, taa=None, time=None):
    if isinstance(planet_, str):
        planet = SSObject(planet_)
    elif isinstance(planet_, SSObject):
        planet = planet_
    else:
        assert 0, 'Must give a SSObject or a object name.'

    if planet is None:
        assert 0, 'Invalid object name'
    else:
        pass

    if time is not None:
        ## Need to do this
        assert 0, 'This is not verified'
        import spiceypy as spice
        from .load_kernels import load_kernels
        kernels = load_kernels()

        et = spice.str2et(inputs.geometry.time.isot)
        posvel, lt = spice.spkezr(inputs.geometry.planet.object, et, 'J2000',
                                  'LT+S', 'Sun')

        position = np.array(posvel[0:3])*u.km
        r = np.sqrt(np.sum(position**2))

        velocity = np.array(posvel[3:])*u.km/u.s
        v_r = np.sum(position*velocity)/r
        r = r.to(u.au)
    elif taa is not None:
        a = planet.a
        eps = planet.e

        # make sure taa is in radians. If not a quantity, assume it is.
        try:
            if taa.unit == u.deg:
                taa_ = taa.to(u.rad).value
            elif taa.unit == u.rad:
                taa_ = taa.value
            else:
                pass
        except:
            taa_ = taa

        if eps > 0:
            ## determine r
            r = a * (1-eps**2)/(1+eps*np.cos(taa_))
            P = np.sqrt(a**3/(1*u.au)**3) * u.yr

            ## determine v_r = dr/dt
            def trueanom(time):
                ## Mean anomally
                M = 2*np.pi*time/P.value

                ## Determine eccentric anomaly from M = E-e*sin(E)
                EEtemp = np.linspace(0, 2*np.pi, 1001)
                mm = EEtemp - eps*np.sin(EEtemp)
                EE = np.array([np.interp(x, mm, EEtemp) for x in M])

                ## True anomaly
                phi = (2*np.arctan(np.sqrt((1+eps)/(1-eps)) * np.tan(EE/2)) +
                       (2*np.pi)) % (2*np.pi)
                return phi

            def radius(time):
                phi = trueanom(time)
                r = a * (1-eps**2)/(1+eps*np.cos(phi))
                return r.value

            time = np.linspace(0, 1, 1001)*P.value
            radvel = derivative(radius, time, dx=1e-3)
            radvel = radvel.astype(np.float64)
            ttt = trueanom(time)
            v_r = np.interp(taa_, ttt, radvel, period=2*np.pi)
            v_r *= a.unit/P.unit
            v_r = v_r.to(u.km/u.s)
        else:
            r, v_r = a, 0.*u.km/u.s
    else:
        print('Neither a time nor a true anomaly was given.')
        return None

    #print('Distance from Sun: %.2f %s' % (r.value, r.unit))
    #print('Radial velocity relative to sun: %.2f %s' % (v_r.value, v_r.unit))
    return r, v_r
