import RPi.GPIO as GPIO
import time
br = [17, 18, 27, 22]
#GPIO - 5, 6, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27
#[17, 18, 27, 22, 23, 24], [13, 19, 16, 26, 20, 21]
#left
br1 = [17]
br2 = [17, 27]
br3 = [17, 18]
br4 = [17, 18, 22]
br5 = [17, 22]
br6 = [17, 18, 27]
br7 = [17, 18, 27, 22]
br8 = [17, 27, 22]
br9 = [18, 27]
br0 = [18, 27, 22]
numbers = [br1, br2, br3, br4, br5, br6, br7, br8, br9, br0]

def control(num):
	GPIO.setmode(GPIO.BCM)
	for i in range(0, 4):
		GPIO.setup(br[i], GPIO.OUT)

	for pin in numbers[num - 1]:
		GPIO.output(pin, GPIO.HIGH)
	time.sleep(3)
	#clean
	for pin in numbers[num - 1]:
		GPIO.output(pin, GPIO.LOW)
	print("completed")


def destroy_gpio():
	GPIO.cleanup()

if __name__ == '__main__':
	control(7)
	destroy_gpio()
