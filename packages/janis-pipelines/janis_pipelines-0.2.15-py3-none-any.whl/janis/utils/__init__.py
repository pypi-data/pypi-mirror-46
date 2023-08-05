from typing import Dict, Any, List, Tuple


def first_value(d: Dict):
    return next(iter(d.values()))


def convert_expression_to_wdl(expression):
    import re

    # Some examples
    # $(inputs.filename) -> "{filename}"
    # $(inputs.filename).out -> "{filename}.out"
    # randomtext.filename -> "randomtext.filename

    if not expression:
        return expression

    if not isinstance(expression, str):
        raise Exception(f"Expected expression of type string, got: {expression} ({type(expression)})")

    r1 = re.compile(r"\$\(inputs\..*\)")
    m1 = r1.match(expression)
    if m1:
        return f'"{{{m1.group()[9:-1]}}}{expression[m1.span()[1]:]}"'

    r2 = re.compile(r"\$\(\..*\)")
    m2 = r2.match(expression)
    if m2:
        return f'"{{{m2.group()[9:-1]}}}{expression[m1.span()[1]:]}"'

    return f'"{expression}"'


def get_value_for_hints_and_ordered_resource_tuple(hints: Dict[str, Any], tuples: List[Tuple[str, Dict[str, int]]]):
    for k,d in tuples:
        if k not in hints: continue
        v = hints[k]
        if v not in d: continue
        return d[v]
    return None


def zip_directory(parent_dir, dir_name):
    import subprocess
    from .logger import Logger
    from os import chdir

    Logger.info("Zipping tools")
    chdir(parent_dir)

    zip_result = subprocess.run(["zip", "-r", f"{dir_name}.zip", f"{dir_name}/"])
    if zip_result.returncode == 0:
        Logger.info("Zipped tools")
    else:
        Logger.critical(zip_result.stderr)
