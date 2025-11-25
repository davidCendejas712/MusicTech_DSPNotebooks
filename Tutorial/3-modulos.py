'''
Cualquier archivo Python ejemplo.py es un módulo
que puede importarse con

import ejemplo.py

Mutitud de módulos del sistema
'''

#%%
import math  # importación de multitud de funciones matemáticas

x = math.sqrt(144)
print(x)


#%% se pueden importar funciones aisladas de un modulo
from math import sqrt

x = sqrt(144)   # OJO: ya no se necesita la cualificacion 'math.'
print(x)



#%% o todas de golpe

from math import *   
# la diferencia con import math es que ahora 
# no hay que cualificar

x = sqrt(144)   # OJO: ya no se necesita la cualificacion 'math.'
print(x)




#%%

