import threading, time
from collections import deque

class Task:
    def __init__(self, name, fn, deps=None):
        self.name = name
        self.fn = fn
        self.deps = deps or []
        self.done = False
        self.result = None

class TaskRunner:
    def __init__(self, max_workers=4):
        self.max_workers = max_workers
        self.tasks = {}

    def add(self, name, fn, deps=None):
        self.tasks[name] = Task(name, fn, deps or [])
        return self

    def _can_run(self, task):
        return all(self.tasks[d].done for d in task.deps)

    def run_all(self):
        pending = deque(self.tasks.values())
        active = []
        while pending or active:
            to_start = []
            remaining = deque()
            for t in pending:
                if self._can_run(t) and len(active) < self.max_workers:
                    to_start.append(t)
                else:
                    remaining.append(t)
            pending = remaining
            for t in to_start:
                th = threading.Thread(target=self._exec, args=(t,))
                th.start()
                active.append((t, th))
            active = [(t, th) for t, th in active if th.is_alive()]
            time.sleep(0.05)
        return {n: t.result for n, t in self.tasks.items()}

    def _exec(self, task):
        task.result = task.fn()
        task.done = True
