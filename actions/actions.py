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

class ActionIdentificarse(Action):

    def name(self) -> Text:
        return "action_identificarse"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #usuarios = open('usuarios.txt', 'a')

        intent = tracker.latest_message['intent'].get('name')
        if (str(intent) == "identificarse"):
            nombre = next(tracker.get_latest_entity_values("nombres"), None)
            salida = "¡Un gusto " + str(nombre) + "!"
            dispatcher.utter_message(text=str(salida))
            return [SlotSet("nombre", nombre)]
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
            if (str(carrera) == "Ingeniería Civil"):
                salida = salida + "http://www.quequen.unicen.edu.ar/?page_id=83"
            if (str(carrera) == "Ingeniería Electromecánica"):
                salida = salida + "http://www.quequen.unicen.edu.ar/?page_id=90"
            if (str(carrera) == "Ingeniería Industrial"):
                salida = salida + "http://www.quequen.unicen.edu.ar/?page_id=87"
            if (str(carrera) == "Ingeniería Química"):
                salida = salida + "http://www.quequen.unicen.edu.ar/?page_id=117"
            if (str(carrera) == "Ingeniería en Agrimensura"):
                salida = salida + "http://www.quequen.unicen.edu.ar/?page_id=3906"
            else:
                salida = "Parece que la carrera " + str(carrera) + " no existe en nuestra universidad. Te recuerdo las carreras con las que contamos:\n\t| Licenciatura en Logística Integral\n\t| Ingeniería Civil\n\t| Ingeniería Electromecánica\n\t| Ingeniería Industrial\n\t| Ingeniería Química\n\t| Ingeniería en Agrimensura"
            dispatcher.utter_message(text=str(salida))
            return [SlotSet("carrera_interes", carrera)]
        else:
            return []