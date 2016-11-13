import datetime
import os
import csv
import collections

MonthlyPayment = collections.namedtuple('MonthlyPayment', 'date, amount')

# Total Payments: 101,704.29
# Total Interest: 26,979.95


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
    principle = 74724.34
    total_interest = []
    total_payments = []
    previous_date = datetime.date(2016, 10, 28)  # setting the start date based on current billing cycle
    count = 1

    for payment in data:
        days = days_in_billing_cycle(previous_date, payment.date)
        accrued_interest = daily_interest(principle, days)
        principle -= payment.amount - accrued_interest
        total_interest.append(accrued_interest)
        total_payments.append(payment.amount)
        print('{}, Payment: {}, Interest: {:.2f}, Principle: {:.2f}, Balance: ${:.2f}'.
              format(payment.date, payment.amount, accrued_interest, payment.amount - accrued_interest, principle))

        if principle <= payment.amount:
            final_payment = principle
            final_date = calculate_next_month(payment.date)

            print('{}, Payment: {:.2f}, Interest: {:.2f}, Principle: {:.2f}, Balance: ${:.2f}'.
                   format(final_date, final_payment, accrued_interest, final_payment - accrued_interest, principle - final_payment))

            print()
            print('Total Payments: ${:.2f}'.format(sum(total_payments)))
            print('Total Interest Paid: ${:.2f}'.format(sum(total_interest)))
            print(count)
            break
        count += 1
        previous_date = payment.date


def daily_interest(principle, days):
    total_interest = 0.0
    interest = .075 / 365
    for k in range(days):
        total_interest += principle * interest

    return total_interest


def days_in_billing_cycle(previous_month, current_month):
    return (current_month - previous_month).days


def calculate_next_month(current_date):
    if current_date.month == 12:
        return datetime.date(current_date.year+1, 1, current_date.day)
    else:
        return datetime.date(current_date.year, current_date.month+1, current_date.day)


if __name__ == '__main__':
    main()

