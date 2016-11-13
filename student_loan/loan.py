import datetime
import os
import csv
import collections

MonthlyPayment = collections.namedtuple('MonthlyPayment', 'date, amount')

# Daily: $53893.79
# Monthly: $53881.63
# Yearly: $53750.00
# Start Date 11/28/16


def main():

    filename = get_data_file()
    data = load_file(filename)
    apply_payment(data)


def get_data_file():
    base_folder = os.path.dirname(__file__)
    return os.path.join(base_folder, 'payments.csv')


def load_file(filename):
    payment_schedule = []
    with open(filename, 'r', encoding='utf-8') as fin:
        reader = csv.reader(fin)
        next(reader, None)  # skip the header
        for row in reader:
            start_date = row[0].split('/')
            year = int(start_date[2]) + 2000
            month = int(start_date[0])
            day = int(start_date[1])
            k = MonthlyPayment(date=datetime.date(year, month, day), amount=int(row[1]))
            payment_schedule.append(k)
    return payment_schedule


def apply_payment(data):
    principle = 50000
    previous_date = datetime.date(2016, 10, 28)  # setting the start date based on current billing cycle

    for payment in data:
        days = days_in_billing_cycle(previous_date, payment.date)
        previous_date = payment.date

        principle = daily_interest(principle, days) - payment.amount
        print('{}, Payment: {}, Balance: ${:.2f}'.format(payment.date, payment.amount, principle))
        if principle < 0:
            break


def daily_interest(p, days):
    # Using recursion to get compounded daily
    interest = .075 / 365
    if days == 0:
        return p

    p += (p * interest)

    return daily_interest(p, days - 1)


def days_in_billing_cycle(previous_month, current_month):
    return (current_month - previous_month).days


if __name__ == '__main__':
    main()

