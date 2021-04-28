import pytest
from gen_arg_spec import gen_arg_spec


@pytest.mark.parametrize(
    "key,value,required,expected",
    [
        # int
        ["abc", 123, True, {"type": "int", "required": True, "description": ''}],
        ["abc", 123, False, {"type": "int", "required": False, "description": '', "default": 123}],
        # str
        ["abc", "def", True, {"type": "str", "required": True, "description": ''}],
        ["abc", "def", False, {"type": "str", "required": False, "description": '', "default": "def"}],
        # bool
        ["abc", True, True, {"type": "bool", "required": True, "description": ''}],
        ["abc", False, False, {"type": "bool", "required": False, "description": '', "default": False}],
        # list
        ["abc", [1, 2], True, {"type": "list", "required": True, "description": '', "elements": "int"}],
        [
            "abc", ['d', 'e'], False,
            {"type": "list", "required": False, "description": '', "elements": "str", "default": ['d', 'e']}
        ],
        # list of dicts
        [
            "abc", [{"required": "a"}, {"required": "b", "optional": 123}], True,
            {
                "type": "list", "required": True, "description": '', "elements": "dict",
                "options": {
                    "required": {"type": "str", "required": True, "description": ""},
                    "optional": {"type": "int", "required": False, "description": ""}
                }
            }
        ],
        [
            "abc", [{"required": "a", "optional": True}, {"required": "b"}], False,
            {
                "type": "list", "required": False, "description": '', "elements": "dict",
                "options": {
                    "required": {"type": "str", "required": True, "description": ""},
                    "optional": {"type": "bool", "required": False, "description": ""}
                },
                "default": [{"required": "a", "optional": True}, {"required": "b"}]
            }
        ],
        # dict
        [
            "abc", {"key": "val"}, True,
            {
                "type": "dict", "required": True, "description": '',
                "options": {"key": {"type": "str", "required": True, "description": ""}}
            }
        ],
        [
            "abc", {"a": "b"}, False,
            {
                "type": "dict", "required": False, "description": '', "default": {"a": "b"},
                "options": {"a": {"type": "str", "required": True, "description": ""}}
            }
        ],
    ]
)
def test_gen_arg_spec(key, value, required, expected):
    assert gen_arg_spec(value, required) == expected
