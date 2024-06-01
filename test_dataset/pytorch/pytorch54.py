def test_MaxUnpool_index_errors(self, device, module_name, module_size, output_size, test_index, should_error):
        # NOTE: CUDA tests need to be run in a subprocess because they cause device asserts
        if torch.device(device).type == 'cuda':
            error_msgs = {
                'MaxUnpool2d': r'Assertion `maxind >= 0 && maxind < outputImageSize` failed',
                'MaxUnpool3d': r'Assertion `index >= 0 && index < outputImageSize` failed'}

            script = f'''
import torch
unpool = torch.nn.{module_name}({module_size}).to('{device}')
output = torch.rand({output_size}, dtype=torch.float32, device='{device}')
indices = torch.zeros({output_size}, dtype=torch.int64, device='{device}')
indices.flatten()[0] = {test_index}
unpool(output, indices)
torch.cuda.synchronize()
'''
            p = subprocess.run(
                [sys.executable, '-c', script],
                cwd=os.path.dirname(os.path.realpath(__file__)),
                capture_output=True,
                text=True,
            )

            output = p.stdout + '\n' + p.stderr

            error_msg = error_msgs[module_name]

            if should_error:
                self.assertIn(
                    error_msg,
                    output,
                    'The expected error was not found')
            else:
                self.assertNotIn(
                    'Error',
                    output,
                    'Should not have produced an error')
        else:
            module_class = getattr(torch.nn, module_name)
            unpool = module_class(module_size).to(device)
            output = torch.rand(output_size, dtype=torch.float32, device=device)
            indices = torch.zeros(output_size, dtype=torch.int64, device=device)
            indices.flatten()[0] = test_index

            if should_error:
                with self.assertRaisesRegex(RuntimeError, r'Found an invalid max index:'):
                    unpool(output, indices)
            else:
                unpool(output, indices)
