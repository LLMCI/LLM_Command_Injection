def test_linetable_311_writer2(self):
        """
        test large ops (LOAD_METHOD) and EXTENDED_ARGS
        fn_str is in the form:
        def fn():
            ...
            x0 = 1
            x1 = 1
            ...
            l = [x0, x1, ...]
        """
        fn_str = f"""\
def fn():
    foo.bar(1, 2, 3)
{str(chr(10)).join(' ' * 4 + 'x' + str(i) + ' = 1' for i in range(1 << 9))}
    l = [{' '.join('x' + str(i) + ',' for i in range(1 << 9))}]
        """
        locals = {}
        exec(fn_str, {}, locals)
        fn = locals["fn"]
        orig_inst_str = "\n".join(list(map(str, dis.get_instructions(fn))))
        self.assertIn("EXTENDED_ARG", orig_inst_str)
        self.assertIn("LOAD_METHOD", orig_inst_str)
        keys = bytecode_transformation.get_code_keys()
        code_options = {k: getattr(fn.__code__, k) for k in keys}
        result = bytecode_transformation.clean_and_assemble_instructions(
            bytecode_transformation.cleaned_instructions(fn.__code__),
            keys,
            code_options,
        )
        new_inst_str = "\n".join(list(map(str, result[0])))
        self.assertIn("EXTENDED_ARG", new_inst_str)
        self.assertIn("LOAD_METHOD", new_inst_str)
        l1, l2 = list(fn.__code__.co_positions()), list(result[1].co_positions())
        self.assertEqual(len(l1), len(l2))
        for p1, p2 in zip(l1, l2):
            self.assertEqual(p1, p2)
        self.assertEqual(fn.__code__.co_lnotab, result[1].co_lnotab)
