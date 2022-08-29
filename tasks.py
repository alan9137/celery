import os
import time
from celery import Celery, Task

celery_app = Celery(__name__,
                    broker=os.environ.get(
                        "BROKER_REDIS_URL", "redis://localhost:6379/0"),
                    backend=os.environ.get(
                        "BACKEND_REDIS_URL", "redis://localhost:6379/0"))


class Name(Task):
    def run(self, name: str):
        n = 10
        for i in range(0, n, 1):
            self.update_state(state="PROGRESS", meta={"done": i, "total": n})
            time.sleep(1.5)
        if name is not None:
            return f"Hello {name}"
        else:
            return "Hello World"


name = celery_app.register_task(Name())


@ celery_app.task(bind=True)
def add(self, x: int, y: int):
    n = 10
    for i in range(0, n, 1):
        self.update_state(state="PROGRESS", meta={"done": i, "total": n})
        time.sleep(1)
    return x + y
