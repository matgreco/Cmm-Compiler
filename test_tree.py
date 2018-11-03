from anytree import Node, RenderTree


def Initialize_scope(scope):
	nuevo_scope = Node(dict({}),scope)
	return nuevo_scope

def Finalize_scope(scope):
	nuevo_scope = scope.parent
	return nuevo_scope

def Consultar(scope, name):
	test_scope = scope
	while True :
		if name in test_scope.name:
			print("OK, simbolo encontrado, valor: ", test_scope.name[name])
			return test_scope.name[name]
		else:
			if test_scope.is_root == True:
				break
			test_scope = test_scope.parent

	if test_scope.is_root == True :
		print("Simbolo no existe")





def mostrarArbol(nodo):
	for pre, fill, node in RenderTree(nodo):
		print("%s%s" % (pre, node.name))


global_node = Node(dict({})) # Se declara un nodo del arbol para las variables globales
actual_scope = global_node 	 # de ahora en adelante, actual_scope es el scope a utilizar

actual_scope.name["x"] = 0 	# agrega x, y, z como variables en el scope global
actual_scope.name["y"] = 0
actual_scope.name["z"] = 0

actual_scope = Initialize_scope(actual_scope) # crea un nuevo scope

actual_scope.name["xx"] = 1 	# agrega xx, yy
actual_scope.name["yy"] = 1

actual_scope = Finalize_scope(actual_scope) # termina el scope,  vuelve al scope global

actual_scope.name["aa"] = 2		# agrega aa, bb al scope global
actual_scope.name["bb"] = 2

actual_scope = Initialize_scope(actual_scope) # crea un nuevo scope

actual_scope.name["a4"] = 10





actual_scope = Initialize_scope(actual_scope) # crea un nuevo scope
actual_scope.name["a3"] = 9

actual_scope = Initialize_scope(actual_scope) # crea un nuevo scope 

actual_scope.name["a2"] = 8

actual_scope = Initialize_scope(actual_scope) # crea un nuevo scope 
 

Consultar(actual_scope, "x")


mostrarArbol(global_node)

 
