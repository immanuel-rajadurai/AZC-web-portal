from .services_extras import *


def get_occurence_history(name):
    get_occurence_history = f"""
        query getOccurrenceCounterHistory {{
            getOccurrenceCounterHistory(name: "{ name }") {{
                history
            }}
        }}
    """

    return sendAWSQuery(get_occurence_history).json()["data"][
        "getOccurrenceCounterHistory"
    ]["history"]
