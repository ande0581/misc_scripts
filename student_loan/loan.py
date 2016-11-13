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
    total_payments, total_interest, num_payments = apply_payment(data)
    print_summary(total_interest=total_interest, total_payments=total_payments, num_payments=num_payments)


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
    balance = 74724.34
    total_interest = []
    total_payments = []
    previous_date = datetime.date(2016, 10, 28)  # setting the start date based on current billing cycle
    count = 1

    for payment in data:
        days = days_in_billing_cycle(previous_date, payment.date)
        accrued_interest = daily_interest(balance, days)
        principle_applied = payment.amount - accrued_interest
        balance -= payment.amount - accrued_interest
        total_interest.append(accrued_interest)
        total_payments.append(payment.amount)
        print_payment_details(date=payment.date, payment=payment.amount, interest=accrued_interest,
                              principle=principle_applied, balance=balance)
        count += 1
        previous_date = payment.date

        # Calculate the final payment details
        if balance <= payment.amount:
            final_payment = balance
            final_date = calculate_next_month(payment.date)
            days = days_in_billing_cycle(payment.date, final_date)
            accrued_interest = daily_interest(balance, days)
            principle_applied = final_payment - accrued_interest
            final_balance = balance - final_payment
            total_interest.append(accrued_interest)
            total_payments.append(final_payment)

            print_payment_details(date=final_date, payment=final_payment, interest=accrued_interest,
                                  principle=principle_applied, balance=final_balance)

            return sum(total_payments), sum(total_interest), count


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


def print_payment_details(date, payment, interest, principle, balance):
    print('{}, Payment: {:.2f}, Interest: {:.2f}, Principle: {:.2f}, Balance: ${:.2f}'.
          format(date, payment, interest, principle, balance))


def print_summary(total_payments, total_interest, num_payments):
    print()
    print('Total Payments: ${:.2f}'.format(total_payments))
    print('Total Interest Paid: ${:.2f}'.format(total_interest))
    print('Total Number of Payments: {}'.format(num_payments))


if __name__ == '__main__':
    main()

