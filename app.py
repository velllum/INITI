import time
import random
import threading


# Алгоритм позволяет эмулировать работу светофоров и движение транспорта на перекрестке.
# Подобная имитация может быть полезна для тестирования различных сценариев управления трафиком,
# а также для обучения и понимания принципов работы систем управления перекрестками.
# В дальнейшем алгоритм можно усовершенствовать, добавив более сложную логику переключения светофоров и учета данных
# о трафике для оптимального управления потоками на перекрестке.
#
# Инициализация:
# Создаются объекты TrafficLight для автомобильных светофоров и PedestrianLight для пешеходных светофоров.
# Создается объект TrafficController, который управляет всеми светофорами на перекрестке.
#
# Цикл Контроллера:
# В цикле контроллера переключаются состояния светофоров по заданному расписанию:
# сначала активируется горизонтальное движение машин, затем вертикальное.
# После этого устанавливается короткий период времени с желтым светом для предупреждения.
#
# Потоки Машин и Пешеходов:
# Два отдельных потока car_flow и pedestrian_flow имитируют движение машин и пешеходов соответственно.
# Они периодически проверяют текущее состояние светофоров и осуществляют движение, учитывая зеленый свет и безопасность.
#
# Запуск Потоков:
# После создания светофоров и контроллера, они запускаются в отдельных потоках для параллельной работы.


class TrafficLight:
    """- светофор """

    def __init__(self, name):
        self.name = name
        self.state = 'Красный'  # красный по умолчанию

    def change_state(self, new_state):
        self.state = new_state
        print(f"{self.name} светофор изменился на {self.state}")
        print("=======================================================")


class PedestrianLight:
    """- пешеходный светофор """

    def __init__(self, name):
        self.name = name
        self.state = 'Красный'

    def change_state(self, new_state):
        self.state = new_state
        print(f"{self.name} пешеходный свет изменился на {self.state}")
        print("=======================================================")


class TrafficController:
    """- контроллер движения """

    def __init__(self, lights, ped_lights):
        self.lights = lights
        self.ped_lights = ped_lights

    def run(self):
        while True:
            # Горизонтальное движение
            self.lights['Вверх'].change_state('Зеленый')
            self.lights['Низ'].change_state('Зеленый')
            self.lights['Лева'].change_state('Красный')
            self.lights['Право'].change_state('Красный')

            self.ped_lights['Вверх'].change_state('Красный')
            self.ped_lights['Низ'].change_state('Красный')
            time.sleep(10)

            # Желтый свет
            self.lights['Вверх'].change_state('Жёлтый')
            self.lights['Низ'].change_state('Жёлтый')
            time.sleep(2)

            # Вертикальное движение
            self.lights['Вверх'].change_state('Красный')
            self.lights['Низ'].change_state('Красный')
            self.lights['Лева'].change_state('Зеленый')
            self.lights['Право'].change_state('Зеленый')

            self.ped_lights['Лева'].change_state('Зеленый')
            self.ped_lights['Право'].change_state('Зеленый')
            time.sleep(10)

            # Желтый свет
            self.lights['Лева'].change_state('Жёлтый')
            self.lights['Право'].change_state('Жёлтый')
            time.sleep(2)


def car_flow(lights):
    """- движение машин по дорогам """
    while True:
        if lights['Вверх'].state == 'Зеленый' or lights['Низ'].state == 'Зеленый':
            print("Автомобили движущиеся по дороге верх-низ")
        elif lights['Лева'].state == 'Зеленый' or lights['Право'].state == 'Зеленый':
            print("Автомобили движутся по дороге лева-право")
        time.sleep(random.randint(1, 5))


def pedestrian_flow(ped_lights):
    """- движение пешеходов """
    while True:
        if ped_lights['Вверх'].state == 'Зеленый' or ped_lights['Низ'].state == 'Зеленый':
            print("Пешеходы переходят по пешеходному переход верх-низ")
        elif ped_lights['Лева'].state == 'Зеленый' or ped_lights['Право'].state == 'Зеленый':
            print("Пешеходы переходят по пешеходному переходу лева-право")
        time.sleep(random.randint(1, 5))


def main():
    # Создаются объекты автомобильных и пешеходных светофоров и собираются в словари
    lights = {
        'Вверх': TrafficLight('Вверх'),
        'Низ': TrafficLight('Низ'),
        'Лева': TrafficLight('Лево'),
        'Право': TrafficLight('Право')
    }

    ped_lights = {
        'Вверх': PedestrianLight('Вверх'),
        'Низ': PedestrianLight('Низ'),
        'Лева': PedestrianLight('Лево'),
        'Право': PedestrianLight('Право')
    }

    # Создаем контроллер и запускаем
    controller = TrafficController(lights, ped_lights)
    threading.Thread(target=controller.run).start()

    # Запускаем потоки машин и пешеходов
    threading.Thread(target=car_flow, args=(lights,)).start()
    threading.Thread(target=pedestrian_flow, args=(ped_lights,)).start()


if __name__ == "__main__":
    main()


