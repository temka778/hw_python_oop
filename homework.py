from dataclasses import dataclass
from typing import Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        training_type: str = self.training_type
        duration = self.duration
        distance = self.distance
        speed = self.speed
        calories = self.calories
        return (f'Тип тренировки: {training_type}; '
                f'Длительность: {duration:.3f} ч.; '
                f'Дистанция: {distance:.3f} км; '
                f'Ср. скорость: {speed:.3f} км/ч; '
                f'Потрачено ккал: {calories:.3f}.')


class Training():
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Что-то совсем не то, что ожидалось...')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_RUN_1 = 18
    COEFF_CALORIE_RUN_2 = 20
    COEFF_TIME_MIN = 60

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (self.COEFF_CALORIE_RUN_1 * self.get_mean_speed()
                - self.COEFF_CALORIE_RUN_2) * self.weight\
            / self.M_IN_KM * self.duration * self.COEFF_TIME_MIN


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    LEN_STEP = 0.65
    COEFF_CALORIE_WLK_1 = 0.035
    COEFF_CALORIE_WLK_2 = 2
    COEFF_CALORIE_WLK_3 = 0.029
    COEFF_CALORIE_WLK_4 = 60

    def __init__(self, action: int, duration: float,
                 weight: float, height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (self.COEFF_CALORIE_WLK_1 * self.weight
                + (self.get_mean_speed() ** self.COEFF_CALORIE_WLK_2
                // self.height) * self.COEFF_CALORIE_WLK_3
            * self.weight) * self.duration * self.COEFF_CALORIE_WLK_4


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    COEFF_CALORIE_SWM_1 = 1.1
    COEFF_CALORIE_SWM_2 = 2

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: float):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return self.length_pool * self.count_pool \
            / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        return float(self.get_mean_speed() + self.COEFF_CALORIE_SWM_1)\
            * self.COEFF_CALORIE_SWM_2 * self.weight


def read_package(work_type: str, dt: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    reading_data: Dict[str, classmethod] = {'SWM': Swimming,
                                            'RUN': Running,
                                            'WLK': SportsWalking}
    return reading_data[work_type](*dt)


def main(trena: Training) -> None:
    """Главная функция.:rtype: object"""
    info = trena.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)