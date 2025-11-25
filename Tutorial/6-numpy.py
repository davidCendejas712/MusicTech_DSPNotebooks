'''
numpy:  librería muy EFICIENTE para manejo de arrays de verdad (no listas)

tutorial: https://numpy.org/devdocs/user/quickstart.html

'''

#%% uso básico

import numpy as np  # alias np=numpy

# creacion de array a partir de lista
a1 = np.array([0,1,2,3,4,5,6,7,8,9])

print(a1)  # salida sin separador coma

#%%
print(type(a1))

print(a1.shape, a1.dtype)

#%% más dimensiones, mas inicializaciones
a2 = np.zeros((3,4))
a2[1,2] = 6

print(a2)


#%%
print(a2.shape, a2.dtype)

#%% mismo shape que a2, relleno de ceros
a3 = np.zeros_like(a2) 
print(a3)

#%% notacion de listas o multidimensional
a3[1,1] = 4
print(a3)



#%% version del iterador range para arrays
a4 = np.arange(10)      
print(a4)





#%% tamaño y tipo definidos
a5 = np.zeros(4,dtype=np.float32)
print(a5)
print(a5.dtype)






#%% operaadores y operaciones directas con arrays
a = np.array([10,20,30,40])
b = np.arange(4)

print("a =",a)
print("b =",b)

print()

print("a-b =",a-b)
print("b*10 =",b*10)





#%% mas sofisticado
print(np.sin(a))

#%%
print(1/a)


#%% aleatorios en [0,1]
ns = np.random.random(10)
print(ns)



#%% slicing: IGUAL QUE EN LISTAS!!!
s = ns[2:4]
print(s)


#%% copia... CUIDADO!
a = np.arange(4)
b = a

b[0] = 8
print(a)


#%% el slicing tampoco sirve: devuelve "vistas"
a = np.arange(4)
b = a[:]

b[0] = 8
print(a)



#%% copia bien hecha
a = np.arange(4)
b = a.copy()

b[0] = 8
print(a)
print(b)



#%% uso de vistas
a = np.arange(10)

a[3:6] = -1
print(a)


