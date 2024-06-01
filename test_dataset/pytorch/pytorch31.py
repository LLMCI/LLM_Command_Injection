from torch import SymBool
import sympy


def guard_bool(a):
    if isinstance(a, SymBool):
        return a.node.guard_bool("", 0)  # NB: uses Python backtrace
    assert type(a) is bool, a
    return a

def eval_is_non_overlapping_and_dense(sizes, strides):
    return int(guard_bool(_eval_is_non_overlapping_and_dense(sizes, strides)))

def _eval_is_non_overlapping_and_dense(sizes, strides):
    dim = len(sizes)

    # Short-circuits for tensors of rank one, which are
    # non-overlapping and "dense" if their stride is one
    # or it is a 0/1 element tensor
    if dim == 1:
        return strides[0] == 1 or sizes[0] < 2

    # Checks that there exists a permutation of the strides s.t. the tensor would be contiguous
    # Sorts (length, stride) pairs by stride
    lengths_and_strides = sorted(
        zip(sizes, strides), key=operator.itemgetter(1)
    )

    # Unlike the C++ code, we don't move the 0/1 size dimensions to the
    # end.  So we have to keep going for this code.
    expected_stride = 1
    for length, stride in lengths_and_strides:

        if length == 1:
            continue

        if stride != expected_stride:
            return False

        expected_stride *= length

    return True
    

def cast_symbool_to_symint_guardless(symbool: torch.SymBool) -> torch.SymInt:
    int_sym = sympy.Piecewise((1, symbool.node.expr), (0, True))
    return symbool.node.shape_env.create_symintnode(int_sym, hint=int(symbool.node.require_hint()))


SYMPY_INTERP = {
    'Abs': operator.abs,
    'Eq': operator.eq,
    'Ne': operator.ne,
    'Gt': operator.gt,
    'Lt': operator.lt,
    'Le': operator.le,
    'Ge': operator.ge,
    'Min': min,
    'Max': max,
    'Mod': operator.mod,
    'FloorDiv': operator.floordiv,
    'TrueDiv': operator.truediv,
    'IsNonOverlappingAndDenseIndicator': eval_is_non_overlapping_and_dense,
    'floor': math.floor,
    'ceiling': math.ceil,
    'cast_symbool_to_symint_guardless': cast_symbool_to_symint_guardless,
}


def evaluate_guards_expression(self, code, args):
    arg_names = [f"t{i}" for i in range(len(args))]
    return eval(code, SYMPY_INTERP, {"L": dict(zip(arg_names, args))})


