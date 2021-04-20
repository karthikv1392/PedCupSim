#Subscriber

import time

node.subscribe("cupcarbon/sensor")

def callback(topic, message):
	node.mark(message)

while node.loop():
	time.sleep(1)