@unittest.skipIf(GRAPH_EXECUTOR != ProfilingMode.LEGACY, "Simple Executor doesn't have any shapes to propagate")
def test_tensor_as_tensor_shape_prop(self):
        tensor_template = dedent('''
        def func():
            return torch.{tensor_op}({input})
        ''')
        ops = ['tensor', 'as_tensor']
        inputs = ['[1]', '[False]', '[2.5]', '0.5', '1', 'False', '[[1]]', 'torch.jit.annotate(List[List[int]], [])']
        expected_shape = ["Long(*, device=cpu)", "Bool(*, device=cpu)",
                          "Float(*, device=cpu)", "Float(device=cpu)",
                          "Long(device=cpu)", "Bool(device=cpu)", "Long(*, *, device=cpu)"]

        for op in ops:
            for inp, expect in zip(inputs, expected_shape):
                code = tensor_template.format(tensor_op=op, input=inp)
                scope = {}
                exec(code, globals(), scope)
                cu = torch.jit.CompilationUnit(code)
                torch._C._jit_pass_complete_shape_analysis(cu.func.graph, (), False)
                FileCheck().check(expect).check(f"aten::{op}").run(cu.func.graph)
