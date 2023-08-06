import numba, numpy as np , math 

# Gravatational constant 
G = 6.67408e-11

#######################################
#          Keplers quation            #
#######################################

@numba.njit(fastmath=True)
def kepler(M, E, e) : return M - E - e*math.sin(E) 

@numba.njit(fastmath=True)
def kdepler(E, e) : return -1 + e*math.cos(E) 


@numba.njit(fastmath=True)
def fmod(a, b) : return a % abs(b)

#######################################
#        Eccentric anomaly            #
#######################################
@numba.njit(fastmath=True)
def getEccentricAnomaly(M, e, E_tol):
    m =  fmod(M , 2*math.pi) # should be fmod
    f1 = fmod(m , (2*math.pi) + e*math.sin(m)) + e*e*math.sin(2.0*m)/2.0  # should be fmod around 
    test  =1.0 
    e1 = 0.
    e0 = 1.0 
    while (test > E_tol):
        e0 = e1 
        e1 = e0 + (m-(e0 - e*math.sin(e0)))/(1.0 - e*math.cos(e0))
        test = abs(e1-e0)

    if (e1 < 0) : e1 = e1 + 2*math.pi 
    return e1 
 
#######################################
#      Time of periastron passage     #
#######################################
@numba.njit(fastmath=True)
def t_ecl_to_peri(t_ecl, e, w, incl, p_sid):
    # Define variables used
    efac  = 1.0 - e*2       # check if 2 or power
    sin2i = math.sin(incl)**2.

    # Value of theta for i=90 degrees
    ee = 0.
    theta_0 = (math.pi/2.) - w       # True anomaly at superior conjunction

    if (theta_0 == math.pi) :  ee = math.pi
    else :  ee =  2.0 * math.atan(math.sqrt((1.-e)/(1.0+e)) * math.tan(theta_0/2.0))

    eta = ee - e*math.sin(ee)
    delta_t = eta*p_sid/(2*math.pi)
    return t_ecl  - delta_t 

#######################################
#      Calculate the true anomaly     #
#######################################
@numba.njit(fastmath=True)
def getTrueAnomaly(time, e, w, period,  t_zero, incl, E_tol ):

    # Calcualte the mean anomaly
    M = 2*math.pi*((time -  t_ecl_to_peri(t_zero, e, w, incl, period)  )/period % 1.)

    # Calculate the eccentric anomaly
    E = getEccentricAnomaly(M, e, E_tol)

    # Now return the true anomaly
    return 2.*math.atan(math.sqrt((1.+e)/(1.-e))*math.tan(E/2.)) 

#######################################
#  Calculate the projected seperaton  #
#######################################
@numba.njit(fastmath=True)
def get_z(nu, e, incl, w, radius_1) : return (1-e**2) * math.sqrt( 1.0 - math.sin(incl)**2  *  math.sin(nu + w)**2) / (1 + e*math.sin(nu)) /radius_1

@numba.njit(fastmath=True)
def get_z_(nu, z) : return get_z(nu, z[0], z[1], z[2], z[3]) # for brent

#######################################
#  Calculate the projected seperaton  #
#######################################
@numba.njit(fastmath=True)
def getProjectedPosition(nu, w, incl) : return math.sin(nu + w)*math.sin(incl) 


#######################################
#     Calculate the mass function     #
#######################################
@numba.njit(fastmath=True)
def mass_function_1(e, P, K1) : return (1-e*e) **1.5*P*86400.1* (K1*1000)**3/(2*math.pi*G*1.989e30)

@numba.njit(fastmath=True)
def mass_function_1_(M2, z) : return ((M2*math.sin(z[1]))**3 / ( (z[0] + M2)**2)) - mass_function_1(z[2], z[3], z[4]) 