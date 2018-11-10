# Cmm-Compiler

## Requisitos:
La ejecución del analisador semántico requiere lo siguiente:
- Python 3 (sudo apt-get install python3)
- Biblioteca Anytree para Python3 (pip install anytree)

## Generar la tabla de símbolos de un programa
Para la generación de la tabla de simbolos de un programa hecho en lenguaje C+- debe ejecutar el programa test.py entregando como parámetro el nombre del archivo cmm.

Ejemplo:

python3 test.py MIPROGRAMA.CMM

## Códigos de ejemplos:

Existen los siguientes ejemplos con errores:

- python3 test.py test_sem/error_semantico_funcion.cmm
- python3 test.py test_sem/error_semantico_loop.cmm
- python3 test.py test_sem/error_semantico_struct.cmm
- python3 test.py test_sem/error_sem_redeclaracion.cmm
- python3 test.py test_sem/error_semantico_loop.cmm
- python3 test.py test_sem/error_sem_struct.cmm

Y los siguientes ejemplos sin errores: 

- python3 test.py test_sem/test.cmm
- python3 test.py test_sem/test_semantico_funcion.cmm

 
