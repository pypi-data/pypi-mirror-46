#module for generating sound 
import numpy as np
def generate_sample(freq,amp,duration,phi):
    NTONES =82
    amplitude = 2000 * np.random.random((NTONES,)) + 200
    # duration = 0.19 * np.random.random((NTONES,)) + 0.01
    keys = np.random.random_integers(1,88,NTONES)
    freqs = 440.0 *2**((keys-49)/12)

    # phi = 2 * np.pi * np.random.random((NTONES,))
    RATE = 2
    t = np.linspace(0,duration,duration *RATE)
    data = np.sin(2 * np.pi *freq *t +phi) *amp
    return data.astype(DTYPE)

def dasgenerate():
    for i inxrange(NTONES):
        newtone = generate_sample(freqs[i])