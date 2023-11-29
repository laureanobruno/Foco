import customtkinter as ctk
import tkinter as tk
from pygame import mixer
from tkinter import ttk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from tkinter import filedialog
import tkinter.messagebox as messagebox
import csv
from PIL import Image
import io
import time
from Contador import Contador

contador = Contador()

class Window:
    
    btn_color = "#9C6B5E"
    bg_color = "#55433B"

    # size_x and size_y are relative mearuse units ------------------

    def size_x(self, widget, mult):
        return int(mult * (widget._current_width // 100))

    def size_y(self, widget, mult):
        return int(mult * (widget._current_height // 100))
    
    # ---------------------------------------------------------------
    
    def __init__(self, root):

        self.root = root

        
        root.iconbitmap("recursos\Logo.ico")

        # set window size and maximize it
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
        root.after(0, lambda: root.state("zoomed"))

        ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
        self.root.title("Foco - Control de Horneado")

        mixer.init()
        mixer.music.load("recursos/audio.wav")
        self.sonido_alerta = mixer.Sound("recursos/audio.wav")

        root.protocol("WM_DELETE_WINDOW", self.cerrar_ventana) # Evento de cierre de ventana

        self.init_values()

        self.columna_izquierda(self.root)

        self.columna_derecha(self.root)

    def init_values(self):
        contador.reset()
        self.deseada = 0
        self.tasa = 3
        self.temperaturas = []
        self.intervalo_alerta = 10


    
    def columna_izquierda(self, root):
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

    def columna_derecha(self, root):
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
            font=("Arial Rounded MT Bold", self.size_y(root, 10)),
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
            command=contador.stop,
        )
        button_pausar.pack(side="left", padx=x/2)

        button_reset = ctk.CTkButton(
            frame_botones,
            text=None,
            image=reset_icon,
            fg_color=self.btn_color,
            width=x_btn,
            height=y_btn,
            command=contador.reset,
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

    def iniciar_contador(self):
        contador.start()
        self.label_contador.after(0, self.actualizar_contador)

    def actualizar_contador(self):
        if contador.is_running():
            self.label_contador.config(text=contador.update_time())
            self.label_contador.after(1000, self.actualizar_contador)

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
        label_temp_deseada.pack(side="left", padx = self.size_x(root, 1.5))

        self.label_deseada = ctk.CTkLabel(
            frame_temp_deseada,
            text=f"{self.deseada:.2f}°C",
            font=("Arial Rounded MT Bold", self.size_y(root, 2.9)),
            text_color="#FFFFFF"
        )
        self.label_deseada.pack(side="left")

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
        button_iniciar.pack(side="left", padx=self.size_x(root, 3))

    def mostrar_ingreso_temp(self, root):
        frame = ctk.CTkFrame(
            root,
            fg_color="transparent",
        )
        frame.pack(pady=self.size_y(root, 2))

        # Etiqueta de error para mostrar mensajes de error
        self.error_label_t = ctk.CTkLabel(
            frame,
            text="",
            font=("Arial Rounded MT Bold", self.size_y(root, 2)),
            text_color="red",
        )
        self.error_label_t.pack(side="bottom")


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

        self.ingreso_temp = ctk.CTkEntry(
            frame,
            width=5 * self.size_y(root, 2.5),
            font=("Arial Rounded MT Bold", self.size_y(root, 2.5)),
            text_color="black",
        )
        self.ingreso_temp.pack(side="left")

        self.ingreso_temp.bind("<Return>", lambda event: [self.ingresar_temp(), self.ingreso_temp.delete(0, tk.END)])

        # Imagenes para los botones
        x = self.size_y(root, 2)
        y = self.size_y(root, 2)
        x_btn = self.size_y(root, 4)
        y_btn = self.size_y(root, 4)
        enter_icon = ctk.CTkImage(Image.open("recursos/enter.png"), size=(x, y))
        lista_icon = ctk.CTkImage(Image.open("recursos/lista.png"), size=(x, y))

        boton_ingresar = ctk.CTkButton(
            frame_botones,
            text=None,
            image=enter_icon,
            fg_color=self.btn_color,
            width=x_btn,
            height=y_btn,
            command=self.enter_temp,
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

    def cerrar_ventana(self):
        if self.contador_value:
            if not self.confirmar_salida():
                return
        if self.enable_graph:
            plt.close()
        else:
            root.destroy()