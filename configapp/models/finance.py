from django.db import models
from .auth_user import BaseModel
from .auth_student import Student
from .model_group import GroupStudent

class Invoice(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='invoices')
    group = models.ForeignKey(GroupStudent, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    issued_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(blank=True, null=True)
    paid = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    external_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self): return f"Invoice #{self.id} - {self.student.full_name} - {self.amount}"

class Payment(BaseModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50, blank=True, null=True)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self): return f"Payment {self.amount} for invoice {self.invoice_id}"
