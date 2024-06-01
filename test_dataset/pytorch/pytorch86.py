def _start(
        self, data_dir: str, timeout: int = 60, stderr: Union[int, TextIO, None] = None
    ) -> None:
        sock = find_free_port()
        sock_peer = find_free_port()
        self._port = sock.getsockname()[1]
        peer_port = sock_peer.getsockname()[1]

        etcd_cmd = shlex.split(
            " ".join(
                [
                    self._etcd_binary_path,
                    "--enable-v2",
                    "--data-dir",
                    data_dir,
                    "--listen-client-urls",
                    f"http://{self._host}:{self._port}",
                    "--advertise-client-urls",
                    f"http://{self._host}:{self._port}",
                    "--listen-peer-urls",
                    f"http://{self._host}:{peer_port}",
                ]
            )
        )

        log.info("Starting etcd server: [%s]", etcd_cmd)

        sock.close()
        sock_peer.close()
        self._etcd_proc = subprocess.Popen(etcd_cmd, close_fds=True, stderr=stderr)
        self._wait_for_ready(timeout)