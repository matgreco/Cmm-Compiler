# Cmm-Compiler

## Requisitos:
La ejecución del analisador semántico requiere lo siguiente:
- Python 3 (sudo apt-get install python3)
- Antlr4 Runtime (pip install antlr4-python3-runtime)
- Biblioteca Anytree para Python3 (pip install anytree)
- LLVM (sudo apt-get install llvm)

## Generar código LLVM IR de un programa Cmm
Para la generación de código de un programa hecho en lenguaje C+- debe ejecutar el programa test.py entregando como parámetro el nombre del archivo cmm.

Ejemplo:

python3 test.py MIPROGRAMA.CMM

Los archivos correspondientes deben estar en la misma ruta que el programa test.py.
El programa generará:
 - Un archivo .ll con el codigo LLVM IR.
 - Un archivo .s con el prorgrama objeto.
 - Un archivo de nombre out.out con el programa ejecutable.

## Códigos de ejemplos:

Existen los siguientes ejemplos. Debe primero generar el codigo y luego ejecutar el archivo .out.

- python3 test.py test3.cmm
- ./test3.out

- python3 test.py test4.cmm
- ./test4.out


 
