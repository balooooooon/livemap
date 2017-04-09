import MySQLdb
from balon import LOG


def connect_db(app):
    """Database connection"""
    LOG.info("Connecting to database: %s@%s", app.config["MYSQL_DATABASE_DB"], app.config["MYSQL_DATABASE_HOST"])
    app.mysql = MySQLdb.connect(host=app.config["MYSQL_DATABASE_HOST"],
                                user=app.config["MYSQL_DATABASE_USER"],
                                passwd=app.config["MYSQL_DATABASE_PASSWORD"],
                                db=app.config["MYSQL_DATABASE_DB"])
    return app.mysql

# def init_db():
#     """Initializes the database."""
#     db = get_db()
#     with app.open_resource('schema.sql', mode='r') as f:
#         db.cursor().executescript(f.read())
#     db.commit()


def get_db(app):
    return app.mysql

#
# @app.cli.command('initdb')
# def initdb_command():
#     """Creates the database tables."""
#     init_db()
#     LOG.info('Initialized the database.')
#
#
# @app.teardown_appcontext
# def close_db(error):
#     """Closes the database again at the end of the request."""
#     if app.mysql:
#         app.mysql.close()
