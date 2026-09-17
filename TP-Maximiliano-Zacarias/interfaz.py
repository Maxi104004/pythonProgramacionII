import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from lectores.lector_evtx import leer_evtx


def seleccionar_archivo():
    """
    Permite seleccionar un archivo EVTX desde una ventana.
    """

    ruta_archivo = filedialog.askopenfilename(
        title="Seleccionar archivo EVTX",
        filetypes=[
            ("Archivos EVTX", "*.evtx")
        ]
    )

    # Si el usuario cancela la selección, no hacemos nada.
    if ruta_archivo == "":
        return

    try:
        # Por ahora leeremos solamente 100 eventos
        # para comprobar que todo funcione correctamente.
        eventos = leer_evtx(ruta_archivo, limite=100)

        etiqueta_archivo.config(
            text=f"Archivo: {ruta_archivo}"
        )

        etiqueta_cantidad.config(
            text=f"Eventos cargados: {len(eventos)}"
        )

        cargar_tabla(eventos)

    except Exception as error:
        messagebox.showerror(
            "Error",
            f"No fue posible leer el archivo.\n\n{error}"
        )


def cargar_tabla(eventos):
    """
    Recibe una lista de eventos y los muestra
    dentro de la tabla de la interfaz.
    """

    # Eliminamos registros anteriores.
    for elemento in tabla.get_children():
        tabla.delete(elemento)

    # Agregamos los eventos recibidos.
    for evento in eventos:

        tabla.insert(
            "",
            tk.END,
            values=(
                evento["fecha_hora"],
                evento["event_id"],
                evento["record_id"],
                evento["equipo"],
                evento["proveedor"]
            )
        )


def iniciar_interfaz():
    """
    Crea e inicia la ventana principal de F.E.A.T.
    """

    global etiqueta_archivo
    global etiqueta_cantidad
    global tabla

    ventana = tk.Tk()

    ventana.title(
        "F.E.A.T. - Forensic Event Analysis Tool"
    )

    ventana.geometry("1100x650")

    # --------------------------------------------------
    # TÍTULO
    # --------------------------------------------------

    titulo = ttk.Label(
        ventana,
        text="F.E.A.T. - Forensic Event Analysis Tool",
        font=("Arial", 18, "bold")
    )

    titulo.pack(pady=15)

    # --------------------------------------------------
    # BOTÓN ABRIR EVTX
    # --------------------------------------------------

    boton_abrir = ttk.Button(
        ventana,
        text="Abrir archivo EVTX",
        command=seleccionar_archivo
    )

    boton_abrir.pack(pady=10)

    # --------------------------------------------------
    # INFORMACIÓN DEL ARCHIVO
    # --------------------------------------------------

    etiqueta_archivo = ttk.Label(
        ventana,
        text="Ningún archivo seleccionado"
    )

    etiqueta_archivo.pack(pady=5)

    etiqueta_cantidad = ttk.Label(
        ventana,
        text="Eventos cargados: 0"
    )

    etiqueta_cantidad.pack(pady=5)

    # --------------------------------------------------
    # TABLA DE EVENTOS
    # --------------------------------------------------

    columnas = (
        "fecha",
        "event_id",
        "record_id",
        "equipo",
        "proveedor"
    )

    tabla = ttk.Treeview(
        ventana,
        columns=columnas,
        show="headings"
    )

    tabla.heading(
        "fecha",
        text="Fecha / Hora"
    )

    tabla.heading(
        "event_id",
        text="Event ID"
    )

    tabla.heading(
        "record_id",
        text="Record ID"
    )

    tabla.heading(
        "equipo",
        text="Equipo"
    )

    tabla.heading(
        "proveedor",
        text="Proveedor"
    )

    tabla.column(
        "fecha",
        width=210
    )

    tabla.column(
        "event_id",
        width=90
    )

    tabla.column(
        "record_id",
        width=100
    )

    tabla.column(
        "equipo",
        width=200
    )

    tabla.column(
        "proveedor",
        width=300
    )

    tabla.pack(
        fill=tk.BOTH,
        expand=True,
        padx=20,
        pady=20
    )

    ventana.mainloop()
    