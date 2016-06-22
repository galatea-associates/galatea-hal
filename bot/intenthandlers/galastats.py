import logging
from utils import get_highest_confidence_entity

logger = logging.getLogger(__name__)


def count_galateans(msg_writer, event, wit_entities):

    # We need to get this from our google apps integration instead of hardcoding
    office_counts = {
        'MA': 44,
        'LN': 9,
        'FL': 4,
    }

    # We need to find a geocoding service for this
    location_normalization = {
        "london" : "LN",
        "england": "LN",
        "britan": "LN",
        "great britan": "LN",
        "uk": "LN",
        "boston": "MA",
        "massachusetts": "MA",
        "mass": "MA",
        "tampa": "FL",
        "florida": "FL"
    }

    # Find the location with the highest confidence that met our default threshold
    loc_entity = get_highest_confidence_entity(wit_entities, 'location')
    if loc_entity is not None:
        loc = loc_entity['value'].lower()
    else:
        loc = 'all'

    # We need to normalize the location since wit doesn't do that for us
    # Need to use a geocode service for this instead of our hack
    normalized_loc = location_normalization.get(loc,"all")

    txt = ""
    if normalized_loc == "all":
        txt = "*Office* : *Count*\n"
        for o in office_counts:
            txt = txt + ">" + o + " : " + str(office_counts[o]) + "\n"
    else:
        txt = loc+" : "+str(office_counts[normalized_loc])

    msg_writer.send_message(event['channel'], txt)
