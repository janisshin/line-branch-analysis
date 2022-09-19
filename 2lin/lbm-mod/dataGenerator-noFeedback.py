# this file was created as a comparison to C:\Users\janis\Documents\School\research\leibermeister_models\2st2ex_highKm.py

import csv
import numpy as np
import random
import tellurium as te
import matplotlib.pyplot as plt



model = ("""
# Species:
species X1, X2, s1, s2

# Reactions:
const source, X1, X2
# J1 is neither activated nor inhibited
J1: source -> s1; e1 * ((k1 * ((source/k_source)^t_source)) - k2*(s1/k_s1)^t_s1) /((1 + (source/k_source))^t_source + (1+(s1/k_s1))^t_s1 - 1);

# J2 is neither activated nor inhibited
J2: s1 -> s2; e2 * ((k3 * (s1 / k_s1)^t_s1) - (k4 * (s2 / k_s2)^t_s1))/((1 + s1/k_s1)^t_s1 + (1 + s2/k_s2)^t_s2 - 1);

# J3 is neither activated nor inhibited
J3: s2 -> ; e3 * ((k5 * (s2 / k_s2)^t_s2) /((1 + s2/k_s2)^t_s2));

# J3 is activated by X2 and inhibited by s1
# Species initializations:
X1 = 12.0604;
X2 = 1.2;
s1 = 1.947;
s2 = 0.164;
source = 25;

# Parameter value initializations:

e1 = 1; e2 = 1; e3 = 1; 

leak_X1 = 2.59e-07;
k_X1 = 22.36;
t_X1 = 1;
leak_X2 = 1.51e-06;
k_X2 = 1.52;
t_X2 = 1;
k_s1 = 10.0805;
t_s1 = 2;
k_s2 = 4200.0417;
t_s2 = 1;
k_source = 1
t_source = 1


k1 = 5; k2 = 0.001; k3 = 10000; k4 = 0.001; k5 = 10000; k6 = 10 
""")

r = te.loada(model)
r.simulate(0,100)
r.plot()

header = ['e1_perturbed', 'relative_s2', 'relative_flux']
kvalues = ['k1', 'k2', 'k3', 'k4']
elasticities = ['e_J1/s2', 'e_J4/s2']

"""
with open('MAdata_2stLin_e1_lb.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header + kvalues + elasticities)
    for i in range(500):
        r.resetToOrigin()
        
        e1B = random.uniform(0.2, 3)

        rand_k = np.random.rand(6,)
        rand_x = np.random.rand(2,)
        
        r.k1 = rand_k[0]
        r.k2 = rand_k[1]
        r.k3 = rand_k[2]
        r.k4 = rand_k[3]
        r.k5 = rand_k[4]
        r.k6 = rand_k[5]
        
        r.X1 = rand_x[0]
        r.X2 = rand_x[1]
        
        r.simulate(0,1000)
        r.conservedMoietyAnalysis = True
        r.steadyState()
        
        s2A = r.s2
        v4A = r.J4
        
        r.reset()
        r.e2 = e1B ## perturbation
        r.simulate(0,1000)
        r.steadyState()
    
        s2B = r.s2
        v4B = r.J4
    
        data = [e1B, s2B/s2A, v4B/v4A]
        kvalues = [r.k1, r.k2, r.k3, r.k4]
        elasticities = list(r.getScaledElasticityMatrix().flatten())
        
        writer.writerow(data + kvalues + elasticities)
"""