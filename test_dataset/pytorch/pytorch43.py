def te_compile(self, device, dtype, op):
        if op.name in skip_ops:
            return
        sample_inputs_itr = op.sample_inputs(device, dtype, requires_grad=False)
        for sample_input in sample_inputs_itr:
            arg_values = [sample_input.input] + list(sample_input.args)
            kwarg_values = sample_input.kwargs
            param_names = []
            param_values = []
            fx_args = []
            for idx, v in enumerate(arg_values):
                if isinstance(v, torch.Tensor):
                    param_names.append(f"arg_{idx}")
                    param_values.append(v)
                    fx_args.append(param_names[-1])
                else:
                    fx_args.append(f'{repr(v)}')

            for k, v in kwarg_values.items():
                if isinstance(v, torch.Tensor):
                    param_names.append(k)
                    param_values.append(v)
                    fx_args.append(f'{k} = {k}')
                else:
                    fx_args.append(f'{k} = {repr(v)}')

            code = f"""
def f({', '.join(param_names)}):
    return op.op({', '.join(fx_args)})"""
            g = {'torch': torch, 'inf' : math.inf, 'op': op}
            exec(code, g)
            f = g['f']
            f.__module__ = 'test'
            out = f(*param_values)

            ts_g = torch.jit.trace(f, param_values)
            kernel = torch._C._te.TensorExprKernel(ts_g.graph)
            correct_val = f(*param_values)
            self.assertEqual(kernel.run(tuple(param_values)), correct_val)
            self.assertEqual(kernel.fallback(tuple(param_values)), correct_val)
