from celery import Celery , shared_task

app = Celery(
    "companyrag",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

# Important
import tasks