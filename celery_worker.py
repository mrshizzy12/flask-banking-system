from app import celery, create_app, tasks


app = create_app()
app.app_context().push()
