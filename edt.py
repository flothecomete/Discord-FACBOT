import json
import os
import icalendar as ics
import requests as rq
import datetime
import pytz
from PIL import Image, ImageDraw, ImageFont

class EDT():
    def __init__(self, composante, td, tp) -> None:
        self.composante = composante
        self.td = td
        self.tp = tp
        self.id_cal = self.get_id_cal()
        self.events = self.read_calendar()
        self.generate_schedule_image()

    def get_id_cal(self):
        composante = self.composante
        with open("json/ical.json") as ical_json:
            les_id_ical = json.load(ical_json)
        return les_id_ical[composante]

    def a_jour(self):
        composante = self.composante
        if not os.path.exists(f"calendar/{composante}_calendar.ics"):
            return False
        with open(f"calendar/{composante}_calendar.ics", 'rb') as icalfile:
            gcal = ics.Calendar.from_ical(icalfile.read())
            if gcal.walk()[1].get("LAST-MODIFIED").dt.strftime('%Y-%m-%d')!=datetime.datetime.now().strftime('%Y-%m-%d'):
                return False
        return True
    
    def get_calendar(self):
        url = "https://aderead2022.univ-orleans.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data="
        id_cal = self.id_cal
        composante = self.composante
        ical = rq.get(url+id_cal)
        with open(f"calendar/{composante}_calendar.ics", "w") as f:
            f.write(ical.text)

    def read_calendar(self):
        composante = self.composante
        grp = self.tp
        td = self.td
        tp = self.tp
        events = []
        if not self.a_jour():
            self.get_calendar()
        with open(f"calendar/{composante}_calendar.ics", 'rb') as icalfile:
            gcal = ics.Calendar.from_ical(icalfile.read())
            for component in gcal.walk():
                if component.name == "VEVENT":
                    if component.get('dtstart').dt.strftime('%Y-%m-%d')==datetime.datetime.now().strftime('%Y-%m-%d'):
                        tz = pytz.timezone('Europe/Paris')
                        dt_start = component.get('dtstart').dt.astimezone(tz).strftime('%H:%M')
                        dt_end = component.get('dtend').dt.astimezone(tz).strftime('%H:%M')
                        if self.is_line_relevant(component.get('description').split("\n")):
                            events.append({"summary": component.get('summary'), "start": dt_start, "end": dt_end, "location": component.get('location')})
                        

        return events


    def is_line_relevant(self, line):
        composante = self.composante
        td = self.td
        tp = self.tp

        def is_other_grp():
            for el in line:
                if "TD" in el or "TP" in el:
                    return True
            return False
        
        if composante not in line:
            return False

        if td in line or tp in line:
            return True
        
        if td not in line and is_other_grp():
            return False

        if tp not in line and is_other_grp():
            return False

        print(line, "autre")
        return True

    def time_difference(self, start_time, end_time):
        # Convertir les chaînes de temps en objets datetime
        start = datetime.datetime.strptime(start_time, '%H:%M')
        end = datetime.datetime.strptime(end_time, '%H:%M')
        
        # Calculer la différence en minutes
        delta = end - start
        return delta.total_seconds() / 60

    def time_to_position(self, time_str, image_height, start_time=8, end_time=19):
        time_obj = datetime.datetime.strptime(time_str, '%H:%M')
        total_minutes = (time_obj.hour - start_time) * 60 + time_obj.minute
        max_minutes = (end_time - start_time) * 60
        position = (total_minutes / max_minutes) * image_height
        return position + 30

    def generate_schedule_image(self):
        events = self.events
        composante = self.composante
        td = self.td
        tp = self.tp
        events.sort(key=lambda x: datetime.datetime.strptime(x['start'], '%H:%M'))

        # Dimensions de l'image
        width, height = 600, 800
        margin = 50

        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()

        # Centrage du texte pour le nom de la promo
        draw.text((width / 4, 10), f"{composante} - {td} - {tp}", fill='black', font=font)

        # Dessinez les heures à gauche
        start_time = 8
        end_time = 19
        for hour in range(start_time, end_time + 1):
            position = self.time_to_position(f"{hour}:00", height)
            draw.text((10, position), f"{hour}:00", fill='black', font=font)

        # Dessinez les événements
        for event in events:
            y_start = self.time_to_position(event['start'], height)
            y_end = self.time_to_position(event['end'], height)
            draw.rectangle([margin, y_start, width-margin/2, y_end], fill='green')
             # Placez le summary au centre du rectangle
            draw.text((margin + 10, y_end - 50), f"{event['summary']}", fill='white', font=font)
            draw.text((margin + 10, y_end - 35), f"{event['location']}", fill='white', font=font)
            # Placez les horaires en bas du rectangle
            draw.text((margin + 10, y_end - 20), f"{event['start']} - {event['end']}", fill='white', font=font)

        image.save("images/emploi_du_temps.png")

if __name__ == "__main__":
    e = EDT("L3 MIAGE", "Gr TD2", "Gr TP1")