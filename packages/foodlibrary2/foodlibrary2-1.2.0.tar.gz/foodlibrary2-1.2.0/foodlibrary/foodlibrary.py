from enum import Enum
from typing import List


# FOOD LIBRARY 1.0.0
# Author: Aleksy Bernat

class DietType(Enum):
    """
    Diet type
    """
    CARNIVORE = 1
    VEGAN = 2
    VEGETARIAN = 3


class Food:
    """
    Food class represents a kind of food with name and information
    for which person it is. It has also the information about
    amount for one person.
    """
    name: str
    available_for: List
    amount_for_one_person: float

    def __init__(self, name, available_for, amount_for_one_person):
        """
        The constructor
        :param name: to set
        :param available_for: to set
        :param amount_for_one_person: to set
        """
        self.name = name
        self.available_for = available_for
        self.amount_for_one_person = amount_for_one_person

    def is_available_for(self, diet_type: DietType):
        """
        Decides if food is available for given diet type
        :param diet_type: to check
        :return: boolean
        """
        for a in self.available_for:
            if a == diet_type:
                return True
        return False


menu = [
    Food("meat", [DietType.CARNIVORE], 1),
    Food("lettuce", [DietType.CARNIVORE, DietType.VEGAN, DietType.VEGETARIAN], 8),
    Food("egg", [DietType.CARNIVORE, DietType.VEGETARIAN], 4)]


def prepare_menu(number_of_carnivores: int,
                 number_of_vegans: int,
                 number_of_vegetarians: int):
    """
    Prepares menu for given people
    :param number_of_carnivores: number of carnivores
    :param number_of_vegans: number of vegans
    :param number_of_vegetarians: number of vegetarians
    :return:
    """
    to_buy = ""
    for f in menu:
        amount = 0
        if f.is_available_for(DietType.CARNIVORE):
            amount += f.amount_for_one_person * number_of_carnivores
        if f.is_available_for(DietType.VEGAN):
            amount += f.amount_for_one_person * number_of_vegans
        if f.is_available_for(DietType.VEGETARIAN):
            amount += f.amount_for_one_person * number_of_vegetarians
        to_buy += f.name + " - " + str(amount) + "\n"
    return to_buy


def prepare_huge_menu(number_of_carnivores: int,
                 number_of_vegans: int,
                 number_of_vegetarians: int):
    """
    Prepares menu for given people
    :param number_of_carnivores: number of carnivores
    :param number_of_vegans: number of vegans
    :param number_of_vegetarians: number of vegetarians
    :return:
    """
    to_buy = ""
    for f in menu:
        amount = 0
        if f.is_available_for(DietType.CARNIVORE):
            amount += f.amount_for_one_person * number_of_carnivores * 2
        if f.is_available_for(DietType.VEGAN):
            amount += f.amount_for_one_person * number_of_vegans * 2
        if f.is_available_for(DietType.VEGETARIAN):
            amount += f.amount_for_one_person * number_of_vegetarians * 2
        to_buy += f.name + " - " + str(amount) + "\n"
    return to_buy


def prepare_very_huge_menu(number_of_carnivores: int,
                 number_of_vegans: int,
                 number_of_vegetarians: int):
    """
    Prepares menu for given people
    :param number_of_carnivores: number of carnivores
    :param number_of_vegans: number of vegans
    :param number_of_vegetarians: number of vegetarians
    :return:
    """
    to_buy = ""
    for f in menu:
        amount = 0
        if f.is_available_for(DietType.CARNIVORE):
            amount += f.amount_for_one_person * number_of_carnivores * 3
        if f.is_available_for(DietType.VEGAN):
            amount += f.amount_for_one_person * number_of_vegans * 3
        if f.is_available_for(DietType.VEGETARIAN):
            amount += f.amount_for_one_person * number_of_vegetarians * 3
        to_buy += f.name + " - " + str(amount) + "\n"
    return to_buy

def version():
    """
    Returns the library version
    :return:
    """
    return "1.2.0"
