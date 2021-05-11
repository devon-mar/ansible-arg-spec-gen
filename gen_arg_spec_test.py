import pytest
from gen_arg_spec import gen_arg_spec


@pytest.mark.parametrize(
    "key,value,required,expected",
    [
        # int
        ["abc", 123, True, {"type": "int", "required": True, "description": ''}],
        ["abc", 123, False, {"type": "int", "description": '', "default": 123}],
        # str
        ["abc", "def", True, {"type": "str", "required": True, "description": ''}],
        ["abc", "def", False, {"type": "str", "description": '', "default": "def"}],
        # bool
        ["abc", True, True, {"type": "bool", "required": True, "description": ''}],
        ["abc", False, False, {"type": "bool", "description": '', "default": False}],
        # list
        ["abc", [1, 2], True, {"type": "list", "required": True, "description": '', "elements": "int"}],
        [
            "abc", ['d', 'e'], False,
            {"type": "list", "description": '', "elements": "str", "default": ['d', 'e']}
        ],
        # list of dicts
        [
            "abc", [{"required_key": "a"}, {"required_key": "b", "optional_key": 123}], True,
            {
                "type": "list", "required": True, "description": '', "elements": "dict",
                "options": {
                    "required_key": {"type": "str", "required": True, "description": ""},
                    "optional_key": {"type": "int", "description": ""}
                }
            }
        ],
        [
            "abc", [{"required_key": "a", "optional_key": True}, {"required_key": "b"}], False,
            {
                "type": "list", "description": '', "elements": "dict",
                "options": {
                    "required_key": {"type": "str", "required": True, "description": ""},
                    "optional_key": {"type": "bool", "description": ""}
                },
                "default": [{"required_key": "a", "optional_key": True}, {"required_key": "b"}]
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
                "type": "dict", "description": '', "default": {"a": "b"},
                "options": {"a": {"type": "str", "required": True, "description": ""}}
            }
        ],
    ]
)
def test_gen_arg_spec(key, value, required, expected):
    assert gen_arg_spec(value, required) == expected
