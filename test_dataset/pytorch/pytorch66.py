def report_compile_source_on_error():
    try:
        yield
    except Exception as exc:
        tb = exc.__traceback__

        
        stack = []
        while tb is not None:
            filename = tb.tb_frame.f_code.co_filename
            source = tb.tb_frame.f_globals.get("__compile_source__")

            if filename == "<string>" and source is not None:
                
                with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".py") as f:
                    f.write(source)
                # Create a frame.  Python doesn't let you construct
                # FrameType directly, so just make one with compile
                frame = tb.tb_frame
                code = compile('__inspect_currentframe()', f.name, 'eval')
                code = code.replace(co_name=frame.f_code.co_name)
                # Python 3.11 only
                if hasattr(frame.f_code, 'co_linetable'):
                    code = code.replace(  # type: ignore[call-arg]
                        co_linetable=frame.f_code.co_linetable,  # type: ignore[attr-defined]
                        co_firstlineno=frame.f_code.co_firstlineno,  # type: ignore[attr-defined]
                    )
                fake_frame = eval(
                    code,
                    frame.f_globals,
                    {
                        **frame.f_locals,
                        '__inspect_currentframe': inspect.currentframe
                    }
                )
                fake_tb = TracebackType(
                    None, fake_frame, tb.tb_lasti, tb.tb_lineno
                )
                stack.append(fake_tb)
            else:
                stack.append(tb)

            tb = tb.tb_next

        # Reconstruct the linked list
        tb_next = None
        for tb in reversed(stack):
            tb.tb_next = tb_next
            tb_next = tb

        raise exc.with_traceback(tb_next)  # noqa: TRY200
