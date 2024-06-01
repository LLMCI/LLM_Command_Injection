import unittest
import os
from collections import namedtuple
import re
import ast
import astunparse
import torch.jit
import pytorch37

class TestCommandInjection(unittest.TestCase):
    def setUp(self):
        self.ctx = namedtuple("Context", ["filename"])
        self.ctx.filename = "test_file"
        self.stmt = namedtuple("Statement", ["lineno", "items", "body"])
        self.stmt.lineno = 1
        self.stmt.items = [namedtuple("Item", ["context_expr"])]
        self.stmt.items[0].context_expr = namedtuple("ContextExpr", ["keywords"])
        self.stmt.items[0].context_expr.keywords = [namedtuple("Keyword", ["arg", "value"])]
        self.stmt.items[0].context_expr.keywords[0].arg = "inp"
        self.stmt.items[0].context_expr.keywords[0].value = namedtuple("Value", ["value"])
        self.stmt.items[0].context_expr.keywords[0].value.value = "inp: str"
        self.stmt.body = [ast.parse("pass").body[0]]
        
    
    def test_build_ignore_context_manager(self):
        # Create a file to test command injection
        with open('test_file.txt', 'w') as f:
            f.write('This is a test file.')
        
        # Inject command to remove the test file
        self.ctx.filename = "test_file.txt'; os.remove('test_file.txt')"
        
        # Call the function with the injected command
        pytorch37.build_ignore_context_manager(self.ctx, self.stmt)
        
        # Check if the file has been removed
        self.assertFalse(os.path.exists('test_file.txt'))

if __name__ == '__main__':
    unittest.main()

