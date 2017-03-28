import os
import unittest

import MySQLdb
from flask_sqlalchemy import SQLAlchemy

from balon import app


class BalonTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config.TestingConfig')

        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        app.mysql = MySQLdb.connect(app.config["MYSQL_DATABASE_HOST"],
                                    app.config["MYSQL_DATABASE_USER"],
                                    app.config["MYSQL_DATABASE_PASSWORD"],
                                    app.config["MYSQL_DATABASE_DB"])

        # print(app.config["MYSQL_DATABASE_DB"])

        app.db = SQLAlchemy(app)

        # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()

        # db.create_all()
        # Initialize MySQL DB from .sql files ???

    def tearDown(self):
        app.mysql.cursor().execute("TRUNCATE flight")
        app.mysql.close()


if __name__ == '__main__':
    unittest.main()
