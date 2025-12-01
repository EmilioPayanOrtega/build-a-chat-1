# Build a chat Backend

The backend for **Build a chat**, built with Flask, Socket.IO, and MySQL.

## Setup

### Prerequisites
- Python 3.12+
- MySQL (or Docker to run the container)

### Installation

1.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Configuration:**
    Create a `.env` file in the `backend/` directory with the following variables:
    ```env
    SECRET_KEY=your_secret_key
    DB_HOST=127.0.0.1
    DB_USER=root
    DB_PASSWORD=your_password
    DB_NAME=chatbotdb
    DB_PORT=3306
    GEMINI_API_KEY=your_gemini_api_key
    ```

### Database Setup
You can run a MySQL container using the provided script:
```bash
./scripts/docker_script.sh
```
This will start a MySQL container named `mysql-container` and create the `chatbotdb` database.

## Running the Application

To start the development server:
```bash
python run.py
```
The server will start on `http://127.0.0.1:5001`.

## Testing

To run the unit test suite:
```bash
python run_tests.py --all
```
This runs both the unit tests (using `pytest`) and the End-to-End verification script.

For more options (e.g. running only unit tests or only E2E), see [TESTING.md](TESTING.md).

## API Endpoints

### Authentication
- `POST /auth/login`
- `POST /auth/register`
- `POST /auth/logout`

### Chatbots
- `GET /chatbots?search=xyz` (Public search)
- `GET /chatbots/<id>` (Fetch tree data - returns nested JSON)
- `POST /chatbots` (Create new bot - accepts nested JSON tree)
- `PUT /chatbots/<id>` (Update tree)
- `POST /chatbots/<id>/ask-ai` (Gemini interaction)
- `POST /chat-sessions` (Create a new support chat session)

### Socket.IO Events
- `connect`: Authenticate user.
- `join_chat`: Join a specific session room.
- `chat_message`: Send/receive messages.
- `resolve_chat`: Mark chat as resolved.

## Project Structure

- **`app/`**: Application package.
    - `__init__.py`: App factory and configuration.
    - `models.py`: Database models (SQLAlchemy).
    - `routes.py`: HTTP route handlers (Controller).
    - `services.py`: Business logic layer.
    - `events.py`: Socket.IO event handlers.
- **`scripts/`**: Utility scripts.
    - `docker_script.sh`: MySQL Docker setup.
    - `test_endpoints.py`: Manual endpoint verification.
    - `verify_env.py`: Environment verification.
    - `verify_models.py`: Model verification.
- **`tests/`**: Unit tests.
    - `conftest.py`: Pytest fixtures.
    - `test_routes.py`: API tests.
    - `test_services.py`: Logic tests.
- **`run.py`**: Entry point.
- **`run_tests.py`**: Test runner script.
