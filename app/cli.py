from flask.cli import with_appcontext
import click
from app import create_app
from app.models import db
from app.routes import schedule_update

app = create_app()

@click.command(name='init_db')
@with_appcontext
def init_db():
    db.create_all()
    click.echo('Initialized the database.')

@click.command(name='start_scheduler')
@with_appcontext
def start_scheduler():
    schedule_update()
    click.echo('Started the scheduler.')

app.cli.add_command(init_db)
app.cli.add_command(start_scheduler)

if __name__ == '__main__':
    app.run()