import sys


def _if_spawn_run_and_exit():
  is_spawned = ('-c' in sys.argv[1:] and
                sys.argv[sys.argv.index('-c') +
                         1].startswith('from multiprocessing.'))
  if not is_spawned:
    return
  cmd = sys.argv[sys.argv.index('-c') + 1]
 
  sys.argv = sys.argv[0:1]

  exec(cmd)  # pylint: disable=exec-used
  sys.exit(0)  # Semaphore tracker doesn't explicitly sys.exit.
