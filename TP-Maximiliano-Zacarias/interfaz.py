import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from lectores.lector_evtx import leer_evtx
from filtros import filtrar_eventos


def seleccionar_archivo():
    """
    Permite seleccionar un archivo EVTX desde una ventana.
    """
    global eventos_cargados
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
        
        eventos_cargados = leer_evtx(
        ruta_archivo,
        limite=100
       )

        etiqueta_archivo.config(
            text=f"Archivo: {ruta_archivo}"
        )

        etiqueta_cantidad.config(
            text=f"Eventos cargados: {len(eventos_cargados)}"
        )

        cargar_tabla(eventos_cargados)

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

def aplicar_filtros():
    """
    Obtiene los criterios ingresados en la interfaz
    y utiliza la función filtrar_eventos().
    """

    # Verificamos que exista un archivo cargado.
    if not eventos_cargados:
        messagebox.showwarning(
            "Sin archivo",
            "Primero debe cargar un archivo EVTX."
        )
        return

    # Obtenemos los valores ingresados por el usuario.
    texto_event_id = entrada_event_id.get().strip()
    usuario = entrada_usuario.get().strip()
    ip = entrada_ip.get().strip()
    categoria = combo_categoria.get().strip()
    texto = entrada_texto.get().strip()

    # ---------------------------------------------
    # VALIDACIÓN DEL EVENT ID
    # ---------------------------------------------

    event_id = None

    if texto_event_id:

        if not texto_event_id.isdigit():
            messagebox.showerror(
                "Event ID inválido",
                "El Event ID debe contener solamente números."
            )
            return

        event_id = int(texto_event_id)

    # Si el usuario selecciona "Todos",
    # no aplicamos filtro de categoría.
    if categoria == "Todos":
        categoria = None

    # ---------------------------------------------
    # APLICAR FILTROS
    # ---------------------------------------------

    resultados = filtrar_eventos(
        eventos_cargados,
        event_id=event_id,
        usuario=usuario,
        ip=ip,
        categoria=categoria,
        texto=texto
    )

    # Mostramos únicamente los eventos encontrados.
    cargar_tabla(resultados)

    etiqueta_cantidad.config(
        text=f"Eventos encontrados: {len(resultados)}"
    )
def limpiar_filtros():
    """
    Limpia todos los campos de búsqueda y vuelve
    a mostrar la lista completa de eventos.
    """

    entrada_event_id.delete(0, tk.END)
    entrada_usuario.delete(0, tk.END)
    entrada_ip.delete(0, tk.END)
    entrada_texto.delete(0, tk.END)

    combo_categoria.set("Todos")

    cargar_tabla(eventos_cargados)

    etiqueta_cantidad.config(
        text=f"Eventos cargados: {len(eventos_cargados)}"
    )




def iniciar_interfaz():
    """
    Crea e inicia la ventana principal de F.E.A.T.
    """

    global etiqueta_archivo
    global etiqueta_cantidad
    global tabla
    global entrada_event_id
    global entrada_usuario
    global entrada_ip
    global entrada_texto
    global combo_categoria

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
    # PANEL DE FILTROS
    # --------------------------------------------------

    marco_filtros = ttk.LabelFrame(
        ventana,
        text="Filtros de búsqueda"
    )

    marco_filtros.pack(
        fill=tk.X,
        padx=20,
        pady=10
    )
    ttk.Label(
        marco_filtros,
        text="Event ID:"
    ).grid(
        row=0,
        column=0,
        padx=5,
        pady=5
    )

    entrada_event_id = ttk.Entry(
        marco_filtros,
        width=15
    )

    entrada_event_id.grid(
        row=0,
        column=1,
        padx=5,
        pady=5
    )

    ttk.Label(
        marco_filtros,
        text="Usuario:"
    ).grid(
        row=0,
        column=2,
        padx=5,
        pady=5
    )

    entrada_usuario = ttk.Entry(
        marco_filtros,
        width=20
    )

    entrada_usuario.grid(
        row=0,
        column=3,
        padx=5,
        pady=5
    )

    ttk.Label(
        marco_filtros,
        text="IP:"
    ).grid(
        row=0,
        column=4,
        padx=5,
        pady=5
    )

    entrada_ip = ttk.Entry(
        marco_filtros,
        width=20
    )

    entrada_ip.grid(
        row=0,
        column=5,
        padx=5,
        pady=5
    )
    
    ttk.Label(
    marco_filtros,
    text="Categoría:"
    ).grid(
        row=1,
        column=0,
        padx=5,
        pady=5
    )

    combo_categoria = ttk.Combobox(
    marco_filtros,
        values=(
         "Todos",
         "Autenticación",
         "Cuentas",
         "Procesos",
         "Dispositivos",
         "Sistema",
         "Auditoría",
         "Otros"
    ),
    state="readonly",
        width=18
    )

    combo_categoria.grid(
    row=1,
        column=1,
        padx=5,
        pady=5
    )

    combo_categoria.set("Todos")


    # -----------------------------
    # BOTONES
    # -----------------------------

    boton_filtrar = ttk.Button(
        marco_filtros,
        text="Aplicar filtros",
        command=aplicar_filtros
    )

    boton_filtrar.grid(
        row=2,
        column=2,
        padx=5,
        pady=10
    )

    boton_limpiar = ttk.Button(
        marco_filtros,
        text="Limpiar filtros",
        command=limpiar_filtros
    )

    boton_limpiar.grid(
        row=2,
        column=3,
        padx=5,
        pady=10
    )

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
    