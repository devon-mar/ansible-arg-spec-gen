#!/usr/bin/env python3
import yaml
import argparse
from typing import Any, Dict, List


def get_type_str(v: Any) -> str:
    return type(v).__name__


def nested_options(vars: List[Dict[str, Any]]):
    all_opts: Dict[str, Any] = vars[0]
    is_required: Dict[str, bool] = {key: True for key in all_opts}

    for list_dict in vars[1:]:
        # Set keys as optional
        for key in is_required:
            if key not in list_dict:
                is_required[key] = False
        # Add any other keys as optional
        for key in list_dict:
            if key not in is_required:
                all_opts[key] = list_dict[key]
                is_required[key] = False
    # Generate an argspec for all keys
    spec = gen_arg_specs(all_opts)

    # Update required
    for k, v in spec.items():
        v["required"] = is_required[k]
    return spec


def gen_arg_spec(arg_value: Any, required: bool = True) -> Dict:
    """
    Generate a arg spec for a single var.
    """
    spec = {
        "type": get_type_str(arg_value),
        "required": required,
        "description": ''
    }
    if spec["type"] == "list" and len(arg_value) > 0:
        spec["elements"] = get_type_str(arg_value[0])
        if spec["elements"] == "dict":
            spec["options"] = nested_options(arg_value)

    if spec["type"] == "dict" and len(arg_value) > 0:
        spec["options"] = gen_arg_specs(arg_value)

    # Add the default for require
    if required is False:
        spec["default"] = arg_value

    return spec


def gen_arg_specs(vars: Dict, required: bool = True) -> Dict:
    """
    Generate an argspec for all vars in the given dict.
    """
    return {k: gen_arg_spec(v, required=required) for k, v in vars.items()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "yaml_file",
        type=str,
        help="Path to the YAML file with the variables."
    )
    parser.add_argument(
        "-o", "--output",
        default="argspec.yml",
        type=str,
        help="Path to the output file."
    )
    parser.add_argument(
        "--required",
        dest="required",
        default=False,
        action="store_true",
        help="Set all top level options as required."
    )
    parser.add_argument(
        "--entrypoint",
        dest="entrypoint",
        default="main",
        help="Name of the entrypoint to the role."
    )
    args = parser.parse_args()
    with open(args.yaml_file) as f:
        defaults = yaml.load(f, Loader=yaml.FullLoader)

    argspec = {"argument_specs": {args.entrypoint: {"options": gen_arg_specs(defaults, required=args.required)}}}
    with open(args.output, 'w') as f:
        yaml.dump(argspec, f, sort_keys=False)
