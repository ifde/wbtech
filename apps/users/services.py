from decimal import Decimal

from django.contrib.auth import get_user_model


User = get_user_model()


def top_up_balance(user: User, amount: Decimal) -> User:
    user.balance += amount
    user.save(update_fields=["balance"])
    return user
