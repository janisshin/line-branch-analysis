import csv
import numpy as np
import random
import tellurium as te

r = te.loada("""
	J1: $s1 -> s2; e1 * (k1 * s1 - k2 * s2);
    J2: s2 -> s3; e2 * (k3 * s2 - k4 * s3);
    J3: s3 -> s4; e3 * (k5 * s3 - k6 * s4);
    J4: s4 -> $s5; e4 * (k7 * s4 - k8 * s5);
    
	s1 = 0.67; s2 = 0.23; s3 = 0.77; s4 = 0.53; s5 = 0.33;
	k1 = 0.56; k2 = 0.26; k3 = 0.67; k4 = 0.56;
    k5 = 0.77; k6 = 0.54; k7 = 0.33; k8 = 0.48;
	e1 = 1; e2 = 1; e3 = 1; e4 = 1;
    """)

header = ['perturbation', 'rel_s2', 'rel_s3', 'rel_s4', 'relative_flux']
kvalues = ['k1', 'k2', 'k3', 'k4', 'k5', 'k6', 'k7', 'k8']
elasticities = ['e_J1/s2', 'e_J1/s3','e_J1/s4',
                'e_J2/s2', 'e_J2/s3','e_J2/s4',
                'e_J3/s2', 'e_J3/s3','e_J3/s4',
                'e_J4/s2', 'e_J4/s3','e_J4/s4']

perturbation='e4'

with open(f'MAdata_4stLin_{perturbation}.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header + kvalues + elasticities)
    for i in range(5000):
        r.resetToOrigin()
        
        eB = random.uniform(0.2, 3)
        
        #rand_k = np.random.rand(8,)
        #rand_s = np.random.rand(2,)
        
        rand_k = np.random.uniform(0,1,8)
        rand_s = np.random.uniform(0,1,2)
        
        r.k1 = rand_k[0]
        r.k2 = rand_k[1]
        r.k3 = rand_k[2]
        r.k4 = rand_k[3]
        r.k5 = rand_k[4]
        r.k6 = rand_k[5]
        r.k7 = rand_k[6]
        r.k8 = rand_k[7]
        
        r.s1 = rand_s[0]
        r.s5 = rand_s[1]
        
        r.simulate(0,1000)
        r.conservedMoietyAnalysis = True
        r.steadyState()
        
        s2A = r.s2
        s3A = r.s3
        s4A = r.s4
        v4A = r.J4
        
        r.reset()
        r.setValue(perturbation,eB)  ## e perturbation
        r.simulate(0,1000)
        r.steadyState()
    
        s2B = r.s2
        s3B = r.s3
        s4B = r.s4
        v4B = r.J4

        data = [eB, s2B/s2A, s3B/s3A, s4B/s4A,v4B/v4A]
        kvalues = [r.k1, r.k2, r.k3, r.k4, r.k5, r.k6, r.k7, r.k8]
        elasticities = list(r.getScaledElasticityMatrix().flatten())
    
        writer.writerow(data + kvalues + elasticities)

