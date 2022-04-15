import paho.mqtt.client as mqtt

global MSG
# while True:
    #Connection success callback

def sub_string(text):
    text = text.replace('b','')
    text = text.replace("'",'')
    res = text.split(',')
    return res

def on_connect(client, userdata, flags, rc):
    print('Connected with result code '+str(rc))
    client.subscribe('machima/1/#')
    client.subscribe('machima/patient/set')

# Message receiving callback
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    print(sub_string(str(msg.payload)))
#     print(res[0])

#     MSG = str(msg.payload)

client = mqtt.Client("mqtt-test")

# Specify callback function
client.on_connect = on_connect
client.on_message = on_message

# Establish a connection
client.username_pw_set("machima", "123456")
client.connect('192.168.1.99', 1883, 60)
# Publish a message
client.publish('machima/1/',payload='FW,FW,FW,LW,LW,RW',qos=0)

#     print(MSG)

client.loop_forever()