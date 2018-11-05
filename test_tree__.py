from anytree import Node, RenderTree

class symbol:
    def __init__(self, stype, name, vtype, info, line = 0):
        self.stype = stype #function, struct, variable, value
        self.name = name #name. If stype = 'value': it's value if constant, None if dependant of runtime
        self.vtype = vtype
        self.info = info #information about symbol:
        #function: [[arg1, opts], [arg2, opts], ...]
        #struct: [[member1, type], [member2, type], ...]
        #variable: []
        #value: []
        self.line = line
    def __str__(self):
        return self.name + "("+ self.vtype + ")"
    def __repr__(self):
    	return "("+ self.vtype + ")"

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
		return None

def Insertar(scope, sym):
	test_scope = scope
	if sym.name not in test_scope.name :
		test_scope.name[sym.name] = sym
	else :
		print("Ya existe una definicion previa de la variable ", sym.name)




def mostrarArbol(nodo):
	for pre, fill, node in RenderTree(nodo):
		print( pre, node.name)


global_node = Node(dict({})) # Se declara un nodo del arbol para las variables globales
actual_scope = global_node 	 # de ahora en adelante, actual_scope es el scope a utilizar

#actual_scope.name["x"] = 0 	# agrega x, y, z como variables en el scope global
#actual_scope.name["y"] = 0
#actual_scope.name["z"] = 0
Insertar(actual_scope, symbol("stype","x","int","info",0))
Insertar(actual_scope, symbol("stype","y","int","info",0))
Insertar(actual_scope, symbol("stype","z","int","info",0))

actual_scope = Initialize_scope(actual_scope) # crea un nuevo scope

#actual_scope.name["xx"] = 1 	# agrega xx, yy
#actual_scope.name["yy"] = 1
Insertar(actual_scope, symbol("stype","xx","int","info",0))
Insertar(actual_scope, symbol("stype","yy","int","info",0))

actual_scope = Finalize_scope(actual_scope) # termina el scope,  vuelve al scope global

#actual_scope.name["aa"] = 2		# agrega aa, bb al scope global
#actual_scope.name["bb"] = 2
Insertar(actual_scope, symbol("stype","aa","int","info",0))
Insertar(actual_scope, symbol("stype","bb","int","info",0))

actual_scope = Initialize_scope(actual_scope) # crea un nuevo scope

#actual_scope.name["a4"] = 10
Insertar(actual_scope, symbol("stype","a4","int","info",0))




actual_scope = Initialize_scope(actual_scope) # crea un nuevo scope
#actual_scope.name["a3"] = 9
Insertar(actual_scope, symbol("stype","a3","int","info",0))

actual_scope = Initialize_scope(actual_scope) # crea un nuevo scope 

#actual_scope.name["a2"] = 8
Insertar(actual_scope, symbol("stype","a2","int","info",0))

actual_scope = Initialize_scope(actual_scope) # crea un nuevo scope 
 

Consultar(actual_scope, "x")


mostrarArbol(global_node)


print({"a": symbol("stype","a2","int","info",0), "b":symbol("stype","a2","int","info",0)} )

 
