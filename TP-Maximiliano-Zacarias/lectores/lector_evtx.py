# ---------------------------------------------------------
# F.E.A.T. - Forensic Event Analysis Tool
# Módulo: lector_evtx.py
#
# Este módulo se encarga de leer archivos EVTX y extraer
# información básica de cada registro.
# ---------------------------------------------------------

from pathlib import Path
from Evtx.Evtx import Evtx
import xml.etree.ElementTree as ET


def extraer_datos_basicos(xml_evento):
    """
    Recibe el XML de un evento de Windows y extrae
    algunos de sus datos principales.

    Retorna un diccionario con la información obtenida.
    """

    # Namespace utilizado por los eventos de Windows
    namespace = {
        "e": "http://schemas.microsoft.com/win/2004/08/events/event"
    }

    # Convertimos el texto XML en una estructura que Python
    # puede recorrer.
    raiz = ET.fromstring(xml_evento)

    # Buscamos los diferentes elementos del evento.
    event_id_elemento = raiz.find("./e:System/e:EventID", namespace)
    record_id_elemento = raiz.find("./e:System/e:EventRecordID", namespace)
    computer_elemento = raiz.find("./e:System/e:Computer", namespace)
    time_elemento = raiz.find("./e:System/e:TimeCreated", namespace)
    provider_elemento = raiz.find("./e:System/e:Provider", namespace)

    # Obtenemos los valores encontrados.
    event_id = (
        event_id_elemento.text
        if event_id_elemento is not None
        else ""
    )

    record_id = (
        record_id_elemento.text
        if record_id_elemento is not None
        else ""
    )

    equipo = (
        computer_elemento.text
        if computer_elemento is not None
        else ""
    )

    # TimeCreated guarda la fecha dentro del atributo SystemTime.
    fecha_hora = ""

    if time_elemento is not None:
        fecha_hora = time_elemento.attrib.get("SystemTime", "")

    # Provider guarda el nombre dentro del atributo Name.
    proveedor = ""

    if provider_elemento is not None:
        proveedor = provider_elemento.attrib.get("Name", "")

    # Creamos un diccionario para representar el evento.
    evento = {
        "event_id": event_id,
        "record_id": record_id,
        "fecha_hora": fecha_hora,
        "equipo": equipo,
        "proveedor": proveedor,
        "xml": xml_evento
    }

    return evento


def leer_evtx(ruta_archivo, limite=None):
    """
    Lee un archivo EVTX.

    Parámetros:
        ruta_archivo:
            Ruta del archivo que se desea analizar.

        limite:
            Cantidad máxima de eventos a leer.
            Es opcional. Si vale None se leen todos.

    Retorna:
        Una lista de diccionarios.
        Cada diccionario representa un evento.
    """

    ruta = Path(ruta_archivo)

    # Validamos que el archivo exista.
    if not ruta.exists():
        raise FileNotFoundError(
            "El archivo seleccionado no existe."
        )

    # Validamos que la extensión sea EVTX.
    if ruta.suffix.lower() != ".evtx":
        raise ValueError(
            "El archivo seleccionado debe tener extensión .evtx."
        )

    # Lista donde almacenaremos todos los eventos.
    eventos = []

    # Abrimos el archivo EVTX.
    with Evtx(str(ruta)) as archivo:

        # Recorremos registro por registro.
        for registro in archivo.records():

            # Obtenemos el XML original.
            xml_evento = registro.xml()

            # Interpretamos los datos básicos del XML.
            evento = extraer_datos_basicos(xml_evento)

            # Agregamos el diccionario a nuestra lista.
            eventos.append(evento)

            # Si se indicó un límite y ya se alcanzó,
            # detenemos la lectura.
            if limite is not None and len(eventos) >= limite:
                break

    return eventos