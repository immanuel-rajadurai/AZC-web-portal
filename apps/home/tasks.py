from celery import shared_task
from apps.home.services.services_extras import sendAWSQuery


def getOccurenceCounters():
    current_occurences = """
        query listOccurrenceCounter {
            listOccurrenceCounter {
                items {
                    name
                    count
                }
            }
        }
    """

    return sendAWSQuery(current_occurences).json()["data"]["listOccurrenceCounter"]["items"]


def getOccurenceCounterHistories():
    current_occurences_history = """
        query listOccurrenceCounterHistory {
            listOccurrenceCounterHistory {
                items {
                    name
                    history
                }
            }
        }
    """

    return sendAWSQuery(current_occurences_history).json()["data"]["listOccurrenceCounterHistory"]["items"]


def convertListToDict(lst):
    dict = {}

    for item in lst:
        dict[item[0]] = item[1]

    return dict


def edit_occurence_history(name, count):
    edit_occurence_history = f"""
        mutation updateOccurenceCounterHistory {{
            updateOccurenceCounterHistory(input: {{
                name: {name},
                count: {count}
            }}, condition: null) {{
                name
                count
            }}
        }}
    """

    sendAWSQuery(edit_occurence_history)


@shared_task(bind=True)
def updateCounterHistory():
    current_occurences = getOccurenceCounters()
    current_occurences_history = convertListToDict(getOccurenceCounterHistories())

    for occurence in current_occurences:
        tmp = current_occurences_history[occurence[0]] + [occurence[1]]
        edit_occurence_history(occurence[0], tmp)
