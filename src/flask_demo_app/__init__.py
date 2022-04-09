import random


CHARS = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


class Hungry:
    def __init__(self) -> None:
        self.blob = ''
    def eat(self, how_much: int=1000000):
        c = ''
        while len(c) < how_much:
            c = '{}{}'.format(
                c,
                random.choice(CHARS)*1000
            )
        self.blob = '{}{}'.format(
            self.blob,
            c
        )