from os import mkdir

try:
    mkdir('resources')
except FileExistsError:
    pass
