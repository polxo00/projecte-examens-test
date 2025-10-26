import streamlit as st
import json
import random

# Carrega JSON
with open("preguntes.json", "r", encoding="utf-8") as f:
    totes_preguntes = json.load(f)

# Estat inicial
if "index" not in st.session_state:
    st.session_state.index = 0
    st.session_state.encerts = 0
    st.session_state.respostes_usuari = []
    st.session_state.iniciat = False
    st.session_state.preguntes_seleccionades = []

# Tria nombre de preguntes
if not st.session_state.iniciat:
    n_total = len(totes_preguntes)
    n_test = st.slider("Nombre de preguntes del test:", 1, n_total, min(10, n_total))
    if st.button("Començar test"):
        st.session_state.preguntes_seleccionades = random.sample(totes_preguntes, n_test)
        st.session_state.iniciat = True
        st.experimental_rerun()

# Si el test ha començat
if st.session_state.iniciat:
    n_preguntes = len(st.session_state.preguntes_seleccionades)
    actual = st.session_state.preguntes_seleccionades[st.session_state.index]

    st.progress(st.session_state.index / n_preguntes)
    st.write(f"**Pregunta {st.session_state.index + 1} de {n_preguntes}**")
    st.markdown(f"### {actual['pregunta']}")
    resposta = st.radio("Tria una resposta:", actual["opcions"], key=st.session_state.index)

    if st.button("Següent"):
        correcta = actual["resposta"]
        st.session_state.respostes_usuari.append((actual["pregunta"], resposta, correcta))

        if resposta == correcta:
            st.session_state.encerts += 1
            st.success(f"✅ Correcte! La resposta era: `{correcta}`")
        else:
            st.error(f"❌ Incorrecte. La resposta correcta era: `{correcta}`")

        # Incrementa i passa a la següent pregunta
        st.session_state.index += 1

        # Comprova si hem arribat al final
        if st.session_state.index >= n_preguntes:
            st.success(f"✅ Test completat! Has encertat {st.session_state.encerts} de {n_preguntes}.")
            st.balloons()
            st.subheader("Resultats:")
            for i, (preg, resp, corr) in enumerate(st.session_state.respostes_usuari, start=1):
                if resp == corr:
                else:
                    st.markdown(f"❌ **{i}. {preg}**")
                    st.markdown(f"&nbsp;&nbsp;&nbsp;Resposta correcta: `{corr}`")
            if st.button("Reiniciar test 🔄"):
                for k in ["index", "encerts", "respostes_usuari", "iniciat", "preguntes_seleccionades"]:
                    st.session_state[k] = 0 if k != "preguntes_seleccionades" else []
                st.experimental_rerun()
        else:
            st.experimental_rerun()
