from dataclasses import dataclass, asdict
"""Импортировать из модуля декоратор и метод."""

@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self):
        return self.message.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: float = 1000
    LEN_STEP: float = 0.65
    MIN_IN_HOUR: float = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения,км/ч."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        if not float:
            raise NotImplementedError('Расчет калорий не выполнен')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self, action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Рассчитать расход калорий для бега."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * (self.duration * self.MIN_IN_HOUR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    WEIGHT_MULTIPLIER: float = 0.035
    WEIGHT_MULTIPLIER_2: float = 0.029
    KMH_TO_MSEC: float = 0.278
    SM_TO_M: float = 100

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Рассчитать расход калорий для ходьбы."""
        return (((self.WEIGHT_MULTIPLIER * self.weight
                + ((self.get_mean_speed() * self.KMH_TO_MSEC)**2
                 / (self.height / self.SM_TO_M))
                * self.WEIGHT_MULTIPLIER_2 * self.weight)
                * self.duration * self.MIN_IN_HOUR))


class Swimming(Training):
    """Тренировка: плавание."""

    SWIM_SPEED_COEFFICIENT: float = 1.1
    SWIM_WEIGHT_COEFFICIENT: float = 2
    LEN_STEP: float = 1.38

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Рассчитать среднюю скорость для плавания,км/ч"""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Рассчитать расход калорий для плавания."""
        return ((self.get_mean_speed() + self.SWIM_SPEED_COEFFICIENT)
                * self.SWIM_WEIGHT_COEFFICIENT * self.weight
                * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные, полученные от датчиков:
    код типа тренировки, список числовых значений."""
    dict_workout: type[dict_workout] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }
    if workout_type in dict_workout:
        return dict_workout[workout_type](*data)
    else:
        raise ValueError('Тип тренировки не определен.')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
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
