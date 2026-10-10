"""ALE-CN portable synthetic thermal engines, not EnergyPlus or GLM."""
import numpy as np


def building_step(state,weather,cooling):
    air,wall=state;outside,solar,occupied=weather
    return np.array([.90*air+.05*wall+.05*outside+.0012*solar+.12*occupied-.28*cooling,
                     .02*air+.97*wall+.01*outside])


def lake_column(forcing,params,layers=16):
    mixing,exchange,attenuation=params
    n=len(forcing);z=np.arange(layers)+.5;state=np.ones(layers)*10.;out=np.empty((n,layers))
    for t,(air,solar,wind) in enumerate(forcing):
        # Four explicit substeps with no-flux bottom and wind-driven diffusion.
        for _ in range(4):
            diffusion=np.r_[state[1]-state[0],state[:-2]-2*state[1:-1]+state[2:],state[-2]-state[-1]]
            gain=.0006*solar*np.exp(-attenuation*z)
            gain[0]+=exchange*(air-state[0])
            state+=.25*(mixing*(1+.12*wind)*diffusion+gain)
        out[t]=state
    return out
