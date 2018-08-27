from django import db

from admin_panel.models import ReviewHistory


@db.transaction.atomic
def review_transaction(request, transaction):
    if transaction is None:
        return

    if 'accept' in request.POST:
        action = 'A'
    elif 'skip' in request.POST:
        action = 'S'
    elif 'reject' in request.POST:
        action = 'R'
    else:
        raise ValueError('Expected an action')

    review_history_object = ReviewHistory(
        reviewer=request.user,
        transaction=transaction,
        status_before=transaction.status,
        action=action
    )
    review_history_object.save()

    if action == 'A':
        transaction.status = 'A'
    elif action == 'R':
        transaction.status = 'R'
    transaction.save()
