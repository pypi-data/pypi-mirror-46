#!/usr/bin/env python
import copy
import json
import logging
import os
import queue
import random
from importlib import import_module
from multiprocessing import Lock, Process, Queue, current_process
from typing import ClassVar
from typing import Dict
from typing import List

import namesgenerator
from frisbee.utils import gen_logger
from frisbee.utils import str_datetime
from frisbee.utils import now_time


os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'


class Frisbee:

    """Class to interact with the core code."""

    NAME: ClassVar[str] = "Frisbee"
    PROCESSES: ClassVar[int] = 100
    MODULE_PATH: ClassVar[str] = 'frisbee.modules'

    def __init__(self, project: str = namesgenerator.get_random_name(),
                 log_level: int = logging.INFO, save: bool = False):
        """Creation."""
        self.project: str = project
        self._log: logging.Logger = gen_logger(self.NAME, log_level)
        self.output: bool = save
        self.folder: str = os.getcwd()
        self._config_bootstrap()

        self._unfullfilled: Queue = Queue()
        self._fulfilled: Queue = Queue()
        self._processes: List = list()
        self._processed: List = list()

        self.results: List = list()
        self.saved: List = list()

    def _reset(self) -> None:
        """Reset some of the state in the class for multi-searches."""
        self.project: str = namesgenerator.get_random_name()
        self._processed: List = list()
        self.results: List = list()

    def _config_bootstrap(self) -> None:
        """Handle the basic setup of the tool prior to user control.

        Bootstrap will load all the available modules for searching and set
        them up for use by this main class.
        """
        if self.output:
            self.folder: str = os.getcwd() + "/" + self.project
            os.mkdir(self.folder)

    def _dyn_loader(self, module: str, kwargs: str):
        """Dynamically load a specific module instance."""
        package_directory: str = os.path.dirname(os.path.abspath(__file__))
        modules: str = package_directory + "/modules"
        module = module + ".py"
        if module not in os.listdir(modules):
            raise Exception("Module %s is not valid" % module)
        module_name: str = module[:-3]
        import_path: str = "%s.%s" % (self.MODULE_PATH, module_name)
        imported = import_module(import_path)
        obj = getattr(imported, 'Module')
        return obj(**kwargs)

    def _job_handler(self) -> bool:
        """Process the work items."""
        while True:
            try:
                task = self._unfullfilled.get_nowait()
            except queue.Empty:
                break
            else:
                self._log.debug("Job: %s" % str(task))
                engine = self._dyn_loader(task['engine'], task)
                task['start_time'] = now_time()
                results = engine.search()
                task['end_time'] = now_time()
                duration: str = str((task['end_time'] - task['start_time']).seconds)
                task['duration'] = duration
                task.update({'results': results})
                self._fulfilled.put(task)
        return True

    def _save(self) -> None:
        """Save output to a directory."""
        self._log.info("Saving results to '%s'" % self.folder)
        path: str = self.folder + "/"
        for job in self.results:
            if job['domain'] in self.saved:
                continue
            job['start_time'] = str_datetime(job['start_time'])
            job['end_time'] = str_datetime(job['end_time'])
            jid: int = random.randint(100000, 999999)
            filename: str = "%s_%s_%d_job.json" % (self.project, job['domain'], jid)
            handle = open(path + filename, 'w')
            handle.write(json.dumps(job, indent=4))
            handle.close()

            filename = "%s_%s_%d_emails.txt" % (self.project, job['domain'], jid)
            handle = open(path + filename, 'w')
            for email in job['results']['emails']:
                handle.write(email + "\n")
            handle.close()
            self.saved.append(job['domain'])

    def search(self, jobs: List[Dict[str, str]]) -> None:
        """Perform searches based on job orders."""
        if not isinstance(jobs, list):
            raise Exception("Jobs must be of type list.")
        self._log.info("Project: %s" % self.project)
        self._log.info("Processing jobs: %d", len(jobs))
        for _, job in enumerate(jobs):
            self._unfullfilled.put(job)

        for _ in range(self.PROCESSES):
            proc: Process = Process(target=self._job_handler)
            self._processes.append(proc)
            proc.start()

        for proc in self._processes:
            proc.join()

        while not self._fulfilled.empty():
            output: Dict = self._fulfilled.get()
            output.update({'project': self.project})
            self._processed.append(output['domain'])
            self.results.append(output)

            if output['greedy']:
                bonus_jobs: List = list()
                observed: List = list()
                for item in output['results']['emails']:
                    found: str = item.split('@')[1]
                    if found in self._processed or found in observed:
                        continue
                    observed.append(found)
                    base: Dict = dict()
                    base['limit'] = output['limit']
                    base['modifier'] = output['modifier']
                    base['engine'] = output['engine']
                    base['greedy'] = False
                    base['domain'] = found
                    bonus_jobs.append(base)

                if len(bonus_jobs) > 0:
                    self.search(bonus_jobs)

        self._log.info("All jobs processed")
        if self.output:
            self._save()

    def get_results(self) -> List:
        """Return results from the search."""
        return self.results
