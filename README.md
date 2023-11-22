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

`pyinstaller` (para generar el .exe)


## English
### Description
Foco is a Windows application designed to control the temperature of a wood-fired ceramic kiln. It allows you to graphically view things like the current temperature, the desired temperature, and the cooking time.

### General
The project can be exported for 64-bit systems using the `pyinstaller` library from a 64-bit Python installation.

A virtual environment with Python 3.7.9 can be created in case one wishes to export a new version for 32-bit systems.

### Necessary Libraries
The libraries used are:

`customtkinter`

`matplotlib` (version 2.2.2 is used in the virtual environment as other versions have issues)

`pygame`

`pyinstaller` (to generate the .exe file)
