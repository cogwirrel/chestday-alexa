from chestday.speechlet_helper import build_response
import random

class Day(object):
    def is_today(self, date):
        raise NotImplementedError()

    def day(self):
        raise NotImplementedError()

    def quips(self):
        raise NotImplementedError()

    def response(self):
        day_name = self.day()
        quip = random.choice(self.quips())
        return build_response("It's {day}, {quip}".format(day=day_name, quip=quip))


class ChristmasDay(Day):

    def is_today(self, date):
        return date.day == 25 and date.month == 12

    def day(self):
        return "Christmas Day"

    def quips(self):
        return [
            "Do you even gift?",
            "I hope you got a bench for Christmas this year.",
            "Christmas dinner hits all your macros."
        ]

class ArnoldsBirthday(Day):

    def is_today(self, date):
        return date.day == 30 and date.month == 6

    def day(self):
        return "Arnold's Birthday"

    def quips(self):
        return [
            "Happy Birthday Arnold!",
            "Train chest to wish Arnold many happy returns.",
            "Today is an honorary chest day.",
            "Arnold's training chest all day, so should you."
        ]

class ChestDay(Day):

    def is_today(self, date):
        return date.format('dddd') == 'Monday'

    def day(self):
        return "Chest Day"

    def quips(self):
        return [
            "Go train chest!",
            "What are you waiting for?!",
            "Hit the gym!",
            "Get on the bench now!",
            "Why aren't you on the bench?!",
            "You should be under a barbell right now.",
            "Time to pump iron!",
            "Smash it!",
            "Pump iron like Arnold!",
            "Why aren't you under a barbell?!",
            "Go hard or go home!",
            "Train like a beast!",
            "Why are you still looking at this?!",
            "Go own the bench!",
            "Cancel your date.",
            "Make Arnold proud!",
            "Get pumped with a peakin' track!",
            "Psych yourself up with the headphones below!",
            "Get amped with the headphones below!"
        ]

class AnyDay(Day):

    def is_today(self, date):
        return True

    def day(self):
        return "Not Chest Day"

    def quips(self):
        return [
            "Go train an inferior muscle group.",
            "Maybe train legs? ...Nah",
            "It's not worth going.",
            "Don't even bother.",
            "Just go home.",
            "Go back to bed.",
            "What's the point?",
            "Shouldn't have taken your preworkout.",
            "Guess it's biceps again.",
            "Hang up your tank."
        ]

# Priority ordered list of days
DAYS = [
    ChristmasDay(),
    ArnoldsBirthday(),
    ChestDay(),
    AnyDay(),
]
