class LeaveType:
    def __init__(self, leave_id, name, limit):
        self.leave_id = leave_id
        self.name = name
        self.limit = limit  # None for unlimited (unpaid)


class LeaveRequest:
    def __init__(self, leave_type, days_requested, status):
        self.leave_type = leave_type
        self.days_requested = days_requested
        self.status = status  # "Approved" or "Rejected"


class LeaveBalance:
    def __init__(self, leave_type, used=0):
        self.leave_type = leave_type
        self.used = used

    def get_balance(self):
        if self.leave_type.limit is None:
            return "Unlimited"
        return self.leave_type.limit - self.used


class Employee:
    def __init__(self, emp_id, name):
        self.emp_id = emp_id
        self.name = name
        self.leave_balances = {}  # {leave_type_id: LeaveBalance}
        self.leave_requests = []

    def add_leave_type(self, leave_type, used=0):
        self.leave_balances[leave_type.leave_id] = LeaveBalance(leave_type, used)

    # checking for wherther he is eligiblr or not...!
    def is_eligible(self, leave_type_id, days_requested):
        leave_balance = self.leave_balances.get(leave_type_id)
        if not leave_balance:
            return False

        if leave_balance.leave_type.limit is None:
            return True  # Unlimited

        return leave_balance.get_balance() >= days_requested

    # Applying for a leave...!
    def apply_leave(self, leave_type_id, days_requested):
        leave_balance = self.leave_balances.get(leave_type_id)
        if not leave_balance:
            print("Invalid leave type.")
            return None

        if self.is_eligible(leave_type_id, days_requested):
            leave_balance.used += days_requested
            request = LeaveRequest(leave_balance.leave_type, days_requested, "Approved")
            print(f"Leave approved for {days_requested} days of {leave_balance.leave_type.name}.")
        else:
            request = LeaveRequest(leave_balance.leave_type, days_requested, "Rejected")
            print(f"Leave request rejected due to insufficient balance.")

        self.leave_requests.append(request)
        return request

    def show_summary(self):
        print(f"Leave Summary for {self.name}:")
        for lb in self.leave_balances.values():
            balance = lb.get_balance()
            print(f"  {lb.leave_type.name}: Used={lb.used}, Balance={balance}")

        print("\nLeave Requests:")
        for req in self.leave_requests:
            print(f"  {req.leave_type.name}: {req.days_requested} days - {req.status}")


# objects created 
# Define leave types
sick_leave = LeaveType(1,"Sick Leave", 10)
casual_leave = LeaveType(2, "Casual Leave", 8)
unpaid_leave = LeaveType(3, "Unpaid Leave", None)


# create an employee
emp = Employee(101,"Sai kumar")

# Add leave types to employee
emp.add_leave_type(sick_leave,used=2)
emp.add_leave_type(casual_leave, used=3)
emp.add_leave_type(unpaid_leave)


# Try applying for different leaves
emp.apply_leave(1, 5)   # Sick leave - should be approved
emp.apply_leave(2, 5)   # Casual leave - should be rejected
emp.apply_leave(3, 20)  # Unpaid leave - should be approved
# emp.apply_leave(1,10)

emp.show_summary()