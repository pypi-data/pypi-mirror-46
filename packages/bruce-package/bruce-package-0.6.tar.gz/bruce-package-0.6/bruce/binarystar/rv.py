

# Python imports
import numba, numba.cuda, numpy as np , math 

import matplotlib.pyplot as plt 

# bruce imports
from .kepler import getTrueAnomaly

@numba.njit(fastmath=True)
def _rv( time, RV, RV_err, J,
        t_zero, period, 
        K1, fs, fc,
        V0, dV0,
        incl,
        E_tol, 
        loglike_switch):

    # Unpack and convert (assume incl in radians)
    w = math.atan2(fs, fc)
    e = fs**2 + fc**2

    loglike=0.
    for i in range(time.shape[0]):
        nu = getTrueAnomaly(time[i], e, w, period,  t_zero, incl, E_tol ) 
        model = K1*(e*math.cos(w) + math.cos(nu + w)) + V0 + dV0*(time[i] - t_zero) 
        if loglike_switch : 
            wt = 1.0 / (RV_err[i]**2 + J**2)
            loglike += -0.5*((RV[i] - model)**2*wt - math.log(wt))
        else : RV[i] = model 

    return loglike


@numba.cuda.jit
def kernel_rv(time, RV, RV_err, J,
        t_zero, period, 
        K1, fs, fc,
        V0, dV0,
        incl,
        E_tol, 
        loglike):

    # Unpack and convert (assume incl in radians)
    w = math.atan2(fs, fc)
    e = fs**2 + fc**2

    i = numba.cuda.grid(1)

    nu = getTrueAnomaly(time[i], e, w, period,  t_zero, incl, E_tol ) 
    model = K1*(e*math.cos(w) + math.cos(nu + w)) + V0 + dV0*(time[i] - t_zero) 
    wt = 1.0 / (RV_err[i]**2 + J**2)
    loglike[i] = -0.5*((RV[i] - model)**2*wt - math.log(wt))        


@numba.cuda.reduce
def sum_reduce(a, b):
    return a + b


def rv( time, RV = np.zeros(1), RV_err=np.zeros(1), J=0,
        t_zero=0., period=1., 
        K1=10., fs=0., fc=0.,
        V0=10., dV0=0.,
        incl=90.,
        E_tol=1e-5, 
        gpu=0, loglike=np.zeros(1), blocks = 10, threads_per_block = 512):

    # Convert inclination 
    incl = np.pi * incl/180.
    if not gpu:
        # First, let's see if we need loglike or not!
        if RV_err[0]==0 : loglike_switch = 0
        else            : loglike_switch = 1

        # Now, let's initiase the arrays, if needed
        if not loglike_switch : RV = np.empty_like(time) 

        # Now make the call
        loglike = _rv( time, RV, RV_err, J,
            t_zero, period, 
            K1, fs, fc,
            V0, dV0,
            incl,
            E_tol, 
            loglike_switch) 

        if loglike_switch : return loglike 
        else              : return RV 
    

    if gpu:
        # Loglike ony supported 
        # assumeing loglike is array

        ## Call the kernel to populate loglike 
        kernel_rv[blocks, threads_per_block](time, RV, RV_err, J,
            t_zero, period, 
            K1, fs, fc,
            V0, dV0,
            incl,
            E_tol, 
            loglike)
        
        # let's synchronise to ensure it's finished
        numba.cuda.synchronize() 

        # Now reduce the loglike array
        return sum_reduce(loglike)


'''
time = np.linspace(2450000, 2450001, 100000)
RV = rv(time)
RV = np.random.normal(RV, 1) 
RV_err = np.random.uniform(0.5,1.5, RV.shape[0])
J = 0.2 

CPU_loglike = rv(time, RV, RV_err, J=J) 
print('CPU loglike = ', CPU_loglike)

# Now copy stuff over to GPU for compliance 
d_time = numba.cuda.to_device(time)
d_RV = numba.cuda.to_device(RV)
d_RV_err = numba.cuda.to_device(RV_err)
loglike = np.empty_like(time) 
d_loglike = numba.cuda.to_device(loglike)

threads_per_block=512 
blocks = int(np.ceil(time.shape[0]/threads_per_block))
GPU_loglike = rv(d_time, d_RV, d_RV_err, J=J, gpu=1, loglike=d_loglike, blocks=blocks, threads_per_block=threads_per_block) 
print('GPU loglike = ', GPU_loglike)



# Time it 
timeit GPU_loglike = rv(d_time, d_RV, d_RV_err, J=J, gpu=1, loglike=d_loglike, blocks=blocks, threads_per_block=threads_per_block) 



plt.plot(time,RV)

plt.figure() 
K1 = np.linspace(5,15, 100)
for i in range(len(K1)) : plt.scatter(K1[i] , rv(time, RV, RV_err, J=J, K1=K1[i]))
plt.show()
'''