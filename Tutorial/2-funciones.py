#%% definicion de funcion
def suma(x,y):
    return x+y


# llamada a función
print(suma(5,6))


#%% que escribe esto?
def f(x):
    x = x+1

print(f(6))




 
# Implícitamente 'return None'  (similar a void)




#%%
def f(x):
    x = x+1
    return x

print(f(6))




#%%  paso de parámetros
def f(x):
    x = x+1

y = 4
f(y)
print(y)



#%% devuelve los dos valores ordenados
def ordena(a,b):
    return min([a,b]),max([a,b])

print(ordena(3,5))
print(ordena(5,3))


#%% valores por defecto
def suma(a,b=0):
    return a+b

print(suma(4))
print(suma(4,5))



#%% parametros nombrados
def divide(dividendo,divisor=1):
    return dividendo//divisor

#%%
print(divide(divisor=3,dividendo=10))

#%%
print(divide(dividendo=10))



#%% tipos mutables -> como paso por ref
# mutables: list, set, dict


#%% cambia negativos por cero en la lista
def ponCeros(ls): 
    for i in range(len(ls)):
        if ls[i]<0:
            ls[i]=0
    # no hace falta return


l1 = list(range(-6,6))
print(l1)

ponCeros(l1)
print(l1)






#%% recursion... como en cualquier otro lenguaje
def fact(n):
    if n==0:
        return 1
    else:
        return n*fact(n-1)

print(fact(6))







#%% Lambdas (funciones anonimas)
# funcion que toma un argumento y calcula su cuadrado
cua = lambda x : x**2     
print(cua)

# para que puede servir esto?


#%% las funciones son ciudadanos de primera clase...
# orden superior: funciones como argumento de funciones
def map(f,ls):
    res = []
    for x in ls:
        res.append(f(x))
    return res

l1 = [x for x in range(4)]
l2 = map(cua,l1)

print(l2)


#%% alternativa con listas intensionales
def map2(f,ls):
    return [f(x) for x in ls]

print(map(cua,l1))


    

#%% mas lambdas
suma = lambda x,y : x+y

inc = lambda x : suma(x,1)

print(inc(3))




#%% filter

def filter(ls,fun):
    return [x for x in ls if fun(x)]


l1 = [x for x in range(100)]
div7 = lambda x : (x%7==0)
l2 = filter(l1,div7)
print(l2)

# mas compacto
print(filter(
    list(range(100)),
    lambda x : (x%7==0)
    )
    )

# mas
print([x for x in range(100) if x%7==0])





#%% 