# task-runner

Simple parallel task runner with dependency resolution.

## Features
- Dependency-aware execution order
- Configurable concurrency
- Thread-based parallelism

## Usage
```python
from taskrunner import TaskRunner

r = TaskRunner(max_workers=4)
r.add("build", build_fn)
r.add("test", test_fn, deps=["build"])
r.run_all()
```

## License
MIT
