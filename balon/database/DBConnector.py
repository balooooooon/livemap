import MySQLdb
from balon import LOG


def connect_db(app):
    """
    Initializes database connection
    @param app: Flask application object
    @type app: Flask
    @return: MySQL Connection object
    @rtype: MySQLdb.Connection
    """
    LOG.info("Connecting to database: %s@%s", app.config["MYSQL_DATABASE_DB"], app.config["MYSQL_DATABASE_HOST"])
    try:
        app.mysql = MySQLdb.connect(host=app.config["MYSQL_DATABASE_HOST"],
                                    user=app.config["MYSQL_DATABASE_USER"],
                                    passwd=app.config["MYSQL_DATABASE_PASSWORD"],
                                    db=app.config["MYSQL_DATABASE_DB"])
    except MySQLdb.OperationalError as e:
        LOG.error(e)
        LOG.critical("Can't connect to MySQL database")
        return None

    return app.mysql


# def init_db():
#     """Initializes the database."""
#     db = get_db()
#     with app.open_resource('schema.sql', mode='r') as f:
#         db.cursor().executescript(f.read())
#     db.commit()


def get_db(app):
    """
    Returns MySQL Connection object
    @param app: Flask application object
    @return: MySQLdb.Connection
    """
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
