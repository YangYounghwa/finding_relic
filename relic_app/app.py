
import os

from flask import Flask, abort, jsonify, request
from flask_cors import CORS

from dotenv import load_dotenv
from marshmallow import ValidationError

from relic_app.dto.EmuseumDTO import APIResponse, BriefList, DetailInfo

from google.auth.transport import requests
from google.oauth2 import id_token

from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity

from relic_app.services.searchService.SearchService import searcher
from relic_app.services.emuseumService.EmuseumService import emuseum
from relic_app.dto.EmuseumDTO import DetailInfoList


from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from sqlalchemy.orm import relationship
import logging
logger = logging.getLogger(__name__)

load_dotenv()

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "YOUR_WEB_CLIENT_ID.apps.googleusercontent.com")
def create_app():
    """
    Application factory function for the Flask app.
    
    """
    
    app = Flask(__name__)
    from flask.logging import default_handler
    
    # --- Logging Configuration ---
    # When running with Gunicorn, all loggers should use Gunicorn's handlers.
    if __name__ != '__main__':
        gunicorn_logger = logging.getLogger('gunicorn.error')
        
        # Configure the root logger
        root_logger = logging.getLogger()
        root_logger.handlers = gunicorn_logger.handlers
        root_logger.setLevel(gunicorn_logger.level)
        
        # Also configure the Flask app's logger for consistency
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)
        
        app.logger.info("Logging configured to use Gunicorn's logger.")
    else:
        # This is for local development with `flask run`
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        
        # Configure the root logger for development
        root_logger = logging.getLogger()
        root_logger.addHandler(handler)
        root_logger.setLevel(logging.DEBUG)
        
        app.logger.info("Logging configured for development.")

    CORS(app)

    
    
    app.logger.debug(f"{datetime.now()} app started.")

    # --- Configuration and Sanity Check ---
    app.secret_key = os.getenv("FLASK_SECRET_KEY")
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "MYSQL_DATABASE_URI", 
    "mysql+pymysql://root:password@localhost:3306/your_app_db"
)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    if os.getenv("TEST_MODE")=="True":
        app.config['TEST_MODE'] = True
    else:
        app.config['TEST_MODE'] = False
        
        
    app.logger.debug(f"TEST_MODE:{app.config['TEST_MODE']}")
    
    
    # Scheduler setup
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    
    
    app.config['GOOGLE_CLIENT_ID'] = os.environ.get("GOOGLE_CLIENT_ID")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY") 
    jwt = JWTManager(app)
    
    
    db = SQLAlchemy(app)
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        google_id = db.Column(db.String(128), unique=True, nullable=False)
        search_query = relationship("SearchQuery", back_populates="user", uselist=False)

        def __repr__(self):
            return f"<User {self.id}>"

    class SearchQuery(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        queries_left = db.Column(db.Integer, default=10, nullable=False)
        last_reset_timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
        user = relationship("User", back_populates="search_query")
        
        
    
    @scheduler.task('cron', id='reset_daily_searches',hour=0)
    def reset_daily_searches():
        with app.app_context():
            try:
                search_queires = SearchQuery.query.all()
                for sq in search_queires:
                    sq.queries_left = 20
                    sq.last_reset_timestamp = datetime.now(timezone.utc)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                app.logger.error(f"Error resetting daily searches: {e}")

    
    @app.route("/google-login", methods=["POST"])
    def google_login():
        token = request.json.get("id_token")
        if not token:
            return jsonify({"msg": "ID token is missing"}), 400

        try:
            # Verify the Google ID token
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
            # idinfo =0
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

    @app.route("/test/token",methods=["POST"])
    def test_token():
        if app.config['TEST_MODE'] != True:
            abort(404)
        
        
        token = request.json.get('test_token') 
        if token == os.getenv("TEST_TOKEN"):
            user = User.query.filter_by(google_id=token).first()
            if not user:
                user = User(google_id=token)
                db.session.add(user)
                db.session.commit()
            access_token = create_access_token(identity=token)
            return jsonify(access_token=access_token)
            
            
             
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
        
    @app.route("/test/jwtTokenTest",methods=['GET'])
    @jwt_required()
    def jwtTokenTest():
        if app.config['TEST_MODE'] != True:
            abort(404)
        msg = {"msg":"Valid Token"}
        return jsonify(msg)
    
    
    @app.route("/searchByText", methods=['POST'])
    @jwt_required()
    def searchText():
        current_user_google_id = get_jwt_identity()
        user = User.query.filter_by(google_id=current_user_google_id).first()
        
        if not user:
            return jsonify({"msg": "User not found"}), 404

        if not user.search_query:
            search_query = SearchQuery(user_id=user.id,queries_left=20)
            db.session.add(search_query)
            db.session.commit()
            # Refresh the user object to get the new search_query relationship
            db.session.refresh(user)


        if user.search_query.queries_left <= 0:
            return jsonify({"msg": "No search queries left"}), 403
        text = request.json.get("data")
        app.logger.debug(f"text : {text}")
        
        try:
            user.search_query.queries_left -= 1
            db.session.commit()

            result: BriefList = searcher.getItemList(text)
            if not result:
                app.logger.debug(f"result :  {result.totalCount}") 
                return jsonify({"msg":"No result found"}), 500
            
            responseObj = APIResponse(message="Success", success=True, userId=user.id, data=result)
            return jsonify(responseObj.model_dump())
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"An error occurred during search: {e}")
            return jsonify({"msg": "An error occurred during the search process"}), 500

    @app.route("/test/searchByText", methods=['POST'])
    def searchTextTest():

        if app.config['TEST_MODE'] != True:
            abort(404)
        text = request.json.get("data")
        app.logger.debug(f"text : {text}")
        result = None
        
        try:


            result: BriefList = searcher.getItemList(text)
            app.logger.debug(f"result :  {result.totalCount}") 
            
            if not result:
                
                return jsonify({"msg":"No result found"}), 500
            
            responseObj = APIResponse(message="Success", success=True, userId=1, data=result)
            return jsonify(responseObj.model_dump())
        except Exception as e:
            app.logger.error(f"An error occurred during search: {e}")
            return jsonify({"msg": "An error occurred during the search process"}), 500

    
    
    @app.route("/detailInfo",methods=['GET'])
    @jwt_required()
    def detailInfo():
        detail_id = request.args.get("id")
        app.logger.debug(f"/detailInfo called with id : {detail_id}") 
        if not detail_id:
            return jsonify({"msg": "id is missing"}), 400
        
        try:
            detail = emuseum.getDetailInfo(detail_id)
            result = DetailInfoList(detail_info_list=[detail]) if detail else DetailInfoList(detail_info_list=[])
        except ValidationError as ve:
            app.logger.warning(f"Validation error while creating DetailInfo: {ve}")
            return jsonify(APIResponse(
                message="Invalid data from upstream",
                success=False,
                userId=0,
                data=DetailInfoList(detail_info_list=[])
            ).model_dump()), 200
        result = DetailInfoList(detail_info_list=[detail])
        responseObj = APIResponse(message="Success",success=True,userId=0,data=result)
        return jsonify(responseObj.model_dump())
    
    
    
    @app.route("/test/detailInfo",methods=['GET'])
    def test_detailInfo():
        app.logger.debug("test_detailInfo called.")
        if app.config['TEST_MODE'] != True:
            abort(404)
        id = request.args.get("id")  

        detail:DetailInfo = emuseum.getDetailInfo(id)
        result = DetailInfoList(detail_info_list=[detail])
        responseObj = APIResponse(message="Success",success=True,userId=0,data=result)
        return jsonify(responseObj.model_dump())
    
    @app.route("/test/userAdd", methods=['GET'])
    def test_user_add():
        """
        Endpoint to add a user to the database.
        """
        if app.config['TEST_MODE'] != True:
            abort(404)
        google_id = request.args.get("google_id")
        if not google_id:
            # Return a 400 Bad Request if the Google ID is missing
            return jsonify({"msg": "Google ID is missing"}), 400

        user = User.query.filter_by(google_id=google_id).first()

        if user:
            return jsonify({"msg": "User already exists"})
        else:
            try:
                new_user = User(google_id=google_id)
                db.session.add(new_user)
                # FIX: Added parentheses to correctly call the commit method
                db.session.commit()
                return jsonify({"msg": "User added successfully"})
            except ValueError:
                db.session.rollback()
                return jsonify({"msg": "Invalid Google ID"}), 401
            except Exception as e:
                db.session.rollback()
                app.logger.error(f"Error adding user: {e}")
                return jsonify({"msg": "An error occurred while adding the user"}), 500
         
    with app.app_context():
        db.create_all()
    return app