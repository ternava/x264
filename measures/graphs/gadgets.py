# libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
 
plt.rcParams.update({'font.size': 15})

# Data
df=pd.DataFrame({'x_values': range(1, 64), 
            'configurations': [55425, 40770, 31587, 89494, 21317, 50284, 59661, 59661, 57194, 4474, 
            22585, 22585, 22585, 22585, 22585, 81550, 34030, 22179, 20910, 31773, 
            20889, 106878, 106878, 23280, 59526, 4182,  4182, 74252, 64327, 41013, 
            42682, 20967, 107125, 106522, 106857, 107352, 106878, 89846, 108787, 89568, 
            103015, 106878, 109290, 88550, 109456, 106878, 106878, 106878, 106878, 106021, 
            106809, 106955, 106878, 104601, 104601, 69744, 65383, 106878, 93768, 96425, 
            96577, 98091, 106878], 
            'baseline': [106878, 106878, 106878, 106878, 106878, 
            106878, 106878, 106878, 106878, 106878, 106878, 106878,
            106878, 106878, 106878, 106878, 106878, 106878, 106878,
            106878, 106878, 106878, 106878, 106878, 106878, 106878, 
            106878, 106878, 106878, 106878, 106878, 106878, 106878, 
            106878, 106878, 106878, 106878, 106878, 106878, 106878,
            106878, 106878, 106878, 106878, 106878, 106878, 106878, 
            106878, 106878, 106878, 106878, 106878, 106878, 106878, 
            106878, 106878, 106878, 106878, 106878, 106878, 106878, 
            106878, 106878] })
 
# multiple line plots
plt.plot( 'x_values', 'configurations', data=df, marker='x', markerfacecolor='blue', markersize=4, color='black', linewidth=2)
plt.plot( 'x_values', 'baseline', data=df, marker='', color='red', linewidth=2)
#plt.plot( 'x_values', 'y3_values', data=df, marker='', color='olive', linewidth=2, linestyle='dashed', label="toto")
# show legend
plt.legend()

plt.xticks(np.arange(0, 64, 5.0))
plt.yticks(np.arange(4000, 111000, 7000)) 
#109456
#4182

# plt.xlabel('configurations')
plt.ylabel('# of found gadgets')

# show graph
plt.show()