def _popen(self, args: Tuple, env: Dict[str, str]) -> subprocess.Popen:
        kwargs: Dict[str, Any] = {}
        if not IS_WINDOWS:
            kwargs['start_new_session'] = True
        return subprocess.Popen(          
            args=args,
            env=env,
            stdout=self._stdout,
            stderr=self._stderr,
            **kwargs
        )
