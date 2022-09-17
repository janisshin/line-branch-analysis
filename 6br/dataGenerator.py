import csv
import numpy as np
import random
import tellurium as te

sixstep = te.loada("""
    J1: $x0 -> s1; e1 * (k1*x0-k2*s1)
    J2: s1 -> s2; e2 * (k3*s1-k4*s2)
    J3: s2 -> s3; e3 * (k5*s2-k6*s3)
    J4: s2 -> s4; e4 * (k7*s2-k8*s4)
    J5: s3 -> $x1; e5 * (k9*s3-k10*x1)
    J6: s4 -> $x2; e6 * (k11*s4-k12*x2)
    
    e1 = 1; e2 = 1; e3 = 1; e4 = 1; e5 = 1; e6 = 1;
    k1 = 1; k2 = 1; k3 = 1; k4 = 1; k5 = 1; k6 = 1; 
    k7 = 1; k8 = 1; k9 = 1; k10 = 1; k11 = 1; k12 = 1; 
    x0 = 10; x1 = 2; x2 = 3;
    s1 = 0.2; s2 = 0.2; s3 = 0.4; s4 = 0.2;
    
    """)

header = ['perturbation', 'rel_s1','rel_s2', 'rel_s3', 'rel_s4', 'relative_flux_J5', 'relative_flux_J6']
kvalues = ['k1', 'k2', 'k3', 'k4', 'k5', 'k6', 'k7', 'k8', 'k9', 'k10', 'k11', 'k12']
elasticities = ['e_J1/s1', 'e_J1/s2', 'e_J1/s3', 'e_J1/s4',
                'e_J2/s1', 'e_J2/s2', 'e_J2/s3', 'e_J2/s4', 
                'e_J3/s1', 'e_J3/s2', 'e_J3/s3', 'e_J3/s4', 
                'e_J4/s1', 'e_J4/s2', 'e_J4/s3', 'e_J4/s4',
                'e_J5/s1', 'e_J5/s2', 'e_J5/s3', 'e_J5/s4',
                'e_J6/s1', 'e_J6/s2', 'e_J6/s3', 'e_J6/s4']

perturbation='e2'

with open(f'MAdata_6stbr_{perturbation}.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header + kvalues + elasticities)
    for i in range(4500):
        sixstep.resetToOrigin()
        
        eB = random.uniform(0.2, 3)
        
        rand_k = np.random.uniform(0,1,12)
        rand_s = np.random.uniform(0,1,3)
        
        sixstep.k1 = rand_k[0]
        sixstep.k2 = rand_k[1]
        sixstep.k3 = rand_k[2]
        sixstep.k4 = rand_k[3]
        sixstep.k5 = rand_k[4]
        sixstep.k6 = rand_k[5]
        sixstep.k7 = rand_k[6]
        sixstep.k8 = rand_k[7]
        sixstep.k9 = rand_k[8]
        sixstep.k10 = rand_k[9]
        sixstep.k11 = rand_k[10]
        sixstep.k12 = rand_k[11]
        
        sixstep.x0 = rand_s[0]
        sixstep.x1 = rand_s[1]
        sixstep.x2 = rand_s[1]
        
        sixstep.simulate(0,1000)
        sixstep.conservedMoietyAnalysis = True
        sixstep.steadyState()
        
        s1A = sixstep.s1
        s2A = sixstep.s2
        s3A = sixstep.s3
        s4A = sixstep.s4
        v5A = sixstep.J5
        v6A = sixstep.J6
        
        sixstep.reset()
        sixstep.setValue(perturbation, eB) ## perturbation
        sixstep.simulate(0,1000)
        sixstep.steadyState()
    
        s1B = sixstep.s1
        s2B = sixstep.s2
        s3B = sixstep.s3
        s4B = sixstep.s4
        v5B = sixstep.J5
        v6B = sixstep.J6
    
        data = [eB, s1B/s1A, s2B/s2A, s3B/s3A, s4B/s4A, v5B/v5A, v6B/v6A]
        kvalues = [sixstep.k1,sixstep.k2,sixstep.k3,sixstep.k4,sixstep.k5,sixstep.k6,sixstep.k7,sixstep.k8,sixstep.k9,sixstep.k10,sixstep.k11,sixstep.k12]
        elasticities = list(sixstep.getScaledElasticityMatrix().flatten())
        
        writer.writerow(data + kvalues + elasticities)