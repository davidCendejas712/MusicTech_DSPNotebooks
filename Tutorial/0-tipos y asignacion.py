'''
UNA INTRODUCCIÓN A PYTHON 3.x PARA PROGRAMADORES

Recursos:
  - Guión. https://www.programiz.com/python-programming/tutorial
  - Notebooks de Rafa Caballero (ejemplos)


Lenguaje Interpretado.

Tipos básicos: 
- int, float, bool, string  (tipado dinámico)


Instrucciones básicas:
- asignación, if-elif-else, while

'''

# es un comentario de línea


#%% una celda para Hola mundo
print("Hola mundo")








#%% " y ' funcionan igual
print('Hola mundo')


#%% Comillas dentro de comillas
print("Hola 'Juan'")
print('Hola \'Juan\'')


#%% Python es un lenguaje interpretado -> ejecuta línea a línea
print('Esta instrucción funciona!')
escribe('Esta no funciona... pero ya ha escrito la anterior')
print('Y esta tampoco, porque ha habido un error previo')





#%% variables y asignación
a = 5




#%% print con múltiples argumentos
print('a =',9)

a= 7
print('a =',a,'    2*a =',2*a)



#%%
num = 'seis'
print('seis =',num)

#%% asignacion multiple
x = y = 3
print(x,y,a)


#%%
print("Una linea")
print("y otra")

#%% print por defecto acaba con salto de línea
print("una linea ",end='')  
print("y solo una")




#%% asignación simultánea
a, b = 1, 4
print(a,b)


#%% swap de valores
a, b = b, a  # como funciona?
print(a, b)







#%% operadores +, -, *
a, b = 2, 8
print('suma: ',a+b)






#%% divisiones y otras operaciones
print('div real: ',10/3)
print('div entera: ',10//3)
print('modulo: ',10%3)
print('potencia: ',10**3)






#%% enteros de tamaño cualquiera
x = 3481256483612846123412341234125546856823452
y = 5893465897234642341235348725982347529
print(x*y)

#%% operadores += -=  ...
x = 1
x += 1  
print(x)

# ojo, no funciona "x++", "x--"", etc





#%% comentarios de línea con #


'''
comentarios 
multilinea
con 
triple
comilla ' o "
'''








#%% tipos numéricos
a = 3 # enteros
b = 5.8 # float

#%% conversion de tipos
c = int(b)  # trunca
print(c)


#%%
c = float(c) # tipado dinamico!!
print(c)



#%% string (secuencias de texto)
hola = 'hola' + ' ' + 'mundo' + '\n'
print(hola)
print(type(hola))






#%% más conversiones
print(str(3),'+',str(4),' es ', 7)
# que pasa sin str?


#%% tipo de una expresion
print(type(3))
print(type(c))
print(type("hola"))



#%% tipo de una expresion
print(type("True"))
print(type(False))



#%% booleanos
a = b = True
b = (a and not(a)) or b
print(b)
print(b==False)

#%%
type(fdasf)

#%%

'''
TIPOS ESTRUCTURADOS
- listas: list
- tuplas: tuple
- conjuntos: set
- diccionarios: dict
'''

#%% lista vacia
ls = []
print(ls)

#%% con eltos
ls = [1,2,3]
print(ls)

#%% no necesariamente del mismo tipo!!!
ls = [1, 3.14, 'hola', True, ['lista','anidada']]
print(ls)




#%% similares a los arrays de otros lenguajes, pero sin 
# tamaño prefijado

# indexan de 0 en adelante
print(ls[3])
print(ls[2])
print(type(ls))




#%% append
ls = [0,1,2]
ls.append(4)
print(ls)


#%% insert (en una posición dada)
ls.insert(1,7)  # inserta 7 en la posicion 1
print(ls)

#%% remove
ls.remove(2) # elimina la primera aparicion del 2
print(ls)

#%% pop elimina el elto de una posicion dada (y lo devuelve)
ls = [0,1,2]
ls.pop(1)
print(ls)


#%% accesos "desde el final"
print(ls[-1])
print(ls[-2])

# len -> long de la lista
# index -> posicion de la prim aparicion de un elto
# count -> n de apariciones de un elto
# pop -> quita y devuelve el primero
# del, remove, reverse, sort, max, min, sum ...


#%% sobrecarga de *
l = [0]*3
print(l)

#%%
l1 = [l]*4
print(l1)

#%% efecto "curioso"
l1[0][1] = 34
print(l1)
# por que este comportamiento?



#%%
'''
SLICES
Slices
Un tipo especial de operadores son los de "rodaja"
 o slice, que extraen una subsecuencia de la secuencia

a[start:stop]  # elementos desde start hasta stop -1
a[start:]      # desde start hasta el final
a[:stop]       # desde el principio hasta stop-1
a[:]           # copia la secuencia
a[start:stop:step] # desde start hasta stop-1, saltando step


ls[i:j] es la lista desde el elto i (incluido) al j (excluido). 

Si se omite i se asume el primero 
Si se omite j se asume el último 

'''

#%%
x = [0,1,2,3,4,5,6,7,8,9,10]
print(x[3:6])
print(x[3:7:2])
print(x[::3])

#%%
print(x[4:])  # se asume ultimo
print(x[:4])  # se asume primero
print(x[:9:3]) # se asume primero y va a saltos

#%%
print(x)
print(min(x),max(x),sum(x))



#%% concatenacion, pertenencia
print(x+[11,12])

print("esta el 3?", 3 in x)

#%% conversiones
print(list("hola"))


#%% ordenaccion por defecto (alfabética en cadenas)
xs = ['ab','y','xrc','cdessa','da']
xs.sort()
print(xs)


#%% ordenaccion con otro criterio: por longitud
xs = ['ab','y','xrc','cdessa','da']
xs.sort(key=len)
print(xs)




#%% copia de listas OJO!!!
xs = [0,1,2,3]
ys = xs
ys[1]=8
print(xs)  # que ha pasado?


# EL TIPO LISTA ES "MUTABLE" (referencia, puntero)
# ys = xs   es una asignación de referencias!

#%% como hacer la copia? varias formas
xs = [0,1,2,3]
ys = xs[:]   # utilizando slicing
zs = xs.copy()

# OJO: cuando pasan como argumento a funciones siguen
# siendo mutables





'''
TUPLAS
Similares a las listas
PERO son inmutables!! no pueden cambiar
'''

#%%
t = (0,1,2,3)
print(t)


#%%
t = (0,1,5,3)
print(t[2])



#%%
t = (0,1,2,3)
t[2] = 7

#%% utilidad? cto de valores fijados, q no cambian
x = 19
(cociente, resto) = (x//3, x%3)   # o tb divmod(x,3)
print(cociente,resto)

#%% tupla vacia
t = ()
print(t)


#%% tupla unitaria?
t = (7)
print(t)


#%% tupla unitaria, ahora si
t = (7,)
print(t)

#%% listas a tuplas
t = tuple([1,2,'barco'])
print(t)

#%% las tuplas se acceden igual que las listas
print(t[2])   # pero no pueden cambiarse!!


#%% veiamos asignación simultanea
a, b = 1, 2   # en realidad es asignacion de tuplas (a,b) = (1,2)


#%% predefinidas para tuplas: index, count...
t = (1,2,3,4,3,2,1,3)
print(t.index(3))
print(t.count(3))



'''
STRINGS str (revisitados)

- son secuencias INMUTABLES
- similares a las listas
- pueden accedese con índices, hacer slicing
- no pueden cambiarse
'''
#%%
s = 'hola mundo'
print('long:',len(s))
print('s[3]:',s[3])
print('count o:',s.count('o'))
print('index m:',s.index('m'))
print("podemos " + 'concatenar' + "?")



#%%
larga = '''pueden 
escribirse
cadenas multilinea
con la triple 
comilla'''

print(larga)


#%% buscar sucadena en cadena
i = larga.find('de')  
print(i)


#%% a mayusculas
LARGA = larga.upper()
print(LARGA)


#%% quitar blancos iniciales y finales
s = '    algunos blancos iniciales y finales   '
s1 = s.strip(' ')
print(s1)

# romper en palabras (sepradas por ' ')
s2 = s1.split(' ')
print(s2)

#%% salida con formato
# se antepone 'f' a la cadena y se utilizan placeholders {}
# {}   place holder

# obsoleto
# print("Un entero {}    Un float {}   \
#      Un string {}".format(3, 5.67,'hola'))

print("Hola")

#%%
# ahora se hace así
print(f"Un entero {3}    Un float {5.56 + 9}   \
       Un string {'hola'}")











#%%
'''
CONJUNTOS set

- otra estructura MUTABLE
- colecciones no ordenadas 
- eltos únicos
'''

#%% creacion de un cto
s = {1,2,3, 4.5,'hola',3,2,1}
print(s)  # elimina repeticiones





#%% cto vacio
#s = {}   asi no va
s = set()  # llamada a la constructora
s.add(4)
print(s)

print(type(s))


#%% creacion a partir de lista
s = set([1,2,3,1,2,3,4])
print(s)


#%% operaciones
s1 = {0,1,2,3} 
s2 = {2,3,4,5,6}


print(s1.union(s2))
print(s1.intersection(s2))


#%%
s1.remove(1)  # ojo: metodo
print(s1)


#%% operadores
s1 = {0,1,2,3} 
s2 = {2,3,4,5,6}

print(s1 | s2) # union
print(s1 & s2) # interseccion
print(s1 - s2) # diferencia

# otras: issubset, isdisjoint.... 





'''
DICCIONARIOS
- Colección ASOCIATIVA (no ordenada) de eltos
- contiene pares key:value
- TIPO MUTABLE
'''



#%%
d = {}  # o   d = dict()

d1 = {1: 'apple', 2: 'ball'}
print(d1)

d2 = {'name': 'John', 1: [2, 4, 3]}



#%% añadir eltos de manera dinamica
d1[7] = 'home'
print(d1)



#%% acceso y modificacion
print(d1[2])

d1[2] = "nothing special"
print(d1[2])

print(type(d1))


#%% items devuelve los pares key:val como tuplas
# pop elimina una clave y devuelve el valor









'''
MAS SECUENCIAS    range()
- devuelve una secuencia INMUTABLE de numeros entre dos valores
'''

#%%
r = range(1,10)
print(r)  # poco util?


#%% el resultado es una secuencia ITERABLE!
print(list(r))
print(tuple(r))
print(set(r))

#%% incio por defecto a 0
r2 = range(10)
print(list(r2))

#%% a saltos
r3 = range(0,10,2)
print(list(r3))

# sera MUY UTIL para los bucles 'for'




























# list comprehensions


# %%
