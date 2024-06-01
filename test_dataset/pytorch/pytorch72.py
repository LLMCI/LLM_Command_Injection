class AnonymousAxis:
    def __init__(self, value: str) -> None:
        self.value = int(value)
        if self.value < 1:
            raise ValueError(
                f"Anonymous axis should have positive length, not {self.value}"
            )


class ParsedExpression:
    """Structure containing information about one side of an `einops`-style pattern (e.g. 'b c (h w)')."""

    def __init__(
        self,
        expression: str,
        *,
        allow_underscore: bool = False,
        allow_duplicates: bool = False,
    ) -> None:
        """Parse the expression and store relevant metadata.

        Args:
            expression (str): the `einops`-pattern to parse
            allow_underscore (bool): whether to allow axis identifier names to begin with an underscore
            allow_duplicates (bool): whether to allow an identifier to appear more than once in the expression
        """
        self.has_ellipsis: bool = False
        self.has_ellipsis_parenthesized: Optional[bool] = None
        self.identifiers: Set[Union[str, AnonymousAxis]] = set()
        # that's axes like 2, 3, 4 or 5. Axes with size 1 are exceptional and replaced with empty composition
        self.has_non_unitary_anonymous_axes: bool = False
        # composition keeps structure of composite axes, see how different corner cases are handled in tests
        self.composition: List[Union[List[Union[str, AnonymousAxis]], str]] = []
        if "." in expression:
            if "..." not in expression:
                raise ValueError(
                    "Expression may contain dots only inside ellipsis (...)"
                )
            if str.count(expression, "...") != 1 or str.count(expression, ".") != 3:
                raise ValueError(
                    "Expression may contain dots only inside ellipsis (...); only one ellipsis for tensor "
                )
            expression = expression.replace("...", _ellipsis)
            self.has_ellipsis = True

        bracket_group: Optional[List[Union[str, AnonymousAxis]]] = None

        def add_axis_name(x: str) -> None:
            if x in self.identifiers:
                if not (allow_underscore and x == "_") and not allow_duplicates:
                    raise ValueError(
                        f"Indexing expression contains duplicate dimension '{x}'"
                    )
            if x == _ellipsis:
                self.identifiers.add(_ellipsis)
                if bracket_group is None:
                    self.composition.append(_ellipsis)
                    self.has_ellipsis_parenthesized = False
                else:
                    bracket_group.append(_ellipsis)
                    self.has_ellipsis_parenthesized = True
            else:
                is_number = str.isdecimal(x)
                if is_number and int(x) == 1:
                    # handling the case of anonymous axis of length 1
                    if bracket_group is None:
                        self.composition.append([])
                    else:
                        pass  # no need to think about 1s inside parenthesis
                    return
                is_axis_name, reason = self.check_axis_name_return_reason(
                    x, allow_underscore=allow_underscore
                )
                if not (is_number or is_axis_name):
                    raise ValueError(f"Invalid axis identifier: {x}\n{reason}")
                axis_name: Union[str, AnonymousAxis] = (
                    AnonymousAxis(x) if is_number else x
                )
                self.identifiers.add(axis_name)
                if is_number:
                    self.has_non_unitary_anonymous_axes = True
                if bracket_group is None:
                    self.composition.append([axis_name])
                else:
                    bracket_group.append(axis_name)

        current_identifier = None
        for char in expression:
            if char in "() ":
                if current_identifier is not None:
                    add_axis_name(current_identifier)
                current_identifier = None
                if char == "(":
                    if bracket_group is not None:
                        raise ValueError(
                            "Axis composition is one-level (brackets inside brackets not allowed)"
                        )
                    bracket_group = []
                elif char == ")":
                    if bracket_group is None:
                        raise ValueError("Brackets are not balanced")
                    self.composition.append(bracket_group)
                    bracket_group = None
            elif str.isalnum(char) or char in ["_", _ellipsis]:
                if current_identifier is None:
                    current_identifier = char
                else:
                    current_identifier += char
            else:
                raise ValueError(f"Unknown character '{char}'")

        if bracket_group is not None:
            raise ValueError(f"Imbalanced parentheses in expression: '{expression}'")
        if current_identifier is not None:
            add_axis_name(current_identifier)

    @staticmethod
    def check_axis_name_return_reason(
        name: str, allow_underscore: bool = False
    ) -> Tuple[bool, str]:
        """Check if the given axis name is valid, and a message explaining why if not.

        Valid axes names are python identifiers except keywords, and should not start or end with an underscore.

        Args:
            name (str): the axis name to check
            allow_underscore (bool): whether axis names are allowed to start with an underscore

        Returns:
            Tuple[bool, str]: whether the axis name is valid, a message explaining why if not
        """
        if not str.isidentifier(name):
            return False, "not a valid python identifier"
        elif name[0] == "_" or name[-1] == "_":
            if name == "_" and allow_underscore:
                return True, ""
            return False, "axis name should should not start or end with underscore"
        else:
            if keyword.iskeyword(name):
                warnings.warn(
                    f"It is discouraged to use axes names that are keywords: {name}",
                    RuntimeWarning,
                )
            if name in ["axis"]:
                warnings.warn(
                    "It is discouraged to use 'axis' as an axis name and will raise an error in future",
                    FutureWarning,
                )
            return True, ""

    @staticmethod
    def check_axis_name(name: str) -> bool:
        """Check if the name is a valid axis name.

        Args:
            name (str): the axis name to check

        Returns:
            bool: whether the axis name is valid
        """
        is_valid, _ = ParsedExpression.check_axis_name_return_reason(name)
        return is_valid


def parse_pattern(
    pattern: str, axes_lengths: Mapping[str, int]
) -> Tuple[ParsedExpression, ParsedExpression]:
    """Parse an `einops`-style pattern into a left-hand side and right-hand side `ParsedExpression` object.

    Args:
        pattern (str): the `einops`-style rearrangement pattern
        axes_lengths (Mapping[str, int]): any additional length specifications for dimensions

    Returns:
       Tuple[ParsedExpression, ParsedExpression]: a tuple containing the left-hand side and right-hand side expressions
    """
    # adapted from einops.einops._prepare_transformation_recipe
    # https://github.com/arogozhnikov/einops/blob/230ac1526c1f42c9e1f7373912c7f8047496df11/einops/einops.py
    try:
        left_str, right_str = pattern.split("->")
    except ValueError:
        raise ValueError("Pattern must contain a single '->' separator") from None

    if _ellipsis in axes_lengths:
        raise ValueError(f"'{_ellipsis}' is not an allowed axis identifier")

    left = ParsedExpression(left_str)
    right = ParsedExpression(right_str)

    if not left.has_ellipsis and right.has_ellipsis:
        raise ValueError(
            f"Ellipsis found in right side, but not left side of a pattern {pattern}"
        )
    if left.has_ellipsis and left.has_ellipsis_parenthesized:
        raise ValueError(
            f"Ellipsis is parenthesis in the left side is not allowed: {pattern}"
        )

    return left, right


def _create_rearrange_callable(
    tensor_ndim: int, pattern: str, **axes_lengths: int
) -> Callable[[torch.Tensor], torch.Tensor]:
    
    left, right = parse_pattern(pattern, axes_lengths)
    validate_rearrange_expressions(left, right, axes_lengths)

    n_anon_dims = sum(not dim for dim in left.composition)
    if left.has_ellipsis:
        n_ellipsis_dims = tensor_ndim - (len(left.composition) - 1)
        n_named_dims = len(left.identifiers) - 1

        if (pattern_ndim := n_anon_dims + n_named_dims) > tensor_ndim:
            raise ValueError(
                f"Number of dimensions in pattern ({pattern_ndim}) must be less than or equal to the number of "
                f"dimensions in the tensor ({tensor_ndim})"
            )
    else:
        n_ellipsis_dims = 0
        n_named_dims = len(left.identifiers)

        if (pattern_ndim := len(left.composition)) != tensor_ndim:
            raise ValueError(
                f"Number of dimensions in pattern ({pattern_ndim}) must be equal to the number of dimensions in "
                f"the tensor ({tensor_ndim})"
            )
    n_dims = n_named_dims + n_ellipsis_dims + n_anon_dims

    if n_dims == 0:
        # an identity rearrangement on a 0-dimension tensor
        return lambda tensor: tensor

    first_class_dims: Tuple[str, ...] = tuple(f"d{i}" for i in range(n_dims))
    identifier_dim_map: Dict[Union[str, AnonymousAxis], Tuple[str, ...]] = {}
    anon_axes: List[AnonymousAxis] = []

    # map the left-hand side identifiers to strings representing first class dims
    dims_i = 0
    for dimension in left.composition:
        if isinstance(dimension, list):
            for identifier in dimension:
                # non-unitary anon axes are not allowed in rearrange & unitary anon axes are represented as empty lists
                assert isinstance(identifier, str)
                identifier_dim_map[identifier] = (first_class_dims[dims_i],)
                dims_i += 1
            if not dimension:
                # unitary anonymous axis
                anon_axis = AnonymousAxis("1")
                identifier_dim_map[anon_axis] = (first_class_dims[dims_i],)
                anon_axes.append(anon_axis)
                dimension.append(anon_axis)
                dims_i += 1
        elif dimension == _ellipsis:
            identifier = _ellipsis
            identifier_dim_map[identifier] = tuple(
                first_class_dims[dims_i + j] for j in range(n_ellipsis_dims)
            )
            dims_i += n_ellipsis_dims
        else:
            raise ValueError(f"Unexpected dimension: {dimension}")

    def composition_to_dims(
        composition: Sequence[Union[List[Union[str, AnonymousAxis]], str]]
    ) -> List[Union[str, Tuple[str, ...]]]:
        """Convert a `ParsedExpression.composition` into a `Tensor.__getitem__` index of strings representing first
        class dims."""
        dim_composition: List[Union[str, Tuple[str, ...]]] = []
        for dimension in composition:
            if isinstance(dimension, list):
                dim_composition.append(
                    tuple(
                        dim
                        for identifier in dimension
                        for dim in identifier_dim_map[identifier]
                    )
                )
            elif dimension == _ellipsis:
                dim_composition.extend(identifier_dim_map[_ellipsis])
            else:
                raise ValueError(f"Unexpected dimension: {dimension}")
        return dim_composition

    left_dims = composition_to_dims(left.composition)
    right_dims = composition_to_dims(right.composition)
    anon_dims = tuple(identifier_dim_map[axis][0] for axis in anon_axes)
    specified_lengths = tuple(
        (identifier_dim_map[axis][0], length) for axis, length in axes_lengths.items()
    )

    custom_rearrange_callable_name = "do_rearrange"
    custom_rearrange_callable_code = (
        (
            f"def {custom_rearrange_callable_name}(tensor):\n"
            f"    {comma_separate(first_class_dims)} = dims({n_dims})\n"
        )
        + (
            "".join(
                f"    {dim}.size = {length}\n" for (dim, length) in specified_lengths
            )
            if specified_lengths
            else ""
        )
        + f"    tensor = tensor[{comma_separate(left_dims)}].order({comma_separate(right_dims)})\n"
        + (
            f"    return tensor.sum({comma_separate([anon_dims])}, keepdim=False)\n"
            if anon_dims
            else "    return tensor\n"
        )
    )

    exec(custom_rearrange_callable_code)
    return locals()[custom_rearrange_callable_name]
