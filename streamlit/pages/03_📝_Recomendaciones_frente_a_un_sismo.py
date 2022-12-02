
import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Earth Data",
    page_icon="🌍",
    layout="wide",   
    initial_sidebar_state="expanded")

with open("src/style_pages.css") as f:
 st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)


#Título principál de la página
st.title("¿Qué hacer frente a un Sismo?")


c1 = st.container()

with c1:
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown('<h2>Antes de un Sismo<h2>', unsafe_allow_html=True)
        st.markdown('''<section class="saltos">
            <ul  id='sec_asismo' style="margin-top=0%">
                <li class="big-font">En la construcción de una casa debemos tener en cuenta los parámetros de seguridad y diseño.</li>
                <li class="big-font">Debemos revisar con periodicidad las instalaciones de gas, electricidad y agua.</li>
                <li class="big-font">Tener preparada una mochila de emergencias con elementos de primeros auxilos, agua, comida enlatada, linterna y radio es fundamental</li>
                <li class="big-font">Participar de los simulacros de sismos es importante para saber a qué nos vamos a enfrentar.</li>
                <li class="big-font">Debemos identificar las zonas seguras y las salidas de emergencias.</li>
            </ul></section>''', unsafe_allow_html=True)

with col2:
    info_antes = Image.open(r'src/antes_sismos.jpg')
    st.image(info_antes, caption='¿Qué hacer antes de un sismo? (imagen)', use_column_width="auto")

c2 = st.container()

with c2:
    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.markdown('<h2>Durante un Sismo<h2>', unsafe_allow_html=True)
        st.markdown('''<section class="saltos"><ul>
            <li class="big-font">Conservar la calma y mantenerse alerta.</li>
            <li class="big-font">Colocarse debajo de objetos resistentes que nos puedan proteger.</li>
            <li class="big-font">Nos debemos alejar de muros, objetos pesados y ventanas de vidrio.</li>
            <li class="big-font">!NO USAR ASCENSORES! Debemos ir a zonas seguras.</li>
            <li class="big-font">Si estamos afuera debemos ubicarnos en un lugar despejado.</li>
            <li class="big-font">Si estamos conduciendo un auto debemos detenerlo y salir.</li>
        </ul></section>''', unsafe_allow_html=True)   
    
    with col2:
        info_durante = Image.open(r'src/durante_sismos.jpg')
        st.image(info_durante, caption='¿Qué hacer durante de un sismo? (imagen)', use_column_width="auto")   
    
c3 = st.container()

with c3:
    col1, col2 = st.columns([1.5, 1])    
    with col1:
        st.markdown('<h2>Después un Sismo<h2>', unsafe_allow_html=True)
        st.markdown('''<section><ul>
            <li class="big-font">Mantenerse preparado para las réplicas.</li>
            <li class="big-font">Debemos evacuar el lugar dónde estamos e ir a zonas seguras.</li>
            <li class="big-font">Revisamos si existen personas heridas.</li>
            <li class="big-font">Debemos revisar que las instalaciones de gas o electricidad no están dañadas.</li>
            <li class="big-font">Nos debemos comunicar por medio de mensajes de texto o aplicaciones móviles.</li>       
            <li class="big-font">Nos debemos mantener informados por medios de comunicación oficiales.</li>
        </ul></section>''', unsafe_allow_html=True)

    with col2:
        info_despues = Image.open(r'src/despues_sismos.jpg')
        st.image(info_despues, caption='¿Qué hacer después de un sismo? (imagen)', use_column_width="auto")


