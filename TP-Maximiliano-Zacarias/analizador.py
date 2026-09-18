# ---------------------------------------------------------
# F.E.A.T. - Forensic Event Analysis Tool
# Módulo: analizador.py
#
# Contiene información para interpretar y clasificar
# determinados eventos de Windows.
# ---------------------------------------------------------


# Diccionario:
# relaciona un Event ID con una descripción comprensible.
DESCRIPCIONES_EVENTOS = {
    1102: "Registro de auditoría borrado",
    4624: "Inicio de sesión satisfactorio",
    4625: "Inicio de sesión fallido",
    4634: "Cierre de sesión",
    4647: "Cierre de sesión iniciado por el usuario",
    4688: "Creación de un nuevo proceso",
    4720: "Creación de una cuenta de usuario",
    4726: "Eliminación de una cuenta de usuario",
    6416: "Nuevo dispositivo externo reconocido",
    6005: "Servicio de registro de eventos iniciado",
    6006: "Servicio de registro de eventos detenido",
    6008: "Apagado inesperado",
    1074: "Proceso que inició un apagado o reinicio"
}


# Tuplas:
# contienen conjuntos de Event ID asociados a categorías.
EVENTOS_AUTENTICACION = (
    4624,
    4625,
    4634,
    4647
)

EVENTOS_CUENTAS = (
    4720,
    4726
)

EVENTOS_PROCESOS = (
    4688,
)

EVENTOS_DISPOSITIVOS = (
    6416,
)

EVENTOS_SISTEMA = (
    6005,
    6006,
    6008,
    1074
)


def obtener_descripcion(event_id):
    """
    Devuelve una descripción conocida para un Event ID.

    Si el evento no está incluido en nuestro catálogo,
    devuelve 'Evento no catalogado'.
    """

    return DESCRIPCIONES_EVENTOS.get(
        event_id,
        "Evento no catalogado"
    )


def obtener_categoria(event_id):
    """
    Clasifica un Event ID dentro de una categoría general.
    """

    if event_id in EVENTOS_AUTENTICACION:
        return "Autenticación"

    elif event_id in EVENTOS_CUENTAS:
        return "Cuentas"

    elif event_id in EVENTOS_PROCESOS:
        return "Procesos"

    elif event_id in EVENTOS_DISPOSITIVOS:
        return "Dispositivos"

    elif event_id in EVENTOS_SISTEMA:
        return "Sistema"

    elif event_id == 1102:
        return "Auditoría"

    else:
        return "Otros"


def interpretar_evento(evento):
    """
    Recibe el diccionario de un evento y agrega
    descripción y categoría.

    Retorna un nuevo diccionario.
    """

    evento_interpretado = evento.copy()

    event_id = evento_interpretado["event_id"]

    evento_interpretado["descripcion"] = obtener_descripcion(
        event_id
    )

    evento_interpretado["categoria"] = obtener_categoria(
        event_id
    )

    return evento_interpretado