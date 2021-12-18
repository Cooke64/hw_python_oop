from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Info message"""

    def __init__(self, training_type: str,
                 duration_in_hour: float, distance: float,
                 speed: float, calories: float) -> None:
        self.training_type: str = training_type

        self.duration_in_hour: float = duration_in_hour

        self.distance: float = distance

        self.speed: float = speed

        self.calories: float = calories

    def get_message(self) -> str:
        """getting message about training season"""
        return (

            f'Тип тренировки: {self.training_type}; '

            f'Длительность: {self.duration_in_hour:.3f} ч.; '

            f'Дистанция: {self.distance:.3f} км; '

            f'Ср. скорость: {self.speed:.3f} км/ч; '

            f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Main class of training"""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self, action: int,
                 duration_in_hour: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration_in_hour
        self.weight = weight

        self.duration_in_hour = duration_in_hour

    def get_distance(self) -> float:
        """calculate distance"""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Getting avg speed"""

        return self.get_distance() / self.duration_in_hour

    def get_spent_calories(self) -> float:
        """Getting spent calories"""
        pass

    def show_training_info(self) -> InfoMessage:
        """Returning results about training season """

        show_me = InfoMessage(training_type=self.__class__.__name__,

                              duration_in_hour=self.duration_in_hour,

                              distance=self.get_distance(),

                              speed=self.get_mean_speed(),

                              calories=self.get_spent_calories())
        return show_me


class Running(Training):
    """Running CLASS"""

    CONST_RUN_1: int = 18

    CONST_RUN_2: int = 20

    min_in_hour: int = 60

    def get_spent_calories(self) -> float:
        """Getting spent calories"""

        lost_weight = (self.CONST_RUN_1 * self.get_mean_speed() -
                       self.CONST_RUN_2) * self.weight
        cal = (lost_weight / self.M_IN_KM *
               self.duration_in_hour * self.min_in_hour)

        return cal


class SportsWalking(Training):
    """Jogging."""

    CONST_WALK_1: float = 0.035

    CONST_WALK_2: float = 0.029

    min_in_hour: int = 60

    def __init__(self, action: int, duration_in_hour: float,

                 weight: float, height: float) -> None:
        super().__init__(action, duration_in_hour, weight)

        self.height = height

    def get_spent_calories(self) -> float:

        time_in_min = self.duration_in_hour * self.min_in_hour

        speed = self.get_mean_speed()

        calories_spent = (self.CONST_WALK_1 * self.weight

                          + (speed ** 2 // self.height) * self.CONST_WALK_2

                          * self.weight) * time_in_min

        return calories_spent


class Swimming(Training):
    """Swimming"""

    LEN_STEP: float = 1.38

    CONST_SWIM_1: float = 1.1

    CONST_SWIM_2: int = 2

    def __init__(self, action: int, duration_in_hour: float, weight: float,

                 length_pool: float, count_pool: float) -> None:
        super().__init__(action, duration_in_hour, weight)

        self.count_pool = count_pool

        self.length_pool = length_pool

    def get_mean_speed(self) -> float:
        time = self.duration_in_hour

        return (self.length_pool * self.count_pool) / self.M_IN_KM / time

    def get_spent_calories(self) -> float:

        total = (self.get_mean_speed() + self.CONST_SWIM_1)
        return total * self.CONST_SWIM_2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Read data from dict"""

    training_codes = {'SWM': Swimming,

                      'RUN': Running,

                      'WLK': SportsWalking

                      }
    try:
        train_name: Training = training_codes[workout_type](*data)
    except KeyError:
        print('Такой вид тренировки отсутствует, используйте только'
              'существующие виды тренировок')
    return train_name


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
