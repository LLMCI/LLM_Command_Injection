def _eval_code(self, code, name):
    globs = {}
    exec(code, globs)  # pylint:disable=exec-used
    return globs[name]
