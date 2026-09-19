# ---------------------------------------------------------
# F.E.A.T. - Forensic Event Analysis Tool
# Módulo: filtros.py
#
# Contiene las funciones utilizadas para filtrar
# los eventos obtenidos de archivos EVTX.
# ---------------------------------------------------------


def filtrar_eventos(
    eventos,
    event_id=None,
    usuario=None,
    ip=None,
    categoria=None,
    texto=None
):
    """
    Filtra una lista de eventos utilizando distintos
    criterios de búsqueda.

    Todos los filtros son opcionales.

    Retorna una lista con los eventos que cumplen
    todos los criterios indicados.
    """

    resultados = []

    # Recorremos todos los eventos cargados.
    for evento in eventos:

        # Filtro por Event ID
        if event_id is not None:
            if evento["event_id"] != event_id:
                continue

        # Filtro por usuario
        if usuario:
            usuario_evento = evento["usuario"].lower()

            if usuario.lower() not in usuario_evento:
                continue

        # Filtro por IP
        if ip:
            if ip.lower() not in evento["ip"].lower():
                continue

        # Filtro por categoría
        if categoria:
            if categoria.lower() != evento["categoria"].lower():
                continue

        # Búsqueda por texto libre
        if texto:

            contenido_evento = (
                str(evento["event_id"]) + " " +
                evento["usuario"] + " " +
                evento["ip"] + " " +
                evento["equipo"] + " " +
                evento["descripcion"] + " " +
                str(evento["datos_evento"])
            ).lower()

            if texto.lower() not in contenido_evento:
                continue

        # Si llegó hasta acá, cumple todos los filtros.
        resultados.append(evento)

    return resultados