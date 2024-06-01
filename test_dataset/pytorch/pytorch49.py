import os

current_dir = os.path.dirname(os.path.abspath(__file__))
print(current_dir)
filepath = os.path.join(current_dir, 'test_cuda.py')
print(current_dir)
exec(compile(open(filepath).read(), filepath, mode='exec'))
