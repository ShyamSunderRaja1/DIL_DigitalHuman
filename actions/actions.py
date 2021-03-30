# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
# https://rasa.com/docs/action-server/sdk-dispatcher

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted, EventType
import re
import requests
import json 

class ActionValidateNRICRegex(Action):
    '''Validate NIRC that was extracted from entity in the 'nric_regex' slot.
    Sets the 'nric_regex' slot to None if the NRIC value is invalid
    '''
    def name(self) -> Text:
         return "action_validate_NRIC_regex"
         
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 

        nric_regex_template = '^[SFTG]\d{7}[A-Z]$' 
        # except value from slot
        try: 
            nric = tracker.get_slot("nric_regex")

            # validate NRIC saved in slot to check if it fits the format of a valid NRIC value
            if (re.search(nric_regex_template,nric)): 
                dispatcher.utter_message(text="Okay, your NRIC is " + nric)
                return [SlotSet("nric_regex", nric)]
            else:
                dispatcher.utter_message(text="Your NRIC is invalid, please enter the correct NRIC")
                return [SlotSet("nric_regex", None)] # Sets the value of the slot 'nric_regex' to None
        except:
            dispatcher.utter_message(text="NRIC validation intent is triggered but action not carried out")

        return [SlotSet("nric_regex", None)]

class ActionValidateEmailRegex(Action):
    '''Validate email that was extracted from entity in the 'email' slot.
    '''
    def name(self) -> Text:
         return "action_validate_email_regex"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            email_regex_template = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            # except value from slot
            try:
                email_address = tracker.get_slot("email")

                # validate email saved in slot to check if it fits the format of a valid email address
                if (re.search(email_regex_template,email_address)):
                    dispatcher.utter_message(text="Email Address is Valid")
                else:
                    dispatcher.utter_message(text="Email Address is invalid")

            except:
                dispatcher.utter_message(text="Email validation intent triggered but action not carried out")

            return []

class ActionValidatePhoneNumberRegex(Action):
    '''Validate phone number that was extracted from entity in the 'telnum_regex' slot.
    '''
    def name(self) -> Text:
         return "action_validate_phonenumber_regex"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            number_regex_template = '^[+]65(6|8|9)\d{7}$'
            
            try:
            
                number = tracker.get_slot("telnum_regex")
                dispatcher.utter_message(text="The number is " + number)
            except:
                dispatcher.utter_message(text="did not capture slot data")


            try:
                # except value from slot
                number = tracker.get_slot("telnum_regex")

                if (re.search(number_regex_template,number)):
                    dispatcher.utter_message(text="Phone number is Valid")
                else:
                    dispatcher.utter_message(text="Phone number is invalid")

                # validate NRIC

            except:
                dispatcher.utter_message(text="Phone number intent triggered but action not carried out")

            return []


class ActionGenerateSummaryList(Action):
    '''Generate a summary list for the customer based on the slots filled from the conversation
    Only utters the slots which has been filled.
    Any slots which are not filled will not be uttered by the bot
    '''
    def name(self) -> Text:
        return "action_summary_list"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            try:
                slotState = tracker.current_state()["slots"] # get slot states
                
                dispatcher.utter_message(text="Here is a summary review of your conversation:")
                summarylist = [] # List to store filled slots
                for key,value in slotState.items():
                
                    # check if slot is filled 
                    if value:
                        string = key + ": " + value + "<br>"
                        summarylist.append(string)

                finalList = '\n'.join(summarylist) # Generate string with newline for each slot item in list for bot utterance
                dispatcher.utter_message(text = finalList)

            except:

                dispatcher.utter_message(text="summary list generation error")
            
            return []

class ActionSubmissionType(Action):
    ''' Bot utterances for submission instructions based on intent detected from latest message
        Currently supports 4 categories, [email, upload to bot, post mail, eclaim]
    '''
    def name(self) -> Text:
        return "action_submission_type"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        intent = tracker.get_intent_of_latest_message() # Get intent of latest message

         # EMAIL
        if (intent == "inform_submission_type_email"): 
            dispatcher.utter_message(template="utter_submission_type_email")
        # UPLOAD TO BOT
        elif (intent == "inform_submission_type_upload_to_bot"):
            dispatcher.utter_message(template="utter_submission_type_upload_to_bot")
        # POST MAIL
        elif (intent == "inform_submission_type_post_mail"):
            dispatcher.utter_message(template="utter_submission_type_post_mail")
        # ECLAIM FACILITY
        elif (intent == "inform_submission_type_eclaim_facility"):
            dispatcher.utter_message(template="utter_submission_type_eclaim_facility")
        
        else:
            dispatcher.utter_message(text="BOT DID NOT UNDERSTAND SUBMISSION TYPE")
        
        return []

class ActionHandoff(Action):
    '''Placeholder action for handoff functionality
        Based on the intent of the latest message, whether it is [Affirm/Deny]
        If intent is 'Affirm', utters message for handover of chat to live agent and provides the agent with a summary of the conversation
        If intent is 'Deny', restarts story from the top, asking the user to select a main topic
    '''
    def name(self) -> Text:
        return "action_handoff"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        intent = tracker.get_intent_of_latest_message() # Get intent of latest message

        # INTENT AFFIRM
        if (intent == "affirm"):
            dispatcher.utter_message(text="Your request to chat with our live agent has been processed.")
            dispatcher.utter_message(text="Transferring your chat to the live agent")

            # generate summary list
            try:
                slotState = tracker.current_state()["slots"] # get slot states
                
                dispatcher.utter_message(text="conversation handed off to chat agent with the following summary:")
                summarylist = [] # List to story filled slots
                for key,value in slotState.items():
                
                    # check if slot is filled 
                    if value:
                        string = key + ": " + value + "<br>"
                        summarylist.append(string)

                finalList = '\n'.join(summarylist) # Generate string with newline for each slot item in list for bot utterance
                dispatcher.utter_message(text = finalList)

            except:
                 dispatcher.utter_message(text="summary list generation error")
            
        # INTENT DENY
        elif (intent == "deny"):
            #dispatcher.utter_message(text="What else would you like to know?")
            dispatcher.utter_message(template= "utter_ask_main_topic")
            # generate buttons here
        
        return []  

class ActionResetStorySlots(Action):
    '''Reset slots when conversation restarts.
        Resets all slots affecting storyflow except personal details such as name, nric, email, telnum
    '''
    def name(self) -> Text:
        return "action_reset_story_slots"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # Reset slots which influence the story flow
        return [ 
            SlotSet("main_topic", None),
            SlotSet("claim_topic", None),
            SlotSet("claim_type", None),
            SlotSet("is_inpatient", None),
            SlotSet("is_panel_hospital", None),
            SlotSet("submission_type", None)
                ]

####################################################################################################
# TODOs
'''
class ActionAdmin_ShowConversations(Action):
    def name(self) -> Text:
        return "action_admin_show_conversations"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        last_msgs=tracker.get_intent_of_latest_message()

        cuisine = tracker.get_slot('cuisine')
        q = f"select * from restaurants where cuisine='{cuisine}' limit 1"
        
        db_results_json = {
            "results": [{
                "type": "section",
                "text": {
                    "text": "Make a bet on when the world will end:",
                    "type": "mrkdwn"
                },
                "accessory": {
                    "type": "datepicker",
                    "initial_date": "2019-05-21",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a date"
                    }
                }
            }]
        }

        
        dispatcher.utter_message(json_message=db_results_json)

        return []
'''

'''
def Call_NEAWeather_Forecast():    
    url='https://api.data.gov.sg/v1/environment/2-hour-weather-forecast'
    #url = f'http://{RASA_SERVER}:{RASA_API_PORT}/webhooks/rest/webhook'
    headers = {"Content-Type": "application/json"}
    resp = requests.post(url,verify=False,headers=headers)
    resp_data = {}
'''