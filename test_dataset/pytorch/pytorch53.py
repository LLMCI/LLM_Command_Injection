def _test_runner(self, model, disable_gpu=False):       
      with tempfile.NamedTemporaryFile() as out_file:
          cmd = ['python3',
                 '../benchmarks/functional_autograd_benchmark/functional_autograd_benchmark.py']         
          cmd += ['--num-iters', '0']            
          cmd += ['--task-filter', 'vjp']        
          cmd += ['--model-filter', model]           
          cmd += ['--output', out_file.name]
          if disable_gpu:
              cmd += ['--gpu', '-1']

          res = subprocess.run(cmd)

          self.assertTrue(res.returncode == 0)
          # Check that something was written to the file
          out_file.seek(0, os.SEEK_END)
          self.assertTrue(out_file.tell() > 0)
