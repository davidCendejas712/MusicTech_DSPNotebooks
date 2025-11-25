#%%
class Complex:
    # constructura de la clase
    def __init__(self, r=0, i=0):
        self.real = r
        self.img  = i
    
    # método suma
    def add(self, c):
        self.real += c.real
        self.img  += c.img
    
    # metódo de escritura
    def write(self):
        print('{} + {}i'.format(self.real, self.img))
        # aqui  no va... print('{self.real} + {self.img}i')


    ## SOBRECARGA DE OPERADORES
    # otra forma: sobrecarga de str (conversión a string)
    def __str__(self):
        return '{} + {}i'.format(self.real, self.img)
        # no va... return '{self.real} + {self.img}i'

    # resta con sobrecarga: __sub__ (devuelve un nuevo complejo)
    def __sub__(self,c):
        return Complex(
            self.real - c.real,
            self.img  - c.img)


#%%
c1 = Complex(1,2)
c1.write()

#%%
c2 = Complex()
c2.write()

#%%
c3 = Complex(6)
c1.add(c3)

#%% utilizando la sobrecarga de conversión a strint (__str__)
print(c1)

#%% utilizanzo sobrecarga de __sub__ y __str__ 
print(c3-c1)

# tb hay herencia... no lo necesitaremos en ppio.
