# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 02:24:02 2020

@author: Ege
"""

import matplotlib.pyplot as plt

# Pie chart
labels = users['index']
sizes = users['User']
# only "explode" the 2nd slice (i.e. 'Hogs')
explode = [0.1,0,0,0,0,0,0,0,0,0]

#explode = [0.1,0,0,0,0,0]



fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, explode = explode, autopct='%1.1f%%',
        shadow=True, startangle=90)
# Equal aspect ratio ensures that pie is drawn as a circle
plt.title('Who Talks Most ?')
ax1.axis('equal')  
plt.tight_layout()
plt.show()

plt.bar(sizes,labels,align='edge')

plt.bar(range(len(), my_dict.values(), align='center')