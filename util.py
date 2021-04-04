import subprocess
from sched import scheduler

def exec_command(command):
    """Execute 'command' as shell command and returns result"""
    try:
        process = subprocess.run(command,
                                check=True, universal_newlines=True, shell=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
         raise e
    return True, process.stdout

class UpgradedScheduler(scheduler):
    """Extend basic scheduler with repeative event"""
    def enterrep(self, interval, priority, action, argument=(), kwargs={}):
        self.enter(interval, priority, self.enterrep, (interval, action, action, argument))
        action(*argument, **kwargs)