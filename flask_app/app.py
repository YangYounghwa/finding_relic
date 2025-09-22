import datetime
import logging
import os

from flask import Flask
from flask_cors import CORS

from dotenv import load_dotenv
load_dotenv()

def create_app():
    """
    Application factory function for the Flask app.
    
    """
    
    app = Flask(__name__)
    from flask.logging import default_handler
    
    # Logging added
    app.logger.removeHandler(default_handler)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)
    # app.logger.setLevel(logging.DEBUG)

    CORS(app)

    
    
    app.logger.debug(f"{datetime.now()} app started.")

    # --- Configuration and Sanity Check ---
    app.secret_key = os.getenv("FLASK_SECRET_KEY")




    @app.route("/user",methods=['GET'])
    def getUserId():
        return 


    return app