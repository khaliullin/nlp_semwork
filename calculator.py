#! /usr/bin/env python
# -*- coding: utf-8 -*-


def count_incoming_word(words, dictonary):
    count = 0
    for word in words:
        if word in dictonary:
            count += 1
    return count


def calculate_percentage(required_words_count, words):
    if len(words) != 0.0:
        return required_words_count * 1.0 / len(words)
    return 0.0
