from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.sensor import INPUT_3
from ev3dev2.sensor.lego import GyroSensor
import time

from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.sensor import INPUT_3
from ev3dev2.sensor.lego import GyroSensor
import time

tank = MoveTank(OUTPUT_A, OUTPUT_B)   # A — ліве колесо, B — праве
gyro = GyroSensor(INPUT_3)            # ⚠️ у Gears порт обов'язковий
time.sleep(0.5)

print("гіроскоп:", gyro.angle)

# Крок 1
tank.on_for_seconds(SpeedPercent(20),SpeedPercent(-20),1.0)
time.sleep(0.5)
print("Кут повороту:", gyro.angle)

# Крок 2-3
# 10 поворотів за часом + похибка
"""
print()
print("Повороти на час:")

previous = gyro.angle

timed_angles = []

for i in range(1, 11):

    tank.on_for_seconds(
        SpeedPercent(20),
        SpeedPercent(-20),
        1.0
    )

    time.sleep(0.5)

    current = gyro.angle
    turn_angle = current - previous

    timed_angles.append(turn_angle)

    print(i, turn_angle)

    previous = current

timed_average = sum(timed_angles) / len(timed_angles)
timed_error = timed_average - 90
timed_spread = max(timed_angles) - min(timed_angles)

print()
print("Середнє:", timed_average)
print("Систематична похибка:", timed_error)
print("Розкид:", timed_spread)
"""

# Крок 4
# 10 поворотів по гіроскопу

"""
print()
print("Повороти по гіроскопу:")

gyro_angles = [90]

for i in range(1, 11):

    gyro.reset()

    tank.on(
        SpeedPercent(20),
        SpeedPercent(-20)
    )

    while gyro.angle < 90:
        pass

    tank.off()

    time.sleep(0.5)

    angle = gyro.angle
    gyro_angles.append(angle)

    print(i, angle)


# Statistics for gyro turns

gyro_average = sum(gyro_angles) / len(gyro_angles)
gyro_error = gyro_average - 90
gyro_spread = max(gyro_angles) - min(gyro_angles)

print()
print("Середнє:", gyro_average)
print("Систематична похибка:", gyro_error)
print("Розкид:", gyro_spread)
"""
