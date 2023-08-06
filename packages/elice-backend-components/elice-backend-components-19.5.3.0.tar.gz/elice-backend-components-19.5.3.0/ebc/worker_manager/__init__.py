import functools
import signal
import subprocess
import sys
import threading
import time
import traceback
from typing import Dict, List, NamedTuple, Optional

__all__ = ['run']

_POLL_INTERVAL = 0.1
_SIGTERM_TIMEOUT = 15
_MONITOR_THREAD_TIMEOUT = 5
_CONDITION_CHECK_INTERVAL = 1
_CONDITION_CHECK_TIMEOUT = 10


class WorkerConfig(NamedTuple):
    name: str
    num_workers: int
    cmd: List[str]
    start_condition_cmd: Optional[List[str]] = None


class WorkerProcessInfo(NamedTuple):
    name: str
    popen_obj: subprocess.Popen
    monitor: threading.Thread


class WorkerProcess(NamedTuple):
    worker_config: WorkerConfig
    process_info_list: List[WorkerProcessInfo]


WorkerConfigDict = Dict[str, WorkerConfig]


def run(worker_config_dict: WorkerConfigDict):
    '''Run a set of processes defined by `worker-config`

    .. note:: Example Configuration

        worker_config = {
            'manager': {
                'num_workers': 1,
                'cmd': ['python', 'launcher_manager.py']
            },
            'http-server': {
                'num_workers': 1,
                'cmd': ['gunicorn',
                        '-c', './assets/gunicorn_conf.py',
                        'launcher_http_server:server.app']
            },
            'http-server-nginx': {
                'num_workers': 1,
                'cmd': ['nginx', '-g', 'daemon off;'],
                'start_condition_cmd': ['curl',
                                        '--fail', '-s',
                                        'http://0.0.0.0:8080/ping']
            },
            'tcp-server': {
                'num_workers': os.environ.get('TCP_SERVER_NUM_WORKERS', 1),
                'cmd': ['python', 'launcher_tcp_server.py']
            }
        }
    '''

    term_signal = signal.Signals.SIGTERM
    term_event = threading.Event()

    def _signal_handler(signum, frame):
        if term_event.is_set():
            print('Forced termination of manager', flush=True)
            sys.exit(1)

        nonlocal term_signal
        term_signal = signal.Signals(signum)
        term_event.set()
        print('Signal handler called with signal :', term_signal.name,
              flush=True)

    signal.signal(signal.SIGTERM, _signal_handler)
    signal.signal(signal.SIGINT, _signal_handler)

    max_name_length = max(
        len('%s_%d' % (worker_config.name, worker_config.num_workers + 1))
        for worker_config in worker_config_dict.values()
    )

    def _p_print(prefix: str, txt: str, *, is_stdout: bool = False):
        formatstr = '%-{:d}s %s %s'.format(max_name_length)
        print(formatstr % (prefix, '|' if is_stdout else '>', txt), flush=True)

    def _process_launcher(worker_process: WorkerProcess):
        worker_config = worker_process.worker_config
        process_info_list = worker_process.process_info_list

        if worker_config.start_condition_cmd is not None:
            _p_print(
                worker_config.name,
                'Check start condition...'
            )

            while not term_event.is_set():
                try:
                    condition_result = subprocess.run(
                        worker_config.start_condition_cmd,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.STDOUT,
                        timeout=_CONDITION_CHECK_TIMEOUT
                    )
                    if condition_result.returncode == 0:
                        break
                except Exception:
                    pass

                _p_print(
                    worker_config.name,
                    'Start condition is not met'
                )

                time.sleep(_CONDITION_CHECK_INTERVAL)

        for idx in range(worker_config.num_workers):
            if term_event.is_set():
                return

            process_name = '%s_%d' % (worker_config.name, idx + 1)

            popen_obj = subprocess.Popen(
                worker_config.cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                start_new_session=True
            )

            _p_print(
                process_name,
                'Started a process with PID %d' % popen_obj.pid
            )

            monitor = threading.Thread(
                target=functools.partial(
                    _process_monitor, process_name, popen_obj
                ),
                daemon=True
            )
            monitor.start()

            process_info_list.append(
                WorkerProcessInfo(
                    name=process_name,
                    popen_obj=popen_obj,
                    monitor=monitor
                )
            )

    def _process_monitor(process_name: str, popen_obj: subprocess.Popen):
        while True:
            try:
                output = popen_obj.stdout.readline()
            except Exception:
                print('Error while reading outputs from "%s"\n%s'
                      % (process_name, traceback.format_exc()),
                      flush=True)
                break

            if not output:
                break

            _p_print(process_name, output.rstrip(), is_stdout=True)

        while True:
            retcode = popen_obj.poll()
            if retcode is not None:
                break
            time.sleep(_POLL_INTERVAL)

        _p_print(process_name, 'Terminated (retcode: %s)' % retcode)

    worker_processes: List[WorkerProcess] = []
    for worker_config in worker_config_dict.values():
        worker_process = WorkerProcess(worker_config, [])
        worker_processes.append(worker_process)

        worker_process_launcher = threading.Thread(
            target=functools.partial(_process_launcher, worker_process),
            daemon=True
        )
        worker_process_launcher.start()

    def _work_all_worker_process_info():
        for worker_process in worker_processes:
            for process_info in worker_process.process_info_list:
                yield process_info

    # Monitor the liveness of all worker processes
    done_process_info: Optional[WorkerProcessInfo] = None
    try:
        while not term_event.is_set():
            for process_info in _work_all_worker_process_info():
                if process_info.popen_obj.poll() is not None:
                    done_process_info = process_info
                    term_event.set()
                    break

                time.sleep(_POLL_INTERVAL)
        else:
            print(
                'Terminate all workers... (cuased by %s)'
                % (done_process_info.name if done_process_info else 'unknown'),
                flush=True
            )

    except Exception:
        traceback.print_exc()

    # Send stop signals to worker processes
    for process_info in _work_all_worker_process_info():
        retcode = process_info.popen_obj.poll()
        if retcode is not None:
            continue
        _p_print(process_info.name, '%s is requested' % term_signal.name)
        process_info.popen_obj.send_signal(term_signal.value)

    # Wait until all worker processes termintate
    wait_until_ts = time.time() + _SIGTERM_TIMEOUT
    while time.time() < wait_until_ts:
        for process_info in _work_all_worker_process_info():
            retcode = process_info.popen_obj.poll()
            if retcode is None:
                break
        else:
            break
        time.sleep(_POLL_INTERVAL)
    else:
        print('Timeout while waiting the termination of worker processes',
              flush=True)

    wait_until_ts = time.time() + _MONITOR_THREAD_TIMEOUT
    while time.time() < wait_until_ts:
        for process_info in _work_all_worker_process_info():
            process_info.monitor.join(0)
            if process_info.monitor.is_alive():
                break
        else:
            break
        time.sleep(_POLL_INTERVAL)
    else:
        print('Timeout while waiting the termination of monitor threads',
              flush=True)

        print('Live monitor threads:', flush=True)
        for process_info in _work_all_worker_process_info():
            if process_info.monitor.is_alive():
                print('- %s' % process_info.pname, flush=True)
