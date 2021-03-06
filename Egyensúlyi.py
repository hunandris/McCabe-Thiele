import matplotlib.pyplot as plt
import math
import pandas as pd
import numpy as np
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from shapely.geometry import LineString

#Kezdeti értékek
R_Rmin_arány = float(input('R:Rmin arány: ' ))
q = 0.4
xD = 0.96
yD = 0.96
xW = 0.05
yW = 0.05
xF = 0.35
yF = 0.35

#q-vonal
q_endy = yF -1 * math.sin(np.arctan(q/(q-1)))
q_endx = xF -1 * math.cos(np.arctan(q/(q-1)))
q_x = [xF, q_endx]
q_y = [yF, q_endy]

#csv VLE calcról be
data = pd.read_csv("Egyensúlyi_adatok.csv")

#Tengelyek kezdeti beállításai
fig, ax = plt.subplots()
plt.xlim(0,1)
plt.ylim(0,1)
plt.gca().set_aspect('equal', adjustable = 'box')


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

class Végtelen_egyenes:

    def __init__(self, xy1, xy2):
        self.xy1 = xy1
        self.xy2 = xy2

    def ábrázol(self, szín):
        ax.axline(self.xy1, self.xy2, c=szín)
        return ax.axline(self.xy1, self.xy2, c=szín)

    def meredekség(self):
        meredekség = (self.xy2[1]-self.xy1[1])/(self.xy2[0]-self.xy1[0])
        return meredekség

    def y_metszet(self):
        y_metszet = (self.xy2[1]-(self.xy2[0]*self.meredekség()))
        return y_metszet

    def return_x(self):
        return self.ábrázol().get_xdata()

    def return_y(self):
        return self.ábrázol().get_ydata()



def metszéspont(függvény1, függvény2):
    line_1 = LineString(np.column_stack((függvény1.return_x(), függvény1.return_y())))
    line_2 = LineString(np.column_stack((függvény2.return_x(), függvény2.return_y())))
    intersection = line_1.intersection(line_2)
    x,y = intersection.xy
    return x[0], y[0]


#görbe, átló, q-vonal, felső,alsó munkavonal
görbe = Függvény(data['x1'].values, data['y1'].values)
görbe.ábrázol('blue')

egyenes = Függvény([0,1], [0,1])
egyenes.ábrázol('black')

q_vonal = Függvény(q_x, q_y)
q_vonal.ábrázol('grey')

Rmin_vonal = Végtelen_egyenes([xD,yD], metszéspont(q_vonal,görbe))
Rmin_vonal.ábrázol('grey')
Rmin = (xD/Rmin_vonal.y_metszet())-1

felső_munkavonal_y_metszet = xD/(Rmin*R_Rmin_arány+1)

felső_munkavonal = Függvény([0,xD], [felső_munkavonal_y_metszet, yD])
felső_munkavonal.ábrázol('green')

alsó_munkavonal = Függvény([metszéspont(felső_munkavonal, q_vonal)[0], xW], [metszéspont(felső_munkavonal, q_vonal)[1],yW])
alsó_munkavonal.ábrázol('green')

egybe_x = [xW, metszéspont(felső_munkavonal, q_vonal)[0], xD]
egybe_y = [yW, metszéspont(felső_munkavonal, q_vonal)[1], yD]
egybe_munkavonal = Függvény(egybe_x,egybe_y)
egybe_munkavonal.ábrázol('green')


#lépcsők
x = np.interp(yD, görbe.return_y(), görbe.return_x())
lépcső1 = Függvény([xD,x], [yD,yD])
lépcső1.ábrázol('red')

y = np.interp(x, egybe_munkavonal.return_x(), egybe_munkavonal.return_y())
lépcső2 = Függvény([x,x],[yD, y])
lépcső2.ábrázol('red')


x_regi = x
y_regi = y

while x_regi > xW:

    x_uj = np.interp(y_regi, görbe.return_y(),görbe.return_x())
    lépcső = Függvény([x_regi, x_uj], [y_regi,y_regi])
    lépcső.ábrázol('red')

    y_uj = np.interp(x_uj, egybe_munkavonal.return_x(),egybe_munkavonal.return_y())
    lépcső = Függvény([x_uj,x_uj], [y_regi, y_uj])
    lépcső.ábrázol('red')

    x_regi = x_uj
    y_regi = y_uj



ax.xaxis.set_major_locator(MultipleLocator(0.05))
ax.xaxis.set_minor_locator(MultipleLocator(0.01))

ax.yaxis.set_major_locator(MultipleLocator(0.05))
ax.yaxis.set_minor_locator(MultipleLocator(0.01))

plt.xlabel('x(n-hexán) [-]')
plt.ylabel('y(n-hexán) [-]')
plt.title('R:Rmin arány = %s' % (R_Rmin_arány))


plt.grid()
plt.show()
