# Foco
### Descripción
Foco es una aplicación de Windows orientada a controlar la temperatura de un horno de cerámica a leña. Permite ver gráficamente cosas como la temperatura actual la deseada y el tiempo de cocción.

### General

El proyecto puede exportarse para 64 bits si se hace con la librería `pyinstaller` desde una instalación de python para 64 bits.

Se puede generar un entorno virtual con python 3.7.9 por si se deseara exportar una ueva versión para 32 bits.

### Librerías necesarias
Las librerías que se utilizan son:

`customtkinter`

`matplotlib` (se usa la versión 2.2.2 en el entron virtual ya que el resto presentan fallas)

`pygame`

`packaging` (si se usa python 3.7.9)

`pyinstaller` (para generar el .exe)

IMPORTANTE: en caso de usar Python 3.7.9 se deben instalar las librerías de la carpeta "libs_for_py37" de la siguiente manera
`pip install /libs_for_py37/matplotlib-3.3.4-cp37-cp37m-win32.whl`

### Creando el ejecutable
Una vez instalado pyinstaller, crear el ejecutable a partir del script de python es tan simple como ejecutar el comando

`pyinstaller -F -n "Foco" -i "recursos\Logo.ico" -w Foco.py`

En el que `-F` es para que solo se genere un archivo `-n "Foco"` para darle el nombre a la app, `-i "recursos\Logo.ico"` para agregarle el ícono al .exe y `-w` para que la app se corra en una ventana de Windows.

Finalmente, el .exe se almacenará en `\dist` y será necesario moverlo a la carpeta raíz para que pueda ser ejecutado.


## English
### Translation
#### Description
Foco is a Windows application designed to control the temperature of a wood-fired ceramic kiln. It allows to graphically display things like the current temperature, the desired temperature, and the cooking time.

#### General

The project can be exported for 64-bit if done with the `pyinstaller` library from a 64-bit Python installation.

A virtual environment can be created with Python 3.7.9 in case one wishes to export a new version for 32 bits.

#### Required Libraries
The libraries used are:

`customtkinter`

`matplotlib` (version 2.2.2 is used in the virtual environment since the others present issues)

`pygame`

`packaging` (if using Python 3.7.9)

`pyinstaller` (to generate the .exe)

IMPORTANT: If using Python 3.7.9, the libraries from the "libs_for_py37" folder must be installed as follows:
`pip install /libs_for_py37/matplotlib-3.3.4-cp37-cp37m-win32.whl`

#### Creating the Executable
Once pyinstaller is installed, creating the executable from the Python script is as simple as running the command

`pyinstaller -F -n "Foco" -i "resources\Logo.ico" -w Foco.py`

Where `-F` is to generate only one file, `-n "Foco"` to name the app, `-i "resources\Logo.ico"` to add the icon to the .exe, and `-w` so that the app runs in a Windows window.

Finally, the .exe will be stored in `\dist` and it will be necessary to move it to the root folder for it to be executed.