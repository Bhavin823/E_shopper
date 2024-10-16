from django.db import models

# Create your models here.
class RazorpayOrder(models.Model):
    order_id = models.CharField(max_length=255, primary_key=True)
    amount = models.IntegerField()
    currency = models.CharField(max_length=10)
    status = models.CharField(max_length=50)
    attempts = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order_id}-{self.amount}-{self.status}-{self.created_at}"
    
class RazorpayPayment(models.Model):
    payment_id = models.CharField(max_length=255, primary_key=True)
    amount = models.IntegerField()
    status = models.CharField(max_length=50)
    order = models.ForeignKey(RazorpayOrder, on_delete=models.CASCADE, related_name='payments')
    method = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    error_reason = models.CharField(max_length=255, null=True, blank=True)
    error_code = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.payment_id}-{self.order}-{self.amount}-{self.status}-{self.method}-{self.created_at}"