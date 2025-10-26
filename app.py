import streamlit as st
import json
import random

# Carrega JSON
with open("preguntes.json", "r", encoding="utf-8") as f:
    totes_preguntes = json.load(f)

# Inicialitza estat
if "index" not in st.session_state:
    st.session_state.index = 0
    st.session_state.encerts = 0
    st.session_state.respostes_usuari = []
    st.session_state.iniciat = False
    st.session_state.preguntes_seleccionades = []
    st.session_state.mostra_solucio = False

# Pantalla inicial
if not st.session_state.iniciat:
    n_total = len(totes_preguntes)
    n_test = st.slider("Nombre de preguntes del test:", 1, n_total, min(10, n_total))
    if st.button("Començar test"):
        st.session_state.preguntes_seleccionades = random.sample(totes_preguntes, n_test)
        st.session_state.iniciat = True

# Test en curs
if st.session_state.iniciat:
    n_preguntes = len(st.session_state.preguntes_seleccionades)

    if st.session_state.index < n_preguntes:
        # Bloque dependent de la pregunta actual
        actual = st.session_state.preguntes_seleccionades[st.session_state.index]

        st.progress(st.session_state.index / n_preguntes)
        st.write(f"**Pregunta {st.session_state.index + 1} de {n_preguntes}**")
        st.markdown(f"### {actual['pregunta']}")

        # Clau única per radio button per cada pregunta
        radio_key = f"pregunta_{st.session_state.index}"
        resposta = st.radio("Tria una resposta:", actual["opcions"], key=radio_key)

        # Botó únic per mostrar solució i passar a següent
        if st.button("Comprovar / Següent"):
            correcta = actual["resposta"]

            if not st.session_state.mostra_solucio:
                st.session_state.respostes_usuari.append((actual["pregunta"], resposta, correcta))
                if resposta == correcta:
                    st.session_state.encerts += 1
                    st.success(f"✅ Correcte! La resposta era: `{correcta}`")
                else:
                    st.error(f"❌ Incorrecte. La resposta correcta era: `{correcta}`")
                st.session_state.mostra_solucio = True
            else:
                st.session_state.index += 1
                st.session_state.mostra_solucio = False

    else:
        # Test completat
        st.success(f"✅ Test completat! Has encertat {st.session_state.encerts} de {n_preguntes}.")
        st.balloons()
        incorrectes = [ (preg, resp, corr) for preg, resp, corr in st.session_state.respostes_usuari if resp != corr ]
        if incorrectes:
            st.subheader("Respostes incorrectes:")
            for i, (preg, resp, corr) in enumerate(incorrectes, start=1):
                st.markdown(f"❌ **{i}. {preg}**")
                st.markdown(f"&nbsp;&nbsp;&nbsp;Resposta correcta: `{corr}`")
        else:
            st.info("✅ Has respost totes les preguntes correctament!")

        if st.button("Reiniciar test 🔄"):
            st.session_state.index = 0
            st.session_state.encerts = 0
            st.session_state.respostes_usuari = []
            st.session_state.iniciat = False
            st.session_state.preguntes_seleccionades = []
            st.session_state.mostra_solucio = False
