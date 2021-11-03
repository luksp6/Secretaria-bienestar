# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_documentos"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        documento = tracker.latest_message['entities'][0]['value']
        salida = "Para solicitar tu " + str(documento) + " debes: \n"
        if str(documento) == "certificado" :
            salida = salida + "1. Iniciar sesión con tu cuenta en el SIU Guarani"
        elif str(documento) == 'titulo' :
            salida = salida + "1. bla bla bla"
        dispatcher.utter_message(text=str(salida))

        return []
