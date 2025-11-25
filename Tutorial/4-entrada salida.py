#%% leer un arvhivo y escribir su
# contenido en pantalla

f = open('4-entrada salida.py','r')  # r=read (w=write)

st = f.read()   # lee todo el contenido de una vez
print(st)

f.close()



#%% leer linea a linea
# y escribir solo lineas comentario

f = open('4-entrada salida.py','r')  # r=read (w=write)

for line in f:   # iterador para leer línea a línea
    if line[0]=='#':
        print(line,end='')

f.close()


#%% contar numero de print
f = open('4-entrada salida.py','r') 

n = 0
for line in f:
    n += line.count('print')

print("num prints:",n)
f.close()


#%% escritura
f = open('test','w')

f.write('Algunas cosas\n')
f.write('Algunas cosas mas')

f.close()


#%% mirar directorio
import os

curr = os.getcwd()
print(curr)

fs = os.listdir()
print(fs)

# mkdir, remove, chdir ...