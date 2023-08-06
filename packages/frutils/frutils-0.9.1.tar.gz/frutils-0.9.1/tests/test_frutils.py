#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `frutils` package."""

import pytest

from jinja2.environment import Environment

from frutils.frutils import *  # noqa: F403


@pytest.mark.parametrize(
    "input_obj, expected",
    [
        (["a", "b", "c"], True),
        (("a", "b", "c"), True),
        (["a", 1, "c"], False),
        (("a", 1, "c"), False),
        ((u"a", "b", "c"), True),
    ],
)
def test_list_of_strings(input_obj, expected):
    assert is_list_of_strings(input_obj) == expected


TEST_DICTS = [
    ({}, {}, {}),
    ({"a": 1}, {"a": 1}, {"a": 1}),
    ({"a": 1}, {"b": 1}, {"a": 1, "b": 1}),
    ({"a": 1}, {"a": 2}, {"a": 2}),
    ({"a": 1, "aa": 11}, {"b": 2, "bb": 22}, {"a": 1, "aa": 11, "b": 2, "bb": 22}),
    ({"a": 1, "aa": 11}, {"b": 2, "aa": 22}, {"a": 1, "b": 2, "aa": 22}),
]


@pytest.mark.parametrize("dict1, dict2, expected", TEST_DICTS)
def test_dict_merge_copy_result(dict1, dict2, expected):
    dict1_orig = copy.deepcopy(dict1)
    dict2_orig = copy.deepcopy(dict2)
    merged = dict_merge(dict1, dict2, True)
    assert merged == expected
    assert dict1 == dict1_orig
    assert dict2 == dict2_orig


@pytest.mark.parametrize("dict1, dict2, expected", TEST_DICTS)
def test_dict_merge_dont_copy_result(dict1, dict2, expected):
    # dict1_orig = copy.deepcopy(dict1)
    dict2_orig = copy.deepcopy(dict2)
    merged = dict_merge(dict1, dict2, False)
    assert merged == expected
    assert dict1 == expected
    assert dict2 == dict2_orig


TEST_DICT_LISTS = [
    ([{}, {}, {}], {}, {}),
    ([{"a": 1}, {"b": 2}, {"c": 3}], {}, {"a": 1, "b": 2, "c": 3}),
    ([{"a": 1}, {"a": 2}, {"b": 3}], {}, {"a": 2, "b": 3}),
    ([{"a": {"b": {"c": 1}}}, {"a": {"c": 2}}], {}, {"a": {"b": {"c": 1}, "c": 2}}),
    ([{"a": {"b": {"c": 1}}}, {"a": {"b": {"c": 2}}}], {}, {"a": {"b": {"c": 2}}}),
]


@pytest.mark.parametrize("dict_list, starting_dict, expected", TEST_DICT_LISTS)
def test_merge_list_of_dicts(dict_list, starting_dict, expected):
    result = merge_list_of_dicts(dict_list, starting_dict)

    assert result == expected


KEY_PATH_DICTS = [
    ({"a": 1, "b": 2, "c": 3}, "b", ".", "XXX", 2),
    ({"a": {"b": {"c": 2}}}, "a-b-c", "-", "XXX", 2),
    ({"a": {"b": {"c": 2}}}, "a-b-d", "-", "XXX", "XXX"),
]


@pytest.mark.parametrize(
    "source_dict, key_path, split_token, default_value, expected", KEY_PATH_DICTS
)
def test_get_key_path_value(
    source_dict, key_path, split_token, default_value, expected
):
    result = get_key_path_value(source_dict, key_path, split_token, default_value)

    assert result == expected


KEY_PATH_ADD_DICTS = [
    ({"a": 1, "b": 2, "c": 3}, "b", "x", ".", False, {"a": 1, "b": "x", "c": 3}),
    (
        {"a": {"b": 2, "c": {"d": 3}}},
        "axcxd",
        "xx",
        "x",
        False,
        {"a": {"b": 2, "c": {"d": "xx"}}},
    ),
    (
        {"a": {"b": 2, "c": {"d": 3}}},
        "a.c.e",
        "xx",
        ".",
        False,
        {"a": {"b": 2, "c": {"d": 3, "e": "xx"}}},
    ),
]


@pytest.mark.parametrize(
    "target_dict, key_path, value, split_token, ordered, expected", KEY_PATH_ADD_DICTS
)
def test_add_key_to_dict(target_dict, key_path, value, split_token, ordered, expected):
    add_key_to_dict(target_dict, key_path, value, split_token, ordered)

    assert target_dict == expected


KEY_PATH_APPEND_DICTS = [
    ({"a": 1, "b": 2, "c": [3]}, "c", "x", ".", {"a": 1, "b": 2, "c": [3, "x"]}),
    (
        {"a": {"b": 2, "c": {"d": [3]}}},
        "axcxd",
        "xx",
        "x",
        {"a": {"b": 2, "c": {"d": [3, "xx"]}}},
    ),
]


@pytest.mark.parametrize(
    "target_dict, key_path, value, split_token, expected", KEY_PATH_APPEND_DICTS
)
def test_append_key_to_dict(target_dict, key_path, value, split_token, expected):
    append_key_to_dict(target_dict, key_path, value, split_token)

    assert target_dict == expected


FLATTEN_LISTS_LISTS = [
    (["a", "b", "c"], ["a", "b", "c"]),
    (["a", ["b", "c"]], ["a", "b", "c"]),
    (["a", ["b", ["c"]]], ["a", "b", ["c"]]),
]


@pytest.mark.parametrize("lists, expected", FLATTEN_LISTS_LISTS)
def test_flatten_lists(lists, expected):
    result = flatten_lists(lists)
    assert result == expected


TEMPLATED_STRINGS = [("abcde", False), ("{{abc", True), ("{%", True)]


@pytest.mark.parametrize("string, expected", TEMPLATED_STRINGS)
def test_is_templated(string, expected):
    result = string_is_templated(string, Environment())

    assert result == expected


REPL_DICT = {"var_a": "AAA", "var_b": "BBB"}
REPLACE_STRINGS = [
    ("THIS IS {{ var_a }}", REPL_DICT, "THIS IS AAA"),
    ("WHAT {{ var_a }} {{ var_b }}", REPL_DICT, "WHAT AAA BBB"),
]


@pytest.mark.parametrize("text, replacement_dict, expected", REPLACE_STRINGS)
def test_replace_string(text, replacement_dict, expected):
    result = replace_string(text, replacement_dict, Environment())

    assert result == expected


INDENT_STRINGS = [
    ("a\nb", 2, True, "  a\n  b"),
    ("  a\nb", 2, False, "  a\n  b"),
    ("  a\n  b", 2, True, "    a\n    b"),
]


@pytest.mark.parametrize("text, num_spaces, keep_current, expected", INDENT_STRINGS)
def test_reindent(text, num_spaces, keep_current, expected):
    result = reindent(text, num_spaces, keep_current)

    assert result == expected


CACHE_URLS = [
    ("http://a.server.com/what/now", "http/a.server.com/what/now"),
    ("https://a.server.com/what?a+b", "https/a.server.com/what/a/b"),
]


@pytest.mark.parametrize("url, expected", CACHE_URLS)
def test_calculate_cache_location_for_url(url, expected):
    result = calculate_cache_location_for_url(url)

    assert result == expected
