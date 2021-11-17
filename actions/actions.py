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

    def agregarUsuario(self, dict, nuevo):
        datos = {
                    'edad' : None,
                    'carrera_interes' : None,
                    'taller_interes' : None,
                    'beca_interes' : None,
                    'ingresante/reinscripto' : None,
                    'mood' : []
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
            verif = 0
            salida = "Podrás obtener más información sobre la carrera de " + str(carrera) + " en la siguiente página: "
            if (str(carrera) == "logistica"):
                salida = salida + "http://www.quequen.unicen.edu.ar/?page_id=75"
            elif (str(carrera) == "civil"):
                salida = salida + "http://www.quequen.unicen.edu.ar/?page_id=83"
            elif (str(carrera) == "electromecanica"):
                salida = salida + "http://www.quequen.unicen.edu.ar/?page_id=90"
            elif (str(carrera) == "industrial"):
                salida = salida + "http://www.quequen.unicen.edu.ar/?page_id=87"
            elif (str(carrera) == "quimica"):
                salida = salida + "http://www.quequen.unicen.edu.ar/?page_id=117"
            elif (str(carrera) == "agrimensura"):
                salida = salida + "http://www.quequen.unicen.edu.ar/?page_id=3906"
            else:
                salida = "Parece que la carrera " + str(carrera) + " no existe en nuestra universidad. Te recuerdo las carreras con las que contamos:\n\t| Licenciatura en Logística Integral\n\t| Ingeniería Civil\n\t| Ingeniería Electromecánica\n\t| Ingeniería Industrial\n\t| Ingeniería Química\n\t| Ingeniería en Agrimensura"
                verif = 1
            dispatcher.utter_message(text=str(salida))
            if (verif == 0):
                return [SlotSet("carrera_interes", carrera)]
            else:
                return []
        else:
            return []

class ActionInformacion(Action):

    def name(self) -> Text:
        return "action_informacion"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        if (intent == "pedir_informacion"):
            info = next(tracker.get_latest_entity_values("inf_general"), None)
            salida = "Para obtener informacion detallada sobre " + str(info) + " mira la siguiente página: "
            if (str(info) == "Calendario"):
                salida = salida + "http://www.quequen.unicen.edu.ar/wp-content/uploads/2021/08/2021-Calendario-Acad%C3%A9mico-UEUQ-DEFINITIVO-1.pdf"
            elif (str(info) == "Horarios"):
                salida = salida + "http://www.quequen.unicen.edu.ar/?page_id=83"
            elif (str(info) == "Fechas"):
                salida = salida + "http://www.quequen.unicen.edu.ar/?page_id=491"
            else:
                salida = ""
        else:
            return []

class ActionMateriasCarerra(Action):

    def name(self) -> Text:
        return "action_materias_carreras"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        if (intent == "preguntar_materia_carrera"):
            carrera = next(tracker.get_latest_entity_values("carreras"), None)
            verif = 0
            salida = "Las materias de la carrera " + str(carrera) + " estan colocadas en el plan de estudio donde veran correlatividades y cuales son las materias de su carrera, el siguiente link es para que lo puedas ver:  "
            if (str(carrera) == "logistica"):
                salida = salida + "http://quequen.unicen.edu.ar/wp-content/uploads/2012/10/plan-de-estudios-logistica.pdf"
            elif (str(carrera) == "civil"):
                salida = salida + "http://www.quequen.unicen.edu.ar/wp-content/uploads/2019/07/Plan-de-Estudio-CII.pdf"
            elif (str(carrera) == "electromecanica"):
                salida = salida + "http://www.quequen.unicen.edu.ar/wp-content/uploads/2019/07/Plan-de-Estudio-CII.pdf"
            elif (str(carrera) == "industrial"):
                salida = salida + "http://www.quequen.unicen.edu.ar/wp-content/uploads/2019/07/Plan-de-Estudio-CII.pdf"
            elif (str(carrera) == "quimica"):
                salida = salida + "http://www.quequen.unicen.edu.ar/wp-content/uploads/2019/07/Plan-de-Estudio-CII.pdf"
            elif (str(carrera) == "agrimensura"):
                salida = salida + "http://www.quequen.unicen.edu.ar/wp-content/uploads/2019/07/Plan-de-Estudio-CII.pdf"
            else:
                salida = "Parece que la carrera " + str(carrera) + " no existe en nuestra universidad. Te recuerdo las carreras con las que contamos:\n\t| Licenciatura en Logística Integral\n\t| Ingeniería Civil\n\t| Ingeniería Electromecánica\n\t| Ingeniería Industrial\n\t| Ingeniería Química\n\t| Ingeniería en Agrimensura"
                verif = 1
            dispatcher.utter_message(text=str(salida))
            if (verif == 0):
                return [SlotSet("carrera_interes", carrera)]
            else:
                return []
        else:
            return []            

class ActionInfoTalleres(Action):

    def name(self) -> Text:
        return "action_info_talleres"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        if (intent == "pedir_info_talleres"):
            taller = next(tracker.get_latest_entity_values("talleres"), None)
            verif = 0
            salida = "Como norma general, los talleres se arbrirán si cumnplen con el cupo mínimo de 15 inscriptos.\n Valor de la cuota: $400/mes – Todos los talleres otorgan certificado expedido por la Secretaría de Extensión de la UNICEN"
            if (str(taller) == "neuroaprendizaje"):
                salida = salida + "\n\t| Tallerista: Prof. Sandra Olthoff\n\t| Descripción: Técnicas de estudio basadas en neuroaprendizaje. Proceso de aprendizaje. Captación y selección de información. Codificación de la información. Memorización de contenidos. Sistemas mnemotécnicos.\n\t| Duración: 3 meses\n\t| Día y horario: Lunes de 17.00 a 19.00"
            elif (str(taller) == "crecimiento"):
                salida = salida + "\n\t| Tallerista: Prof. Sandra Olthoff\n\t| Descripción: Herramientas para determinar 'qué quiere' en su vida. Cambiar el paradigma 'no puedo' por 'si puedo'. Utilizar sus recursos internos y externos.\n\t| Duración: 3 meses\n\t| Día y horario: Lunes de 15.00 a 17.00."
            elif (str(taller) == "español"):
                salida = salida + "\n\t| Tallerista: Téc. Sup. Luis Pérez\n\t| Descripción: Identificar palabras según su acentuación. Aplicar coherencia y cohesión en la elaboración de una respuesta de examen. Identificar recursos y estructura en los textos expositivos y argumentativos.\n\t| Duración: 2 meses\n\t| Día y horario: Miércoles de 16.00 a 18.00"
            elif (str(taller) == "audiovisual"):
                salida = salida + "\n\t| Tallerista: Bianca Ratti\n\t| Descripción: Adquirir las herramientas básicas para la producción y la realización audiovisual, así como el reconocimiento social y cultural de todas las sensibilidades y narrativas en que se plasma la creatividad política y cultural de nuestras sociedades.\n\t| Duración: 3 meses\n\t| Día y horario: Lunes de 17.00 a 19.00"
            elif (str(taller) == "canina"):
                salida = salida + "\n\t| Tallerista: Natalia Ugolini\n\t| Descripción: actividades en las que el propietario pueda aprender, entender y empatizar con su animal de compañía. Educación básica canina: conductas de sentado, echado, quedarse quieto, andar al lado y venir a la llamada.\n\t| Duración: 2 meses\n\t| Día y horario: Miércoles de 14.00 a 15.00, o de 15.00 a 16.00"
            elif (str(taller) == "dibujo"):
                salida = salida + "\n\t| Tallerista: Fabiana Luna\n\t| Descripción: El objetivo es conseguir que a través de una imagen dada busquen la suya propia.\n\t| Duración: 3 meses\n\t| Día y horario: Lunes 14.00 a 16.00"
            elif (str(taller) == "interiores"):
                salida = salida + "\n\t| Tallerista: Leonardo Mejuto\n\t| Descripción: Incorporación de conocimientos esenciales a la hora de decorar, diseñar y proyectar una vivienda, desarrollar una mirada crítica y transformadora del espacio obteniendo el máximo resultado de acuerdo a la disponibilidad de los recursos dados. \n\t| Duración: 3 meses\n\t| Día y horario: Viernes de 16.30 a 18.30"
            elif (str(taller) == "derecho"):
                salida = salida + "\n\t| Tallerista: Abg. Ma. Eugenia Quehé\n\t| Descripción: Existe la ficción legal de qué: 'EL DERECHO SE PRESUME CONOCIDO POR TODOS' ¿Qué tan verdadera es esta ficción? ¿Qué tanto sabemos de Derecho los ciudadanos? El taller apunta a democratizar el saber del Derecho a todos los ciudadanos. Destinado a alumnos y publico en general.\n\t| Duración: 3 meses\n\t| Día y horario: Viernes de 16.00 a 18.00"
            elif (str(taller) == "preventiva"):
                salida = salida + "\n\t| Tallerista: Abg. Ma. Eugenia Quehé\n\t| Descripción: Se abordarán situaciones jurídicas que resultan de conocimiento imprescindible para que comerciantes y emprendedores, para que sean capaces de decidir cómo actuar en pos de la mitigación de conflictos legales.\n\t| Duración: 2 meses\n\t| Día y horario: Viernes de 14.00 a 16.00"
            elif (str(taller) == "negocio"):
                salida = salida + "\n\t| Tallerista: Lic. Gabriela Rentería\n\t| Descripción: Comprender la importancia de la IDEA de negocio. Obtener conocimientos de formas legales de un negocio. Obtener herramientas para desarrollar un plan de negocios.\n\t| Duración: 3 meses\n\t| Día y horario: Jueves de 18.00 a 20.00"
            elif (str(taller) == "gestion"):
                salida = salida + "\n\t| Tallerista: Lic. Gabriela Rentería\n\t| Descripción: controlar y reportar los costos de alimentos y bebidas, comprender la importancia de la estandarización de recetas. Fijar precios de venta y, diseñar un menú acorde a los clientes a quienes deseen dirigirse contemplando su rentabilidad y popularidad.\n\t| Duración: 3 meses\n\t| Día y horario: Jueves de 14.00 a 16.00"
            elif (str(taller) == "cafe"):
                salida = salida + "\n\t| Tallerista: Lic. Gabriela Rentería\n\t| Descripción: Obtener conocimientos de cómo se produce y de servicios del café, té, chocolate y yerba mate\n\t| Duración: 2 meses\n\t| Día y horario: Miércoles de 13.00 a 15.00"
            elif (str(taller) == "vino"):
                salida = salida + "\n\t| Tallerista: Lic.Gabriela Rentería\n\t| Descripción: Obtener conocimientos de cómo se produce la transformación de la uva en vino. Nociones de coctelería. Reconocer los tipos de licores y aguardientes y también cómo organizar las tareas en un bar.\n\t| Duración: 2 meses\n\t| Día y horario: Miércoles de 17.30 a 19.30"
            elif (str(taller) == "italiano"):
                salida = salida + "\n\t| Tallerista: Eduardo Montalti\n\t| Descripción: Lectura y comprensión de la lengua a nivel básico. Expresiones de uso habitual y frases de base para necesidades concretas en lo cotidiano.\n\t| Duración: 3 meses\n\t| Día y horario: Viernes de 16.00 a 18.00"
            elif (str(taller) == "marketing"):
                salida = salida + "\n\t| Tallerista: Lic. Anahí Herrero\n\t| Descripción: Qué se comunica, de qué manera, cada cuánto, qué refleja en sus mensajes. Identificación de fortalezas y debilidades. Reconocimiento de oportunidades y desafíos de la presencia online.\n\t| Duración: 2 meses\n\t| Día y horario: Viernes de 17.30 a 19.00"
            else:
                salida = "Parece que el taller " + str(taller) + " no esta disponible en nuestra universidad."
                verif = 1
            dispatcher.utter_message(text=str(salida))
            if (verif == 0):
                return [SlotSet("taller_interes", taller)]
            else:
                return []
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
        else:
            return []

class ActionBeneficioBecas(Action):

    def name(self) -> Text:
        return "action_beneficio_becas"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        if (intent == "pedir_beneficios_becas"):
            beca = next(tracker.get_latest_entity_values("becas"), None)
            veirf = 0
            salida = "Los beneficios de todas nuestras becas siempre serán un monto fijo de dinero, el cual, junto con la duración del beneficio, variarán acorde al tipo de beca y a la condición del postulante, discriminando entre ingresantes y reinscriptos."
            if (str(beca) == "finalizacion"):
                salida = salida + "\n\t| Ingresantes: No acceden a esta beca.\n\t| Reinscriptos: $2935 (beneficio durante 10 meses)"
            elif (str(becas) == "ayuda"):
                salida = salida + "\n\t| Ingresantes: $810 (beneficio durante 9 meses)\n\t| Reinscriptos: $1515 (beneficio durante 10 meses)"
            elif (str(becas) == "transporte"):
                salida = salida + "\n\t| $810 de carga en saldo para tarjeta de transporte público (beneficio durante 10 meses)"
            else:
                salida = "Parece que esa beca no forma parte de nuestro programa. Te recuerdo que el Programa de Becas de la UNICEN se conforma por las siguientes becas:\n\t| Beca de finalización de carrera\n\t| Beca de ayuda económica\n\t| Beca de 3er beneficio"
                verif = 1
            dispatcher.utter_message(text=str(salida))
            if (verif == 0):
                return [SlotSet("beca_interes", taller)]
            else:
                return []
        else:
            return []

class ActionSetBecaAplica(Action):

    def name(self) -> Text:
        return "action_set_beca_aplica"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        if (intent == "entrevista_tipo_beca"):
            beca = next(tracker.get_latest_entity_values("becas"), None)
            return [SlotSet("beca_aplica", str(beca))]
        else:
            return []

class ActionSetIngReins(Action):

    def name(self) -> Text:
        return "action_set_ingresante/reinscripto"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        if (intent == "entrevista_soy_ingresante"):
            return [SlotSet("ingresante/reinscripto", "ingresante")]
        elif (intent == "entrevista_soy_reinscripto"):
            return [SlotSet("ingresante/reinscripto", "reinscripto")]
        else:
            return []

class ActionSetAnCurs(Action):

    def name(self) -> Text:
        return "action_set_años_cursados"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        if (intent == "entrevista_años_cursados"):
            anio = next(tracker.get_latest_entity_values("años cursando"), None)
            return [SlotSet("años_cursados", float(anio))]
        else:
            return []

class ActionSetMatCurs(Action):

    def name(self) -> Text:
        return "action_set_materias_cursadas"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        if (intent == "entrevista_materias_cursadas"):
            materias = next(tracker.get_latest_entity_values("materias cursadas"), None)
            return [SlotSet("materias_cursadas", float(materias))]
        else:
            return []

class ActionSetMatApr(Action):

    def name(self) -> Text:
        return "action_set_materias_aprobadas"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        if (intent == "entrevista_materias_aprobadas"):
            aprobadas = next(tracker.get_latest_entity_values("materias aprobadas"), None)
            if (str(aprobadas) == "todas"):
                return [SlotSet("materias_aprobadas", tracker.get_slot("materias_cursadas"))]
            else:
                return [SlotSet("materias_aprobadas", float(aprobadas))]
        else:
            return []

class ActionOpinarMaterias(Action):

    def name (self) -> Text:
        return "action_opinar_materias_aprobadas"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        if (intent == "entrevista_materias_aprobadas" and tracker.get_slot("materias_cursadas") >= 0):
            if (tracker.get_slot("materias_cursadas") == tracker.get_slot("materias_aprobadas")):
                coeficiente = 1
            else:
                coeficiente = tracker.get_slot("años cursando") / tracker.get_slot("materias_cursadas") - tracker.get_slot("materias_aprobadas")
            if (coeficiente < 0.25):
                salida = "Parece que la carrera te está resultando bastante difícil. No sé si sabías, pero se necesita cierta cantidad de materias aprobadas por año para acceder a nuestras becas"
                dispatcher.utter_message(text=str(salida))
            elif (coeficiente >= 0.25 and coeficiente < 0.5):
                salida = "Bueno, la verdad es que deberías elevar tu promedio de materias aprobadas por año, tus números son un poco bajos y eso es un limitante al momento de acceder a nuestras becas"
                dispatcher.utter_message(text=str(salida))
            elif (coeficiente >= 0.5 and coeficiente < 0.75):
                salida = "Estás bien, pero para tener más probabilidades de ser seleccionado para la beca tendrías que meterle un poco más de pilas"
                dispatcher.utter_message(text=str(salida))
            elif (coeficiente >= 0.75 and coeficiente < 1):
                salida = "Bien, tus materias aprobadas por año en relación a las cursadas están dentro de los márgenes de aceptación de nuestras becas"
                dispatcher.utter_message(text=str(salida))
            elif (coeficiente == 1):
                salida = "¡Excelente! Un desempeño tan alto abre más puertas y eleva tus chances de acceder a la beca que desees"
                dispatcher.utter_message(text=str(salida))
        return []

class ActionSetMood(Action):

    def name(self) -> Text:
        return "action_set_mood"

    mood = []

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        if (intent == "mood_great"):
            self.mood.append(1)
            return [SlotSet("mood", mood)]
        elif (intent == "mood_unhappy"):
            self.mood.append(0)
            return [SlotSet("mood", mood)]
        else:
            return []

def getMood(lista):
    cont = 0
    for indice in lista:
        cont += indice
    return (cont / len(lista))


class ActionOtraBeca(Action):

    def name (self) -> Text:
        return "action_entrevista_recibis_otra_beca"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        mood = getMood(tracker.get_slot("mood"))
        if (mood < 0.5):
            salida = "Bueno " + tracker.get_slot("nombre") + ", a pesar de tu desempeño, lograste aplicar para alguna otra beca?"
            dispatcher.utter_message(text=str(salida))
        elif (mood >= 0.5):
            salida = "Sos beneficiario de alguna otra beca?"
            dispatcher.utter_message(text=str(salida))
        return []

class ActionSetOtraBeca(Action):
    
    def name(self) -> Text:
        return "action_set_cobra_otra_beca"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        if (intent == "affirm"):
            return [SlotSet("otra_beca", True)]
        elif (intent == "deny"):
            return [SlotSet("otra_beca", False)]
        else:
            return []

class ActionOpinarOtraBeca(Action):

    def name(self) -> Text:
        return "action_opinar_cobra_otra_beca"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if (tracker.get_slot("otra_beca")):
            salida = "Ser beneficiario de otras becas no es una condición que impulse a los postulantes a estar más cerca de convertirse en beneficiarios de nuestro programa"
            disptacher.utter_message(text=str(salida))
        elif not (tracker.get_slot("otra_beca")):
            salida = "Eso te da un buen empujón, las becas de la universidad no son compatibles con otro tipo de ayudas"
            disptacher.utter_message(text=str(salida))
        return []

class ActionCantidadFamilia(Action):

    def name(self) -> Text:
        return "action_cantidad_grupo_familiar"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        mood = getMood(tracker.get_slot("mood"))
        if (mood < 0.5):
            salida = "Y contame " + tracker.get_slot("nombre") + ", cuantas personas viven con vos"
            dispatcher.utter_message(text=str(salida))
        elif (mood >= 0.5):
            salida = "Por cuantas personas esta conformado tu grupo familiar conviviente?"
            dispatcher.utter_message(text=str(salida))
        return []

class ActionSetCantidadFamilia(Action):

    def name(self) -> Text:
        return "action_set_cantidad_familia"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        if (intent == "entrevista_cantidad_familia"):
            cantidad = next(tracker.get_latest_entity_values("cantidad familia"), None)
            return [SlotSet("cantidad_familia", float(cantidad))]
        else:
            return []

class ActionSetCantidadTrabajan(Action):

    def name(self) -> Text:
        return "action_set_cantidad_trabajan"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        if (intent == "entrevista_cantidad_trabajan"):
            cantidad = next(tracker.get_latest_entity_values("familia trabajadora"), None)
            if (str(cantidad) == "ninguno"):
                return [SlotSet("familia_trabajadora", 0)]
            else:
                return [SlotSet("familia_trabajadora", float(cantidad))]
        else:
            return []

class ActionOpinarTrabajos(Action):

    def name(Self) -> Text:
        return "action_opinar_trabajo_familia"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        cantidad_miembros = tracker.get_slot("cantidad_familia")
        cantidad_trabajan = tracker.get_slot("familia_trabajadora")
        if (cantidad_miembros != None and cantidad_trabajan != None):
            coeficiente = cantidad_trabajan / cantidad_miembros
            if (coeficiente < 0.5):
                salida = "En familias donde menos de la mitad de sus miembros cuentan con un trabajo, la secretaría de bienestar suele darles una chance más de convertirse en beneficiarios de la beca"
                dispatcher.utter_message(text=str(salida))
            elif (coeficiente >= 0.5):
                salida = "Nuestas becas suelen estar dedicadas a familias cuya situación económica sea más delicada, considerando situaciones de desempleo y los salarios de sus integrantes"
                dispatcher.utter_message(text=str(salida))
        return []

class ActionIngresosFamiliares(Action):

    def name(self) -> Text:
        return "action_ingresos_familiares"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        coeficiente_trabajo = tracker.get_slot("familia_trabajadora") / tracker.get_slot("cantidad_familia")
        if (coeficiente_trabajo < 0.5):
            salida = "Y siendo que menos de la mitad de tus familiares cercanos tienen trabajo, de cuánto son los ingresos mensuales de tu familia?"
            dispatcher.utter_message(text=str(salida))
        elif (coeficiente_trabajo >= 0.5):
            salida = "Veo que más de la mitad de tu familia trabaja, de cuánto son los ingresos mensuales en tu casa?"
            dispatcher.utter_message(text=str(salida))
        return []

class ActionSetIngresos(Action):

    def name(self) -> Text:
        return "action_set_ingresos"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        if (intent == "entrevista_ingresos_familiares"):
            ingresos = next(tracker.get_latest_entity_values("ingreso familiar"), None)
            return [SlotSet("ingreso_familiar", float(ingresos))]
        else:
            return []

class ActionGastosFamiliares(Action):

    def name(self) -> Text:
        return "action_gastos_familiares"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ingresos = tracker.get_slot("ingreso_familiar")
        salida = "Y de esos $" + ingresos + ", cuantos están destinados todos los meses a los gastos fijos de la vivienda?"
        dispatcher.utter_message(text=str(salida))
        return []

class ActionSetGastos(Action):

    def name(self) -> Text:
        return "action_set_gastos"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        if (intent == "entrevista_gastos_familiares"):
            ingresos = next(tracker.get_latest_entity_values("gasto familiar"), None)
            return [SlotSet("gasto_familiar", float(ingresos))]
        else:
            return []

SALARIO_MINIMO = 31.104,00

class ActionOpinarEconomia(Action):

    def name(self) -> Text:
        return "action_opinar_economia_familia"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        diferencia = tracker.get_slot("ingreso_familiar") - tracker.get_slot("gasto_familiar")
        if (diferencia >= 1.5 * SALARIO_MINIMO):
            salida = "Parece que gozan de una alta cantidad de dinero al mes por fuera de sus gastos fijos. Como te comenté anteriormente, nuestas becas están destinadas a familias con una situación económica más delicada"
            dispatcher.utter_message(text=str(salida))
        if (diferencia < 1.5 * SALARIO_MINIMO):
            salida = "Deben llegar bastante ajustados a fin de mes. Espero que desde la universidad podamos brindarles una mano con esta beca"
            dispatcher.utter_message(text=str(salida))
        return []


class ActionSetDistanciaUni(Action):

    def name(self) -> Text:
        return "action_set_distancia_universidad"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        if (intent == "entrevista_distancia_universidad"):
            distancia = next(tracker.get_latest_entity_values("distancia universidad"), None)
            return [SlotSet("distancia_universidad", float(distancia))]
        else:
            return []

class ActionSetAuto(Action):

    def name(self) -> Text:
        return "action_set_tienen_auto"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        if (intent == "entrevista_cantidad_auto"):
            distancia = next(tracker.get_latest_entity_values("cantidad vehiculos"), None)
            return [SlotSet("cantidad_vehiculos", float(distancia))]
        elif (intent == "deny"):
            return [SlotSet("cantidad_vehiculos", 0)]
        else:
            return []

class ActionSetFamiliaresEnfermos(Action):

    def name(self) -> Text:
        return "action_set_familiares_enfermos"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        if (intent == "affirm"):
            return [SlotSet("familiares_enfermos", True)]
        elif (intent == "deny"):
            return [SlotSet("familiares_enfermos", False)]
        else:
            return []

class ActionFinalizarEntrevista(Action):

    def name(self) -> Text:
        return "action_finalizar_entrevista"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet("entrevista_terminada", True)]

class ActionResultadoBeca(Action):

    def name(self) -> Text:
        return "action_get_resultado_beca"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if (tracker.get_slot("entrevista_terminada") or tracker.get_slot("usuarios")[tracker.get_slot("nombre")]["entrevista_terminada"]):
            if (tracker.get_slot("beca_aplica") == "finalizacion"):
                #ser reinscripto
                condicion1 = (tracker.get_slot("ingresante/reinscripto") == "reinscripto") or (tracker.get_slot("usuarios")[tracker.get_slot("nombre")]["ingresante/reiscripto"] == "reinscripto")
                #haber cursado 3 o mas años
                condicion2 = (tracker.get_slot("años_cursados") >= 3) or (tracker.get_slot("usuarios")[tracker.get_slot("nombre")]["años_cursados"] >= 3)
                #haber aprobado mas del 65% de las materias cursadas
                condicion3 = (tracker.get_slot("materias_aprobadas") / tracker.get_slot("materias_cursadas") > 0.65) or (tracker.get_slot("usuarios")[tracker.get_slot("nombre")]["materias_aprobadas"] / tracker.get_slot("usuarios")[tracker.get_slot("nombre")]["materias_cursadas"] > 0.65)
                #no recibir otra beca
                condicion4 = (not tracker.get_slot("otra_beca")) or (not tracker.get_slot("usuarios")[tracker.get_slot("nombre")]["otra_beca"])
                if (condicion1 and condicion2 and condicion3 and condicion4):
                    disptacher.utter_message(text="¡Felicitaciones! ¡Tu solicitud de beca fue aprobada!")
                    return [SlotSet("beca_aprobada", "finalizacion")]
                else:
                    disptacher.utter_message(text="Lo lamento, pero tu aplicación a la beca no ha sido aceptada. Podrás volver a postularte en el próximo llamado")
                    return []
            elif (tracker.get_slot("beca_aplica") == "ayuda economica"):
                #que lo que sobre del sueldo menos gastos no supere a 1.5 * salario minimo
                condicion1 = (tracker.get_slot("ingreso_familiar") - tracker.get_slot("gasto_familiar") < 1,5 * SALARIO_MINIMO) or (tracker.get_slot("usuarios")[tracker.get_slot("nombre")]["ingreso_familiar"] - tracker.get_slot("usuarios")[tracker.get_slot("nombre")]["gasto_familiar"] < 1,5 * SALARIO_MINIMO)
                #que trabajen menos de 1/3 de los familiares
                condicion2 = (tracker.get_slot("familia_trabajadora") / tracker.get_slot("cantidad_familia") <= 1/3) or (tracker.get_slot("usuarios")[tracker.get_slot("nombre")]["familia_trabajadora"] / tracker.get_slot("usuarios")[tracker.get_slot("nombre")]["cantidad_familia"] <= 1/3)
                #tener familiar enfermo
                condicion3 = (tracker.get_slot("familiares_enfermos")) or (tracker.get_slot("usuarios")[tracker.get_slot("nombre")]["familiares_enfermos"])
                if (condicion1 and (condicion2 or condicion3)):
                    disptacher.utter_message(text="¡Felicitaciones! ¡Tu solicitud de beca fue aprobada!")
                    return [SlotSet("beca_aprobada", "ayuda economica")]
                else:
                    disptacher.utter_message(text="Lo lamento, pero tu aplicación a la beca no ha sido aceptada. Podrás volver a postularte en el próximo llamado")
                    return []
            elif (tracker.get_slot("beca_aplica") == "transporte publico"):
                #menos de un vehiculo cada 3 miembros de la familia
                condicion1 = (tracker.get_slot("cantidad_vehiculos") / tracker.get_slot("cantidad_familia") < 1/3) or (tracker.get_slot("usuarios")[tracker.get_slot("nombre")]["cantidad_vehiculos"] / tracker.get_slot("usuarios")[tracker.get_slot("nombre")]["cantidad_familia"] < 1/3)
                #vivir a mas de 1500 metros de la universidad
                condicion2 = (tracker.get_slot("distancia_universidad") > 1500) or (tracker.get_slot("usuarios")[tracker.get_slot("nombre")]["distancia_universidad"] > 1500)
                if (condicion1 and condicion2):
                    disptacher.utter_message(text="¡Felicitaciones! ¡Tu solicitud de beca fue aprobada!")
                    return [SlotSet("beca_aprobada", "transporte publico")]
                else:
                    disptacher.utter_message(text="Lo lamento, pero tu aplicación a la beca no ha sido aceptada. Podrás volver a postularte en el próximo llamado")
                    return []
        else:
            disptacher.utter_message(text="No existe registro en nuestra base de datos que indique que ya hayas sido entrevistado para aplicar a una beca.")