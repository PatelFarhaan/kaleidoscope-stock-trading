import sys
import click
sys.path.append('../')
from project.models import AdminPortal
from werkzeug.security import generate_password_hash


#<==================================================================================================>
#                                    ADMIN PANEL LOGIN
#<==================================================================================================>
@click.command()
@click.option('--email', '-e', type=str, help="Enter the username of the admin")
@click.option('--password', '-p', type=str, help="Enter the password of the admin")
def add_admin(email, password):
    req = {
        "email": email,
        "password": generate_password_hash(password),
    }
    # noinspection PyArgumentList
    new_admin = AdminPortal(**req)
    new_admin.save()
    print("New admin created")



if __name__ == '__main__':
    add_admin()