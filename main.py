from infrastructure.file_repository import FileRepository
from application.request_service import RequestService
from domain.exceptions import (
    DuplicateRequestError,
    RequestNotFoundError,
    InvalidPriorityError,
    AlreadyResolvedError,
)

MENU = """
===== Smart Service Desk =====
1. Create Service Request
2. View All Requests
3. Search Request
4. Resolve Request
5. Exit
==============================
"""


def handle_create(service):
    request_id = input("Enter Request ID: ").strip()

    if service.is_duplicate(request_id):
        print(f"Error: Request ID '{request_id.upper()}' already exists.")
        return

    employee_name = input("Enter Employee Name: ").strip()
    issue = input("Enter Issue: ").strip()
    priority = input("Enter Priority (LOW/MEDIUM/HIGH): ").strip()

    try:
        service.create_request(request_id, employee_name, issue, priority)
        print("Service Request created successfully.")
    except DuplicateRequestError as e:
        print(f"Error: {e}")
    except InvalidPriorityError as e:
        print(f"Error: {e}")

def handle_view(service):
    requests = service.view_requests()
    if not requests:
        print("No service requests found.")
        return
    for request in requests:
        print(request)

def handle_search(service):
    request_id = input("Enter Request ID to search: ").strip()
    try:
        print(service.search_request(request_id))
    except RequestNotFoundError as e:
        print(f"Error: {e}")

def handle_resolve(service):
    request_id = input("Enter Request ID to resolve: ").strip()
    try:
        service.resolve_request(request_id)
        print(f"Request {request_id.upper()} resolved successfully.")
    except RequestNotFoundError as e:
        print(f"Error: {e}")
    except AlreadyResolvedError as e:
        print(f"Error: {e}")

def main():
    repository = FileRepository()
    service = RequestService(repository)

    while True:
        print(MENU)
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            handle_create(service)
        elif choice == "2":
            handle_view(service)
        elif choice == "3":
            handle_search(service)
        elif choice == "4":
            handle_resolve(service)
        elif choice == "5":
            print("Exiting Smart Service Desk System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")

if __name__ == "__main__":
    main()