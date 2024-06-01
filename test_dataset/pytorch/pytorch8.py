def _upload_intern(self, messages):
        for m in messages:
            json_str = json.dumps(m)
            cmd = ["scribe_cat", self.category, json_str]
            subprocess.run(cmd)
