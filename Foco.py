import customtkinter as ctk
from customtkinter import CTkImage
import tkinter as tk
from pygame import mixer
from tkinter import ttk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from tkinter import filedialog
import tkinter.messagebox as messagebox
import csv
from PIL import Image, ImageTk
import io
import time

initial = time.time()
contador_value = 0
deseada = 0
tasa = 3
temperaturas = []
filepath = ""
close = False


class Foco:
    btn_color = "#9C6B5E"
    bg_color = "#55433B"

    def size_x(self, widget, mult):
        return int(mult * (widget._current_width // 100))

    def size_y(self, widget, mult):
        return int(mult * (widget._current_height // 100))

    def __init__(self, root):
        # ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
        # ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        self.root = root

        mixer.init()
        mixer.music.load("recursos/audio.wav")
        self.sonido_alerta = mixer.Sound("recursos/audio.wav")

        root.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

        self.init_values()

        self.columna_izquierda()

        self.columna_derecha()

    def reproducir_alerta(self):
        # Reproducir el sonido de alerta
        self.sonido_alerta.play()

        # Actualizar el tiempo del último alerta
        self.ultimo_alerta_tiempo = self.contador_value

    def init_values(self):
        self.first_time = True
        self.initial = time.time()
        self.contador_value = contador_value
        self.is_contador_running = False
        self.update_interval = 1000
        self.deseada = deseada
        self.tasa = tasa
        self.temperaturas = temperaturas
        self.intervalo_alerta = 10

    def columna_izquierda(self):
        frame_izquierda = ctk.CTkFrame(
            root,
            width=self.size_x(root, 20),
            height=self.size_y(root, 100),
            fg_color=self.bg_color,
            bg_color=self.bg_color,
        )
        frame_izquierda.pack(side="left", fill="both", expand=True)

        self.mostrar_contador(frame_izquierda)

        self.mostrar_botones_contador(frame_izquierda)

        self.mostrar_temp_deseada(frame_izquierda)

        self.mostrar_ingreso_temp(frame_izquierda)

        self.mostrar_ingreso_alerta(frame_izquierda)

    def columna_derecha(self):
        frame_derecha = ctk.CTkFrame(
            root,
            width=self.size_x(root, 80),
            height=self.size_y(root, 100),
            fg_color="transparent",
        )
        frame_derecha.pack(fill="both", expand=True)

        self.frame_derecha = frame_derecha

        self.mostrar_grafico(frame_derecha)

    def mostrar_grafico(self, root):
        # Datos del gráfico
        x = []
        y = []
        y2 = []
        for tiempo, temp, deseada, tasa in self.temperaturas:
            x.append(tiempo / 60)
            y.append(temp)
            y2.append(deseada)

        fig = plt.figure()

        # Crear el gráfico
        plt.grid(linestyle="-", linewidth=1)
        plt.plot(x, y, "-o")
        plt.plot(x, y2, "--ro")

        # insert the plot into the tkinter window
        canvas = FigureCanvasTkAgg(fig, root)
        self.canvas = canvas
        canvas.draw()
        canvas.get_tk_widget().place(
            relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1
        )
        self.frame_derecha.pack(fill="both", expand=True)

    def mostrar_contador(self, root):
        self.label_contador = ctk.CTkLabel(
            root,
            text="00:00:00",
            font=("Arial Rounded MT Bold", self.size_y(root, 7)),
            text_color="#FFFFFF",
        )
        self.label_contador.pack(pady=self.size_y(root, 5))

    def mostrar_botones_contador(self, root):
        frame_botones = ctk.CTkFrame(
            root,
            fg_color="transparent",
        )  # Crear un frame para los botones
        frame_botones.pack(pady=self.size_y(root, 1))  # Los botones se empaquetarán en la misma fila

        # Crear los iconos de los botones
        y = self.size_y(root, 3)
        x = self.size_y(root, 3)
        y_btn = self.size_y(root, 6)
        x_btn = self.size_y(root, 6)
        play_icon = ctk.CTkImage(Image.open("recursos/play.png"), size=(x, y))
        pausa_icon = ctk.CTkImage(Image.open("recursos/pausa.png"), size=(x, y))
        reset_icon = ctk.CTkImage(Image.open("recursos/reiniciar.png"), size=(x, y))
        clock_icon = ctk.CTkImage(Image.open("recursos/reloj.png"), size=(x, y))
        temp_icon = ctk.CTkImage(Image.open("recursos/temperatura.png"), size=(x, y))

        button_iniciar = ctk.CTkButton(
            frame_botones,
            text=None,
            image=play_icon,
            fg_color=self.btn_color,
            width=x_btn,
            height=y_btn,
            command=self.iniciar_contador,
        )
        button_iniciar.pack(side="left", padx=x/2)

        button_pausar = ctk.CTkButton(
            frame_botones,
            text=None,
            image=pausa_icon,
            fg_color=self.btn_color,
            width=x_btn,
            height=y_btn,
            command=self.pausar_contador,
        )
        button_pausar.pack(side="left", padx=x/2)

        button_reset = ctk.CTkButton(
            frame_botones,
            text=None,
            image=reset_icon,
            fg_color=self.btn_color,
            width=x_btn,
            height=y_btn,
            command=self.reset_contador,
        )
        button_reset.pack(side="left", padx=x/2)

        button_ingresar = ctk.CTkButton(
            frame_botones,
            text=None,
            image=clock_icon,
            fg_color=self.btn_color,
            width=x_btn,
            height=y_btn,
            command=self.mostrar_hora_inicio,
        )
        button_ingresar.pack(side="left", padx=x/2)

        button_ingresar_temp = ctk.CTkButton(
            frame_botones,
            text=None,
            image=temp_icon,
            fg_color=self.btn_color,
            width=x_btn,
            height=y_btn,
            command=self.mostrar_temp_inicio,
        )
        button_ingresar_temp.pack(side="left", padx=x/2)

    def mostrar_temp_inicio(self):
        # Crear una nueva ventana para ingresar la temperatura
        temperatura_window = ctk.CTkToplevel(self.root)
        temperatura_window.after(0, lambda: temperatura_window.wm_attributes("-topmost", True))
        temperatura_window.title("Temperatura inicial")


        ctk.CTkLabel(
            temperatura_window,
            text="Ingrese la temperatura inicial",
            font=("Arial Rounded MT Bold", 20)
        ).pack(padx = 10, pady = 10)

        temperatura_entry = ctk.CTkEntry(
            temperatura_window,
            placeholder_text="Temperatura (°C)"
        )
        temperatura_entry.pack(pady=10)

        def confirmar_temperatura_inicial(temperatura):
            try:
                temperatura = float(temperatura)
                self.deseada = temperatura
                temperatura_window.destroy()
            except ValueError:
                print("Error: Ingresa un valor numérico válido para la temperatura inicial.")

        confirm_button = ctk.CTkButton(
            temperatura_window,
            text="Confirmar",
            command=lambda: [confirmar_temperatura_inicial(temperatura_entry.get())],
            fg_color=self.btn_color,
            text_color="#FFFFFF"
        )
        confirm_button.pack(pady=10)

    def mostrar_temp_deseada(self, root):
        frame_temp_deseada = ctk.CTkFrame(
            root,
            fg_color="transparent",
        )  # Crear un frame para el mensaje de la temperatura
        frame_temp_deseada.pack(
            pady=self.size_y(root, 5)
        )

        label_temp_deseada = ctk.CTkLabel(
            frame_temp_deseada,
            text="Temperatura deseada:",
            font=("Arial Rounded MT Bold", self.size_y(root, 2.5)),
            text_color="#FFFFFF"
        )
        label_temp_deseada.pack(side="top", padx = self.size_x(root, 1.5))

        self.label_deseada = ctk.CTkLabel(
            frame_temp_deseada,
            text=f"{self.deseada:.2f}°C",
            font=("Arial Rounded MT Bold", self.size_y(root, 10)),
            text_color="#FFFFFF"
        )
        self.label_deseada.pack(side="top", padx = 2)

        # Imagen para el boton
        opciones_icon = ctk.CTkImage(Image.open("recursos/opciones.png"), size=(self.size_y(root, 2), self.size_y(root, 2)))

        button_iniciar = ctk.CTkButton(
            frame_temp_deseada,
            text=None,
            image=opciones_icon,
            fg_color=self.btn_color,
            width=self.size_y(root, 4),
            height=self.size_y(root, 4),
            command=self.ventana_tasa,
        )
        button_iniciar.pack(side="top", padx=self.size_x(root, 3))

    def mostrar_ingreso_temp(self, root):
        frame = ctk.CTkFrame(
            root,
            fg_color="transparent",
        )
        frame.pack(pady=self.size_y(root, 2))

        # Etiqueta de error para mostrar mensajes de error
        error_label_t = ctk.CTkLabel(
            root,
            text="",
            font=("Arial Rounded MT Bold", self.size_y(root, 2)),
            text_color="red",
        )
        error_label_t.pack(side="top")


        frame_botones = ctk.CTkFrame(
            frame,
            fg_color="transparent",
        )
        frame_botones.pack(side="bottom", pady=self.size_y(root, 1.5))

        label_ingreso_temp = ctk.CTkLabel(
            frame,
            text="Ingresar temperatura:",
            font=("Arial Rounded MT Bold", self.size_y(root, 2.5)),
            text_color="#FFFFFF"
        )
        label_ingreso_temp.pack(side="left", padx=self.size_x(root, 1.5))

        ingreso_temp = ctk.CTkEntry(
            frame,
            width=5 * self.size_y(root, 2.5),
            font=("Arial Rounded MT Bold", self.size_y(root, 2.5)),
            text_color="black",
        )
        ingreso_temp.pack(side="left")

        ingreso_temp.bind("<Return>", lambda event: [ingresar_temp(), ingreso_temp.delete(0, tk.END)])

        # Imagenes para los botones
        x = self.size_y(root, 2)
        y = self.size_y(root, 2)
        x_btn = self.size_y(root, 4)
        y_btn = self.size_y(root, 4)
        enter_icon = ctk.CTkImage(Image.open("recursos/enter.png"), size=(x, y))
        lista_icon = ctk.CTkImage(Image.open("recursos/lista.png"), size=(x, y))

        def ingresar_temp():
            try:
                #consider decimal point as a dot or a comma
                temp = float(ingreso_temp.get().replace(",", "."))
                self.temperaturas.append(
                    (self.contador_value, temp, self.deseada, self.tasa)
                )  # Agregar la temperatura a la lista
                # update error_label_t text to ""
                error_label_t.configure(text="")
                self.frame_derecha.destroy()
                self.columna_derecha()
                self.guardar_datos()
                plt.close() #cierro el grafico anterior
            except ValueError:
                # Si ocurre un error al convertir el valor a float, muestra un mensaje de error
                error_label_t.configure(text="Número invalido.")

        boton_ingresar = ctk.CTkButton(
            frame_botones,
            text=None,
            image=enter_icon,
            fg_color=self.btn_color,
            width=x_btn,
            height=y_btn,
            command=lambda: [ingresar_temp(), ingreso_temp.delete(0, tk.END)],
        )
        boton_ingresar.pack(side= "left", padx=x_btn/2)

        boton_lista = ctk.CTkButton(
            frame_botones,
            text=None,
            image=lista_icon,
            fg_color=self.btn_color,
            width=x_btn,
            height=y_btn,
            command=self.mostrar_tabla_temperaturas,
        )
        boton_lista.pack(side= "left", padx=x_btn/2)

    def mostrar_ingreso_alerta(self, root):
        frame_interval = ctk.CTkFrame(root, fg_color="transparent")
        frame_interval.pack(side="bottom", pady=self.size_y(root, 10))

        frame_temp = ctk.CTkFrame(frame_interval, fg_color="transparent")
        frame_temp.pack(pady=10)

        label_tasa = ctk.CTkLabel(
            frame_temp,
            text="Alertar cada",
            font=("Arial Rounded MT Bold", self.size_y(root, 2)),
            text_color="#FFFFFF"
        )
        label_tasa.pack(side="left", padx=5)

        self.entry_intervalo = ctk.CTkEntry(
            frame_temp,
            width=2 * self.size_y(root, 2.5),
            font=("Arial Rounded MT Bold", self.size_y(root, 2)),
            text_color="black",
            placeholder_text="10",
        )
        self.entry_intervalo.pack(side="left", padx=5)

        self.entry_intervalo.bind("<Return>", lambda event: self.actualizar_intervalo())

        label_unidad = ctk.CTkLabel(
            frame_temp,
            text="minutos",
            font=("Arial Rounded MT Bold", self.size_y(root, 2)),
            text_color="#FFFFFF"
        )
        label_unidad.pack(side="left", padx=5)

        x = self.size_y(root, 2)
        y = self.size_y(root, 2)
        x_btn = self.size_y(root, 4)
        y_btn = self.size_y(root, 4)
        enter_icon = ctk.CTkImage(Image.open("recursos/enter.png"), size=(x, y))

        boton_actualizar = ctk.CTkButton(
            frame_temp,
            text=None,
            image=enter_icon,
            fg_color=self.btn_color,
            width=x_btn,
            height=y_btn,
            command=self.actualizar_intervalo,
        )
        boton_actualizar.pack(padx=self.size_x(root, 1))

        # Etiqueta de error para mostrar mensajes de error
        self.error_label_intervalo = ctk.CTkLabel(
            frame_interval,
            text="",
            font=("Arial Rounded MT Bold", self.size_y(root, 2)),
            text_color="red",
        )
        self.error_label_intervalo.pack()

    def iniciar_contador(self):
        if self.first_time: # para evitar que arranque con otro valor si se pone "play" una rato despues de abrir la app
            self.initial = time.time() - self.contador_value - 1
            self.first_time = False
        if not self.is_contador_running:
            self.is_contador_running = True
            self.ultimo_alerta_tiempo = self.contador_value
            self.actualizar_contador()

    def actualizar_contador(self):
        if not self.is_contador_running:
            return

        # tiempo_actual = time.time()
        if (
            self.contador_value - self.ultimo_alerta_tiempo
            >= self.intervalo_alerta * 60
        ):
            self.reproducir_alerta()

        #self.deseada = (self.contador_value / 60) * self.tasa

        # Para evitar que aumante en la primera iteración
        if self.contador_value:
            self.deseada = self.deseada + self.tasa / 60
        self.label_deseada.configure(text=f"{self.deseada:.2f}°C")

        tiempo_formateado = self.obtener_tiempo_formateado(self.contador_value)
        self.label_contador.configure(text=tiempo_formateado)
        self.contador_value = time.time() - self.initial

        self.root.after(self.update_interval, self.actualizar_contador)

    def reset_contador(self):
        self.is_contador_running = False
        self.guardar_datos()
        self.contador_value = 0
        self.initial = time.time()
        self.deseada = 0
        self.temperaturas.clear()
        self.label_contador.configure(text="00:00:00")

    def pausar_contador(self):
        self.is_contador_running = False

    def actualizar_tasa(self):
        try:
            self.tasa = float(self.tasa_aumento.get())
            self.error_label.configure(text="")
        except ValueError:
            # Si ocurre un error al convertir el valor a float, muestra un mensaje de error
            self.error_label.configure(
                text="Error: Número inválido (el punto decimal es '.')"
            )
            print("Error: Ingresa un valor numérico válido para la tasa de aumento.")

    def actualizar_intervalo(self):
        try:
            self.intervalo_alerta = float(self.entry_intervalo.get())
            self.error_label_intervalo.configure(text="")
        except ValueError:
            # Si ocurre un error al convertir el valor a float, muestra un mensaje de error
            self.error_label_intervalo.configure(
                text="Error: Número inválido (el punto decimal es '.')"
            )
            print("Error: Ingresa un valor numérico válido para la tasa de aumento.")

    def obtener_tiempo_formateado(self, segundos):
        segundos = int(segundos)
        horas = segundos // 3600
        minutos = (segundos % 3600) // 60
        segundos = segundos % 60

        tiempo_formateado = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
        return tiempo_formateado

    def mostrar_tabla_temperaturas(self):
        tabla_window = ctk.CTkToplevel(self.root)
        tabla_window.after(0, lambda: tabla_window.wm_attributes("-topmost", True))
        tabla_window.title("Tabla de Temperaturas")
        # Open the window at the top left corner of the screen
        tabla_window.geometry("+0+0")

        frame_tabla = ctk.CTkFrame(
            tabla_window,
            fg_color="transparent",
        )
        frame_tabla.pack(side="top", fill="both", expand=True, pady=10, padx=10)

        tabla = ttk.Treeview(
            frame_tabla, columns=("Index", "Tiempo", "Temperatura", "Deseada", "Tasa de aumento"), show="headings"
        )
        tabla.heading("Index", text="")
        tabla.heading("Tiempo", text="Tiempo")
        tabla.heading("Temperatura", text="Temperatura")
        tabla.heading("Deseada", text="Temperatura deseada")
        tabla.heading("Tasa de aumento", text="Tasa de aumento (°C/min)")

        # Agregar los datos de la lista de temperaturas a la tabla
        i = 0
        for tiempo, temperatura, deseada, tasa in self.temperaturas:
            tabla.insert(
                "",
                "end",
                values=(
                    i,
                    self.obtener_tiempo_formateado(tiempo),
                    temperatura,
                    f"{deseada:.2f}",
                    tasa,
                ),
            )
            i += 1

        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        tabla.column("Index", anchor=tk.CENTER, width=50)
        tabla.column("Tiempo", anchor=tk.CENTER)
        tabla.column("Temperatura", anchor=tk.CENTER)
        tabla.column("Deseada", anchor=tk.CENTER)
        tabla.column("Tasa de aumento", anchor=tk.CENTER)

        # Crear la barra lateral
        scrollbar = ctk.CTkScrollbar(frame_tabla, command=tabla.yview)
        tabla.configure(yscrollcommand=scrollbar.set)

        # Ubicar la tabla y la barra lateral en la ventana
        tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        ctk.CTkLabel(
            tabla_window,
            text="Eliminar fila:",
            font=("Arial Rounded MT Bold", self.size_y(root, 3)),
            #text_color="#FFFFFF"
        ).pack(side="left", pady=10, padx=10)

        self.selected_row = ctk.CTkEntry(
            tabla_window,
            width=5 * self.size_y(root, 2.5),
            font=("Arial Rounded MT Bold", self.size_y(root, 3)),
            text_color="black",
        )
        self.selected_row.pack(side="left", pady=10, padx=10)

        def eliminar_fila():
            fila = self.selected_row.get()
            try:
                self.temperaturas.pop(int(fila))
                self.mostrar_tabla_temperaturas()
                self.frame_derecha.destroy()
                self.columna_derecha()
                plt.close()
            except IndexError:
                print("Error: El índice ingresado no existe.")
                self.mostrar_tabla_temperaturas()

        self.selected_row.bind("<Return>", lambda event: [eliminar_fila(), tabla_window.destroy()])

    def cerrar_ventana(self):
        if self.contador_value:
            if not self.confirmar_salida():
                return
        plt.close()
        root.destroy()

    def confirmar_salida(self):
        respuesta = messagebox.askyesno(
            "Confirmar Salida",
            "Hay una horneada en curso. ¿Estás seguro de que querés salir?",
            icon="warning",
        )
        if not respuesta:
            return False
        return True

    def guardar_datos(self):
        # Abrir un cuadro de diálogo para que el usuario seleccione la ubicación y el nombre del archivo.
        # file_path = filedialog.asksaveasfilename(
        #     defaultextension=".csv",
        #     filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
        # )
        if filepath:
            with open((filepath + ".csv"), "w", newline="") as file:
                # Crear el objeto writer para escribir los datos en formato CSV.
                writer = csv.writer(file)

                # Escribir la primera fila con los nombres de las columnas.
                writer.writerow(
                    [
                        "Tiempo",
                        "Temperatura (°C)",
                        "Temperatura deseada (°C)",
                        "Tasa de aumento (°C/min)",
                    ]
                )

                # Guardar los datos en el archivo CSV.
                for tiempo, temp, deseada, tasa in self.temperaturas:
                    writer.writerow(
                        [self.obtener_tiempo_formateado(tiempo), temp, deseada, tasa]
                    )
        #graph_file_path = os.path.splitext(filepath)[0] + ".png"
        self.exportar_imagen(filepath + ".png") #graph_file_path

    def exportar_imagen(self, file_path):
        # Crear un objeto BytesIO para guardar la imagen en memoria.
        image_buffer = io.BytesIO()

        # Guardar la imagen del gráfico en el objeto BytesIO.
        self.canvas.print_png(image_buffer)

        # Guardar la imagen en disco.
        with open(file_path, "wb") as file:
            file.write(image_buffer.getvalue())

    def ventana_tasa(self):
        tasa_window = ctk.CTkToplevel(self.root)
        tasa_window.after(0, lambda: tasa_window.wm_attributes("-topmost", True))
        tasa_window.title("Modificar tasa de aumento")

        frame_texto = ctk.CTkFrame(
            tasa_window,
            fg_color="transparent",
        )
        frame_texto.pack(side="top", fill="both", expand=True, pady=10, padx=10)

        label_tasa = ctk.CTkLabel(
            frame_texto,
            text="Tasa de aumento:",
            font=("Arial Rounded MT Bold", self.size_y(root, 2.5)),
        )
        label_tasa.pack(side="left", padx=5)

        tasa_aumento = ctk.CTkEntry(
            frame_texto,
            width=3 * self.size_y(root, 2.5),
            font=("Arial Rounded MT Bold", self.size_y(root, 2.5)),
            placeholder_text=str(self.tasa),
        )
        tasa_aumento.pack(side="left", padx=5)

        

        def actualizar_tasa():
            try:
                self.tasa = float(tasa_aumento.get())
                error_label.pack_forget()
                tasa_window.destroy()
            except ValueError:
                error_label.pack(side="bottom")
                print("Error: Ingresa un valor numérico válido para la tasa de aumento.")

        tasa_aumento.bind("<Return>", lambda event: [actualizar_tasa()])

        label_unidad = ctk.CTkLabel(
            frame_texto,
            text="°C por minuto",
            font=("Arial Rounded MT Bold", self.size_y(root, 2.5)),
        )
        label_unidad.pack(side="left", padx=5)

        # Imagen para le boton
        y = self.size_y(root, 3)
        x = self.size_y(root, 3)
        y_btn = self.size_y(root, 5)
        x_btn = self.size_y(root, 5)
        enter_icon = ctk.CTkImage(Image.open("recursos/enter.png"), size=(x, y))

        boton_actualizar = ctk.CTkButton(
            frame_texto,
            text=None,
            image=enter_icon,
            width=x_btn,
            height=y_btn,
            fg_color=self.btn_color,
            command=actualizar_tasa,
        )
        boton_actualizar.pack(pady=10)

        # Etiqueta de error para mostrar mensajes de error
        error_label = ctk.CTkLabel(
            tasa_window,
            text="Error: Número inválido (el punto decimal es '.')",
            font=("Arial Rounded MT Bold", self.size_y(root, 2)),
            text_color="red",
        )
        error_label.pack_forget()

    def mostrar_hora_inicio(self):
        # Abro una nueva ventana para ingresar la hora de inicio
        hora_inicio_window = ctk.CTkToplevel(self.root)
        hora_inicio_window.after(0, lambda: hora_inicio_window.wm_attributes("-topmost", True))
        hora_inicio_window.title("Hora de inicio")
        
        # Creo un frame para el contenido
        hora_inicio_frame = ctk.CTkFrame(
            hora_inicio_window,
            fg_color="transparent"
        )
        hora_inicio_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Creo un label para el texto
        hora_inicio_label = ctk.CTkLabel(
            hora_inicio_frame,
            font=("Arial Rounded MT Bold", 20),
            text="Ingrese la hora de inicio"
        )
        hora_inicio_label.pack(pady=10)
        
        # Creo un sub-frame para empaquetar las entradas y el separador
        sub_frame = ctk.CTkFrame(hora_inicio_frame, fg_color="transparent")
        sub_frame.pack(side="top", pady=10)
        
        # Creo un entry para ingresar la hora de inicio
        hora_inicio_entry = ctk.CTkEntry(
            sub_frame,
            placeholder_text="HH",
            width=70
        )
        hora_inicio_entry.pack(side="left", pady=10)
        
        separador_label = ctk.CTkLabel(
            sub_frame, 
            text=":"
        )
        separador_label.pack(side="left", pady=10, padx=5)
        
        minuto_inicio_entry = ctk.CTkEntry(
            sub_frame,
            placeholder_text="MM",
            width=70
        )
        minuto_inicio_entry.pack(side="left", pady=10)

        def toggle_temperature_entry():
            if checkbox_var.get():
                pass
            else:
                # Opción marcada: No hacer nada
                self.mostrar_temp_inicio()

        # Variable para el estado de la casilla de verificación
        checkbox_var = ctk.BooleanVar()
        checkbox_var.set(True)

        # Casilla de verificación
        checkbox = ctk.CTkCheckBox(
            hora_inicio_frame,
            text="Calcular temperatura en base a la hora de inicio",
            variable=checkbox_var,
            command=toggle_temperature_entry
        )
        checkbox.pack(side="top", pady=10)

        def confirmar_hora_inicio():
            # Obtengo la hora ingresada
            hora_inicio = hora_inicio_entry.get()
            minuto_inicio = minuto_inicio_entry.get()

            #Transformo la hota ingresada en segundos
            hora_inicio = int(hora_inicio) * 3600 + int(minuto_inicio) * 60

            hora_actual = time.localtime(time.time())
            hora_actual = hora_actual.tm_hour * 3600 + hora_actual.tm_min * 60 + hora_actual.tm_sec

            self.initial = time.time() - hora_actual + hora_inicio
            self.contador_value = time.time() - self.initial


            # Actualizo la temperatura deseada
            if checkbox_var.get(): # Si la casilla está marcada calculo la temperatura en base a la hora de inicio
                self.deseada = (self.contador_value / 60) * self.tasa

            # Cierro la ventana
            hora_inicio_window.destroy()

        minuto_inicio_entry.bind("<Return>", lambda event: [confirmar_hora_inicio(), hora_inicio_window.destroy()])
        
        # Creo un boton para confirmar la hora
        hora_inicio_boton = ctk.CTkButton(
            hora_inicio_frame,
            text="Confirmar",
            text_color="#FFFFFF",
            fg_color=self.btn_color,
            command=confirmar_hora_inicio,
        )
        hora_inicio_boton.pack(side="bottom", pady=10)

class WelcomeWindow:
    btn_color = "#FFFFFF"
    bg_color = "#55433B"

    def size_x(self, widget, mult):
        return int(mult * (widget._current_width / 100))

    def size_y(self, widget, mult):
        return int(mult * (widget._current_height / 100))
    
    def __init__(self, root):
        self.root = root

        ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        root.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

        self.columna_izquierda(root)
        self.columna_derecha(root)

        # Crear una etiqueta con el mensaje de bienvenida


    def columna_izquierda(self, root):
        frame_izquierda = ctk.CTkFrame(
            root,
            width=int(root.winfo_screenwidth()*0.4),
            height=self.size_y(root, 100),
            fg_color=self.bg_color,
            bg_color=self.bg_color,
        )
        frame_izquierda.pack(side="left", fill="both", expand=True)

        #frame_izquierda.winfo_screenwidth


        # Cargar y mostrar la imagen
        img = Image.open("recursos/Square.png")  # Reemplazar con la ruta de tu imagen
        self.show_image(frame_izquierda, img)

    def show_image(self, parent, img):
        # Cargar la imagen con PIL y convertirla a formato compatible con CTkImage

        # Resize the image using resize() method
        resize_image = img.resize((self.size_x(parent, 100), self.size_x(parent, 100)))
        img = ImageTk.PhotoImage(resize_image)
        
        # create label and add resize image
        label1 = tk.Label(parent, image=img, bg=self.bg_color)
        label1.image = img
        label1.pack(expand = True, pady=0, padx=0)


    def columna_derecha(self, root):

        def buttons(root):
            frame_botones = ctk.CTkFrame(
                root,
                fg_color="transparent",
            )  # Crear un frame para los botones
            frame_botones.pack()  # Los botones se empaquetarán en la misma fila

            # Crear los iconos de los botones
            y = self.size_y(root, 10)
            x = self.size_y(root, 10)
            y_btn = self.size_y(root, 10)
            x_btn = self.size_y(root, 10)
            mas_icon = ctk.CTkImage(Image.open("recursos/btn_mas.png"), size=(x, y))
            file_icon = ctk.CTkImage(Image.open("recursos/btn_file.png"), size=(x, y))

            button_new = ctk.CTkButton(
                frame_botones,
                corner_radius=int(x_btn/4),
                border_spacing=int(x_btn/4),
                text=None,
                image=mas_icon,
                fg_color=self.btn_color,
                width=x_btn,
                height=y_btn,
                command=self.new_project,
            )
            button_new.pack(side="left", padx=int(x_btn/1.5))

            button_file = ctk.CTkButton(
                frame_botones,
                corner_radius=int(x_btn/4),
                border_spacing=int(x_btn/4),
                text=None,
                image=file_icon,
                fg_color=self.btn_color,
                width=x_btn,
                height=y_btn,
                command=self.load_csv,
            )
            button_file.pack(side="left", padx=int(x_btn/1.5))

        def show_image(parent, img):
            # Cargar la imagen con PIL y convertirla a formato compatible con CTkImage

            # Resize the image using resize() method
            mult = parent._current_width / img.width
            x = int(img.width * mult)
            y = int(img.height * mult)
            resize_image = img.resize((x, y))
            img = ImageTk.PhotoImage(resize_image)
            
            # create label and add resize image
            label1 = tk.Label(parent, image=img, bg=self.bg_color)
            label1.image = img
            label1.pack(side = "top", padx=0)

        frame = ctk.CTkFrame(
            root,
            width=int(root.winfo_screenwidth()*0.6),
            height=self.size_y(root, 100),
            fg_color=self.bg_color,
            bg_color=self.bg_color,
        )
        frame.pack(side="left", fill="both", expand=True)

        
        frame_spacing = ctk.CTkFrame(
            frame,
            height=int(root.winfo_screenheight()*0.1),
            fg_color=self.bg_color,
            bg_color=self.bg_color,
        )
        frame_spacing.pack(side="top")

        
        img = Image.open("recursos/welcome_label.png")  # Reemplazar con la ruta de tu imagen
        show_image(frame, img)

        buttons(frame)


    def load_csv(self):
        global filepath
        # open file dialog box to select CSV file
        # The dialogue box has a title "Open"
        filepath = filedialog.askopenfilename(
            title="Cargar datos anteriores", filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        # print the location of the file
        if filepath:
            global temperaturas
            global contador_value
            global deseada
            global tasa
            global initial
            print("Cargando la data...\n")
            #read the csv, avoid the first row and append the data to the list keeping the format (hora, temp, temp_deseada, tasa)
            with open(filepath, newline="") as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    last_time = row[0].split(":") #split the time in hours, minutes and seconds
                    last_time = int(last_time[0]) * 3600 + int(last_time[1]) * 60 + int(last_time[2])
                    temp = float(row[1])
                    temp_deseada = float(row[2])
                    tasa = float(row[3])
                    temperaturas.append(
                        (last_time, temp, temp_deseada, tasa)
                    )
                # update the globals with the last values
                initial = time.time() - last_time
                contador_value = last_time
                deseada = temp_deseada
                tasa = tasa
        else:
            return

        self.root.destroy()

    def new_project(self):
        global filepath
        # Función para iniciar un proyecto nuevo
        # Aquí puedes añadir la lógica para iniciar un nuevo proyecto
        print("Nuevo proyecto iniciado")
        # choose a name and a location for the new project
        # The dialogue box has a title "Save"
        try:
            filepath = filedialog.asksaveasfilename(
                title="Guardar el nuevo proyecto", filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
            )
        except:
            print("Error al crear el archivo")
        if filepath:
            print(filepath)
            self.root.destroy()

    def cerrar_ventana(self):
        global close
        close = True
        self.root.destroy()


def root_init():
    root = ctk.CTk()
    root.iconbitmap("recursos\Logo.ico")	
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
    root.after(0, lambda: root.state("zoomed"))
    root.title("Foco - Control de Horneado")
    ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
    ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
    return root


if __name__ == "__main__":
    root = root_init()
    os.system("cls")
    WelcomeWindow(root)
    root.mainloop()
    if not close:
        root = root_init()
        os.system("cls")
        print("Bienvenido a Foco")
        app = Foco(root)
        root.mainloop()
