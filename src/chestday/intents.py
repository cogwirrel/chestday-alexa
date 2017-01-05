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

        timezone_difference = db.get_timezone_difference(session['user']['userId'])

        if timezone_difference is not None:
            date = date.to(timezone_difference)

            for day in DAYS:
                if day.is_today(date):
                    return day.response()

            # This should be handled, but just in case...
            return AnyDay().response()
        else:
            return build_response(
                "Let me ask you something first. What's the time?",
                reprompt_text="Tell me the time so I can be better at telling you when it's chest day.",
                should_end_session=False
            )


class WhatTimeIsItIntent(Intent):

    def handle(self, request, session):
        user_time = get_slots(request)['time']

        utc_time = arrow.get(request['timestamp'])
        utc_hour = utc_time.hour

        # Work out the timezone offset
        user_hour, user_minute = map(int, user_time.split(':'))

        # This works well enough, but may not work on the international date line, and will be wrong
        # It's impossible to distinguish between UTC+13 and UTC-11, so it won't work in New Zealand daylight savings time
        timezone_offsets = {((utc_hour + i) % 24): i for i in range(-12, 13)}

        timezone_offset = timezone_offsets[user_hour]

        # Store the offset for that user
        db.set_timezone_offset(session['user']['userId'], timezone_offset)

        return ChestDayIntent().handle(request, session)


class IntentHandler(object):

    def handle(self, request, session):

        intent_name = request['intent']['name']

        for intent in Intent.__subclasses__():
            if intent.__name__ == intent_name:
                return intent().handle(request, session)

        return build_response("Do you even lift?")
