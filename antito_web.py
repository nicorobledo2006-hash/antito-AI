import streamlit as st
from groq import Groq
import base64

# 1. Configuración
st.set_page_config(page_title="Antito AI", page_icon="💖",layout="wide")

# 2. Función para el fondo de My Melody
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: contain;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-color: #FFC0CB; /* Color de fondo rosa pastel para complementar la imagen */
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('antito.PNG')

# 3. Lógica de Groq
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("💖 Antito AI")
st.subheader("Tu mejor amig@ y confidente")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Cuéntame algo, soy Antito..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Creamos la lista de mensajes incluyendo la instrucción de personalidad
            messages_for_api = [
                {
                    "role": "system", 
                    "content": "Tu nombre es Antito. Eres mi mejor amig@. Hablas siempre en español neutro. No eres una IA, eres Antito."
                }
            ]
            # Añadimos el historial
            for m in st.session_state.messages:
                messages_for_api.append({"role": m["role"], "content": m["content"]})

            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages_for_api
            )
            
            # Arreglo del error 'list'
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error: {e}")
set_background("antito.PNG")