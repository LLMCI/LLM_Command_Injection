def is_ignored_only(output):
    try:
        report = cmc.parse(output)
    except cmc.ParseError:
        # in case the simple parser fails parsing the output of cuda memcheck
        # then this error is never ignored.
        return False
    count_ignored_errors = 0
    for e in report.errors:
        if 'libcublas' in ''.join(e.stack) or 'libcudnn' in ''.join(e.stack) or 'libcufft' in ''.join(e.stack):
            count_ignored_errors += 1
    return count_ignored_errors == report.num_errors

# Set environment PYTORCH_CUDA_MEMCHECK=1 to allow skipping some tests
os.environ['PYTORCH_CUDA_MEMCHECK'] = '1'

# Discover tests:
# To get a list of tests, run:
# pytest --setup-only test/test_torch.py
# and then parse the output
proc = subprocess.Popen(['pytest', '--setup-only', args.filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = proc.communicate()
lines = stdout.decode().strip().splitlines()
for line in lines:
    if '(fixtures used:' in line:
        line = line.strip().split()[0]
        line = line[line.find('::') + 2:]
        line = line.replace('::', '.')
        ALL_TESTS.append(line)