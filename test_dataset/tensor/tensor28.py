def _get_num_nvidia_gpus():
  """Gets the number of NVIDIA GPUs by using CUDA_VISIBLE_DEVICES and nvidia-smi.

  Returns:
    Number of GPUs available on the node
  Raises:
    RuntimeError if executing nvidia-smi failed
  """
  try:
    return len(os.environ['CUDA_VISIBLE_DEVICES'].split(','))
  except KeyError:
    pass  # Ignore and fallback to using nvidia-smi
  try:
    output = subprocess.check_output(['nvidia-smi', '--list-gpus'],
                                     encoding='utf-8')
    return sum(l.startswith('GPU ') for l in output.strip().split('\n'))
  except subprocess.CalledProcessError as e:
    raise RuntimeError('Could not get number of GPUs from nvidia-smi. '
                       'Maybe it is missing?\nOutput: %s' % e.output)

