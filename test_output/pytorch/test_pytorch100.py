import os
import unittest
import subprocess
from unittest.mock import patch

def format_flamegraph(flamegraph_lines, flamegraph_script=None):
    if flamegraph_script is None:
        flamegraph_script = f'/tmp/{os.getuid()}_flamegraph.pl'
    if not os.path.exists(flamegraph_script):
        import urllib.request
        print(f"Downloading flamegraph.pl to: {flamegraph_script}")
        urllib.request.urlretrieve(
            'https://raw.githubusercontent.com/brendangregg/FlameGraph/master/flamegraph.pl', flamegraph_script)
        subprocess.check_call(['chmod', '+x', flamegraph_script])
    args = [flamegraph_script, '--countname', 'bytes']
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')
    assert p.stdin is not None
    assert p.stdout is not None
    p.stdin.write(flamegraph_lines)
    p.stdin.close()
    result = p.stdout.read()
    p.stdout.close()
    p.wait()
    assert p.wait() == 0
    return result

class TestFormatFlamegraph(unittest.TestCase):
    def test_format_flamegraph_injection(self):   
        test_file = "test_file.txt"
        with open(test_file, "w") as file:
            file.write("This is a test file")
        # Create a malicious flamegraph_script
        malicious_script = "test_file; rm test_file.txt"
        # Call the function with the malicious script
        format_flamegraph("test", malicious_script)
        # Check if the malicious command was executed
        self.assertFalse(os.path.exists(test_file))
        
        
if __name__ == '__main__':
    unittest.main()

