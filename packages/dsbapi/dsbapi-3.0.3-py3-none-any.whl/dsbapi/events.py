from dataclasses import dataclass
import datetime
import bs4
import requests
from typing import Optional, List
from mashumaro import DataClassJSONMixin


__all__ = ["Event", "parse_events"]


@dataclass
class Event(DataClassJSONMixin):
    """Ein Event repräsentiert einen Termin des CHGs.
    Falls das '''startdate''' '''None''' ist, so ist es ein eintägiges Event,
    falls das nicht der Fall ist geht der Termin von eingeschlossen startdate
    zu eingeschlossen enddate.
    """

    title: str
    startdate: Optional[datetime.date]
    enddate: datetime.date
    time: Optional[str]
    location: Optional[str]


def _parse_date(date: bs4.element.Tag) -> datetime.date:
    months = {
        "jan": 1,
        "feb": 2,
        "mrz": 3,
        "apr": 4,
        "mai": 5,
        "jun": 6,
        "jul": 7,
        "aug": 8,
        "sep": 9,
        "okt": 10,
        "nov": 11,
        "dez": 12,
    }
    day = date.find("div", {"class": "event-day"}).text
    year = date.find("div", {"class": "event-year"}).text
    monthstr = date.find("div", {"class": "event-month"}).text
    month = months[monthstr.lower()]

    return datetime.date(int(year), month, int(day))


def parse_events() -> List[Event]:
    """liest die Seite "Aktuelle Termine" des CHGs aus und verarbeitet
    diese in eine Liste aus '''Event'''s
    """
    response = requests.get("http://carl-humann.de/leben-am-chg/aktuelle-termine/")
    soup = bs4.BeautifulSoup(response.content, "html.parser")

    htmlevents = soup.find("ul", {"class": "event-list-view"}).findAll("li")

    events = []  # type: List[Event]
    for htmlevent in htmlevents:
        htmldate = htmlevent.find("div", {"class": "event-date"})

        startdate = None

        if htmldate is not None:
            if "multi-date" in htmldate.attrs["class"]:
                startdate = _parse_date(htmldate.find("div", {"class": "startdate"}))
                enddate = _parse_date(htmldate.find("div", {"class": "enddate"}))
            else:
                enddate = _parse_date(htmldate.find("div", {"class": "enddate"}))
        else:
            enddate = events[-1].enddate
            pass

        h3 = htmlevent.find("div", {"class": "event-title"}).find("h3")

        timespan = htmlevent.find("span", {"class": "event-time"})
        locationspan = htmlevent.find("span", {"class": "event-location"})
        timestr = timespan.text if timespan is not None else None
        location = locationspan.text if locationspan is not None else None
        events.append(Event(h3.text, startdate, enddate, timestr, location))

    return events
