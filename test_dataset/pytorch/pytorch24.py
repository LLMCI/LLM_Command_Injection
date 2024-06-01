import ast
import inspect
import textwrap
import copy
import functools
from types import FunctionType
from typing import cast, Union, Callable, Dict, Optional, Any
from torch.fx._symbolic_trace import Tracer
from torch.fx.graph import Graph
from torch._sources import normalize_source_lines
import torch

class AST_Rewriter(ast.NodeTransformer):

    def rewrite(self, fn: FunctionType):

        # Normalize the source lines
        sourcelines, _ = inspect.getsourcelines(fn)
        sourcelines = normalize_source_lines(sourcelines)
        source = ''.join(sourcelines)
        normalized_str = textwrap.dedent(source)

        # Rewrite the original AST
        source_ast = ast.parse(normalized_str)
        dest_ast = ast.fix_missing_locations(self.visit(source_ast))

        # Pull out the compiled function from the newly-created Module
        code = compile(dest_ast, "", "exec")
        globals_dict = copy.copy(fn.__globals__)
        keys_before = set(globals_dict.keys())
        exec(code, globals_dict)
