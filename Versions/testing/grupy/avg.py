__author__ = 'alex-admin'
import json
### Calculate AVERAGE Gruneisen parameter (i.e. mode Gruneisen weighed by contribution to specific heat)

def cv(omega,T):
    import math
    e = math.e
    kB = 1.3806488e-23
    hbar = 1.05457173e-34
    omega = float(omega)* 10.0e12
    T = float(T)
    x = (hbar*omega)/(kB*T)
    cv = kB * (x**2) * ( e**x / (e**x-1)**2 )
    return cv

#def GetAcousticModes():



def avg(Gin,temps):

    modes = "optical"

    ret = {}
    gru=[]
    omega=[]
    with open("%s.grupy.out"%Gin.prefix) as f:
        modes = []
        #for line in f:
        #    l = json.loads(line)
        #    if float(l['q']) == 0:
        #        modes.append


        for line in f:
            l=json.loads(line)

            if modes=="optical":
                if l['Mode_Type'] == "O":
                    gru.append(l['Gru'])
                    omega.append(l['Omega_eq'])

    for t in range(len(temps)):
    gru_avg = 0.0
        CV = 0.0
        for i in xrange(len(gru)):
            gru_avg += float(gru[i])* cv(omega[i],temps[t])
            CV += cv(omega[i],temps[t])
        gru_avg /= CV
        ret[t]= {'temperature (K)':temps[t], 'average Gruneisen': gru_avg, 'Cv':CV}
    
    with open("%s.avg.gru"%Gin.prefix, 'w') as g:
        if modes=="optical":
            g.writelines("Weighted optical mode average Gruneisen")
        for key in ret:
            g.writelines("%s\n"%ret[key])
    return ret


