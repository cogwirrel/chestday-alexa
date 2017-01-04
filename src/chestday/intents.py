from chestday.speechlet_helper import build_response, get_slots
from chestday.days import DAYS, AnyDay
import chestday.db as db
import arrow

class Intent(object):

    def handle(self, request, session):
        raise NotImplementedError("You need to implement 'handle'!")


class ChestDayIntent(Intent):

    def handle(self, request, session):
        date = arrow.get(request['timestamp'])

        timezone_offset = db.get_timezone_offset(session['user']['userId'])

        if timezone_offset is not None:
            timezone_difference = '+' if timezone_offset >= 0 else '-'
            timezone_difference += '{:02d}:00'.format(abs(timezone_offset))
            date = date.to(timezone_difference)

        for day in DAYS:
            if day.is_today(date):
                return day.response()

        # This should be handled, but just in case...
        return AnyDay().response()


class WhatTimeIsItIntent(Intent):

    def handle(self, request, session):
        user_time = get_slots(request)['time']

        utc_time = arrow.get(request['timestamp'])
        utc_hour = utc_time.hour

        # Work out the timezone offset
        user_hour, user_minute = map(int, user_time.split(':'))

        timezone_offset = (user_hour - utc_hour) % 24

        # Store the offset for that user
        db.set_timezone_offset(session['user']['userId'], timezone_offset)

        return build_response("Thanks, now I'll be better at telling you when it's chest day")


class IntentHandler(object):

    def handle(self, request, session):

        intent_name = request['intent']['name']

        for intent in Intent.__subclasses__():
            if intent.__name__ == intent_name:
                return intent().handle(request, session)

        return build_response("Do you even lift?")
