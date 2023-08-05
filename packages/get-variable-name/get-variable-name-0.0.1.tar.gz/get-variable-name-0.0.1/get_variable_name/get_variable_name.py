def get_variable_name(x):
    """
    Returns variable name as string
    """
    import re
    import traceback
    pattern = re.compile(r'[\W+\w+]*get_variable_name\((\w+)\)')
    var = pattern.match(traceback.extract_stack(limit=2)[0][3]).group(1)
    return var

if __name__ == "__main__":
    pass
