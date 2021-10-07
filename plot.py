import matplotlib.pyplot as plt
import math

durations_d = [6435.73, 6909.09, 8769.08, 11048.29, 12190.18, 13149.05, 16312.94, 14617.13, 13979.82, 14656.01, 14437.51, 16565.9, 13897.53, 12794.64, 9857.17, 7832.54, 5227.49, 3220.46]
densitys = [0.1,0.15,0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]

#plt.plot(densitys, durations_d)
#plot1.show()

durations_s = [7.64, 61.56, 210.82, 639.5, 1532.1, 2979.96, 5675.62, 8757.4, 15745.16, 18230.7]
sizes = [2, 3, 4,5,6,7,8,9,11,12]

nlog = []
for i in sizes:
    nlog.append(i**2*math.log(i**2))

print(nlog)

plt.plot(sizes, durations_s, color='r', label='sim')
plt.plot(sizes, nlog, color='g', label='nlog')
plt.show()
