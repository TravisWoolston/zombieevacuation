from datetime import datetime as dt

name = input('What is your name? ')
age = int(input('How old are you? '))
print('Hello {}! You were born in {}.'.format(name, dt.today().year - age))
