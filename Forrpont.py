import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
from shapely.geometry import LineString
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

data = pd.read_csv("Forrpont.csv")

xD = 0.96
yD = 0.96
xW = 0.05
yW = 0.05
xF = 0.35
yF = 0.35

temp = data['Temperature'].values
x = data['x1'].values
y = data ['y1'].values

fig, ax = plt.subplots()
plt.xlim(0,1)
plt.ylim(min(temp),max(temp))

class Függvény:

    def __init__(self, x_értékek, y_értékek):
        self.x_értékek = x_értékek
        self.y_értékek = y_értékek

    def ábrázol(self, szín):
        ax.plot(self.x_értékek, self.y_értékek, c=szín)

    def return_x(self):
        return(self.x_értékek)

    def return_y(self):
        return(self.y_értékek)


buborékpont_görbe = Függvény(x,temp)
buborékpont_görbe.ábrázol('blue')

harmatpont_görbe = Függvény(y,temp)
harmatpont_görbe.ábrázol('blue')

y_1 = np.interp(xW, harmatpont_görbe.return_x(),harmatpont_görbe.return_y())
egyenesek_1 = Függvény([xW,xW,0],[0,y_1,y_1])
egyenesek_1.ábrázol('red')

plt.annotate(f'{round(y_1,2)}°C', (0,y_1))

y_2 = np.interp(xD, harmatpont_görbe.return_x(),harmatpont_görbe.return_y())
egyenesek_2 = Függvény([xD,xD,0],[0,y_2,y_2])
egyenesek_2.ábrázol('red')

plt.annotate(f'{round(y_2,2)}°C', (0,y_2))

ax.xaxis.set_major_locator(MultipleLocator(0.05))
ax.xaxis.set_minor_locator(MultipleLocator(0.01))

ax.yaxis.set_major_locator(MultipleLocator(5))
ax.yaxis.set_minor_locator(MultipleLocator(1))

plt.xlabel('x(n-hexán), y(n-hexán) [-]')
plt.ylabel('T [°C]')

plt.grid()
plt.show()
