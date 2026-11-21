# Smart Service Desk
A console-based **Service Request Management System** built in Python, demonstrating a layered (Domain-Driven Design-inspired) architecture, SOLID principles, custom exception handling, and JSON-based persistence with no external dependencies.


## Overview
Smart Service Desk is a command-line application that lets an organization log, track, and resolve employee service requests (e.g. IT tickets, HR queries). It is intentionally built as a **4-layer architecture** — Presentation, Application, Domain, and Infrastructure — so that business rules, storage format, and user interaction are never tangled together in the same file.


## Features
- Create a new service request with a unique ID, employee name, issue description, and priority.
- View all logged service requests in a readable, formatted list.
- Search for a specific request by its ID.
- Resolve an open request (one-way status transition: `OPEN → RESOLVED`).
- All data persists automatically to a local JSON file — requests survive an application restart.
- Specific, friendly error messages for invalid input instead of raw Python tracebacks.


## Design Principles Applied
**Single Responsibility** : Each layer has exactly one reason to change — domain = business rules, infrastructure = storage format, application = workflow, presentation = console I/O 

**Dependency Inversion** : `RequestService` depends only on an injected object exposing `load_all()`/`save_all()` — never on `json` or a file path directly 

**Encapsulation** : `ServiceRequest.status` can only change via `resolve()`; nothing outside the class sets it directly

**Open/Closed** : Swapping storage (e.g. to SQLite) means writing one new repository class — zero changes to domain or application code

**Basic DDD** : Code is organized by business layer (`domain/`, `application/`, `infrastructure/`), not by technical file type


### Run the application
python main.py


## Usage Guide
===== Smart Service Desk =====
1. Create Service Request
2. View All Requests
3. Search Request
4. Resolve Request
5. Exit

==============================

Enter your choice: 1

Enter Request ID: SR101

Enter Employee Name: Gokul Ganesh

Enter Issue: Laptop is not starting

Enter Priority (LOW/MEDIUM/HIGH): HIGH

Service Request created successfully.

Enter your choice: 2
SR101 | Gokul Ganesh | Laptop is not starting | HIGH | OPEN

Enter your choice: 4
Enter Request ID to resolve: SR101
Request SR101 resolved successfully.


## Business Rules
- A Request ID must be unique — duplicates are rejected immediately, before any other field is collected.
- Priority must be one of `LOW`, `MEDIUM`, `HIGH` (case-insensitive input, stored upper-case).
- Status only ever moves one way: `OPEN → RESOLVED`. Resolving an already-resolved request raises an error instead of silently succeeding.


## Exception Handling
- DuplicateRequestError is raised when Request ID already exists and caught in main.py → handle_create()
- RequestNotFoundError is raised when ID not found on search/resolve and caught in main.py → handle_search(), handle_resolve()
- InvalidPriorityError is raised when Priority isn't LOW/MEDIUM/HIGH and caught in main.py → handle_create()
- AlreadyResolvedError is raised when Resolving a request already RESOLVED and caught in main.py → handle_resolve()

All four inherit from a common `ServiceDeskError` base class defined in `domain/exceptions.py`, so callers that don't need per-type handling can catch everything service-related with one `except ServiceDeskError`.


## Data Persistence
Requests are stored as a JSON array in `data/requests.json`, auto-created on first run:
[
    {
        "request_id": "SR101",
        "employee_name": "Gokul Ganesh",
        "issue": "Laptop is not starting",
        "priority": "HIGH",
        "status": "RESOLVED"
    }
]

The file is loaded into memory once at startup and rewritten after every create/resolve operation, so the CLI can be closed and reopened without losing data.


## Running Tests
python -m unittest discover
