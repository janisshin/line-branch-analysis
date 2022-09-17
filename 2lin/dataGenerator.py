import csv
import numpy as np
import random
import tellurium as te
import matplotlib.pyplot as plt

r = te.loada("""
	J1: $s1 -> s2; e1 * (k1 * s1 - k2 * s2);
    J2: s2 -> $s3; e2 * (k3 * s2 - k4 * s3);
    
	s1 = 0.67; s2 = 0.23; s3 = 0.77; 
	k1 = 0.56; k2 = 0.26; k3 = 0.67; k4 = 0.56;
    e1 = 1; e2 = 1; 
    """)

header = ['perturbation', 'relative_s2', 'relative_flux']
kvalues = ['k1', 'k2', 'k3', 'k4']
elasticities = ['e_J1/s2', 'e_J2/s2']

with open('MAdata_2stLin_e2.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header + kvalues + elasticities)
    for i in range(5000):
        r.resetToOrigin()
        
        eB = random.uniform(0.2, 3)
        
        rand_k = np.random.rand(4,)
        rand_s = np.random.rand(2,)
        
        r.k1 = rand_k[0]
        r.k2 = rand_k[1]
        r.k3 = rand_k[2]
        r.k4 = rand_k[3]
        
        r.s1 = rand_s[0]
        r.s3 = rand_s[1]
        
        r.simulate(0,1000)
        r.conservedMoietyAnalysis = True
        r.steadyState()
        
        s2A = r.s2
        v4A = r.J2
        
        r.reset()
        r.e2 = eB ## perturbation
        r.simulate(0,1000)
        r.steadyState()
    
        s2B = r.s2
        v4B = r.J2
    
        data = [eB, s2B/s2A, v4B/v4A]
        kvalues = [r.k1, r.k2, r.k3, r.k4]
        elasticities = list(r.getScaledElasticityMatrix().flatten())
        
        writer.writerow(data + kvalues + elasticities)

