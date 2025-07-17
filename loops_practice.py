import random
import time


class LoopPracticeClass:
    def __init__(self):
        self.numbers = list(range(1, 8))
        self.words = [f"str{i}" for i in range(10)]

    def print_nth_number(self, loop_number: int):
        """Печатает числа до 5, затем прерывается"""
        for n in self.numbers:
            if n == loop_number:
                break
            print(n)

    def print_all_words(self):
        for word in self.words:
            print(word)

    def imitate_robotics_load(self, delay: float = 0.2):
        for _ in range(10):
            load = random.randint(0, 100)
            if load > 85:
                print(f"Крылышки в опасности! Нагрузка - {load}")
            else:
                print(f"Крылышки в опасности! Нагрузка - {load}")
            time.sleep(delay)  # пауза для реализма


def main():
    homework = LoopPracticeClass()
    homework.print_all_words()
    homework.print_nth_number(10)
    homework.imitate_roctics_load()


if __name__ == "__main__":
    main()
