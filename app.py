import math

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="ANI | Algoritmos y Nodos Interactivos",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at 10% 0%, #142c4b 0%, transparent 35%),
        linear-gradient(135deg, #080d19, #0b1020 60%, #10102a);
    color: #e8f5ff;
}

[data-testid="stSidebar"] {
    background: #0a1425;
    border-right: 1px solid #17415e;
}

[data-testid="stHeader"] {
    background: rgba(8, 13, 25, 0.85);
}

h1, h2, h3, h4, p, label, .stMarkdown {
    color: #e8f5ff;
}

.hero {
    padding: 1.6rem;
    border: 1px solid #176078;
    border-radius: 20px;
    background: linear-gradient(120deg, #102b45, #171531);
    box-shadow: 0 0 28px rgba(0, 229, 255, 0.08);
    margin-bottom: 1.2rem;
}

.kicker {
    color: #00e5ff;
    font-size: 0.75rem;
    font-weight: 800;
    letter-spacing: 0.18em;
    text-transform: uppercase;
}

.hero h1 {
    color: #ffffff;
    font-size: 2.5rem;
    margin: 0.4rem 0;
    text-shadow: 0 0 18px rgba(0, 229, 255, 0.3);
}

.hero p {
    color: #a9c1df;
    margin-bottom: 0;
}

.panel {
    background: #101d31;
    border: 1px solid #21415e;
    border-radius: 14px;
    padding: 1rem;
    margin: 0.4rem 0;
}

.metric-card {
    background: linear-gradient(145deg, #122943, #11172d);
    border: 1px solid #20506a;
    border-radius: 14px;
    padding: 1rem;
    min-height: 105px;
}

.metric-label {
    color: #9bb8d5;
    font-size: 0.78rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

.metric-value {
    color: #f2fbff;
    font-size: 1.8rem;
    font-weight: 800;
    margin-top: 0.3rem;
    overflow-wrap: anywhere;
}

.metric-note {
    color: #00e5c7;
    font-size: 0.75rem;
    margin-top: 0.3rem;
}

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea,
div[data-testid="stSelectbox"] > div > div {
    background: #0c192b !important;
    color: #e8f5ff !important;
    border: 1px solid #254563 !important;
}

div[data-testid="stButton"] > button {
    background: linear-gradient(90deg, #007f96, #5634a5);
    color: white;
    border: 1px solid #00cfe8;
    border-radius: 10px;
    font-weight: 750;
}

div[data-testid="stButton"] > button:hover {
    border-color: #00fff0;
    box-shadow: 0 0 14px rgba(0, 207, 232, 0.25);
    color: white;
}

[data-testid="stMetric"] {
    background: #101e33;
    border: 1px solid #204664;
    border-radius: 12px;
    padding: 12px;
}

[data-testid="stMetricLabel"] {
    color: #9cb6d2 !important;
}

[data-testid="stMetricValue"] {
    color: #e7f3ff !important;
}

hr {
    border-color: #203d5b;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


def tarjeta(titulo, valor, nota=""):
    """Muestra una tarjeta visual para un resultado."""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{titulo}</div>
            <div class="metric-value">{valor}</div>
            <div class="metric-note">{nota}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def cambiar_paso(clave, incremento, maximo):
    """Avanza o retrocede un paso sin salir de los límites."""
    paso_actual = st.session_state.get(clave, 1)
    st.session_state[clave] = max(
        1,
        min(maximo, paso_actual + incremento),
    )


# =========================================================
# 2. ALGORITMO HAMILTONIANO
# =========================================================

def buscar_hamiltoniano(grafo, buscar_ciclo=False):
    """
    Busca un camino o ciclo hamiltoniano usando backtracking.

    Camino: visita cada vértice exactamente una vez.
    Ciclo: visita cada vértice y regresa al inicio.
    """

    vertices = list(grafo.nodes())

    if not vertices:
        return None

    # Para un ciclo basta fijar el primer vértice.
    inicios = [vertices[0]] if buscar_ciclo else vertices

    for inicio in inicios:

        camino = [inicio]
        visitados = {inicio}

        def retroceder(actual):

            if len(camino) == len(vertices):

                if not buscar_ciclo:
                    return camino.copy()

                if grafo.has_edge(actual, inicio):
                    return camino.copy() + [inicio]

                return None

            for vecino in grafo.neighbors(actual):

                if vecino not in visitados:

                    visitados.add(vecino)
                    camino.append(vecino)

                    resultado = retroceder(vecino)

                    if resultado is not None:
                        return resultado

                    camino.pop()
                    visitados.remove(vecino)

            return None

        resultado = retroceder(inicio)

        if resultado is not None:
            return resultado

    return None


# =========================================================
# 3. ENCABEZADO Y BARRA LATERAL
# =========================================================

st.markdown("""
<div class="hero">
    <h1>Algoritmos y Nodos Interactivos</h1>
    <p>Sistema gráfico de grafos · Euler · Hamilton · Dijkstra</p>
</div>
""", unsafe_allow_html=True)


with st.sidebar:

    st.markdown("## ANI")
    st.caption("PANEL DE CONTROL")

    algoritmo = st.radio(
        "Selecciona el algoritmo",
        ["Dijkstra", "Euler", "Hamilton"],
    )

    st.divider()

    st.markdown("### Guía del sistema")

    st.markdown("""
    **Dijkstra**

    Encuentra una ruta de menor costo.

    **Euler**

    Recorre cada arista exactamente una vez.

    **Hamilton**

    Visita cada vértice exactamente una vez.
    """)

    st.divider()

    animar = st.checkbox(
        "Activar recorrido paso a paso",
        value=True,
    )


# =========================================================
# 4. ENTRADA DE DATOS
# =========================================================

st.markdown("### 1. Configuración del grafo")

with st.expander("ℹ️ Cómo introducir los datos"):

    st.markdown("""
    **Vértices:** sepáralos con comas.

    **Aristas:** escribe una por línea con este formato:

    `A, B, 5`

    Esto crea una arista entre A y B con costo 5.
    Si omites el peso, se utiliza 1 por defecto.

    No se permiten vértices duplicados, bucles,
    conexiones duplicadas ni pesos negativos.
    """)


vertices_texto = st.text_input(
    "Vértices",
    value="A, B, C, D, E, F, G, H",
)


aristas_texto = st.text_area(
    "Aristas: origen, destino, costo (opcional)",
    value=(
        "A, B, 2\n"
        "B, C, 3\n"
        "C, D, 1\n"
        "D, A, 4\n"
        "A, C, 10\n"
        "D, E, 2\n"
        "E, F, 2\n"
        "F, G, 2\n"
        "G, H, 2\n"
        "H, E, 2"
    ),
    height=180,
)


# =========================================================
# 5. CREACIÓN Y VALIDACIÓN DEL GRAFO
# =========================================================

vertices = [
    v.strip()
    for v in vertices_texto.split(",")
    if v.strip()
]

G = nx.Graph()
G.add_nodes_from(vertices)

errores = []

if len(vertices) != len(set(vertices)):
    errores.append("La lista contiene vértices duplicados.")


for numero, linea in enumerate(aristas_texto.splitlines(), start=1):

    if not linea.strip():
        continue

    partes = [p.strip() for p in linea.split(",")]

    if len(partes) not in (2, 3):

        errores.append(
            f"Línea {numero}: utiliza origen, destino y costo opcional."
        )
        continue

    origen, destino = partes[0], partes[1]

    if not origen or not destino:

        errores.append(
            f"Línea {numero}: falta el origen o el destino."
        )
        continue

    if origen not in G or destino not in G:

        errores.append(
            f"Línea {numero}: el origen o destino no está definido."
        )
        continue

    if origen == destino:

        errores.append(
            f"Línea {numero}: no se permiten bucles."
        )
        continue

    peso = 1.0

    if len(partes) == 3:

        try:
            peso = float(partes[2])

        except ValueError:

            errores.append(
                f"Línea {numero}: el costo debe ser numérico."
            )
            continue

        if not math.isfinite(peso) or peso < 0:

            errores.append(
                f"Línea {numero}: el costo debe ser finito y no negativo."
            )
            continue

    if G.has_edge(origen, destino):

        errores.append(
            f"Línea {numero}: la arista ya existe."
        )
        continue

    G.add_edge(origen, destino, weight=peso)


# Si cambian los datos del grafo, se descarta el resultado anterior
# de Dijkstra para evitar mostrar una ruta de un grafo diferente.

clave_grafo = vertices_texto + "||" + aristas_texto

if st.session_state.get("clave_grafo") != clave_grafo:

    st.session_state["clave_grafo"] = clave_grafo
    st.session_state.pop("resultado_dijkstra", None)


# =========================================================
# 6. RESULTADOS Y ALGORITMOS
# =========================================================

if errores:

    st.error("Corrige los siguientes problemas antes de continuar:")

    for error in errores:
        st.write(f"- {error}")


elif G.number_of_nodes() == 0:

    st.info("Agrega al menos un vértice para comenzar.")


else:

    grados = dict(G.degree())

    # Tarjetas de resumen
    col1, col2, col3 = st.columns(3)

    with col1:

        tarjeta(
            "Vértices",
            G.number_of_nodes(),
            "Nodos registrados",
        )

    with col2:

        tarjeta(
            "ARISTAS",
            G.number_of_edges(),
            "Conexiones registradas",
        )

    with col3:

        cantidad_impares = sum(
            grado % 2 for grado in grados.values()
        )

        tarjeta(
            "GRADOS IMPARES",
            cantidad_impares,
            "Dato importante para Euler",
        )


    st.markdown("### 2. Análisis del algoritmo")

    # Estas variables guardan el recorrido que se dibujará.
    aristas_recorrido = []
    vertices_recorrido = []
    descripcion = ""


    # -----------------------------------------------------
    # DIJKSTRA
    # -----------------------------------------------------

    if algoritmo == "Dijkstra":

        descripcion = (
            "Dijkstra compara los costos acumulados para encontrar "
            "una ruta de costo mínimo. Funciona con costos no negativos."
        )

        st.markdown(
            f'<div class="panel">{descripcion}</div>',
            unsafe_allow_html=True,
        )

        if G.number_of_nodes() < 2:

            st.warning(
                "Necesitas al menos dos vértices para calcular una ruta."
            )

        else:

            lista_vertices = list(G.nodes())

            col_origen, col_destino = st.columns(2)

            with col_origen:

                origen_d = st.selectbox(
                    "Vértice de origen",
                    lista_vertices,
                    key="origen_dijkstra",
                )

            with col_destino:

                destino_d = st.selectbox(
                    "Vértice de destino",
                    lista_vertices,
                    index=1,
                    key="destino_dijkstra",
                )


            if st.button(
                "▶ Calcular ruta",
                use_container_width=True,
            ):

                try:

                    costo, camino = nx.single_source_dijkstra(
                        G,
                        source=origen_d,
                        target=destino_d,
                        weight="weight",
                    )

                    st.session_state["resultado_dijkstra"] = {
                        "origen": origen_d,
                        "destino": destino_d,
                        "costo": costo,
                        "camino": camino,
                    }

                except nx.NetworkXNoPath:

                    st.session_state["resultado_dijkstra"] = {
                        "origen": origen_d,
                        "destino": destino_d,
                        "error": (
                            f"No existe una ruta entre "
                            f"{origen_d} y {destino_d}."
                        ),
                    }


            resultado = st.session_state.get(
                "resultado_dijkstra",
                {},
            )

            # Solo se muestra el resultado correspondiente
            # a los vértices seleccionados actualmente.

            if (
                resultado
                and resultado.get("origen") == origen_d
                and resultado.get("destino") == destino_d
            ):

                if "error" in resultado:

                    st.warning(resultado["error"])

                else:

                    camino = resultado["camino"]
                    costo = resultado["costo"]

                    res1, res2 = st.columns(2)

                    with res1:

                        tarjeta(
                            "COSTO TOTAL",
                            f"{costo:g}",
                            "Suma de los costos",
                        )

                    with res2:

                        tarjeta(
                            "VÉRTICES EN RUTA",
                            len(camino),
                            "Incluye origen y destino",
                        )


                    st.markdown(
                        '<div class="panel"><b>Ruta encontrada</b><br>'
                        '<span style="color:#00e5c7">'
                        + " → ".join(camino)
                        + "</span></div>",
                        unsafe_allow_html=True,
                    )

                    vertices_recorrido = camino

                    aristas_recorrido = list(
                        zip(camino, camino[1:])
                    )


                    if animar and len(camino) > 1:

                        st.markdown("#### Recorrido paso a paso")

                        # Control de pasos con botones y barra deslizante.
                        clave_paso = "paso_dijkstra"
                        maximo_paso = len(camino)

                        if clave_paso not in st.session_state:
                            st.session_state[clave_paso] = 1
                        else:
                            st.session_state[clave_paso] = max(
                                1,
                                min(maximo_paso, st.session_state[clave_paso]),
                            )

                        col_menos, col_barra, col_mas = st.columns([1, 6, 1])

                        with col_menos:
                            st.button(
                                "−",
                                key="retroceder_dijkstra",
                                help="Retroceder un paso",
                                disabled=st.session_state[clave_paso] <= 1,
                                on_click=cambiar_paso,
                                args=(clave_paso, -1, maximo_paso),
                            )

                        with col_barra:
                            paso = st.slider(
                                "Avanzar por los vértices",
                                min_value=1,
                                max_value=maximo_paso,
                                key=clave_paso,
                            )

                        with col_mas:
                            st.button(
                                "+",
                                key="avanzar_dijkstra",
                                help="Avanzar un paso",
                                disabled=st.session_state[clave_paso] >= maximo_paso,
                                on_click=cambiar_paso,
                                args=(clave_paso, 1, maximo_paso),
                            )

                        st.info(
                            " → ".join(camino[:paso])
                        )

                        # En el gráfico se muestra únicamente
                        # la parte recorrida hasta este paso.

                        aristas_recorrido = list(
                            zip(camino[:paso], camino[1:paso])
                        )


    # -----------------------------------------------------
    # EULER
    # -----------------------------------------------------

    elif algoritmo == "Euler":

        descripcion = (
            "Un recorrido euleriano utiliza cada arista exactamente "
            "una vez. Un ciclo euleriano también termina en el vértice "
            "donde comenzó."
        )

        st.markdown(
            f'<div class="panel">{descripcion}</div>',
            unsafe_allow_html=True,
        )

        if G.number_of_edges() == 0:

            st.warning(
                "Agrega al menos una arista para buscar un recorrido."
            )

        else:

            # Los vértices aislados no impiden un recorrido Euleriano.

            activos = [
                v for v, grado in G.degree()
                if grado > 0
            ]

            H = G.subgraph(activos).copy()

            if not nx.is_connected(H):

                st.warning(
                    "No existe un recorrido euleriano que use todas "
                    "las aristas: las partes que contienen aristas "
                    "no están conectadas."
                )

            else:

                impares = [
                    v for v, grado in H.degree()
                    if grado % 2 != 0
                ]

                if len(impares) == 0:

                    tipo = "Ciclo euleriano"

                    aristas_recorrido = list(
                        nx.eulerian_circuit(H)
                    )

                elif len(impares) == 2:

                    tipo = "Camino euleriano"

                    aristas_recorrido = list(
                        nx.eulerian_path(H)
                    )

                else:

                    tipo = None

                    st.warning(
                        f"Hay {len(impares)} vértices de grado impar. "
                        "Para un camino euleriano se necesitan "
                        "exactamente 0 o 2."
                    )


                if tipo:

                    vertices_recorrido = [
                        aristas_recorrido[0][0]
                    ] + [
                        destino
                        for _, destino in aristas_recorrido
                    ]

                    st.success(f"¡{tipo} encontrado!")

                    st.markdown(
                        '<div class="panel"><b>Recorrido</b><br>'
                        '<span style="color:#00e5c7">'
                        + " → ".join(vertices_recorrido)
                        + "</span></div>",
                        unsafe_allow_html=True,
                    )

                    tarjeta(
                        "ARISTAS RECORRIDAS",
                        len(aristas_recorrido),
                        f"De {G.number_of_edges()} conexiones",
                    )


                    if animar and aristas_recorrido:

                        st.markdown("#### Recorrido paso a paso")

                        # Control de pasos con botones y barra deslizante.
                        clave_paso = "paso_euler"
                        maximo_paso = len(aristas_recorrido)

                        if clave_paso not in st.session_state:
                            st.session_state[clave_paso] = 1
                        else:
                            st.session_state[clave_paso] = max(
                                1,
                                min(maximo_paso, st.session_state[clave_paso]),
                            )

                        col_menos, col_barra, col_mas = st.columns([1, 6, 1])

                        with col_menos:
                            st.button(
                                "−",
                                key="retroceder_euler",
                                help="Retroceder una arista",
                                disabled=st.session_state[clave_paso] <= 1,
                                on_click=cambiar_paso,
                                args=(clave_paso, -1, maximo_paso),
                            )

                        with col_barra:
                            paso = st.slider(
                                "Cantidad de aristas recorridas",
                                min_value=1,
                                max_value=maximo_paso,
                                key=clave_paso,
                            )

                        with col_mas:
                            st.button(
                                "+",
                                key="avanzar_euler",
                                help="Avanzar una arista",
                                disabled=st.session_state[clave_paso] >= maximo_paso,
                                on_click=cambiar_paso,
                                args=(clave_paso, 1, maximo_paso),
                            )

                        st.info(
                            " → ".join(
                                vertices_recorrido[:paso + 1]
                            )
                        )

                        aristas_recorrido = aristas_recorrido[:paso]


    # -----------------------------------------------------
    # HAMILTON
    # -----------------------------------------------------

    else:

        descripcion = (
            "Un camino hamiltoniano visita cada vértice exactamente "
            "una vez. Un ciclo hamiltoniano hace lo mismo y regresa "
            "al vértice inicial."
        )

        st.markdown(
            f'<div class="panel">{descripcion}</div>',
            unsafe_allow_html=True,
        )

        # La búsqueda por retroceso puede crecer exponencialmente.

        if G.number_of_nodes() > 24:

            st.warning(
                "El algoritmo de Hamilton puede tardar mucho con "
                "grafos grandes. Para esta versión se limita la "
                "búsqueda a 24 vértices."
            )

        else:

            camino_h = buscar_hamiltoniano(
                G,
                buscar_ciclo=False,
            )

            ciclo_h = buscar_hamiltoniano(
                G,
                buscar_ciclo=True,
            )


            if camino_h is not None:

                st.success("Se encontró un camino hamiltoniano.")

                st.markdown(
                    '<div class="panel"><b>Camino</b><br>'
                    '<span style="color:#00e5c7">'
                    + " → ".join(camino_h)
                    + "</span></div>",
                    unsafe_allow_html=True,
                )

            else:

                st.warning(
                    "No se encontró un camino hamiltoniano."
                )


            if ciclo_h is not None:

                st.success("Se encontró un ciclo hamiltoniano.")

                st.markdown(
                    '<div class="panel"><b>Ciclo</b><br>'
                    '<span style="color:#00e5c7">'
                    + " → ".join(ciclo_h)
                    + "</span></div>",
                    unsafe_allow_html=True,
                )

                vertices_recorrido = ciclo_h

                aristas_recorrido = list(
                    zip(ciclo_h, ciclo_h[1:])
                )

            elif camino_h is not None:

                vertices_recorrido = camino_h

                aristas_recorrido = list(
                    zip(camino_h, camino_h[1:])
                )


            if animar and vertices_recorrido:

                st.markdown("#### Recorrido paso a paso")

                # Control de pasos con botones y barra deslizante.
                clave_paso = "paso_hamilton"
                maximo_paso = len(vertices_recorrido)

                if clave_paso not in st.session_state:
                    st.session_state[clave_paso] = 1
                else:
                    st.session_state[clave_paso] = max(
                        1,
                        min(maximo_paso, st.session_state[clave_paso]),
                    )

                col_menos, col_barra, col_mas = st.columns([1, 6, 1])

                with col_menos:
                    st.button(
                        "−",
                        key="retroceder_hamilton",
                        help="Retroceder un paso",
                        disabled=st.session_state[clave_paso] <= 1,
                        on_click=cambiar_paso,
                        args=(clave_paso, -1, maximo_paso),
                    )

                with col_barra:
                    paso = st.slider(
                        "Vértices del recorrido",
                        min_value=1,
                        max_value=maximo_paso,
                        key=clave_paso,
                    )

                with col_mas:
                    st.button(
                        "+",
                        key="avanzar_hamilton",
                        help="Avanzar un paso",
                        disabled=st.session_state[clave_paso] >= maximo_paso,
                        on_click=cambiar_paso,
                        args=(clave_paso, 1, maximo_paso),
                    )

                st.info(
                    " → ".join(vertices_recorrido[:paso])
                )

                # Si se encontró un ciclo, se incluye la arista
                # de regreso al inicio al completar todos los pasos.

                aristas_recorrido = list(
                    zip(
                        vertices_recorrido[:paso],
                        vertices_recorrido[1:paso],
                    )
                )

                if (
                    ciclo_h is not None
                    and paso == len(vertices_recorrido)
                ):

                    aristas_recorrido.append(
                        (ciclo_h[-2], ciclo_h[-1])
                    )


    # =====================================================
    # 7. VISUALIZACIÓN DEL GRAFO
    # =====================================================

    st.markdown("### 3. Visualización del grafo")

    st.caption(
        "Cian: vértices · Azul: aristas · "
        "Rosa neón: recorrido resaltado."
    )

    cantidad_vertices = G.number_of_nodes()

    if cantidad_vertices > 1:

        posiciones = nx.spring_layout(
            G,
            seed=42,
            k=1.3 / math.sqrt(cantidad_vertices),
        )

    else:

        posiciones = nx.spring_layout(G, seed=42)


    figura, ax = plt.subplots(figsize=(15, 9))

    figura.patch.set_facecolor("#080d19")
    ax.set_facecolor("#080d19")

    tamano_nodo = (
        750 if cantidad_vertices <= 25 else 350
    )

    tamano_letra = (
        9 if cantidad_vertices <= 25 else 6
    )


    # Dibujar los vértices.

    nx.draw_networkx_nodes(
        G,
        posiciones,
        node_color="#102e4a",
        edgecolors="#00e5ff",
        linewidths=1.8,
        node_size=tamano_nodo,
        ax=ax,
    )


    # Dibujar los nombres de los vértices.

    nx.draw_networkx_labels(
        G,
        posiciones,
        font_size=tamano_letra,
        font_color="#f0fbff",
        font_weight="bold",
        ax=ax,
    )


    # Dibujar todas las conexiones normales.

    nx.draw_networkx_edges(
        G,
        posiciones,
        edge_color="#37506e",
        width=1.5,
        alpha=0.9,
        ax=ax,
    )


    # Resaltar las conexiones del recorrido actual.

    if aristas_recorrido:

        nx.draw_networkx_edges(
            G,
            posiciones,
            edgelist=aristas_recorrido,
            edge_color="#ff3ea5",
            width=3.2,
            ax=ax,
        )


    # Mostrar los pesos de las conexiones.

    etiquetas = {
        (u, v): f"{datos['weight']:g}"
        for u, v, datos in G.edges(data=True)
    }

    nx.draw_networkx_edge_labels(
        G,
        posiciones,
        edge_labels=etiquetas,
        font_size=(
            8 if cantidad_vertices <= 25 else 6
        ),
        font_color="#b7d5f0",
        bbox={
            "alpha": 0.75,
            "color": "#080d19",
            "pad": 1,
        },
        ax=ax,
    )

    ax.axis("off")
    figura.tight_layout()

    st.pyplot(figura, use_container_width=True)

    plt.close(figura)


    # =====================================================
    # 8. TABLAS DEL GRAFO
    # =====================================================

    with st.expander("📋 Tabla de vértices y grados"):

        datos_vertices = [
            {
                "Vértice": vertice,
                "Grado": grado,
            }
            for vertice, grado in grados.items()
        ]

        st.dataframe(
            datos_vertices,
            use_container_width=True,
            hide_index=True,
        )


    with st.expander("📋 Tabla de aristas y costos"):

        datos_aristas = [
            {
                "Origen": origen,
                "Destino": destino,
                "Costo": datos["weight"],
            }
            for origen, destino, datos
            in G.edges(data=True)
        ]

        st.dataframe(
            datos_aristas,
            use_container_width=True,
            hide_index=True,
        )


    # =====================================================
    # 8.1 MATRICES DE ADYACENCIA E INCIDENCIA
    # =====================================================

    st.markdown("### 4. Representación matricial del grafo")

    # Se conserva el orden en que fueron ingresados los vértices.

    lista_vertices = list(G.nodes())


    # Cada arista recibe una etiqueta para identificar su columna
    # en la matriz de incidencia.

    lista_aristas = list(G.edges(data=True))

    etiquetas_aristas = [
        f"e{i + 1}: {origen}-{destino}"
        for i, (origen, destino, _) in enumerate(lista_aristas)
    ]


    # -----------------------------------------------------
    # MATRIZ DE ADYACENCIA BINARIA
    # -----------------------------------------------------
    # Coloca 1 si existe una conexión entre dos vértices.
    # Coloca 0 si no existe conexión.
    # No utiliza los pesos de las aristas.

    matriz_adyacencia = []

    for origen in lista_vertices:

        fila = []

        for destino in lista_vertices:

            if G.has_edge(origen, destino):
                fila.append(1)

            else:
                fila.append(0)

        matriz_adyacencia.append(fila)


    df_adyacencia = pd.DataFrame(
        matriz_adyacencia,
        index=lista_vertices,
        columns=lista_vertices,
    )


    # -----------------------------------------------------
    # MATRIZ DE INCIDENCIA BINARIA
    # -----------------------------------------------------
    # En un grafo no dirigido, cada columna representa una arista.
    # Coloca 1 en los dos vértices que forman esa arista.
    # Coloca 0 en los demás vértices.

    matriz_incidencia = []

    for vertice in lista_vertices:

        fila = []

        for origen, destino, _ in lista_aristas:

            if vertice == origen or vertice == destino:
                fila.append(1)

            else:
                fila.append(0)

        matriz_incidencia.append(fila)


    df_incidencia = pd.DataFrame(
        matriz_incidencia,
        index=lista_vertices,
        columns=etiquetas_aristas,
    )


    # Mostrar las matrices en dos columnas.

    col_ady, col_inc = st.columns(2)


    # MATRIZ DE ADYACENCIA

    with col_ady:

        with st.expander(
            "📊 Matriz de adyacencia",
            expanded=True,
        ):

            st.caption(
                "Filas y columnas representan vértices. "
                "1 significa que existe una conexión y "
                "0 que no existe conexión."
            )

            st.dataframe(
                df_adyacencia,
                use_container_width=True,
            )


    # MATRIZ DE INCIDENCIA

    with col_inc:

        with st.expander(
            "📊 Matriz de incidencia",
            expanded=True,
        ):

            st.caption(
                "Las filas representan vértices y las columnas "
                "representan aristas. Un 1 indica que el vértice "
                "forma parte de esa arista."
            )

            if lista_aristas:

                st.dataframe(
                    df_incidencia,
                    use_container_width=True,
                )

            else:

                st.info(
                    "Agrega al menos una arista para construir "
                    "la matriz de incidencia."
                )


# =========================================================
# 9. PIE DE PAGINA
# =========================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#6f8eae; font-size:.8rem">
        ANI
        <br>
        Algoritmos de Euler, Hamilton y Dijkstra
    </div>
    """,
    unsafe_allow_html=True,
)