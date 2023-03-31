class REQUEST():
    def __init__(self, task_id=None, customer_id=None, support_id=None, type_of_task=None, task_data=None, description=None, status=None, error_message=None, created_date=None, approval_date=None, completed_date=None):
        self.task_id = task_id
        self.customer_id = customer_id
        self.support_id = support_id
        self.type_of_task = type_of_task
        self.task_data = task_data
        self.status = status
        self.created_date = created_date
        self.description = description
        self.error_message = error_message
        self.approval_date = approval_date
        self.completed_date = completed_date
