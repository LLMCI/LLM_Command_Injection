def test_converted_call_exec_generated_code(self):

    temp_mod = types.ModuleType('test_module')
    dynamic_code = """
      def foo(x):
        return x + 1
    """
    exec(textwrap.dedent(dynamic_code), temp_mod.__dict__)  # pylint:disable=exec-used
    opts = converter.ConversionOptions(optional_features=None)

    x = api.converted_call(temp_mod.foo, (1,), None, options=opts)

    self.assertAllEqual(x, 2)
