import argparse
from typing import Any, Dict

from . import ProcessConfig, WorkerConfig, run

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='worker_manager',
        description='Worker manager to execute a set of worker processes.'
    )
    parser.add_argument('config', help='configuration file (.py)')
    args = parser.parse_args()

    config_locals: Dict[str, Any] = {}
    with open(args.config, 'rb') as f:
        code = compile(f.read(), args.config, 'exec')
        exec(code, config_locals)  # nosec

    if 'worker_config' not in config_locals:
        raise RuntimeError('There is no local variable `worker_config` '
                           'in the configuration file')

    assert isinstance(config_locals['worker_config'], dict)

    worker_config: WorkerConfig = dict()
    for process_name, process_config in config_locals['worker_config'].items():
        worker_config[process_name] = ProcessConfig(**process_config)

    run(worker_config)
