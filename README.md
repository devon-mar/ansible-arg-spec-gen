# ansible-arg-spec-gen

A script to generate a skeleton Ansible argument specification for roles.

```
usage: gen_arg_spec.py [-h] [-o OUTPUT] [--required] [--entrypoint ENTRYPOINT] yaml_file

positional arguments:
  yaml_file             Path to the YAML file with the variables.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Path to the output file.
  --required            Set all top level options as required.
  --entrypoint ENTRYPOINT
                        Name of the entrypoint.
```

## Example: Add an arg spec to an existing role

1. Generate an arg spec for `defaults/main.yml`
    ```
    ./gen_arg_spec.py my_role/tasks/main.yml
    ```
2. Check the generated arg spec and add a description to each var.
3. Copy `argument_specs` from `argspec.yml` to `meta/main.yml` in your role.
4. Create a YAML file with the required vars for your role.
5. Generate an arg spec with `required: True` for your required vars.
    ```
    ./gen_arg_spec.py --required my_role/tasks/main.yml
    ```
2. Check the generated arg spec and add a description to each required var.
3. Append `argument_specs` from `argspec.yml` to `meta/main.yml` in your role.
