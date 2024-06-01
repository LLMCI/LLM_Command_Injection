def _deploy(self) -> str:
        """Call to Beam."""
        try:
            import beam  # type: ignore

            if beam.__path__ == "":
                raise ImportError
        except ImportError:
            raise ImportError(
                "Could not import beam python package. "
                "Please install it with `curl "
                "https://raw.githubusercontent.com/slai-labs"
                "/get-beam/main/get-beam.sh -sSfL | sh`."
            )
        self.app_creation()
        self.run_creation()

        process = subprocess.run(
            "beam deploy app.py", shell=True, capture_output=True, text=True
        )

        if process.returncode == 0:
            output = process.stdout
            logger.info(output)
            lines = output.split("\n")

            for line in lines:
                if line.startswith(" i  Send requests to: https://apps.beam.cloud/"):
                    self.app_id = line.split("/")[-1]
                    self.url = line.split(":")[1].strip()
                    return self.app_id

            raise ValueError(
                f"""Failed to retrieve the appID from the deployment output.
                Deployment output: {output}"""
            )
        else:
            raise ValueError(f"Deployment failed. Error: {process.stderr}")
