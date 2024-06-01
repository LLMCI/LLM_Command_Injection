def expected_return_type(func):
        """
        Our Pybind functions have a signature of the form `() -> return_type`.
        """
        # Imports needed for the `eval` below.
        from typing import List, Tuple  # noqa: F401

        return eval(re.search("-> (.*)\n", func.__doc__).group(1))
