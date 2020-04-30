"""
Credit Calculator
https://hyperskill.org/projects/90?goal=391
"""
import argparse
import math as m


class Credit:

    def __init__(self, principal=None, periods=None, payment=None, credit_interest=None):
        self.principal = principal
        self.months = periods
        self.annuity_payment = payment
        self.credit_interest = credit_interest

    @property
    def i(self):
        return self.credit_interest / 12 / 100

    def annuitypayment(self):
        """annuity payment"""
        payment = m.ceil(self.principal * (self.i * (1 + self.i) ** self.months) / ((1 + self.i) ** self.months - 1))
        return f'Your annuity payment = {payment}!\nOverpayment = {payment * self.months - self.principal}'

    def principal_credit(self):
        """Principal of annuity payment"""
        principal_ = m.floor(
            self.annuity_payment * ((1 + self.i) ** self.months - 1) / (self.i * (1 + self.i) ** self.months))
        return f"Your credit principal = {principal_}!\nOverpayment = {self.annuity_payment * self.months - principal_}"

    @property
    def month_payment(self):
        """month of annuity payment"""
        return m.ceil(m.log((self.annuity_payment / (self.annuity_payment - self.principal * self.i)), (self.i + 1)))

    def differ_payment(self):
        payment = ''
        summa_payment = 0
        for k in range(1, self.months + 1):
            month_payment = m.ceil(
                self.principal / self.months + self.i * (self.principal - self.principal * (k - 1) / self.months))
            payment += f'Month {k}: paid out {month_payment}\n'
            summa_payment += month_payment
        return payment + f'\nOverpayment = {summa_payment - self.principal}'

    def month_print(self):
        overpayment = self.month_payment * self.annuity_payment - self.principal
        month = self.month_payment % 12
        year = self.month_payment // 12
        year_flag = 'years' if year > 1 else 'year'
        month_flag = 'months' if month > 1 else 'month'
        if not year == 0 and not month == 0:
            return f'You need {year} {year_flag} and {month} {month_flag} to repay this credit!' \
                   f'\nOverpayment = {overpayment}'
        elif not year == 0 and month == 0:
            return f'You need {year} {year_flag} to repay this credit!\nOverpayment = {overpayment}'
        elif year == 0 and not month == 0:
            return f'You need {month} {month_flag} to repay this credit!\nOverpayment = {overpayment}'


def check(number):
    """проверка что введено число"""
    try:  # пробуем вдруг это добробное
        if float(number) > 0:
            return True
        else:
            return False
    except ValueError:
        return False


def check_list(lst):
    for i in lst:
        if i:
            if not check(i):
                return False
    return True


# def __init__(self, principal=None, periods=None, payment=None, credit_interest=None):
parser = argparse.ArgumentParser()
parser.add_argument("--type")
parser.add_argument("--payment")
parser.add_argument("--principal")
parser.add_argument("--periods")
parser.add_argument("--interest")
args = parser.parse_args()
s = 0
for i in [args.type, args.principal, args.periods, args.payment, args.interest]:
    if i:
        s += 1
credit = Credit()
if args.type not in ("diff", "annuity") or s < 4 or not check_list(
        [args.principal, args.periods, args.payment, args.interest]) or (args.type == "diff" and args.payment):
    print("Incorrect parameters")
else:
    if args.type == "diff":
        credit.principal = float(args.principal)
        credit.months = int(args.periods)
        credit.credit_interest = float(args.interest)
        print(credit.differ_payment())
    if args.type == "annuity":
        if not args.payment:
            credit.principal = float(args.principal)
            credit.months = int(args.periods)
            credit.credit_interest = float(args.interest)
            print(credit.annuitypayment())
        if not args.principal:
            credit.annuity_payment = float(args.payment)
            credit.months = int(args.periods)
            credit.credit_interest = float(args.interest)
            print(credit.principal_credit())
        if not args.periods:
            credit.principal = float(args.principal)
            credit.annuity_payment = float(args.payment)
            credit.credit_interest = float(args.interest)
            print(credit.month_print())
