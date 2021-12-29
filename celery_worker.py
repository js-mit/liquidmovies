from liquid import create_app

app = create_app()
app.app_context().push()

from liquid import celery
