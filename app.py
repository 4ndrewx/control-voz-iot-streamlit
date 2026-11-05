import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(
    page_title="Control por Voz - Interfaces Multimodales",
    page_icon="🎙️",
    layout="wide",
)

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown(
    """
    <style>
    .main { background-color: #0E1117; color: #F8FAFC; }
    .stSidebar { background-color: #161B22 !important; }
    .hero-banner {
        background: linear-gradient(135deg, #7C3AED 0%, #4F46E5 50%, #EC4899 100%);
        padding: 25px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }
    .card-box {
        background-color: #161B22;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #30363D;
        margin-bottom: 15px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- BARRA LATERAL: CONFIGURACIÓN IOT ---
st.sidebar.markdown("### 🌐 Configuración IoT")
st.sidebar.markdown(
    "<p style='color: #9CA3AF; font-size: 13px;'>Conexión con Broker MQTT"
    " Dashboard</p>",
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")

st.sidebar.markdown(
    "**Broker:** <span style='color: #10B981;'>broker.mqttdashboard.com</span>",
    unsafe_allow_html=True,
)
st.sidebar.markdown(
    "**Puerto:** <span style='color: #10B981;'>1883</span>",
    unsafe_allow_html=True,
)
st.sidebar.markdown(
    "**Tópico MQTT:** <span style='color: #10B981;'>voicemajo</span>",
    unsafe_allow_html=True,
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    '<div class="card-box" style="background-color: #1E2530; border-left: 4px'
    ' solid #3B82F6; font-size: 13px; color: #93C5FD;">💡 <b>Tip:</b>'
    " Asegúrate de dar permisos de micrófono a tu navegador cuando presiones el"
    " botón.</div>",
    unsafe_allow_html=True,
)

# --- CONTENIDO PRINCIPAL ---
st.markdown(
    """
    <div class="hero-banner">
        <h1 style="margin:0; font-size: 2.2rem;">🎙️ Control por Voz - Interfaces Multimodales</h1>
        <p style="margin-top: 8px; font-size: 1rem; opacity: 0.9;">Captura comandos de voz en tiempo real y transmite instrucciones vía MQTT a sistemas ciberfísicos.</p>
    </div>
""",
    unsafe_allow_html=True,
)

col_voice, col_control = st.columns(2)

with col_voice:
  st.markdown("### 🖼️ Asistente de Voz")
  # Tarjeta con la ilustración/icono de voz simulando la interfaz
  st.markdown(
      """
        <div style="background-color: #FFFFFF; padding: 30px; border-radius: 12px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.3); height: 320px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
            <svg width="180" height="180" viewBox="0 0 24 24" fill="#000000" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z"/>
                <path d="M19 10v1a7 7 0 0 1-14 0v-1H3v1a9 9 0 0 0 8 8.94V22h2v-2.06A9 9 0 0 0 21 11v-1h-2z"/>
            </svg>
        </div>
    """,
      unsafe_allow_html=True,
  )

with col_control:
  st.markdown("### 🔊 Reconocimiento de Voz")
  st.write("Haz clic en el botón inferior para comenzar a escuchar:")

  # Componente HTML/JS interactivo para Web Speech API y Paho MQTT
  voice_html_code = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/paho-mqtt/1.0.1/mqttws31.min.js" type="text/javascript"></script>
        <style>
            body { font-family: Arial, sans-serif; background-color: #161B22; color: white; margin: 0; padding: 15px; border-radius: 10px; border: 1px solid #30363D; }
            .btn-voice { background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%); color: white; border: none; padding: 12px 20px; font-weight: bold; border-radius: 8px; cursor: pointer; width: 100%; font-size: 15px; }
            .btn-voice:hover { background: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%); }
            .status { margin-top: 12px; font-size: 14px; color: #94A3B8; }
            .transcript { margin-top: 10px; background: #0E1117; padding: 10px; border-radius: 6px; color: #10B981; font-weight: bold; min-height: 25px; }
        </style>
    </head>
    <body>
        <button class="btn-voice" onclick="startListening()">🎤 Iniciar Escucha de Voz</button>
        <div class="status" id="status-text">Estado: En espera...</div>
        <div class="transcript" id="transcript-text">Comando reconocido: Ninguno</div>

        <script>
            // Configuración del cliente MQTT
            const client = new Paho.MQTT.Client("broker.mqttdashboard.com", Number(8000), "streamlit_voice_" + Math.random());
            
            client.onConnectionLost = (response) => {
                console.log("MQTT Conexión perdida: " + response.errorMessage);
            };

            client.connect({
                onSuccess: () => { console.log("Conectado al Broker MQTT"); },
                onFailure: (err) => { console.log("Error de conexión MQTT: " + err.errorMessage); }
            });

            function startListening() {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                if (!SpeechRecognition) {
                    alert("Tu navegador no soporta reconocimiento de voz. Usa Google Chrome.");
                    return;
                }

                const recognition = new SpeechRecognition();
                recognition.lang = 'es-ES';
                recognition.interimResults = false;
                recognition.maxAlternatives = 1;

                document.getElementById('status-text').innerText = "Estado: Escuchando activamente...";
                document.getElementById('status-text').style.color = "#F59E0B";

                recognition.start();

                recognition.onresult = (event) => {
                    const speechResult = event.results[0][0].transcript;
                    document.getElementById('transcript-text').innerText = "Comando: " + speechResult;
                    document.getElementById('status-text').innerText = "Estado: Comando enviado por MQTT 🚀";
                    document.getElementById('status-text').style.color = "#10B981";

                    // Publicar el comando por MQTT al tópico voicemajo
                    if (client.isConnected()) {
                        message = new Paho.MQTT.Message(speechResult);
                        message.destinationName = "voicemajo";
                        client.send(message);
                    }
                };

                recognition.onerror = (event) => {
                    document.getElementById('status-text').innerText = "Estado: Error en reconocimiento (" + event.error + ")";
                    document.getElementById('status-text').style.color = "#EF4444";
                };

                recognition.onspeechend = () => {
                    recognition.stop();
                };
            }
        </script>
    </body>
    </html>
    """

  components.html(voice_html_code, height=220)
