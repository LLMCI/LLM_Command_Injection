def _test_code(self, code, global_inputs=None):
        r"""
        This function runs `code` using any vars in `global_inputs`
        """
        # if couldn't find the
        if code is not None:
            expr = compile(code, "test", "exec")
            exec(expr, global_inputs)
