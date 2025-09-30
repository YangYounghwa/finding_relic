# 보물찾기 (Finding Relic) Backend Server

## Overview

"보물찾기" is a backend server designed to find Korean historical artifacts based on a natural language text description. The service leverages a Large Language Model (LLM) to extract key attributes-such as historical period, material, purpose, name - from the user's text. It then queries the official [e-Museum Korean API](https://www.emuseum.go.kr/main) to find matching artifacts from meseums across Korea.

The project also includes a system for creating and stroing vector embeddings of relic data, laying the groundwork for future semantic search capabilities.


## Features

* **Natural Language Search**: Users can describe a historical artifact in plain text to initiate a search.
* **LLM-Powered Keyword Extraction**: Automatically identifies the relic's name, historical era, material, and purpose from the text using an LLM.
* **Concurrent API Queries**: Executes multiple search queries in parallel against the e-Museum API for faster, more comprehensive results.
* **User Authentication**: Secure endpoints using Google OAuth 2.0 and JWT for user management.
* **Data Persistence**: Uses a PostgreSQL database to manage user data and relic information for embedding.
* **Scheduled Tasks**: A daily scheduler resets user search quotas.
* **Vector Embeddings**: Capable of generating and storing text embeddings for relic descriptions to power semantic search.


## Architecture

The application follows a service-oriented architecture:

1.  **API Layer (`app.py`)**: The main Flask application that defines API endpoints for search (`/searchByText`), detail retrieval (`/detailInfo`), and user authentication (`/google-login`). It handles incoming requests and user session management.
2.  **Search Service (`SearchService.py`)**: This is the core orchestrator. It receives the text query, calls the `LLMService` to parse it into structured data, and then queries the `EmuseumService` with the extracted keywords.
3.  **LLM Service (`LLMServiceObject.py`)**: This service communicates with the OpenAI API. It uses specialized prompts and Pydantic output parsers to reliably extract the relic's name, material, purpose, and historical nation from the raw text.
4.  **e-Museum Service (`EmuseumService.py`)**: This service is responsible for all communication with the external e-Museum API. It builds the requests, parses the resulting XML data into Python objects (DTOs), and handles potential API inconsistencies.
5.  **Code Translation Utility (`MuseumCodeTranslator.py`)**: A helper utility that converts human-readable names (e.g., "조선", "금속") into the specific numeric codes required by the e-Museum API, using local CSV files as mapping tables.
6.  **Database & Embedding Service (`db.py`, `EmbeddingService.py`)**: Manages the PostgreSQL database connection and contains the logic for creating and storing vector embeddings of relic data for future retrieval tasks.


## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd finding_relic
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    The project's dependencies are listed in `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the root directory and add the necessary configuration keys:
    ```.env
    # Flask & JWT
    FLASK_SECRET_KEY='your_flask_secret_key'
    JWT_SECRET_KEY='your_jwt_secret_key'

    # Google OAuth
    GOOGLE_CLIENT_ID='your_google_client_id.apps.googleusercontent.com'

    # OpenAI API
    OPENAI_API_KEY='your_openai_api_key'
    OPENAI_MINI_MODEL=gpt-5-mini
    OPENAI_NANO_MODEL=gpt-5-nano

    # Database URL (e.g., Supabase)
    SUPABASE_URL='your_database_connection_string'

    # e-Museum API Key
    EMUSESUM_URL=https://www.emuseum.go.kr/openapi
    EMUSEUM_KEY_DECODED='your_decoded_emuseum_api_key'

    # Secret key for embedding endpoint
    EMBEDDING_SECRET_KEY='a_secure_random_string'

    # Set to True for testing specific routes
    TEST_MODE=True
    ```




## Running the Application

### Development Server

Use the built-in Flask development server for local testing.

```bash
flask run
```
### Production Server
```bash
gunicorn "relic_app.app:create_app()"
```

### Testing
```bash
pytest --log-cli-level=DEBUG
```

## API Endpoints


All endpoints require a valid JWT Bearer token in the Authorization header, except for the login route.

* POST /google-login:
   * Authenticates a user with a Google ID token.
   * Body: { "id_token": "..." }
   * Returns: An access token for use with other endpoints.

* POST /searchByText:
    * Searches for relics based on a text description.
    * Body: { "data": "A text description of the relic..." }
    * Returns: A JSON object containing a list of BriefInfo for the found relics.

* GET /detailInfo:
    * Retrieves detailed information for a specific relic.
    * Query Parameter: id=<relic_id>
    * Returns: A DetailInfo object with comprehensive data and image URLs for the relic
