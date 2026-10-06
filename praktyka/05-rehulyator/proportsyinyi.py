from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_4
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.virtual import GPSSensor
import time


tank = MoveTank(OUTPUT_A, OUTPUT_B)
color = ColorSensor(INPUT_1)
gps = GPSSensor(INPUT_4)

time.sleep(0.5)

# Поріг із роботи 4
PORIH = 50

# Базова швидкість
BAZA = 20

# Коефіцієнт коригування
Kp = 0.5


def obmezhyty(v):
    """Обмеження швидкості від -100 до 100."""
    return max(-100, min(100, v))


pochatok = time.time()

while time.time() - pochatok < 120 and gps.y < 85:

    v = color.reflected_light_intensity

    # Помилка відносно порогу
    e = PORIH - v

    # Пропорційна корекція
    korekciya = Kp * e

    # Корекція швидкості двох коліс
    lije = BAZA - korekciya
    desne = BAZA + korekciya

    tank.on(
        SpeedPercent(obmezhyty(lije)),
        SpeedPercent(obmezhyty(desne))
    )


tank.off()

print("Kp:", Kp)
print("час до кінця траси: %.1f с" % (time.time() - pochatok))
