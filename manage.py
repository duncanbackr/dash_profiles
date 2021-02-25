from flask.cli import FlaskGroup

from app import create_app

cli = FlaskGroup(create_app=create_app)


@cli.command("hello")
def hello():
    print("World!")


if __name__ == '__main__':
    cli()
