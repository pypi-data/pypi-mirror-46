#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `namedex` package."""

import pytest

from namedex import namedex

def test_make_into_list_makeList():

    result = namedex.make_into_list('Robert')
    assert type(result) is list


def test_make_into_list_Lowercase():

    result = namedex.make_into_list('James')

    assert result == ['j', 'a', 'm', 'e', 's']


@pytest.mark.parametrize('list, expected', [(['j', 'a', 'm', 'e', 's'], ['j', 'm', 's']),
                                            (['j', 'o', 'l', 'e', 'e'], ['j', 'l']),
                                            (['d', 'a', 'n'], ['d', 'n']),
                                            (['w', 'a', 't', 's', 'o', 'n'], ['t', 's', 'n'])
                                            ])
def test_remove_dropped_letters(list, expected):

    result = namedex.remove_dropped_letters(list)
    assert result == expected


@pytest.mark.parametrize('name, expected', [(['j', 'm', 's'], ['2', '5', '2']),
                                            (['o', 'e'], ['o', 'e']),
                                            (['g', 'h', 'j'], ['2', 'h', '2']),
                                            ])
def test_convert_to_number(name, expected):

    result = namedex.convert_to_number(name)
    assert result == expected


@pytest.mark.parametrize('list, expected', [(['1', '2', '3', '4'], ['1', '2', '3', '4']),
                                            (['1', '2', '2', '4'], ['1', '2', '4']),
                                            (['6', '7', '6', '7', '7', '8'], ['6', '7', '6', '7', '8']),
                                            (['3', '3'], ['3']),
                                            (['2'], ['2']),
                                            ([], []),
                                            (['1', 'h', '1'], ['h', '1']),
                                            (['2', 'w', '2'], ['w', '2']),
                                            (['1', 'a', '1'], ['1', 'a', '1']),
                                            (['3', 'e', '3'], ['3', 'e', '3']),
                                            (['3', 'i', '3'], ['3', 'i', '3']),
                                            (['3', 'o', '3'], ['3', 'o', '3']),
                                            (['3', 'u', '3'], ['3', 'u', '3']),
                                            (['3', 'y', '3'], ['3', 'y', '3'])
                                            ])
def test_remove_adjacent_letters(list, expected):

    result = namedex.remove_adjacent_letters(list)
    assert result == expected


@pytest.mark.parametrize('list, expected', [(['9', '6', '3', '4', '3', '4', '2', '1'], ['9', '6', '3']),
                                            (['1', '2', '3', '4', '5'], ['1', '2', '3']),
                                            (['1', '2', '3'], ['1', '2', '3']),
                                            (['2', '3'], ['2', '3', '0']),
                                            (['7'], ['7', '0', '0']),
                                            ([], ['0', '0', '0'])
                                            ])
def test_strip_pad(list, expected):

    result = namedex.strip_and_pad(list)
    assert result == expected


@pytest.mark.parametrize('name, sdex', [('Washington', 'W252'),
                                        ('Wu', 'W000'),
                                        ('Joel', 'J400'),
                                        ('DeSmet', 'D253'),
                                        ('Gutierrez', 'G362'),
                                        ('Pfister', 'P236'),
                                        ('Jackson', 'J250'),
                                        ('Tymczak', 'T522'),
                                        ('Ashcraft', 'A261'),
                                        ('joe', 'J000'),
                                        ('Rupert', 'R163'),
                                        ('Robert', 'R163'),
                                        ('Rubin', 'R150'),
                                        ('Pvenster', 'P523'),
                                        ('Kqwen', 'K500'),
                                        ('Pf', 'P000'),
                                        ('Pfc', 'P200')
                                        ])
def test_create_namedex(name, sdex):

    result = namedex.create_soundex(name)
    assert result == sdex
