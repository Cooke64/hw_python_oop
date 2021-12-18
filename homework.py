class InfoMessage:
    """Info message"""

    def __init__(self, training_type: str, duration: float, distance: float,
                 speed: float, calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Main class of training"""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.weight = weight
        self.action = action
        self.duration = duration

    def get_distance(self) -> float:
        """calculate distance"""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Getting avg speed"""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Getting spent calories"""
        pass

    def show_training_info(self) -> InfoMessage:
        """Returning results about training season """
        return InfoMessage(training_type=self.__class__.__name__,
                           duration=self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories())



class Running(Training):
    """Running CLASS"""
    training_code = 'RUN'

    def __init__(self, action: int, duration: float, weight: float):
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Getting spent calories"""
        # формула расчёта
        CONST_1: float = 18
        CONST_2: float = 20
        # постоянные величины из формулы
        lost_weight = (CONST_1 * self.get_mean_speed() - CONST_2) * self.weight
        cal = lost_weight / self.M_IN_KM * self.duration * 60
        return cal


class SportsWalking(Training):
    """Jogging."""
    training_code = 'WLK'

    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        # формула расчёта
        CONST_3: float = 0.035
        CONST_4: float = 0.029
        min_in_hour: int = 60
        time_in_min = self.duration * min_in_hour
        # постоянные величины из формулы
        speed = self.get_mean_speed()
        calories_spent = (CONST_3 * self.weight
                          + (speed**2 // self.height) * CONST_4
                          * self.weight) * time_in_min
        return calories_spent


class Swimming(Training):
    """Swimming"""
    LEN_STEP: float = 1.38
    training_code = 'SWM'

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.count_pool = count_pool
        self.length_pool = length_pool

    def get_mean_speed(self) -> float:
        time = self.duration

        return (self.length_pool * self.count_pool) / self.M_IN_KM / time

    def get_spent_calories(self) -> float:
        # формула расчета
        CONST_5: float = 1.1
        CONST_6: int = 2
        total = (self.get_mean_speed() + CONST_5) * CONST_6 * self.weight
        return total


def read_package(workout_type: str, data: list):
    """Read data from dict"""

    training_codes = {'SWM': Swimming,
                      'RUN': Running,
                      'WLK': SportsWalking
                      }
    return training_codes[workout_type](*data)


def main(training: Training) -> None:
    """The main resulting func"""
    info: InfoMessage = training.show_training_info()
    message_for_print = info.get_message()
    print(message_for_print)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
