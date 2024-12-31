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

    return sendAWSQuery(current_occurences).json()["data"]["listOccurrenceCounters"]["items"]


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

    return sendAWSQuery(current_occurences_history).json()["data"]["listOccurrenceCounterHistories"]["items"]


def convertListToDict(lst):
    dict = {}

    for item in lst:
        dict[item[0]] = item[1]

    return dict


def edit_occurence_history(name, updated_count_history_list):
    # edit_occurence_history = f"""
    #     mutation updateOccurenceCounterHistory {{
    #         updateOccurenceCounterHistory(input: {{
    #             name: {name},
    #             count: {count}
    #         }}, condition: null) {{
    #             name
    #             count
    #         }}
    #     }}
    # """

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
    print("-------------------------")
    print("Updating Counter History")

    current_occurence_counters = getOccurenceCounters()
    print("current occurences: ", current_occurence_counters)
    
    occurence_counter_histories = getOccurenceCounterHistories()
    print("current occurences history: ", getOccurenceCounterHistories())

    print()

    for occurence_count in current_occurence_counters:
        print("occurence count: ", occurence_count)

        for occurence_count_history in occurence_counter_histories:

            if occurence_count_history["name"] == occurence_count["name"]:
                print("found occurence in history: ", occurence_count_history)

                occurence_name = occurence_count["name"]
                latest_count = occurence_count["count"]

                matching_occurence_count_history = occurence_count_history

                matching_occurence_count_history_count_list = matching_occurence_count_history["history"]

                matching_occurence_count_history_count_list.append(latest_count)

                print("updated history count list: ", matching_occurence_count_history_count_list)

                edit_occurence_history(occurence_name, matching_occurence_count_history_count_list)

                print("edited occurence history successfully: ", occurence_name, latest_count)

            else:
                print("not found occurence in history for occurence count: ", occurence_count)
