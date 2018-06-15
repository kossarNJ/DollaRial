from django.shortcuts import render


def transaction_list(request):
    # TODO: read from db
    data = {
        "transactions": [
            {
                "id": "1",
                "transaction_type": "Toefl",
                "amount": "200",
                "currency": "$",
                "owner": "user1",
                "destination": "Toefl Co.",
                "status": "reject"
            },
            {
                "id": "2",
                "transaction_type": "Gaj",
                "amount": "20000000000",
                "currency": "﷼",
                "owner": "user2",
                "destination": "Gaj Co.",
                "status": "unknown"
            },
            {
                "id": "3",
                "transaction_type": "IELTS",
                "amount": "100",
                "currency": "€",
                "owner": "user1",
                "destination": "Soroush Co.",
                "status": "accept"
            },
            {
                "id": "4",
                "transaction_type": "Toefl",
                "amount": "200",
                "currency": "$",
                "owner": "user2",
                "destination": "Toefl Co.",
                "status": "reject"
            },
        ]
    }
    return render(request, 'admin_panel/admin_transaction_list.html', data)


def costumer_list(request):
    # TODO: read from db
    data = {
        "costumers": [
            {
                "id": "1",
                "first_name": "soroush",
                "last_name": "ebadian",
                "account_number": "123456789123",
                "email": "soroushebadian@gmail.com",
                "phone_number": "0989352543617"
            },
            {
                "id": "2",
                "first_name": "soroush2",
                "last_name": "ebadian2",
                "account_number": "1234567891232",
                "email": "soro2ushebadian@gmail.com",
                "phone_number": "0989352523617"
            },
        ]
    }
    return render(request, 'admin_panel/admin_costumer_list.html', data)


def reviewer_list(request):
    # TODO: read from db
    data = {
        "reviewers": [
            {
                "id": "1",
                "username": "soroush",
                "salary": "200000",
            },
            {
                "id": "1",
                "username": "parand",
                "salary": "210000",
            },
            {
                "id": "1",
                "username": "kosar",
                "salary": "100000",
            }
        ]
    }
    return render(request, 'admin_panel/admin_reviewer_list.html', data)


def index(request):
    return render(request, 'admin_panel/admin_index.html')
