import logging
import connexion
from flask_testing import TestCase


class BaseTestCase(TestCase):
    def create_app(self):
        logging.getLogger("connexion.operation").setLevel("INFO")
        app = connexion.App(__name__, specification_dir="../openapi/")
        app.add_api("vAPI.yaml", pythonic_params=True)
        return app.app
