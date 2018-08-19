from django.db import models
from django.utils import timezone

from dollarial import settings
from finance.models import Transaction


class ReportTransaction(models.Model):
    comment = models.TextField(verbose_name="Comment")
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Reviewer")
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, verbose_name="Transaction")

    def __str__(self):
        return "Report %s by %s" % (self.transaction_id, self.reviewer_id)


class ReviewHistory(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, verbose_name="Transaction")
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Reviewer")
    status_before = models.CharField(max_length=1, choices=Transaction.TRANSACTION_STATUS,
                                     verbose_name="Status Before")
    time = models.DateTimeField(default=timezone.now, verbose_name="Time")

    ReviewChoices = (
        ('A', 'Accept'),
        ('R', 'Reject'),
        ('S', 'Skip')
    )
    action = models.CharField(max_length=1, choices=ReviewChoices, verbose_name="Action")

    def __str__(self):
        return "%s action %s by %s" % (self.transaction_id, self.action, self.reviewer_id)
