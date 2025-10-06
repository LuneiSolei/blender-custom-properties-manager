class ReportingMixin:
    """Mixin to add reporting capabilities to any class."""

    def __init__(self):
        self._operator = None

    def set_operator(self, operator):
        """Sets the operator_instance for reporting."""
        self._operator = operator

    def report(self, level, message):
        """Report a message."""
        if self._operator:
            self._operator.report(level, message)
        else:
            # No operator_instance available, print to console instead
            print(f"{level} CPM Report (No operator_instance): {message}")