"""Contains validators for task models."""


def task_instance_args_are_valid(instance, fill_missing_args=False):
    """Determines whether a task instance's arguments are valid.

    The arguments are valid if the instance's argument includes all of
    its task type's required arguments (but not necessarily the
    arguments for which a default value exists).

    Arg:
        instance: A task instance instance. (Yikes!)
        fill_missing_args: A boolean determining whether to fill in any
            missing arguments in the instance with default values.
    Returns:
        A tuple containing a boolean and a string, where the boolean
        signals whether the arguments are valid and the string explains
        why, in the case that the boolean is False (otherwise it's an
        empty string).
    """
    # Validate an instance's args against its required args.
    task_type_required_args = instance.task_type.required_arguments
    task_type_default_vals = (
        instance.task_type.required_arguments_default_values)
    instance_arg_keys = instance.arguments.keys()

    for required_arg in task_type_required_args:
        # Check if the required argument is provided
        if required_arg not in instance_arg_keys:
            # Required argument not provided. Check if default argument
            # value exists.
            if required_arg not in task_type_default_vals:
                # No default exists
                return (
                    False,
                    "required argument '%s' not provided!" % required_arg)

            # Fill in the default value if we're told to
            if fill_missing_args:
                instance.arguments[required_arg] = (
                    task_type_default_vals[required_arg])

    # Valid
    return (True, "")


def task_type_args_are_valid(instance):
    """Determines whether a task type's argument fields are valid.

    The argument fields are valid if the argument keys in the
    required_arguments_default_values field are a subset of its required
    arguments.

    Arg:
        instance: A task type instance.
    Returns:
        A tuple containing a boolean and a string, where the boolean
        signals whether the arguments are valid and the string explains
        why, in the case that the boolean is False (otherwise it's an
        empty string).
    """
    # Ensure that the default arguments form a subset of the required
    # arguments
    if not set(instance.required_arguments_default_values.keys()).issubset(
            set(instance.required_arguments)):
        return (
            False,
            "default arguments not a subset of required arguments")

    # Valid
    return (True, "")
