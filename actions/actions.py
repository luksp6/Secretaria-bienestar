# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import ast

def leerArchivo():
    archivo = open('usuarios.txt', 'r')
    contenido = archivo.read()
    archivo.close()
    return ast.literal_eval(contenido)

def escribirArchivo(dict):
    archivo = open('usuarios.txt', 'w')
    archivo.write(str(dict))
    archivo.close()

class ActionIdentificarse(Action):

    def name(self) -> Text:
        return "action_identificarse"

    #@staticmethod
    def agregarUsuario(self, dict, nuevo):
        datos = {
                    'edad' : None,
                    'carrera_interes' : None,
                    'taller_interes' : None,
                }
        if dict == None:
            return {nuevo : datos}
        else:
            dict[nuevo] = datos
            return dict

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        intent = tracker.latest_message['intent'].get('name')
        if (str(intent) == "identificarse"):
            nombre = next(tracker.get_latest_entity_values("nombres"), None)
            usuarios = leerArchivo()
            if usuarios != None:
                if not nombre in usuarios.keys():
                    usuarios = self.agregarUsuario(usuarios, nombre)
            else:
                usuarios = self.agregarUsuario(usuarios, nombre)
            salida = "¡Un gusto " + str(nombre) + "!"
            dispatcher.utter_message(text=str(salida))
            return [SlotSet("usuarios", usuarios), SlotSet("nombre", nombre)]
        else:
            return []

class ActionDocumentos(Action):

    def name(self) -> Text:
        return "action_documentos"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        if (str(intent) == "pedir_documentos"):
            documento = tracker.latest_message['entities'][0]['value']
            salida = "Para solicitar tu " + str(documento) + " debes: \n"
            if str(documento) == "certificado" :
                salida = salida + "1. Iniciar sesión con tu cuenta en el SIU Guarani"
            elif str(documento) == 'titulo' :
                salida = salida + "1. bla bla bla"
            dispatcher.utter_message(text=str(salida))

        return []

class ActionInfoCarreras(Action):

    def name(self) -> Text:
        return "action_info_carreras"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        if (intent == "pedir_info_carreras"):
            carrera = next(tracker.get_latest_entity_values("carreras"), None)
            salida = "Podrás obtener más información sobre la carrera de " + str(carrera) + " en la siguiente página: "
            if (str(carrera) == "Licenciatura en Logística Integral"):
                salida = salida + "http://www.quequen.unicen.edu.ar/?page_id=75"
            elif (str(carrera) == "Ingeniería Civil"):
                salida = salida + "http://www.quequen.unicen.edu.ar/?page_id=83"
            elif (str(carrera) == "Ingeniería Electromecánica"):
                salida = salida + "http://www.quequen.unicen.edu.ar/?page_id=90"
            elif (str(carrera) == "Ingeniería Industrial"):
                salida = salida + "http://www.quequen.unicen.edu.ar/?page_id=87"
            elif (str(carrera) == "Ingeniería Química"):
                salida = salida + "http://www.quequen.unicen.edu.ar/?page_id=117"
            elif (str(carrera) == "Ingeniería en Agrimensura"):
                salida = salida + "http://www.quequen.unicen.edu.ar/?page_id=3906"
            else:
                salida = "Parece que la carrera " + str(carrera) + " no existe en nuestra universidad. Te recuerdo las carreras con las que contamos:\n\t| Licenciatura en Logística Integral\n\t| Ingeniería Civil\n\t| Ingeniería Electromecánica\n\t| Ingeniería Industrial\n\t| Ingeniería Química\n\t| Ingeniería en Agrimensura"
            dispatcher.utter_message(text=str(salida))
            return [SlotSet("carrera_interes", carrera)]
        else:
            return []

class ActionInfoTalleres(Action):

    def name(self) -> Text:
        return "action_info_talleres"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        if (intent == "pedir_info_talleres"):
            taller = next(tracker.get_latest_entity_values("talleres"), None)
            salida = "Como norma general, los talleres se arbrirán si cumnplen con el cupo mínimo de 15 inscriptos.\n Valor de la cuota: $400/mes – Todos los talleres otorgan certificado expedido por la Secretaría de Extensión de la UNICEN"
            if (str(taller) == "APRENDER A APRENDER. TÉCNICAS DE ESTUDIO BASADAS EN NEUROAPRENDIZAJE"):
                salida = salida + "\n\t| Tallerista: Prof. Sandra Olthoff\n\t| Descripción: Técnicas de estudio basadas en neuroaprendizaje. Proceso de aprendizaje. Captación y selección de información. Codificación de la información. Memorización de contenidos. Sistemas mnemotécnicos.\n\t| Duración: 3 meses\n\t| Día y horario: Lunes de 17.00 a 19.00"
            elif (str(taller) == "CONCRETA TUS OBJETIVOS. CRECIMIENTO PERSONAL"):
                salida = salida + "\n\t| Tallerista: Prof. Sandra Olthoff\n\t| Descripción: Herramientas para determinar 'qué quiere' en su vida. Cambiar el paradigma 'no puedo' por 'si puedo'. Utilizar sus recursos internos y externos.\n\t| Duración: 3 meses\n\t| Día y horario: Lunes de 15.00 a 17.00."
            elif (str(taller) == "TALLER DE LENGUA ESPAÑOLA"):
                salida = salida + "\n\t| Tallerista: Téc. Sup. Luis Pérez\n\t| Descripción: Identificar palabras según su acentuación. Aplicar coherencia y cohesión en la elaboración de una respuesta de examen. Identificar recursos y estructura en los textos expositivos y argumentativos.\n\t| Duración: 2 meses\n\t| Día y horario: Miércoles de 16.00 a 18.00"
            elif (str(taller) == "TALLER DE 'PRODUCCIÓN Y REALIZACIÓN AUDIOVISUAL'"):
                salida = salida + "\n\t| Tallerista: Bianca Ratti\n\t| Descripción: Adquirir las herramientas básicas para la producción y la realización audiovisual, así como el reconocimiento social y cultural de todas las sensibilidades y narrativas en que se plasma la creatividad política y cultural de nuestras sociedades.\n\t| Duración: 3 meses\n\t| Día y horario: Lunes de 17.00 a 19.00"
            elif (str(taller) == "EDUCACIÓN CANINA INCLUSIVA"):
                salida = salida + "\n\t| Tallerista: Natalia Ugolini\n\t| Descripción: actividades en las que el propietario pueda aprender, entender y empatizar con su animal de compañía. Educación básica canina: conductas de sentado, echado, quedarse quieto, andar al lado y venir a la llamada.\n\t| Duración: 2 meses\n\t| Día y horario: Miércoles de 14.00 a 15.00, o de 15.00 a 16.00"
            elif (str(taller) == "INICIACIÓN AL DIBUJO"):
                salida = salida + "\n\t| Tallerista: Fabiana Luna\n\t| Descripción: El objetivo es conseguir que a través de una imagen dada busquen la suya propia.\n\t| Duración: 3 meses\n\t| Día y horario: Lunes 14.00 a 16.00"
            elif (str(taller) == "TALLER DE DISEÑO DE INTERIORES"):
                salida = salida + "\n\t| Tallerista: Leonardo Mejuto\n\t| Descripción: Incorporación de conocimientos esenciales a la hora de decorar, diseñar y proyectar una vivienda, desarrollar una mirada crítica y transformadora del espacio obteniendo el máximo resultado de acuerdo a la disponibilidad de los recursos dados. \n\t| Duración: 3 meses\n\t| Día y horario: Viernes de 16.30 a 18.30"
            elif (str(taller) == "DERECHO PARA NO ABOGADOS"):
                salida = salida + "\n\t| Tallerista: Abg. Ma. Eugenia Quehé\n\t| Descripción: Existe la ficción legal de qué: 'EL DERECHO SE PRESUME CONOCIDO POR TODOS' ¿Qué tan verdadera es esta ficción? ¿Qué tanto sabemos de Derecho los ciudadanos? El taller apunta a democratizar el saber del Derecho a todos los ciudadanos. Destinado a alumnos y publico en general.\n\t| Duración: 3 meses\n\t| Día y horario: Viernes de 16.00 a 18.00"
            elif (str(taller) == "ABOGACÍA PREVENTIVA"):
                salida = salida + "\n\t| Tallerista: Abg. Ma. Eugenia Quehé\n\t| Descripción: Se abordarán situaciones jurídicas que resultan de conocimiento imprescindible para que comerciantes y emprendedores, para que sean capaces de decidir cómo actuar en pos de la mitigación de conflictos legales.\n\t| Duración: 2 meses\n\t| Día y horario: Viernes de 14.00 a 16.00"
            elif (str(taller) == "HERRAMIENTAS PARA UN NEGOCIO EXITOSO"):
                salida = salida + "\n\t| Tallerista: Lic. Gabriela Rentería\n\t| Descripción: Comprender la importancia de la IDEA de negocio. Obtener conocimientos de formas legales de un negocio. Obtener herramientas para desarrollar un plan de negocios.\n\t| Duración: 3 meses\n\t| Día y horario: Jueves de 18.00 a 20.00"
            elif (str(taller) == "GESTIÓN GASTRONÓMICA: ADMINISTRACIÓN Y CONTROL DE COSTOS E INGENIERÍA DE MENÚ"):
                salida = salida + "\n\t| Tallerista: Lic. Gabriela Rentería\n\t| Descripción: controlar y reportar los costos de alimentos y bebidas, comprender la importancia de la estandarización de recetas. Fijar precios de venta y, diseñar un menú acorde a los clientes a quienes deseen dirigirse contemplando su rentabilidad y popularidad.\n\t| Duración: 3 meses\n\t| Día y horario: Jueves de 14.00 a 16.00"
            elif (str(taller) == "INTRODUCCIÓN AL CONOCIMIENTO DEL CAFÉ, TÉ, CHOCOLATE Y YERBA MATE"):
                salida = salida + "\n\t| Tallerista: Lic. Gabriela Rentería\n\t| Descripción: Obtener conocimientos de cómo se produce y de servicios del café, té, chocolate y yerba mate\n\t| Duración: 2 meses\n\t| Día y horario: Miércoles de 13.00 a 15.00"
            elif (str(taller) == "INTRODUCCIÓN AL CONOCIMIENTO DEL VINO Y MARIDAJE"):
                salida = salida + "\n\t| Tallerista: Lic.Gabriela Rentería\n\t| Descripción: Obtener conocimientos de cómo se produce la transformación de la uva en vino. Nociones de coctelería. Reconocer los tipos de licores y aguardientes y también cómo organizar las tareas en un bar.\n\t| Duración: 2 meses\n\t| Día y horario: Miércoles de 17.30 a 19.30"
            elif (str(taller) == "TALLER DE LENGUA ITALIANA"):
                salida = salida + "\n\t| Tallerista: Eduardo Montalti\n\t| Descripción: Lectura y comprensión de la lengua a nivel básico. Expresiones de uso habitual y frases de base para necesidades concretas en lo cotidiano.\n\t| Duración: 3 meses\n\t| Día y horario: Viernes de 16.00 a 18.00"
            elif (str(taller) == "COMUNICACIÓN Y MARKETING DIGITAL PARA EMPRENDEDORES Y CURIOSOS"):
                salida = salida + "\n\t| Tallerista: Lic. Anahí Herrero\n\t| Descripción: Qué se comunica, de qué manera, cada cuánto, qué refleja en sus mensajes. Identificación de fortalezas y debilidades. Reconocimiento de oportunidades y desafíos de la presencia online.\n\t| Duración: 2 meses\n\t| Día y horario: Viernes de 17.30 a 19.00"
            else:
                salida = "Parece que el taller " + str(taller) + " no esta disponible en nuestra universidad."
            dispatcher.utter_message(text=str(salida))
            return [SlotSet("taller_interes", taller)]
        else:
            return []

class ActionCerrarSesion(Action):

    def name(self) -> Text:
        return "action_cerrar_sesion"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        if (intent == "goodbye"):
            usuarios = tracker.get_slot("usuarios")
            for llave in usuarios[tracker.get_slot("nombre")].keys():
                if tracker.get_slot(llave) != None:
                    usuarios[tracker.get_slot("nombre")][llave] = tracker.get_slot(llave)
            escribirArchivo(usuarios)
        return [SlotSet("usuarios", usuarios)]