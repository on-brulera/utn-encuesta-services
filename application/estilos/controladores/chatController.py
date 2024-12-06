from flask_restful import Resource
from flask import request, jsonify
from datetime import datetime, timedelta
import json
import urllib.request

from application.estilos.modelos.asignacionModel import Asignacion
from application.estilos.modelos.credencialesApiModel import CredencialesAPI
from application.estilos.modelos.cursoModel import Curso
from application.estilos.modelos.encuestaModel import Encuesta
from application.estilos.modelos.historialModel import Historial, HistorialSchema
from application.estilos.modelos.materiaModel import Materia
from application.estilos.modelos.notaModel import Nota
from application.utils.response import Response

# Diccionario para manejar sesiones temporales
sesiones = {}
apyKeyOpenAi = ''

class ChatController(Resource):
    def __init__(self):
        super().__init__()

    def post(self):
        """
        Inicia un nuevo chat con el usuario y almacena los datos en una sesión temporal.
        """
        try:
            # Recibir cedula desde el cliente
            datos = request.get_json()
            cedula = datos.get("cedula")
            esEstudiante = datos.get("esEstudiante")
            

            if not cedula:
                return {"mensaje": "Faltan datos para iniciar el chat. (cedula requerido)"}, 400

            # Consultar datos del usuario en la tabla Historial con los detalles completos

            if esEstudiante:

                consulta = (
                    Historial.query
                    .with_entities(
                        Historial.est_cedula,
                        Historial.his_nota_estudiante,
                        Historial.his_resultado_encuesta,
                        Encuesta.enc_titulo,
                        Encuesta.enc_autor,
                        Asignacion.par_parcial_seleccionado,
                        Curso.cur_carrera,
                        Materia.mat_nombre,
                        Curso.cur_nivel,
                        Nota.not_nota
                    )
                    .join(Asignacion, Asignacion.asi_id == Historial.asi_id)
                    .join(Encuesta, Asignacion.enc_id == Encuesta.enc_id)
                    .join(Curso, Asignacion.cur_id == Curso.cur_id)
                    .join(Materia, Asignacion.mat_id == Materia.mat_id)
                    .join(
                        Nota,
                        (Nota.mat_id == Materia.mat_id)
                        & (Nota.cur_id == Curso.cur_id)
                        & (Nota.usu_id == Asignacion.usu_id)
                        & (Nota.par_id == Asignacion.par_parcial_seleccionado)
                    )
                    .filter(Historial.est_cedula == cedula)
                    .all()
                )

                if consulta:
                    # Convertir resultados en un diccionario para contextualización
                    historial_serializado = [
                        {
                            "est_cedula": row.est_cedula,
                            "his_nota_estudiante": row.his_nota_estudiante,
                            "his_resultado_encuesta": row.his_resultado_encuesta,
                            "enc_titulo": row.enc_titulo,
                            "enc_autor": row.enc_autor,
                            "par_parcial_seleccionado": row.par_parcial_seleccionado,
                            "cur_carrera": row.cur_carrera,
                            "mat_nombre": row.mat_nombre,
                            "cur_nivel": row.cur_nivel,
                            "not_nota": row.not_nota
                        }
                        for row in consulta
                    ]

                    # Crear datos del usuario para la sesión
                    datosUsuario = {"cedula": cedula, "historial": historial_serializado}


                    # Crear el mensaje inicial para el usuario
                    if historial_serializado:
                        mensaje_inicial = f"Hola, veo que tienes un historial con {len(historial_serializado)} resultados.\n \n"
                        for h in historial_serializado:
                            mensaje_inicial += (
                                f"En la materia {h['mat_nombre']}, se tomó la encuesta '{h['enc_titulo']}' "
                                f"durante el parcial {h['par_parcial_seleccionado']}. Tu resultado fue: '{h['his_resultado_encuesta']}' "
                                f"y tu nota fue: {h['not_nota']}.\n \n"
                            )
                        mensaje_inicial += "¿En qué materia o estilo específico necesitas ayuda?"
                    else:
                        mensaje_inicial = (
                            f"Hola, no encontré un historial previo asociado a tu cédula {cedula}.\n"
                            f"¿En qué materia o estilo específico necesitas ayuda?"
                        )


                    # Crear contexto para OpenAI
                    mensaje_chat_ia = f"Soy estudiante, cédula {cedula} de " + historial_serializado[0]['cur_carrera'] + "respondi encuestas: " 
                    for h in historial_serializado:
                        mensaje_chat_ia += (
                            f"- {h['enc_titulo']} del Autor: {h['enc_autor']}\n"
                            f" en la Materia: {h['mat_nombre']}.\n"
                            f" en la Parcial: {h['par_parcial_seleccionado']}, mi Nota Parcial fue: {h['not_nota']}.\n"
                            f" mi nota de encuesta cualitativa: {h['his_nota_estudiante']} .\n"
                            f" y el resultado de encuesta: {h['his_resultado_encuesta']}.\n"
                       )            

                else:
                    # Sin historial
                    datosUsuario = {"cedula": cedula, "historial": []}
                    mensaje_inicial = (
                        f"Hola, no encontré un historial previo asociado a tu cédula {cedula}.\n"
                        f"¿En qué materia o estilo específico necesitas ayuda?"
                    )
                    mensaje_chat_ia = (
                        f"Soy estudiante con cédula {cedula} no tengo historial registrado."
                    )
            else:                

                #PARA EL DOCENTE
                consulta = (
                    Asignacion.query
                    .with_entities(                        
                        Encuesta.enc_titulo,
                        Encuesta.enc_autor,                
                        Curso.cur_carrera,
                        Materia.mat_nombre,
                        Curso.cur_nivel,                      
                    )
                    .select_from(Asignacion)
                    .join(Encuesta, Encuesta.enc_id == Asignacion.enc_id)
                    .join(Curso, Curso.cur_id == Asignacion.cur_id)
                    .join(Materia, Materia.mat_id == Asignacion.mat_id)
                    .filter(Asignacion.usu_id_asignador == int(cedula))                    
                    .group_by(
                        Encuesta.enc_titulo,
                        Encuesta.enc_autor,                        
                        Curso.cur_carrera,
                        Materia.mat_nombre,
                        Curso.cur_nivel
                    )
                    .all()
                )

                if consulta:
                    # Convertir resultados en un diccionario para contextualización
                    historial_serializado = [
                        {
                            "enc_titulo": row.enc_titulo,
                            "enc_autor": row.enc_autor,                            
                            "cur_carrera": row.cur_carrera,
                            "mat_nombre": row.mat_nombre,
                            "cur_nivel": row.cur_nivel
                        }
                        for row in consulta
                    ]

                    # Crear el mensaje inicial para el docente
                    mensaje_inicial = f"Hola, veo que tienes datos de las siguientes encuestas:\n\n"
                    for h in historial_serializado:
                        mensaje_inicial += (
                            f"En la materia {h['mat_nombre']}, del nivel {h['cur_nivel']} en la carrera {h['cur_carrera']},\n"
                            f"se tomó la encuesta '{h['enc_titulo']}' (Autor: {h['enc_autor']}).\n\n"
                        )
                    mensaje_inicial += "¿En qué materia o estilo específico necesitas ayuda?"

                    # Crear contexto para OpenAI
                    mensaje_chat_ia = f"Soy docente con ID {cedula}, tengo los siguientes datos de encuestas:\n"
                    for h in historial_serializado:
                        mensaje_chat_ia += (
                            f"- Encuesta: {h['enc_titulo']} del Autor: {h['enc_autor']}\n"
                            f"  Carrera: {h['cur_carrera']}, Nivel: {h['cur_nivel']}, Materia: {h['mat_nombre']}\n"                            
                        )
                else:
                    # Sin historial
                    historial_serializado = []
                    mensaje_inicial = (
                        f"Hola, no encontré un historial previo asociado a tu cédula {cedula}.\n"
                        f"¿En qué materia o estilo específico necesitas ayuda?"
                    )
                    mensaje_chat_ia = (
                        f"El docente con ID {cedula} no tiene historial registrado."
                    )





            
            # Enviar el mensaje inicial al modelo OpenAI (llamada al método que maneja OpenAI)
            enviar_a_openai(mensaje_chat_ia)

            # Guardar datos en la sesión
            sesiones[cedula] = {
                "datos": mensaje_chat_ia,
                "expiracion": datetime.now() + timedelta(hours=4)
            }

            return {
                "mensaje": mensaje_inicial,
                # "respuesta_ia": respuesta_ia,  # Respuesta inicial de la IA                
            }, 200

        except Exception as e:
            return {
                "mensaje": "Error al iniciar el chat.",
                "error": str(e)
            }, 500


class HistorialWithCedulaAllComplete(Resource):
    def __init__(self):
        super().__init__()

    def get(self, est_cedula):
        try:
            consulta = (
                Historial.query
                .with_entities(
                    Historial.est_cedula,
                    Historial.his_nota_estudiante,
                    Historial.his_resultado_encuesta,
                    Encuesta.enc_titulo,
                    Encuesta.enc_autor,
                    Asignacion.par_parcial_seleccionado,
                    Curso.cur_carrera,
                    Materia.mat_nombre,
                    Curso.cur_nivel,
                    Nota.not_nota
                )
                .join(Asignacion, Asignacion.asi_id == Historial.asi_id)
                .join(Encuesta, Asignacion.enc_id == Encuesta.enc_id)
                .join(Curso, Asignacion.cur_id == Curso.cur_id)
                .join(Materia, Asignacion.mat_id == Materia.mat_id)
                .join(
                    Nota,
                    (Nota.mat_id == Materia.mat_id)
                    & (Nota.cur_id == Curso.cur_id)
                    & (Nota.usu_id == Asignacion.usu_id)
                    & (Nota.par_id == Asignacion.par_parcial_seleccionado)
                )
                .filter(Historial.est_cedula == est_cedula)
                .all()
            )

            # Convertir resultados en un diccionario para la respuesta
            data = [
                {
                    "est_cedula": row.est_cedula,
                    "his_nota_estudiante": row.his_nota_estudiante,
                    "his_resultado_encuesta": row.his_resultado_encuesta,
                    "enc_titulo": row.enc_titulo,
                    "enc_autor": row.enc_autor,
                    "par_parcial_seleccionado": row.par_parcial_seleccionado,
                    "cur_carrera": row.cur_carrera,
                    "mat_nombre": row.mat_nombre,
                    "cur_nivel": row.cur_nivel,
                    "not_nota": row.not_nota
                }
                for row in consulta
            ]

            return Response.ok(data=data)

        except Exception as e:
            return Response.error(
                mensaje="Error al obtener el historial", error=str(e), status=500
            )


class MensajeController(Resource):
    def __init__(self):
        super().__init__()

    def post(self):
        """
        Procesa un mensaje del usuario y responde basado en el contexto de su sesión.
        """
        try:
            datos = request.get_json()
            cedula = datos.get("cedula")
            mensaje = datos.get("mensaje")
            mensajeChat = sesiones[cedula]["datos"] + ". Quiero saber: " + mensaje

            esEstudiante = datos.get("esEstudiante")            

            if not cedula or not mensaje:
                return jsonify({
                    "respuesta": "Faltan datos para procesar el mensaje. (cedula y mensaje requeridos)"
                }), 400

            # Verificar si la sesión existe y no ha expirado
            
            sesion = sesiones.get(cedula)
            
            if not sesion:
                return jsonify({
                    "respuesta": "La sesión no existe. Por favor, inicia el chat primero."
                }), 403

            if sesion["expiracion"] < datetime.now():
                return jsonify({
                    "respuesta": "La sesión ha expirado. Por favor, vuelve a iniciar el chat."
                }), 403            
            # Enviar el mensaje al modelo de OpenAI            
            respuesta_ia = enviar_a_openai( mensajeChat)            
            return {"respuesta": respuesta_ia}            

        except Exception as e:
            return {"respuesta": str(e)}            


class InterpretacionChatController(Resource):
    def __init__(self):
        super().__init__()

    def post(self):
        """
        Interpreta los resultados de los gráficos y proporciona recomendaciones.
        """
        try:
            datos = request.get_json()
            texto_datos = datos.get("texto_datos")  # Datos en formato string            

            if not texto_datos:
                return {"mensaje": "Faltan texto_datos en formato string para interpretar."}, 400
            

            # Enviar el contexto al modelo OpenAI
            respuesta_ia = enviar_a_openai(texto_datos)

            # Respuesta final
            return {
                "respuesta": respuesta_ia
            }, 200

        except Exception as e:
            return {
                "mensaje": "Error al procesar la interpretación.",
                "error": str(e)
            }, 500

def enviar_a_openai(mensaje):
    """
    Envía un mensaje al modelo GPT de OpenAI y devuelve solo el texto de la respuesta.
    """

    global apyKeyOpenAi 

    try:        
        if not apyKeyOpenAi:            
            credencial = CredencialesAPI.query.filter_by(nombre_servicio="chat").first()
            if credencial:
                apyKeyOpenAi = credencial.api_key                
            else:
                raise ValueError("No se encontró una clave API válida para el servicio 'chat'.")
        
        url = "https://api.openai.com/v1/chat/completions"
        api_key = apyKeyOpenAi        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "Eres un asistente experto en estilos de aprendizaje, das respuestas muy directas y respondes mensajes en un máximo de 40 palabras, guardas la información del estudiante, cédula y estilos, el historial que tienes y puedes compartir sus datos con el, el estudiante sabe que guardas su información asi que no hace falta que lo menciones, si te piden una interpretación de datos puedes enviar texto hasta de 125 palabras"},
                {"role": "user", "content": mensaje}
            ],
            "temperature": 0.7
        }

        # Convertir el cuerpo de la solicitud a JSON
        json_data = json.dumps(data).encode('utf-8')

        # Crear la solicitud
        req = urllib.request.Request(url, data=json_data, headers=headers, method="POST")

        # Hacer la solicitud
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                respuesta_json = json.loads(response.read().decode('utf-8'))
                # Extraer el texto del contenido de la IA
                contenido = respuesta_json.get("choices", [])[0].get("message", {}).get("content", "")                
                return contenido.strip()  # Devuelve el texto como string
            else:
                # Manejar errores de la API de OpenAI
                error_message = f"Error en la API de OpenAI: {response.status} - {response.reason}"
                return error_message

    except urllib.error.URLError as e:
        # Manejar errores de conexión
        return f"No se pudo conectar a la API de OpenAI. Detalles: {e.reason}"



class LimpiarSesionesController(Resource):
    def __init__(self):
        super().__init__()

    def get(self):
        """
        Limpia todas las sesiones que hayan expirado.
        """
        try:
            ahora = datetime.now()
            expirados = [key for key, value in sesiones.items() if value["expiracion"] < ahora]
            for key in expirados:
                sesiones.pop(key)
            return {
                "mensaje": f"Se eliminaron {len(expirados)} sesiones expiradas."
            }, 200

        except Exception as e:
            return {
                "mensaje": "Error al limpiar sesiones.",
                "error": str(e)
            }, 500
        
