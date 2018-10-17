from sr import app
from app import db
from flask_script import Manager, Shell
from app.models import User, Store, Ecommerce, Function
from flask_migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(
                app=app, db=db,
                User=User, Store=Store, Ecommerce=Ecommerce, Function=Function
                )

manager.add_command("shell", Shell( make_context=make_shell_context) )
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()
