Import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
    print("Topic:", msg.topic)
    print("Message:", msg.payload.decode())

client = mqtt.Client()

client.on_message = on_message

# connect to broker on same machine
client.connect("localhost",1883)
#if the mosquito is installed in the subscriper and if you install mosquito in the publisher you want to specf the address of the subscriber 

client.subscribe("v1/temperature")

print("Waiting for messages...")

client.loop_forever()