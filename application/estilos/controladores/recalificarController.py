from datetime import datetime
from flask import request, jsonify
import json
from flask_restful import Resource
from application.estilos.modelos.asignacionModel import Asignacion
from application.estilos.modelos.historialModel import Historial
from application.estilos.modelos.respuestaModel import Respuesta
from application.estilos.modelos.reglasCalculoModel import ReglasCalculo

class RecalificarTest(Resource):
    def post(self):
        try:
            datos = request.get_json()
            id_asignacion = datos.get('idAsignacion')
            respuestas = datos.get('respuestas', [])
            reglas_json = datos.get('reglas_json', [])

            if not id_asignacion:
                return jsonify({"mensaje": "Bad Request", "error": "El campo 'idAsignacion' es obligatorio"})

            resultado_encuesta, nota_estudiante = recalificar_test(respuestas, reglas_json)

            historial = Historial.query.filter_by(asi_id=id_asignacion).first()
            if not historial:
                return jsonify({"mensaje": "Error", "error": "No se encontró el historial para la asignación proporcionada"})                        
            
            nota_estudiante_dict = {}
            for item in nota_estudiante:
                for key, value in item.items():
                    if key in nota_estudiante_dict:
                        nota_estudiante_dict[key] += value
                    else:
                        nota_estudiante_dict[key] = value
            
            historial.his_resultado_encuesta = resultado_encuesta
            historial.his_nota_estudiante = json.dumps(nota_estudiante_dict)

            historial.save()

            return jsonify({"mensaje": "Éxito", "data": {"his_resultado_encuesta": resultado_encuesta, "his_nota_estudiante": nota_estudiante}})

        except Exception as e:
            return jsonify({"mensaje": "Error desconocido", "error": str(e)})

def recalificar_test(respuestas, reglas_json):
    conteo_estilo_s = {}
    sumatoria_estilos = []
    conteo_parametros = {}

    # Inicializar conteo de estilos basado en las reglas
    for regla in reglas_json[0].get('reglas_json', []):
        conteo_estilo_s[regla.get('estilo')] = False

    # Contar el valor cuantitativo por estilo
    for respuesta in respuestas:
        estilo = respuesta.get('opcion', {}).get('valor_cualitativo')
        valor_opc = respuesta.get('opcion', {}).get('valor_cuantitativo', 0)

        if estilo:
            if estilo not in conteo_parametros:
                conteo_parametros[estilo] = 0

            conteo_parametros[estilo] += valor_opc

    # Evaluar condiciones basadas en las reglas
    for regla in reglas_json[0].get('reglas_json', []):
        estilo = regla.get('estilo')
        condiciones = regla.get('condiciones', [])
        suma_parametros = 0
        operacion = ''
        operadores = []
        condiciones_evaluadas = []

        if condiciones:
            for condicion in condiciones:
                suma_respuestas = 0
                primer_parametro = True
                operadores_parciales = ''
                contador_param = 0

                for parametro in condicion.get('parametros', []):
                    suma_respuestas = 0
                    contador_param += 1
                    operadores_parciales += f"{parametro.get('value')} {operacion} "
                    
                    for respuesta in respuestas:
                        if respuesta.get('opcion', {}).get('valor_cualitativo') in parametro.get('value', []):
                            suma_respuestas += respuesta.get('opcion', {}).get('valor_cuantitativo', 0)

                    if primer_parametro:
                        suma_parametros = suma_respuestas
                        primer_parametro = False
                        operacion = parametro.get('operacion', '')
                    else:
                        suma_parametros = aplicar_operacion(suma_parametros, suma_respuestas, operacion)
                        operacion = parametro.get('operacion', '')

                if condicion.get('condicion') == 'ninguna':
                    sumatoria_estilos.append({estilo: suma_parametros})
                else:
                    resultado_condicion = evaluar_condicion(suma_parametros, condicion.get('condicion'), condicion.get('valor'))
                    operadores.append(resultado_condicion)
                    suma_condiciones += suma_parametros
                    condiciones_evaluadas.append(condicion.get('comparacion'))

            resultado_final = evaluate_conditions(operadores, condiciones_evaluadas)
            conteo_estilo_s[estilo] = resultado_final

        else:
            suma_total = conteo_parametros.get(estilo, 0)
            sumatoria_estilos.append({estilo: suma_total})

    max_valor = max(valor for obj in sumatoria_estilos for valor in obj.values())

    resultado = [{estilo: valor == max_valor} for obj in sumatoria_estilos for estilo, valor in obj.items()]
    for res in resultado:
        clave, valor = list(res.items())[0]
        if clave in conteo_estilo_s:
            conteo_estilo_s[clave] = valor

    resultado_encuesta = generar_mensaje_estilo_predominante(conteo_estilo_s)
    nota_estudiante = sumatoria_estilos

    return resultado_encuesta, nota_estudiante

def aplicar_operacion(valor1, valor2, operacion):
    if operacion == '+':
        return valor1 + valor2
    elif operacion == '-':
        return valor1 - valor2
    elif operacion == '*':
        return valor1 * valor2
    elif operacion == '/':
        return valor1 / valor2
    else:
        return valor1

def evaluar_condicion(suma_parametros, condicion, valor):
    if condicion == 'mayor':
        return suma_parametros > valor
    elif condicion == 'menor':
        return suma_parametros < valor
    elif condicion == 'igual':
        return suma_parametros == valor
    else:
        return False

def evaluate_conditions(operadores, condiciones):
    for operador, condicion in zip(operadores, condiciones):
        if not operador:
            return False
    return True

def generar_mensaje_estilo_predominante(conteo_estilo_s):
    estilos_predominantes = [estilo for estilo, es_predominante in conteo_estilo_s.items() if es_predominante]
    if not estilos_predominantes:
        return 'No se ha identificado ningún estilo predominante.'
    elif len(estilos_predominantes) == 1:
        return f'{estilos_predominantes[0]}.'
    else:
        return f'Posees rasgos relacionados a los estilos {", ".join(estilos_predominantes)}.'





#PARA LOS TEST DE LA APP MOVIL


class RecalificarTestApp(Resource):
    def post(self):
        try:
            # Obtener datos del cuerpo de la solicitud
            datos = request.get_json()
            modelo = datos.get("Modelo")
            respuestas = datos.get("respuestas", [])
            reglas_json = datos.get("reglas_json", [])
            id_asignacion = datos.get("idAsignacion")

            # Validar modelo
            if not modelo:
                return jsonify({"mensaje": "Bad Request", "error": "El campo 'Modelo' es obligatorio"}), 400

            if not respuestas or not reglas_json:
                return jsonify({"mensaje": "Bad Request", "error": "Faltan respuestas o reglas_json"}), 400

            # Seleccionar función según el modelo
            if modelo == "Modelo1":
                resultado_encuesta, conteo_estilos = recalificar_test_dinamico_Modelo1(respuestas, reglas_json)
            elif modelo == "Modelo2":
                resultado_encuesta, conteo_estilos = recalificar_test_dinamico_Modelo2(respuestas, reglas_json)
            elif modelo == "Modelo3":
                resultado_encuesta = recalificar_test_dinamico_Modelo3(respuestas, reglas_json)
                conteo_estilos = None  # El modelo 3 devuelve un diccionario diferente
            else:
                return jsonify({"mensaje": "Bad Request", "error": f"Modelo '{modelo}' no soportado"}), 400

            # Convertir los datos a cadenas para almacenar en la base de datos
            his_nota_estudiante = json.dumps(conteo_estilos) if conteo_estilos else None
            his_resultado_encuesta = str(resultado_encuesta) if resultado_encuesta else None

            asignacionFiltrada = Asignacion.get_by_id(id_asignacion)

            # Crear un nuevo registro de historial
            historial = Historial(
                asi_id=id_asignacion,
                cur_id=asignacionFiltrada.cur_id,  # Manejar campos opcionales
                est_cedula=datos.get("est_cedula", None),  # Manejar campos opcionales
                his_fecha_encuesta=datetime.utcnow(),
                his_nota_estudiante=his_nota_estudiante,
                his_resultado_encuesta=his_resultado_encuesta,
            )

            # Guardar en la base de datos
            historial.save()

            return jsonify({
                "mensaje": "Éxito",
                "data": {
                    "his_resultado_encuesta": resultado_encuesta,
                    "his_nota_estudiante": conteo_estilos,
                }
            })

        except KeyError as e:
            return jsonify({
                "mensaje": "Error de clave",
                "error": f"Falta el campo obligatorio: {e.args[0]}"
            }), 400
        except Exception as e:
            return jsonify({
                "mensaje": "Error desconocido",
                "error": str(e)
            }), 500

def recalificar_test_dinamico_Modelo1(respuestas, reglas_json):
    # Inicializamos el conteo dinámico para los estilos que estén en las reglas
    conteo_estilos = {}
    for regla in reglas_json[0]["reglas_json"]:
        estilo = regla["estilo"]
        if estilo not in conteo_estilos:
            conteo_estilos[estilo] = 0

    # Procesamos las respuestas para sumar los valores según las reglas
    for respuesta in respuestas:
        for regla in reglas_json[0]["reglas_json"]:
            if regla["pregunta"] == respuesta["pregunta"]:
                if respuesta["opcion"]["valor_cualitativo"] in regla["opciones"]:
                    conteo_estilos[regla["estilo"]] += respuesta["opcion"]["valor_cuantitativo"]

    # Identificar los estilos con la puntuación más alta
    max_valor = max(conteo_estilos.values())
    estilos_predominantes = [
        estilo for estilo, valor in conteo_estilos.items() if valor == max_valor
    ]

    # Generar el resultado
    if len(estilos_predominantes) > 1:
        resultado_encuesta = (
            f"Hay un empate entre los estilos: {', '.join(estilos_predominantes)}"
        )
    else:
        resultado_encuesta = f"El estilo predominante es: {estilos_predominantes[0]}"

    return resultado_encuesta, conteo_estilos



def recalificar_test_dinamico_Modelo2(respuestas, reglas_json):
    # BASADO EN GARDNER
    # Inicializamos el conteo de inteligencias dinámicamente
    conteo_inteligencias = {}
    for regla in reglas_json[0]["reglas_json"]:
        estilo = regla["estilo"]
        if estilo not in conteo_inteligencias:
            conteo_inteligencias[estilo] = 0

    # Procesamos las respuestas para sumar los valores según las reglas
    respuestas_verdaderas = {"V", "v", "Verdadero", "verdadero"}  # Valores válidos
    for respuesta in respuestas:
        if respuesta["respuesta"] in respuestas_verdaderas:  # Validar respuesta como verdadera
            for regla in reglas_json[0]["reglas_json"]:
                if respuesta["pregunta"] in regla["preguntas"]:
                    conteo_inteligencias[regla["estilo"]] += 1

    # Identificar el(los) estilo(s) predominante(s)
    max_puntaje = max(conteo_inteligencias.values())
    estilos_predominantes = [
        estilo for estilo, puntaje in conteo_inteligencias.items() if puntaje == max_puntaje
    ]

    # Generar el mensaje de resultado
    if len(estilos_predominantes) > 1:
        resultado_encuesta = (
            f"Hay un empate entre las inteligencias predominantes: {', '.join(estilos_predominantes)}"
        )
    else:
        resultado_encuesta = f"Tu inteligencia predominante es: {estilos_predominantes[0]}"

    return resultado_encuesta, conteo_inteligencias



def recalificar_test_dinamico_Modelo3(respuestas, reglas_json):
    #BASADO EN EL TEST DE FELDER Y SILVERMAN
    # Inicializamos el conteo dinámico para cada categoría y sus estilos
    conteo_estilos = {}
    for regla in reglas_json[0]["reglas_json"]:
        categoria = regla["estilo"]
        if categoria not in conteo_estilos:
            conteo_estilos[categoria] = {"A": 0, "B": 0}

    # Contar respuestas por categoría
    for respuesta in respuestas:
        for regla in reglas_json[0]["reglas_json"]:
            if respuesta["pregunta"] in regla["preguntas"]:
                conteo_estilos[regla["estilo"]][respuesta["respuesta"]] += 1

    # Calcular diferencias y determinar estilo predominante
    resultados = {}
    for categoria, conteos in conteo_estilos.items():
        estilo_a, estilo_b = categoria.split("-")
        diferencia = abs(conteos["A"] - conteos["B"])
        estilo_predominante = estilo_a if conteos["A"] > conteos["B"] else estilo_b
        resultados[categoria] = {
            "diferencia": diferencia,
            "predominante": estilo_predominante,
            "detalle": conteos,
        }

    return resultados
