from torch._inductor.pattern_matcher import gen_pattern

def test_fuse_attention_roundtrip_pattern(self):
        # are we losing anything in serialization
        from torch._inductor.fx_passes.fuse_attention import _get_sfdp_patterns

        global_vals = {
            "aten": torch.ops.aten,
            "prims": torch.ops.prims,
            "torch": torch,
        }

        for name in dir(torch._inductor.pattern_matcher):
            attr = getattr(torch._inductor.pattern_matcher, name)
            if isinstance(attr, type) and issubclass(attr, (PatternExpr, _TargetExpr)):
                global_vals[name] = attr

        with torch._subclasses.FakeTensorMode():
            for _, kwargs in _get_sfdp_patterns():
                gen_kwargs = {
                    key: kwargs[key]
                    for key in (
                        "search_fn",
                        "example_inputs",
                        "trace_fn",
                        "scalar_workaround",
                    )
                }
                pattern = gen_pattern(**gen_kwargs)
                pattern_pp = PatternPrettyPrinter.run(pattern)
                env = global_vals.copy()
                exec(pattern_pp, env)
                pattern_2 = env["output"]
                self.assertEqual(pattern_pp, PatternPrettyPrinter.run(pattern_2))
