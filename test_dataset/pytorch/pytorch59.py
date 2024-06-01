def test_basic(self):
        source = '''\
def f(x):
    def g(x):
        raise RuntimeError()  # HEYA

    x = x * 3
    return g(x) + 1
'''

        out: Dict[str, Any] = {}
        scope = {"__compile_source__": source}
        exec(source, scope, out)

        try:
            with report_compile_source_on_error():
                out["f"](1)
        except RuntimeError as e:
            self.assertIn("HEYA", ''.join(traceback.format_tb(e.__traceback__)))

