import datetime
import logging
import os

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from relic_app.dto.EmuseumDTO import APIResponse, BriefList
load_dotenv()

from google.auth.transport import requests
from google.oauth2 import id_token

from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity
import logging
logger = logging.getLogger(__name__)

from relic_app.services.searchService.SearchService import searcher



GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "YOUR_WEB_CLIENT_ID.apps.googleusercontent.com")


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
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "MYSQL_DATABASE_URI", 
    "mysql+pymysql://root:password@localhost:3306/your_app_db"
)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['GOOGLE_CLIENT_ID'] = os.environ.get("GOOGLE_CLIENT_ID")
    db = SQLAlchemy(app)
    
    
    
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        google_id = db.Column(db.String(128), unique=True, nullable=False)

        def __repr__(self):
            return f"<User {self.email}>"



    @app.before_first_request
    def create_tables():
        db.create_all()


    
    @app.route("/google-login", methods=["POST"])
    def google_login():
        token = request.json.get("id_token")
        if not token:
            return jsonify({"msg": "ID token is missing"}), 400

        try:
            # Verify the Google ID token
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
            
            # Extract user info
            google_id = idinfo['sub']
            
            user = User.query.filter_by(google_id=google_id).first()
            if not user:
                user = User(google_id=google_id)
                db.session.add(user)
                db.session.commit()
                
            # Generate your custom JWT
            access_token = create_access_token(identity=google_id)
            return jsonify(access_token=access_token)
        
        except ValueError:
            return jsonify({"msg": "Invalid Google ID token"}), 401
        
        
    # Example of usr info from jwt
    @app.route("/protected", methods=["GET"])
    @jwt_required()
    def protected_route():
        # The JWT identity is our internal user ID, not the Google ID
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if user:
            return jsonify(message=f"Hello, internal user {user.id}!", google_id=user.google_id), 200
        else:
            return jsonify({"msg": "User not found"}), 404
        
    @app.route("/test/searchText",methods=['POST'])
    def test_searchText():
        text = request.json.get("data").get("text")
        result:BriefList = searcher.getItemList(text)
        
        responseObj = APIResponse(message="Success",success=True,userId=0,data=result)
        return jsonify(responseObj.model_dump())
    
    @app.route("/test/detailInfo",methods=['GET'])
    def test_detailInfo():
        id = request.json.get("data").get("id")
        from relic_app.services.emuseumService.EmuseumService import emuseum
        from relic_app.dto.EmuseumDTO import DetailList
        result:DetailList = emuseum.getDetailInfo(id)
        
        

    return app