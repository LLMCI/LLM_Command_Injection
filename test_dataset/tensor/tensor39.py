def _run_task_in_process(self, cmd_args, cluster_spec, task_type, task_id):
    env = os.environ.copy()
    env['TF_CONFIG'] = json.dumps({
        'cluster': cluster_spec,
        'task': {
            'type': task_type,
            'index': task_id
        }
    })
    return subprocess.Popen(
        cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
