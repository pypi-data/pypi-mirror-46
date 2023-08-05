# GET VARIABLE NAME
Returns the variable name of an object in current program/script as a string.
**Usage:**
get_variable_name(var)

return

**EXAMPLE**
`
>>> import get_variable_name
>>>
>>> foo = ['bar', True, 'buzz']
>>> cat = get_variable_name(foo)
>>> print(foo)
['bar', True, 'buzz']
>>> print(cat)
foo
>>> print(type(foo))
list
>>> print(type(cat))
str
`


