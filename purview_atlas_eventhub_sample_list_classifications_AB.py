###
# Purview Eventhub Sample. This tool shows how to read Purview's EventHub and catch realtime Kafka notifications from the EventHub in Atlas Notifications (https://atlas.apache.org/2.0.0/Notifications.html) format.
# author: github <abandyop>
# contact : arindamba@microsoft.com
# date : December, 2021
# Azure Purview Product Group, Microsoft
###

from azure.eventhub.aio import EventHubConsumerClient
import asyncio
import json
import sys
import csv

# copy "connection_str" from your Purview Account's properties page "Atlas Kafka endpoint primary/secondary connection string"
connection_str = 'Endpoint=sb://atlas-71c10ec1-6fab-4950-87bc-3af8bbab115c.servicebus.windows.net/;SharedAccessKeyName=AlternateSharedAccessKey;SharedAccessKey=GY6gRdoNilLugi6XPFMzrFz3FXGGgiZ09oD6ijZD/HA='
consumer_group = '$Default'
eventhub_entities_name = 'atlas_entities'
eventhub_hook_name = 'atlas_hook'

csvfilename = 'C:/users/arind/Documents/out.txt.csv'
message_counter = 0
message_with_classifications_counter = 0


def processmessage(msgjsonraw):
    global message_counter
    global message_with_classifications_counter
    global csvfilename
    message_counter = message_counter + 1
    jsondata = json.loads(msgjsonraw)
    print(jsondata['message']['entity'])
    msgjson = json.dumps(jsondata, indent=4, sort_keys=True)
    print(msgjson)
    if 'message' in jsondata:
        if 'entity' in jsondata['message']:
            if 'classifications' in jsondata['message']['entity']:
                message_with_classifications_counter = message_with_classifications_counter + 1
                classificationscount = len(jsondata['message']['entity']['classifications'])
                classifications = jsondata['message']['entity']['classifications']
                guid = jsondata['message']['entity']['guid']
                print("Classifications Detected [%3d] :----> " %(classificationscount))
                print("Classifications :-----> ", (classifications))
                with open(csvfilename, 'a+') as csvfile:
                    fieldnames = ["GUID", "#ClassificationsCount","ClassificationsDetected", "JSON"]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writerow({"GUID":guid, "#ClassificationsCount":classificationscount, "ClassificationsDetected":classifications, "JSON":msgjson})
    print("-------------------------------------------------------------------------------------------------------------------")


async def on_event_entities(partition_context, event):
    print("Received the event: JSON: from the EventHub: ATLAS_ENTITIES / Partition ID: ",
          partition_context.partition_id)
    msgjsonraw = event.body_as_str(encoding='UTF-8')
    processmessage(msgjsonraw)
    await partition_context.update_checkpoint(event)


async def on_event_hook(partition_context, event):
    print("Received the event: JSON: from the EventHub: ATLAS_HOOK / Partition ID: ",
          partition_context.partition_id)
    msgjsonraw = event.body_as_str(encoding='UTF-8')
    processmessage(msgjsonraw)
    await partition_context.update_checkpoint(event)


async def receive():
    client_entities = EventHubConsumerClient.from_connection_string(
        connection_str, consumer_group, eventhub_name=eventhub_entities_name)
    async with client_entities:
        await client_entities.receive(
            on_event=on_event_entities,
            starting_position="-1",
        )
    client_hook = EventHubConsumerClient.from_connection_string(
        connection_str, consumer_group, eventhub_name=eventhub_hook_name)
    async with client_hook:
        await client_hook.receive(
            on_event=on_event_hook,
            starting_position="-1",
        )


if __name__ == '__main__':
    sys.stdout = open('C:/users/arind/Documents/out.txt', 'w')
    loop = asyncio.get_event_loop()
    with open(csvfilename, 'w') as csvfile:
        fieldnames = ["GUID", "#ClassificationsCount","ClassificationsDetected", "JSON"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    try:
        loop.run_until_complete(receive())
    except KeyboardInterrupt as e:
        loop.stop()
    finally:
        sys.stdout = open('C:/users/arind/Documents/out_summary.txt', 'w')
        print("Summary :-----> Total %20d Entity Messages. " %(message_counter))
        print(message_with_classifications_counter, " [ ", message_with_classifications_counter/message_counter*100, " % ] Entities With Classifications.")
        print(message_counter-message_with_classifications_counter, " [ ", (1-message_with_classifications_counter/message_counter)*100, " % ] Entities Without Classifications.")

# await client.get_partition_ids()))
