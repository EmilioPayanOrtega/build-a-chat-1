# Backend Testing Strategy

This document outlines the testing strategy for the **Build a chat** backend, ensuring reliability, security, and functional correctness.

## Overview

We employ a two-tiered testing approach:
1.  **Unit Tests**: Isolated tests for individual components (Routes, Services, Models, Socket Events).
2.  **End-to-End (E2E) Verification**: A comprehensive script that simulates a real-world user journey across the entire system.

---

## 1. Unit Tests (`tests/`)

Located in the `tests/` directory, these tests use `pytest` and an in-memory SQLite database to verify logic in isolation.

### Key Test Suites:
-   **`test_routes.py`**: Verifies REST API endpoints (Registration, Login, Chatbot CRUD). Checks for correct HTTP status codes (200, 201, 400, 401) and JSON response structures.
-   **`test_services.py`**: Tests core business logic (User authentication, Chatbot tree validation, Database operations).
-   **`test_ai_integration.py`**: Mocks the Google Gemini API to verify that the backend correctly constructs prompts and handles AI responses.

> **Note**: Real-time Chat (Socket.IO) functionality is verified via the **End-to-End Verification** script, as unit testing WebSockets with in-memory databases can be unreliable.

### How to Run Tests:

We provide a unified test runner `run_tests.py`.

**Run Unit Tests (Default):**
```bash
python run_tests.py
# OR
python run_tests.py --unit
```

**Run End-to-End Verification:**
```bash
python run_tests.py --e2e
```

**Run All Tests:**
```bash
python run_tests.py --all
```

---

## Summary of Confidence

We are confident the backend works because:
1.  **Coverage**: Every major feature (Auth, CRUD, AI, Chat) has both unit tests and E2E verification.
2.  **Realism**: The E2E script mimics actual browser behavior (cookies, socket connections).
3.  **Security**: Tests explicitly check for Unauthorized access (401) and forbidden room joining.
