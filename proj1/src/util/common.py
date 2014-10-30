import os
import subprocess
import shlex
from tempfile import NamedTemporaryFile

import TimeoutThread


def run_command(command, time_out):
    args = shlex.split(command)
    proc = subprocess.Popen(args, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, preexec_fn=os.setsid)

    with TimeoutThread.processTimeout(time_out, proc.pid):
        stdout, stderr = proc.communicate()

    resultcode = proc.wait()
    return resultcode, stdout, stderr

def try_prog(prog_str):
    with NamedTemporaryFile() as tmp_f:
        tmp_f.write(prog_str)
        tmp_f.flush()
        result = run_command("./yices_main %s" % tmp_f.name, 3600000)
        return result[1].find("unsat") is -1, result[1]
