from dotenv import dotenv_values
from ics import Calendar
from ics.alarm import EmailAlarm, DisplayAlarm
from datetime import timedelta

config = dotenv_values(".env")

data = {
    "plastic": {
        "identifier": "Gelber Sack / gelbe Tonne",
        "summary": "Plastic",
        "description": "Take it plastic bags",
        "alarm": timedelta(hours=-7)
    },
    "paper": {
        "identifier": "Papierbehaelter",
        "summary": "Paper",
        "description": "Empty your paper bin",
        "alarm": timedelta(hours=+17)
    }
}


def main():
    input_file = open(config.get("CALENDAR"), "r", newline="")
    calendar = Calendar(input_file.read())
    input_file.close()

    calendar.scale = "GREGORIAN"

    removable_events = []

    for event in calendar.events:
        hit = False

        for key, value in data.items():
            if event.name.strip() == value.get("identifier"):
                hit = True
                event.name = value.get("summary")
                event.description = value.get("description")
                event.location = ""
                event.alarms = [DisplayAlarm(trigger=value.get("alarm")), EmailAlarm(trigger=value.get("alarm"))]

        if not hit:
            removable_events.append(event)

    for removable_event in removable_events:
        calendar.events.remove(removable_event)

    print(calendar.serialize())

    output_file = open("garbage-collection-calendar.ics", "w+", newline="")
    print("\n\nwriting to file")
    output_file.write(calendar.serialize())
    output_file.close()


if __name__ == '__main__':
    main()
