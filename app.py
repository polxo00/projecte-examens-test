import streamlit as st
import json
import random

# Títol de l'aplicació
st.title("Test de Preguntes Interactiu")
st.markdown("---")

# Carrega JSON (Assumeix que 'preguntes.json' conté les dades)
try:
    with open("preguntes.json", "r", encoding="utf-8") as f:
        totes_preguntes = json.load(f)
except FileNotFoundError:
    st.error("❌ Error: No s'ha trobat el fitxer 'preguntes.json'. Assegura't que existeix i té el format correcte.")
    totes_preguntes = []

# Inicialitza estat de la sessió si no existeix
if "index" not in st.session_state:
    st.session_state.index = 0
    st.session_state.encerts = 0
    st.session_state.respostes_usuari = []
    st.session_state.iniciat = False
    st.session_state.preguntes_seleccionades = []
    st.session_state.mostra_solucio = False # Estat per saber si s'ha comprovat la resposta
    st.session_state.resposta_actual = None # Per guardar la tria de l'usuari abans de comprovar

# Pantalla inicial
if not st.session_state.iniciat and totes_preguntes:
    n_total = len(totes_preguntes)
    st.subheader("Configuració del Test")
    n_test = st.slider("Nombre de preguntes del test:", 1, n_total, min(10, n_total))
    if st.button("Començar test 🚀", type="primary"):
        # Selecciona un subconjunt aleatori de preguntes
        st.session_state.preguntes_seleccionades = random.sample(totes_preguntes, n_test)
        st.session_state.iniciat = True
        # Reinicia l'estat per si es reinicia des d'un test completat
        st.session_state.index = 0
        st.session_state.encerts = 0
        st.session_state.respostes_usuari = []
        st.session_state.mostra_solucio = False
        st.rerun() # Força el re-run per anar directament al test

# Test en curs
if st.session_state.iniciat and totes_preguntes:
    n_preguntes = len(st.session_state.preguntes_seleccionades)

    if st.session_state.index < n_preguntes:
        # Bloque dependent de la pregunta actual
        actual = st.session_state.preguntes_seleccionades[st.session_state.index]

        # Càlcul del progrés i visualització
        progress_value = (st.session_state.index) / n_preguntes
        st.progress(progress_value, text=f"Progrés: {st.session_state.index} / {n_preguntes}")

        st.write(f"### Pregunta {st.session_state.index + 1} de {n_preguntes}")
        st.markdown(f"**{actual['pregunta']}**")

        # Clau única per radio button per cada pregunta
        radio_key = f"pregunta_{st.session_state.index}"

        # Emmagatzemem la tria actual de l'usuari
        resposta_tria = st.radio("Tria una resposta:", actual["opcions"], key=radio_key, index=0)

        # ----------------------------------------------------
        # 1. Comprovar la resposta (Botó visible només si no s'ha comprovat)
        # ----------------------------------------------------
        if not st.session_state.mostra_solucio:
            if st.button("Comprovar resposta", type="primary"):
                correcta = actual["resposta"]

                # Log de la resposta i càlcul d'encert
                st.session_state.respostes_usuari.append((actual["pregunta"], resposta_tria, correcta))
                if resposta_tria == correcta:
                    st.session_state.encerts += 1

                # Actualitza l'estat per mostrar la solució i el botó 'Següent'
                st.session_state.mostra_solucio = True
                st.rerun() # Força el re-run per mostrar el feedback i el botó Següent

        # ----------------------------------------------------
        # 2. Mostrar feedback i Botó Següent (Visible només després de comprovar)
        # ----------------------------------------------------
        else:
            # Mostra el feedback de manera persistent
            correcta = actual["resposta"]

            # Agafem l'última resposta guardada que correspon a la pregunta actual
            _, resp_usuari, resp_correcta = st.session_state.respostes_usuari[-1]

            if resp_usuari == resp_correcta:
                st.success(f"✅ Correcte! La resposta és: `{resp_correcta}`")
            else:
                st.error(f"❌ Incorrecte. La resposta correcta era: `{resp_correcta}`. La teva resposta ha estat: `{resp_usuari}`")

            st.write("---")

            if st.button("Següent pregunta ▶️", type="secondary"):
                # Passa a la següent pregunta i reinicia l'estat de solució
                st.session_state.index += 1
                st.session_state.mostra_solucio = False
                st.rerun() # Força el re-run per carregar la nova pregunta

    else:
        # Test completat
        st.subheader("🎉 Test Finalitzat!")
        st.success(f"Has encertat {st.session_state.encerts} de {n_preguntes} preguntes.")
        st.balloons()

        # Resum d'incorrectes
        incorrectes = [ (preg, resp, corr) for preg, resp, corr in st.session_state.respostes_usuari if resp != corr ]
        if incorrectes:
            st.subheader("Respostes incorrectes a revisar:")
            for i, (preg, resp, corr) in enumerate(incorrectes, start=1):
                st.markdown(f"**{i}. {preg}**")
                st.markdown(f"&nbsp;&nbsp;&nbsp;❌ La teva resposta: `{resp}`")
                st.markdown(f"&nbsp;&nbsp;&nbsp;✅ Resposta correcta: `{corr}`")
        else:
            st.info("🥳 Has respost totes les preguntes correctament!")

        st.markdown("---")
        if st.button("Reiniciar test 🔄", type="primary"):
            # Reinicialitza tot l'estat
            st.session_state.index = 0
            st.session_state.encerts = 0
            st.session_state.respostes_usuari = []
            st.session_state.iniciat = False
            st.session_state.preguntes_seleccionades = []
            st.session_state.mostra_solucio = False
            st.rerun()

elif not totes_preguntes:
    st.warning("Si us plau, assegureu-vos de tenir un fitxer `preguntes.json` amb preguntes per iniciar el test.")
