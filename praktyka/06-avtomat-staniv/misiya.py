import time
from ev3dev2.motor import MoveTank, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, OUTPUT_E, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_5
from ev3dev2.sensor.lego import ColorSensor

# ── Порти робота Crane ──────────────────────────────────────────
tank = MoveTank(OUTPUT_A, OUTPUT_B)
arm1 = MediumMotor(OUTPUT_C)    # Перша ланка стріли (плече)
arm2 = MediumMotor(OUTPUT_D)    # Друга ланка стріли (передпліччя)
magnet = MediumMotor(OUTPUT_E)  # Магніт

# Датчики кольору: підлогові (Port 1, 2) та на руці (Port 5)
color_left = ColorSensor(INPUT_1)
color_right = ColorSensor(INPUT_2)
color_arm = ColorSensor(INPUT_5)

time.sleep(0.5)

stan = "pidgotovka_strily"
vkhid = time.time()


def perekhid(novyi):
    """Зміна стану та друк у консоль."""
    global stan, vkhid
    print(f"{stan} -> {novyi}")
    stan = novyi
    vkhid = time.time()


def is_target_object(rgb):
    """Визначення синього об'єкта (#7f86e6ff) датчиком на руці."""
    r, g, b = rgb[0], rgb[1], rgb[2]
    return b > 40 and b > r and b > g


def is_blue_delivery_zone(rgb):
    """Визначення синьою зони доставки (#3413d8ff) підлоговими датчиками."""
    r, g, b = rgb[0], rgb[1], rgb[2]
    return b > 150 and r < 80 and g < 80


while stan != "gotovo":
    rgb_arm = color_arm.raw
    rgb_left = color_left.raw
    rgb_right = color_right.raw

    # СТАН 1: Виставити рукав у позицію моніторингу (КУТИ: 25 та -25)
    if stan == "pidgotovka_strily":
        arm1.on_for_degrees(SpeedPercent(15), 25, block=False)
        arm2.on_for_degrees(SpeedPercent(15), -25, block=True)
        perekhid("ochikuvannya_obiekta")

    # СТАН 2: Очікування об'єкта
    elif stan == "ochikuvannya_obiekta":
        if is_target_object(rgb_arm):
            tank.off()
            perekhid("zakhvat_obiekta")

    # СТАН 3: Точне захоплення
    elif stan == "zakhvat_obiekta":
        # 1. Вмикаємо магніт заздалегідь
        magnet.on(SpeedPercent(100), brake=True)
        time.sleep(0.2)

        # 2. Плавно опускаємо плече (-20°)
        arm1.on_for_degrees(SpeedPercent(3), -20, block=True)
        time.sleep(0.5)

        # 3. Піднімаємо плече (+45°) з вантажем
        arm1.on_for_degrees(SpeedPercent(8), 45, block=True)
        magnet.on(SpeedPercent(100), brake=True)

        perekhid("transportuvannya")

    # СТАН 4: Транспортування та очікування заїзду в синю зону
    elif stan == "transportuvannya":
        # Якщо будь-який із підлогових датчиків зафіксував синю зону
        if is_blue_delivery_zone(rgb_left) or is_blue_delivery_zone(rgb_right):
            tank.off()  # Зупиняємо робота
            perekhid("rozvantazhennya")

    # СТАН 5: Розвантаження (пауза 2 секунди -> опускання -> вимкнення магніту)
    elif stan == "rozvantazhennya":
        print("Заїхали в синю зону. Чекаємо 2 секунди...")
        time.sleep(2.0)  # Пауза 2 секунди після заїзду

        # Опускаємо руку до підлоги (-20°)
        arm1.on_for_degrees(SpeedPercent(5), -20, block=True)

        # Відпускаємо вантаж
        magnet.off()
        time.sleep(0.5)

        # Піднімаємо порожню руку назад (+20°)
        arm1.on_for_degrees(SpeedPercent(10), 20, block=True)

        perekhid("gotovo")

    # Таймаут для безпеки
    if time.time() - vkhid > 90:
        print(f"Таймаут у стані '{stan}'")
        tank.off()
        magnet.off()
        break

tank.off()
print("УСПІХ: Об'єкт захоплено, доставлено в синю зону та розвантажено!")