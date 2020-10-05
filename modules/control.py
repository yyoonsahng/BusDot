import RPi.GPIO as GPIO
import time
br = [17, 18, 27, 22, 23, 24]
'''
17 - left1
27 - left2
23 - left3
18 - right1
22 - right2
24 - right3
'''
br1 = [17, 18, 27, 22, 23, 24]
br2 = [18, 22, 23, 24]
br3 = [27, 22, 23, 24]
br4 = [27, 23, 24]
br5 = [18, 27, 23, 24]
br6 = [22, 23, 24]
br7 = [23, 24]
br8 = [18, 23, 24]
br9 = [17, 22, 23, 24]
br0 = [17, 23, 24]

numbers = [br1, br2, br3, br4, br5, br6, br7, br8, br9, br0]

def setup():
	GPIO.setmode(GPIO.BCM)
	for i in range(0,6):
		GPIO.setup(br[i], GPIO.OUT)

def control(num):
	for pin in numbers[num - 1]:
		GPIO.output(pin, GPIO.HIGH)
	time.sleep(2)
	# #clean
	for pin in numbers[num - 1]:
		GPIO.output(pin, GPIO.LOW)
	print("completed")


def destroy_gpio():
	GPIO.cleanup()
	
#if __name__ == '__main__':
#	setup()
#	control(1)
#	destroy_gpio()
