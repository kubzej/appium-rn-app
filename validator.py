def validate_input_against_output(input, output):
    """Comparing to values"""
    if input != output:
        raise Exception(f"Validation of INPUT:{input} against OUTPUT:{output} failed")


def validate_input_against_more_outputs(input, outputs):
    """Comparing value against more values in list"""
    if input not in outputs:
        raise Exception(f"Validation of INPUT:{input} against OUTPUTS:{outputs} failed")
