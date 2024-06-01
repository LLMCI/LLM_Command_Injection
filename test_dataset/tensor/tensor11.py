def test_posonly(self, args, kwargs):
    major, minor, _ = platform.python_version_tuple()
    if not (major == "3" and int(minor) >= 8):
      self.skipTest("Positional only args are supported in Python 3.8+")

    # Raises syntax error in 3.7 but is important coverage for 3.8+.
    foo = eval("lambda x, y, /, z: x + y + z")  # pylint: disable=eval-used

    polymorphic_type = function_type.FunctionType.from_callable(foo)
    mono_type, _ = function_type.canonicalize_to_monomorphic(
        args, kwargs, {}, {}, polymorphic_type)

    bound_args = mono_type.bind(*args, **kwargs)
    self.assertEqual(bound_args.args, (1, 2, 3))
    self.assertEqual(bound_args.kwargs, {})

    type_context = trace_type.InternalTracingContext()
    expected_type = function_type.FunctionType([
        function_type.Parameter("x", function_type.Parameter.POSITIONAL_ONLY,
                                False, trace_type.from_value(1, type_context)),
        function_type.Parameter("y", function_type.Parameter.POSITIONAL_ONLY,
                                False, trace_type.from_value(2, type_context)),
        function_type.Parameter("z",
                                function_type.Parameter.POSITIONAL_OR_KEYWORD,
                                False, trace_type.from_value(3, type_context)),
    ])

    self.assertEqual(mono_type, expected_type)
