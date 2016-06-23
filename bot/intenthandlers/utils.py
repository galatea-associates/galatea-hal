import logging

logger = logging.getLogger(__name__)


def get_highest_confidence_entity(entities_dict, entity_name, confidence_threshold=0.75):
    if entity_name not in entities_dict:
        return None

    entities_of_interest = entities_dict[entity_name]
    highest_confidence_entity = None
    for entity in entities_of_interest:
        if 'confidence' in entity and entity['confidence'] > confidence_threshold:
            if highest_confidence_entity is None :
                highest_confidence_entity = entity
            elif entity['confidence'] > highest_confidence_entity['confidence']:
                highest_confidence_entity = entity
            else:
                pass

    if highest_confidence_entity is None:
        logger.info("Couldn't find a {} that met our confidence floor {}.".format(entity_name, confidence_threshold))
    else:
        logger.info("Found most likely {} with confidence {}".format(entity_name,
                                                                     highest_confidence_entity['confidence']))

    return highest_confidence_entity

