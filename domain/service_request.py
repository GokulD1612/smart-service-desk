from domain.exceptions import InvalidPriorityError, AlreadyResolvedError

VALID_PRIORITIES = ("LOW", "MEDIUM", "HIGH")

class ServiceRequest:

    def __init__(self, request_id, employee_name, issue, priority, status="OPEN"):
        priority = priority.strip().upper()
        if priority not in VALID_PRIORITIES:
            raise InvalidPriorityError(
                f"Priority must be one of {VALID_PRIORITIES}, got '{priority}'."
            )
        self.request_id = request_id.strip().upper()
        self.employee_name = employee_name.strip()
        self.issue = issue.strip()
        self.priority = priority
        self.status = status.strip().upper()

    def resolve(self):
        if self.status == "RESOLVED":
            raise AlreadyResolvedError(
                f"Request '{self.request_id}' is already RESOLVED."
            )
        self.status = "RESOLVED"

    def to_dict(self):
        return {
            "request_id": self.request_id,
            "employee_name": self.employee_name,
            "issue": self.issue,
            "priority": self.priority,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data):
        return ServiceRequest(
            request_id=data["request_id"],
            employee_name=data["employee_name"],
            issue=data["issue"],
            priority=data["priority"],
            status=data.get("status", "OPEN"),
        )

    def __str__(self):
        return (f"{self.request_id} | {self.employee_name} | {self.issue} | "
                f"{self.priority} | {self.status}")