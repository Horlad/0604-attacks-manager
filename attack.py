from dataclasses import dataclass, field
from datetime import datetime
from util import subprocess, UpgradedScheduler, exec_command
import time
from loguru import logger

@dataclass
class Attack:
    """Class for defining an attack via shell commands and schedule it."""

    name: str = "Default"
    commands: list[str] = field(default_factory=list)
    delay_min: int = 1
    run_at: list[str] = field(default_factory=list)
            
    def run_attack(self):
        "Execute all shell commands for the attack"

        for command in self.commands:
            logger.info(f"The {self.name} -> '{command}' started.")

            try:
                result, output = exec_command(command)
            except subprocess.CalledProcessError as e:
                logger.warning(f"The {self.name} -> '{command}' has crushed.\nOutput:\n\n{e.stdout}Error:\n{e.stderr}")
            if result:
                logger.success(f"The {self.name} -> '{command}' output:\n\n{output}")
            else:
                logger.warning(f"The {self.name} -> '{command}' output:\n\n{output}")
            
    
    def _schedule_attack(self, timefunc = time.time):
        "Create an scheduler object for the attack, set repeative and at-time attack, if present"
        self._sch = UpgradedScheduler(timefunc)
        
        delay_sec = self.delay_min * 60
        self._sch.enterrep(delay_sec, 1, self.run_attack)

        for run_time in self.run_at:
            run_timestamp = datetime.fromisoformat(run_time).timestamp()
            self._sch.enterabs(run_timestamp, 1, self.run_attack)

    def run_sheduled(self):
        "Scheduled attacks and start the scheduler"
        self._schedule_attack()
        logger.info("The attacks were scheduled.")
        self._sch.run()