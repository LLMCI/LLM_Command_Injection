def make_dummy_fn(op):
            exec(f"temp = lambda x: x.{op}()")
            return locals()["temp"]
