'''
SENTENCIAS DE CONTROL
'''

'''
 BLOQUES en Python
Python no utiliza '{' '}'  para los bloques de código
Utiliza indentación (sangrado de línea)

Regla:
- una línea con más indentación que la anterior 
  comienza un nuevo bloque interno
- cuando se vuelve al nivel de indentación previo
  se termina el bloque interno
- las líneas consecutivas con el mismo nivel forman
  parte del mismo bloque
- En general: una instrucción por línea
  (puede utilizarse ';' para separar instrucciones
   en una misma línea, pero no es habitual)
''' 


#%% if-else-if

num = -17
sgn = 0 # -1 para negativos, 1 positivos, 0 para 0
if num > 0:    
    sgn = 1
    print("Positive number")
elif num == 0:
    # sgn = 0  # ya asignado por defecto
    print("Zero")
else:
    sgn = -1
    print("Negative number")
print("El signo calculado es",sgn)


#%%
'''    
Los condicionales no necesitan '(' ')'
Operadores relacionales estándar ==  !=  <  <= ..
Y lógicos and or not
Evaluación de circuito corto

Puede haber 0 mas 'elif' y el 'else' es opcional
Python no tiene switch!
'''

#%%
num = int(input('Dame un numero positivo'))  # introducir en caja de texto superior

if num<0:
    print('No es positivo')
elif num>=10 and num<=20:
    print('No esta mal')
elif num==27 or num==96:
    print('Que bonito')
else:
    print('Me has dado el',num)








#%% bucle while

i = sum = 0  # inicializacion
while i <= 10:
    sum = sum + i
    i = i+1    # incremento

print('Suma',sum)





#%% Bucle for: distinto a otros lenguajes
# formato:  for var in iterador
# se utiliza para iterar sobre 'tipos iterables'
# (listas,tuplas,strings,ranges,...

nums = [0,1,2,3,4,5,6,7,8,9]  # lista de enteros

sum = 0
for val in nums:
  sum = sum+val

print("La suma es", sum) 



#%% con rangos
sum = 0
for i in range(10): # i=0..9
    sum += i

print('Suma',sum)


#%% rangos con "step"
sum = 0
for i in range(0,10,2): # i=0,2,4,6,8
    sum += i

print('Suma',sum)




#%% iterando sobre conjunto
s = {1,2,3,4}  # conjunto 
for x in s:
    print(x,end=' ')  # para que no meta \n


#%% sobre diccionarios
dic = {'alicia': 12, 'luis': 4, 'ana': 9}

for x in dic:  # escribe solo las claves
    print(x,end=' ')

#%%
for x in dic:  # claves y valores
    print(x, 'tiene', dic[x])









#%%
''' 
el "for" y el "if" posibilitan las 
LISTAS INTENSIONALES
(comprehension lists)
'''
 

#%%
ls = [x for x in range(10)]  # "lista de los x con x en el rango [0,10)""
print(ls)

# no es lo mismo que print(range(10))??


#%%
ls = [x for x in range(20) if x%2!=0]  
print(ls)



#%%
''' SINTAXIS GENERAL
lista = [expr for var in estr_iterable if condicion]
'''


#%% 
num = 126
divisores = [x for x in range(1,num+1) if num%x==0]
print(divisores)

esPrimo = divisores==[1,num]
print(esPrimo)

#%% filtro de dígitos
s = "y5o n0o qui1ero9 digitos"
lst = [c for c in s if c.isalpha() or c==' ']
print(lst)

#%% reconstruccion como cadena de texto
s2 = ''.join(lst)  
print(s2)





#%% EXCEPCIONES

a = 5
b = 0


try:
    x = a/b
except ZeroDivisionError:
    print("División por 0")
except AritmeticError: 
    print("Error aritmético")
except KeyError:
    print("La clave no existe")
else:
    print("No hay error")
finally:
    print("yo me ejecuto en todo caso...")