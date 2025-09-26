
import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from dotenv import load_dotenv

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
        with app.app_context(): # ✅ CORRECT: app_context() is called as a method
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
            search_query = SearchQuery(user_id=user.id)
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
            if result:
                app.logger.debug(f"result :  {result.total_count}") 
                return jsonify({"msg":"No result found"}), 500
            
            responseObj = APIResponse(message="Success", success=True, userId=user.id, data=result)
            return jsonify(responseObj.model_dump())
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"An error occurred during search: {e}")
            return jsonify({"msg": "An error occurred during the search process"}), 500

    
    
    @app.route("/detailInfo",methods=['GET'])
    def detailInfo():
        id = request.args.get("id")  # CORRECTED LINE 
    
        detail:DetailInfo = emuseum.getDetailInfo(id)
        result = DetailInfoList(detail_info_list=[detail])
        responseObj = APIResponse(message="Success",success=True,userId=0,data=result)
        return jsonify(responseObj.model_dump())
    
    
    
    @app.route("/test/detailInfo",methods=['GET'])
    def test_detailInfo():
        id = request.args.get("id")  # CORRECTED LINE

        detail:DetailInfo = emuseum.getDetailInfo(id)
        result = DetailInfoList(detail_info_list=[detail])
        responseObj = APIResponse(message="Success",success=True,userId=0,data=result)
        return jsonify(responseObj.model_dump())
    
    @app.route("/test/userAdd", methods=['GET'])
    def test_user_add():
        """
        Endpoint to add a user to the database.
        """
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