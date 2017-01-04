from chestday.speechlet_helper import build_response
from chestday.days import DAYS, AnyDay
import arrow

class Intent(object):

    def handle(self, request):
        raise NotImplementedError("You need to implement 'handle'!")


class ChestDayIntent(Intent):

    def handle(self, request):
        date = arrow.get(request['timestamp'])

        for day in DAYS:
            if day.is_today(date):
                return day.response()

        # This should be handled, but just in case...
        return AnyDay().response()


class IntentHandler(object):

    def handle(self, request):

        intent_name = request['intent']['name']

        for intent in Intent.__subclasses__():
            if intent.__name__ == intent_name:
                return intent().handle(request)

        return build_response("Do you even lift?")
