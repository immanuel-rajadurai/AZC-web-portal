from celery import shared_task
from apps.home.services.services_extras import sendAWSQuery


def getOccurenceCounters():
    current_occurences = """
        query listOccurrenceCounter {
            listOccurrenceCounters {
                items {
                name
                count
                }
            }
        }
    """

    return sendAWSQuery(current_occurences).json()["data"]["listOccurrenceCounters"][
        "items"
    ]


def getOccurenceCounterHistories():
    current_occurences_history = """
        query listOccurrenceCounterHistory {
            listOccurrenceCounterHistories {
                items {
                    name
                    history
                }
            }
        }
    """

    return sendAWSQuery(current_occurences_history).json()["data"][
        "listOccurrenceCounterHistories"
    ]["items"]


def edit_occurence_history(name, updated_count_history_list):
    edit_occurence_history = f"""
        mutation UpdateOccurrenceCounterHistory {{
            updateOccurrenceCounterHistory(input: {{name: "{name}", history: {updated_count_history_list}}}) {{
                name
                history
            }}
        }}
    """

    sendAWSQuery(edit_occurence_history)


@shared_task
def updateCounterHistory():
    current_occurence_counters = getOccurenceCounters()
    occurence_counter_histories = getOccurenceCounterHistories()

    for occurence_count in current_occurence_counters:
        for occurence_count_history in occurence_counter_histories:
            if occurence_count_history["name"] == occurence_count["name"]:
                occurence_name = occurence_count["name"]
                latest_count = occurence_count["count"]
                matching_occurence_count_history = occurence_count_history

                matching_occurence_count_history_count_list = (
                    matching_occurence_count_history["history"]
                )
                matching_occurence_count_history_count_list.append(latest_count)
                
                edit_occurence_history(
                    occurence_name, matching_occurence_count_history_count_list
                )
