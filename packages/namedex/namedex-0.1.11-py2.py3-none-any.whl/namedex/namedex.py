#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
An implementation of the soundex algorithm as mentioned in
https://www.wikiwand.com/en/Soundex.

"""
# Soundex constants
LETTER_TO_DROP = ['a', 'e', 'i', 'o', 'u', 'y', 'h', 'w']
LETTER_REPLACE_1 = ['b', 'f', 'p', 'v']
LETTER_REPLACE_2 = ['c', 'g', 'j', 'k', 'q', 's', 'x', 'z']
LETTER_REPLACE_3 = ['d', 't']
LETTER_REPLACE_4 = ['l']
LETTER_REPLACE_5 = ['m', 'n']
LETTER_REPLACE_6 = ['r']


def command_line():
    """Run namedex in the commandline

    This function runs when the module is ran as a script.
    It only prints the results, it does not output to stout.

    """

    name = input("Enter name: ")
    print(create_soundex(name))

    return 0


def create_soundex(entered_name):
    """Creates the soundex for the given name and returns it.

    :param entered_name: The name to be converted into a soundex.
    :type entered_name: str
    :return: A soundex.
    :rtype: str

    """

    initial = []
    name = make_into_list(entered_name)
    # Append the first letter of the name to initial
    initial.append(name[0].upper())

    name = convert_to_number(name)
    name = remove_adjacent_letters(name)
    name = remove_first_number(name)
    name = remove_dropped_letters(name)
    name = strip_and_pad(name)
    name.insert(0, initial[0])

    name = ''.join(name)

    return name


def make_into_list(name):
    """Lower cases the name and converts it into a list.

    Takes the string passed in and lowercase it. Then it
    converts it to a list.

    :param name: A name as a string.
    :type name: str
    :return: The name all lower cased and made into a list.
    :rtype: list

    """

    name = name.lower()
    return list(name)


def convert_to_number(name):
    """Replaces letters to corresponding numbers to build the soundex.

    :param name: The letters of the name split into a list.
    :type name: list
    :return: The corresponding numbers for the consonants.
    :rtype: list

    """

    soundex = []
    for letter in name:
        if letter in LETTER_REPLACE_1:
            soundex.append('1')
        elif letter in LETTER_REPLACE_2:
            soundex.append('2')
        elif letter in LETTER_REPLACE_3:
            soundex.append('3')
        elif letter in LETTER_REPLACE_4:
            soundex.append('4')
        elif letter in LETTER_REPLACE_5:
            soundex.append('5')
        elif letter in LETTER_REPLACE_6:
            soundex.append('6')
        else:
            soundex.append(letter)

    return soundex


def remove_adjacent_letters(name):
    """Removes digits that repeats.

    Removes duplicate digits that are adjacent to each other with a few
    exceptions.

    Duplicate digit that are adjacent are removed. If duplicate digits are
    separated by a 'w' or 'h' then remove one of the digits. If duplicate
    digits are separated by a 'w' or 'h' then remove one of the digits. If
    duplicate digits are separated by a 'w' or 'h' then remove one of the
    digits. If duplicate digits are separated by a vowel then leave the
    duplicate numbers.

    >>> remove_adjacent_letters(['4', '2', '2'])
    ['4', '2']

    >>> remove_adjacent_letters(['4', '2', 'h', '2'])
    ['4', 'h', '2']

    >>> remove_adjacent_letters(['4', '2', 'a', '2'])
    ['4', '2', 'a', '2']


    :param name: A list of soudex numbers and vowels including 'w' and 'h'.
    :type name: list
    :return: Soundex numbers with duplicated numbers removed.
    :rtype: list

    """

    if name == []:
        return []
    last_letter = name[0]
    # Starts on index 1 because last_letter was initialized with index 0
    for index, element in enumerate(name[1:]):

        # If the letter being compared is the same as last_letter, remove it.
        if element == last_letter:
            name.pop(index)
            last_letter = element
        # If duplicated number is separated by 'w' or 'h' then pop the second.
        elif element in ('h', 'w'):
            if name[index] == name[index + 2]:
                name.pop(index)
                last_letter = element
        else:
            last_letter = element

    return name


def remove_first_number(name):
    """Removes the first digit from list

    The first digit has to be removed at this point
    as required by the soundex algorithm.

    :param name: The name list
    :type name: list
    :return: The name list  with the first digit removed.
    :rtype: list

    """

    name.pop(0)
    return name


def remove_dropped_letters(name):
    """Remove the vowels, 'y', 'h', and 'w' from name.

    Removes all vowels and the the letters 'y', 'h', and 'w' from
    _name_.

    :param name: The name to be processed.
    :type name: list
    :return: name without vowels, 'y', 'h', or 'w' letters.
    :rtype: list

    """

    for letter in name[:]:
        if letter in LETTER_TO_DROP:
            name.remove(letter)

    return name


def strip_and_pad(name):
    """Makes the list 3 digits long.

    If the _name_ list is passed in with more than three digits then
    only the first three digits are kept. If the _name_ list is shorter
    than three digits then the _name_ list is padded with '0' until it
    is three digits long.

    :param name: The name list
    :return: A list that is only 3 digits long.

    """
    if not name:
        return ['0', '0', '0']
    if len(name) > 3:
        name = name[:3]
    elif len(name) < 3:
        while len(name) < 3:
            name.append('0')

    return name


if __name__ == '__main__':
    command_line()
