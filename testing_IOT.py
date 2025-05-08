def cube(x): return x*x*x


cube(5)



#********************MAPEO DE FUNCIONES**************************** 
"""
>>> def cube(x): return x*x*x
... 
>>> cube(5)
125
>>> list(map(cube, range(1,11)))
[1, 8, 27, 64, 125, 216, 343, 512, 729, 1000]
>>> list(map(cube, range(0,11)))
[0, 1, 8, 27, 64, 125, 216, 343, 512, 729, 1000]
>>> list(map(cube, range(5,11)))
[125, 216, 343, 512, 729, 1000]

"""



"""

>>> 

>>> l1 = [1,2,3,4,5,6,7,8,9]
>>> l2 = [9,8,7,6,5,4,3,2,1]
>>> l1
[1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> l2
[9, 8, 7, 6, 5, 4, 3, 2, 1]
>>> def add(x,y): return x+y
... 
>>> list(map(add,l1,l2))
[10, 10, 10, 10, 10, 10, 10, 10, 10]
>>> 

"""






"""

Listas por comprension

yntaxError: invalid syntax
>>> [['el cubo de:',x,'es',x*x*x] for x in l1 if x > 6]
[['el cubo de:', 7, 'es', 343], ['el cubo de:', 8, 'es', 512], ['el cubo de:', 9, 'es', 729]]
>>> l3 = [['el cubo de:',x,'es',x*x*x] for x in l1 if x > 6]
>>> l3[0][0] + l3[0][1] + l3[0][2]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: can only concatenate str (not "int") to str
>>> l3 = [['el cubo de:',x,'es',x*x*x] for x in l1 if x > 6]
>>> l3[0][0] + l3[0][1] + l3[0][2] + l3[0][3]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: can only concatenate str (not "int") to str
>>> print(l3[0][0] , l3[0][1] , l3[0][2] , l3[0][3])
el cubo de: 7 es 343


"""


#---------------------Diccionarios
"""
>>> d1 = {'Jack',4048,'Shape':4139}
  File "<stdin>", line 1
    d1 = {'Jack',4048,'Shape':4139}
                             ^
SyntaxError: invalid syntax
>>> d1 = {'Jack':4048,'Shape':4139}
>>> d1
{'Jack': 4048, 'Shape': 4139}
>>> d1['Jack']
4048
>>> d1['Shape']
4139

"""


# Tener cuidado con .keys(), ya que no devuelve una lista, es el resultado de una funcion
# Por lo tanto hay que ponerle list(d1.keys()), esto lo convierte a lista

"""
>>> d1 = {'Jack',4048,'Shape':4139}
  File "<stdin>", line 1
    d1 = {'Jack',4048,'Shape':4139}
                             ^
SyntaxError: invalid syntax
>>> d1 = {'Jack':4048,'Shape':4139}
>>> d1
{'Jack': 4048, 'Shape': 4139}
>>> d1['Jack']
4048
>>> d1['Shape']
4139

"""


""" Buscando un elemento en un diccionario

>>> 'otro' in d1
True



"""



"""
Convirtiendo listas por comprension a diccionarios

 l3 = dict([(x,x*x*x) for x in l1])

"""