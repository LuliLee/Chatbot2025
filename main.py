#LIBRERIAS
import streamlit as st
import groq

#SALUDOS
st.title("Streamlit")
nombre = st.text_input("¿Cuál es tu nombre?")

if st.button("Saludar"):
    st.write("Hola " + nombre)

#VARIABLES

altura_contenedor_chat = 400
stream_status = True

#CONSTANTES
MODELOS =  ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"]

#FUNCIONES

#ESTA FUNCIÓN UTILIZA STREAMLIT PARA CREAR LA INTERFAZ DE LA PÁGINA Y ADEMÁS RETORNA EL 
# #MODELO ELEGIDO POR EL USUARIO

st.set_page_config(page_title="Chatbot", page_icon="❤️") 

def configurar_pagina(): 

    st.title("Chatbot")

    st.sidebar.title("Seleccion de modelos")

    elegirModelo = st.sidebar.selectbox("Elegí un modelo", options=MODELOS, index=0)

    return elegirModelo

#ESTA FUNCIÓN LLAMA A st.secrets PARA OBTENER LA CLAVE DE LA API DE GROZ Y CREA UN USUARIO
def crear_usuario():    
    clave_secreta = st.secrets["CLAVE_API"]
    return groq.Groq(api_key = clave_secreta)

#CONFIGURA EL MODELO DE LENGUAJE PARA QUE PROCESE EL PROMPT DEL USUARIO
def configurar_modelo(cliente, modelo_elegido, prompt_usuario):
    return cliente.chat.completions.create(
        model = modelo_elegido,
        messages = [{"role":"user","content":prompt_usuario}],
        stream = stream_status
    )

#CREAMOS UNA SESIÓN LLAMADA "mensajes" QUE VA A GUARDAR LO QUE LE ESCRIBIMOS AL CHATBOT
def inicializar_estado():
    if "mensajes" not in st.session_state: #si no hay un msj
        st.session_state.mensajes = [] #guarda los msj del usuario

def actualizar_historial(rol, contenido, avatar): #el chat va a tener un contenido, rol y avatar
    st.session_state.mensajes.append({"role" : rol, "content" : contenido,
                                     "avatar" : avatar}) #agrega a la lista de msjs el msj que introdujo el usuario

def mostrar_historial(): #esta función hace que se guarde el historial y se escriban los msjs
    for mensaje in st.session_state.mensajes: 
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.write(mensaje["content"]) #escribe el contenido del historial 

def area_chat():
    contenedor = st.container(height=altura_contenedor_chat, border=True) #el contenedor es el rectángulo en donde se muestra el código
    with contenedor: #con la función with se abre y se cierra de forma segura el contenedor
        mostrar_historial()

def generar_respuesta(respuesta_completa_del_bot):
    _respuesta_posta = ""
    for frase in respuesta_completa_del_bot:#recorre todo el msj del chatbot
        if frase.choices[0].delta.content:#busca estas cosas y si encontramos 
            _respuesta_posta += frase.choices[0].delta.content #lo agrega a la respuesta posta 
            yield frase.choices[0].delta.content #generar variables de forma gradual. Hace que se vaya escribiendo frase por frase 
    return _respuesta_posta

#-----------------------IMPLEMENTACIÓN-----------------------
def main():

    modelo_elegido_por_el_usuario = configurar_pagina()

    cliente_usuario = crear_usuario()

    inicializar_estado()
    area_chat()

    prompt_del_usuario = st.chat_input("Escribi tu prompt:")

    if prompt_del_usuario: #si promptDelUsuario es distinto al vacío 
        actualizar_historial("user", prompt_del_usuario, "💖") #escribe el usuario
        respuesta_del_bot = configurar_modelo(cliente_usuario, modelo_elegido_por_el_usuario, prompt_del_usuario) #responde el chatbot
        
        if respuesta_del_bot:
            with st.chat_message("assistant"):
                respuesta_posta = st.write_stream(generar_respuesta(respuesta_del_bot))
                actualizar_historial("assistant", respuesta_posta, "🥰")
                st.rerun() #espera otro msj y muestra el historial

if __name__=="__main__":
    main()
