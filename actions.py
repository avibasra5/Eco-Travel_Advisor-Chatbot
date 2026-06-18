from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionRecommendTrip(Action):

    def name(self) -> Text:
        return "action_recommend_trip"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        user_messages = [
            event.get("text")
            for event in tracker.events
            if event.get("event") == "user" and event.get("text")
        ]

        destination = user_messages[-3] if len(user_messages) >= 3 else tracker.get_slot("destination")
        budget = user_messages[-2] if len(user_messages) >= 2 else tracker.get_slot("budget")
        travel_date = user_messages[-1] if len(user_messages) >= 1 else tracker.get_slot("travel_date")

        if not destination:
            destination = "your destination"

        if not budget:
            budget = "your budget"

        if not travel_date:
            travel_date = "your travel date"    

        message = (
            f"Eco Travel Plan for {destination}\n"
            f"Travel Date: {travel_date}\n\n"
            f"Budget: {budget}\n\n"
            f"Recommended Transport: Train (lowest carbon emissions)\n"
            f"Alternative Transport: Bus (budget-friendly)\n"
            f"Accommodation: Eco-certified hotel or hostel\n"
            f"Local Travel: Walking, cycling, or public transport\n\n"
            f"Sustainability Tips:\n"
            f"- Carry a reusable water bottle\n"
            f"- Avoid single-use plastics\n"
            f"- Support local businesses\n\n"
            f"This plan is designed to minimize carbon emissions while staying within your budget."
        )

        dispatcher.utter_message(text=message)

        return []