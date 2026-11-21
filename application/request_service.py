from domain.service_request import ServiceRequest
from domain.exceptions import DuplicateRequestError, RequestNotFoundError

class RequestService:

    def __init__(self, repository):
        self._repository = repository
        self._requests = {}
        self._load_from_repository()

    def _load_from_repository(self):
        for record in self._repository.load_all():
            request = ServiceRequest.from_dict(record)
            self._requests[request.request_id] = request

    def _save_to_repository(self):
        records = [req.to_dict() for req in self._requests.values()]
        self._repository.save_all(records)

    def is_duplicate(self, request_id):
        """Non-raising lookup so the UI can fail fast, BEFORE collecting
        the rest of the form fields."""
        return request_id.strip().upper() in self._requests

    def create_request(self, request_id, employee_name, issue, priority):
        normalized_id = request_id.strip().upper()
        if normalized_id in self._requests:
            raise DuplicateRequestError(f"Request ID '{normalized_id}' already exists.")
        request = ServiceRequest(normalized_id, employee_name, issue, priority)
        self._requests[normalized_id] = request
        self._save_to_repository()
        return request

    def view_requests(self):
        return list(self._requests.values())

    def search_request(self, request_id):
        normalized_id = request_id.strip().upper()
        if normalized_id not in self._requests:
            raise RequestNotFoundError(f"Request ID '{normalized_id}' not found.")
        return self._requests[normalized_id]

    def resolve_request(self, request_id):
        normalized_id = request_id.strip().upper()
        if normalized_id not in self._requests:
            raise RequestNotFoundError(f"Request ID '{normalized_id}' not found.")
        request = self._requests[normalized_id]
        request.resolve()  # raises AlreadyResolvedError if already RESOLVED
        self._save_to_repository()
        return request