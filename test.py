from Backend import *
back = Backend()
data = back.visualizar()
id = back.get_id()
print(f'{data}\n\n')

back.excluir(1)

print(data)