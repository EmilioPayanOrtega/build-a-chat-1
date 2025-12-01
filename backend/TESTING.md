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
-   **`test_socket_events.py`**: Verifies Real-time Chat functionality.
    -   **Connection**: Ensures clients can connect.
    -   **Room Joining**: Verifies that only authorized users (Session Owner or Chatbot Creator) can join a chat session.
    -   **Messaging**: Checks that messages are persisted to the database and broadcasted to the correct room.
-   **`test_ai_integration.py`**: Mocks the Google Gemini API to verify that the backend correctly constructs prompts and handles AI responses.

### How to Run Unit Tests:
```bash
cd backend
python run_tests.py
```
*This runs all tests using `pytest`.*

---

## 2. End-to-End Verification (`scripts/verify_full_flow.py`)

This script is the ultimate "proof of work". It simulates a complete interaction between a **Creator** and a **User**, covering the entire lifecycle of the application.

### What it Simulates:
1.  **Registration & Auth**:
    -   Registers a "Creator" (Bob).
    -   Registers a "User" (Alice).
    -   Logs them in and verifies Session/Token handling.
2.  **Chatbot Creation**:
    -   Creator builds a chatbot with a nested JSON tree (Tech Support -> Hardware/Software).
    -   Verifies the tree is correctly parsed and saved.
3.  **Search & Discovery**:
    -   User searches for the chatbot by title.
4.  **AI Interaction**:
    -   User asks the AI a question about a specific node.
    -   Verifies the backend constructs the context-aware prompt and returns the (mocked) AI response.
5.  **Real-time Human Support (2-Party Chat)**:
    -   **Session Creation**: User initiates a support request via API.
    -   **Simultaneous Connection**: The script spins up **two separate clients** (User and Creator).
    -   **Room Joining**: Both join the Socket.IO room.
    -   **Message Delivery**: User sends "Hello Creator!".
    -   **Verification**: The script **asserts** that the Creator's client received the exact message via the WebSocket channel.

### Why this guarantees functionality:
Unlike unit tests which mock parts of the system, this script runs against the **actual application factory**, using a real (in-memory) database and the actual Socket.IO message queue. It proves that:
-   The API and Database talk correctly.
-   Authentication protects endpoints.
-   Socket.IO rooms are correctly isolated.
-   Messages are actually delivered in real-time between different users.

### How to Run E2E Verification:
```bash
cd backend
python scripts/verify_full_flow.py
```
*Expected Output: `=== Verification Complete ===` with exit code 0.*

---

## Summary of Confidence

We are confident the backend works because:
1.  **Coverage**: Every major feature (Auth, CRUD, AI, Chat) has both unit tests and E2E verification.
2.  **Realism**: The E2E script mimics actual browser behavior (cookies, socket connections).
3.  **Security**: Tests explicitly check for Unauthorized access (401) and forbidden room joining.
