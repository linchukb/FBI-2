import datetime
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy import stats

if __name__ == '__main__':



    month_totals_dict = {}
    totals_by_month_list = []
    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']

    with open('monthlyTotals.csv', newline='') as file:
        for row in file:
            date = row[:7]
            total = row[8:]
            month_totals_dict[date] = total
    file.close()
    month_averages = {}

    def update_totals_by_month():
        global total_by_month_dict
        total_by_month_dict = {'01': 0, '02': 0, '03': 0, '04': 0, '05': 0, '06': 0, '07': 0, '08': 0, '09': 0, '10': 0,
                               '11': 0, '12': 0}
        with open('monthlyTotals.csv') as file:
            for row in file:
                month = row[5:7]
                value = row[8:]
                this_total = total_by_month_dict[month]
                this_total += int(value)
                total_by_month_dict[month] = this_total

    def lookup_record():
        print()
        print('LOOKUP RECORD')
        print('Enter a year-month to lookup in the format yyyy-mm')
        var = input('Enter a year-month: ')
        try:
            record = month_totals_dict[var]
            print('Background Checks:' + record)
        except:
            print('Invalid Entry')
        print()

    def add_record():
        print()
        print('ADD RECORD')
        last = max(month_totals_dict.keys())
        if last[5:] == '12':
            next = str(int(last[:4]) + 1) + '-01'
        else:
            next = last[:5] + months[int(last[5:])]
        print('Year-Month: ' + next)
        try:
            value = int(input('Value: '))
            value = str(value)
            month_totals_dict[next] = value
        except:
            print()
            print('Invalid Entry')

    def update_record():
        print()
        print('UPDATE RECORD')
        print('Select a record to update')
        key = input('Enter a year-month(yyyy-mm): ')
        try:
            value = month_totals_dict[key]
            print('Old record:')
            print(key + ' : ' + value)
            new_value = int(input('Enter new value: '))
            new_value = str(new_value)
            month_totals_dict[key] = new_value
            print('New Record: ')
            print(key + ' : ' + month_totals_dict[key])
        except:
            print('Invalid Entry')
        print()

    def delete_record():
        print()
        print('DELETE RECORD')
        print('Select a record to update')
        key = input('Enter a year-month(yyyy-mm): ')
        try:
            month_totals_dict.pop(key)
            print('Deletion Successful')
        except:
            print('An error occurred')
        print()

    def update_percentage_lists():
        update_totals_by_month()
        global percentages
        percentages = []
        temp = 0
        for month_total in list(total_by_month_dict.values()):
            temp += month_total
        k = 0
        for i in list(total_by_month_dict.values()):
            j = i / temp
            percentage = format((j * 100), '.2f')
            percentages.append(percentage)
            k += 1

    def dashboard():
        print()
        print('Dashboard')
        calculate_month_averages()
        update_percentage_lists()

        # Pie Graph percentages
        # figure 1
        percentages_figure()
        # Bar Graph Averages by Month
        # figure 2
        averages_figure()
        # Line graph
        # figure 3
        totals_line_graph_figure()

        plt.show()

    def totals_line_graph_figure():
        plt.figure(3, facecolor='tan')
        Dates = []
        Checks = []
        for date_i in list(month_totals_dict.keys()):
            temp_date = datetime.date(int(date_i[:4]), int(date_i[5:]), 1)
            Dates.append(temp_date)
        for check_i in list(month_totals_dict.values()):
            temp_check = int(check_i)
            Checks.append(temp_check)
        plt.xticks(rotation=45)
        plt.plot(Dates, Checks)
        plt.title('Date Vs. Checks')
        plt.xlabel('Date')
        plt.ylabel('Checks')
        plt.savefig('line_graph.jpg')

    def averages_figure():
        plt.figure(2, facecolor='tan')
        plt.bar(range(len(month_averages)), list(month_averages.values()), align='center')
        plt.title('Average Background Checks by Month')
        plt.xlabel('Month of Year (e.g., 01 = January)')
        plt.ylabel('Average Background Checks Submitted')
        plt.ticklabel_format(style='plain')
        plt.xticks(range(len(month_averages)), list(month_averages.keys()))
        plt.savefig('averages.jpg')

    def percentages_figure():
        plt.figure(1, facecolor='tan')
        plt.title('Background Checks Percentages by Month')
        explode = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
        centre_circle = plt.Circle((0, 0), 0.70, fc='tan')
        plt.gcf()
        plt.gca().add_artist(centre_circle)
        plt.pie(percentages, labels=month_names, autopct='%.2f%%', pctdistance=0.85, explode=explode)
        plt.savefig('percentages.jpg')

    def records():
        while 1:
            print()
            print('RECORDS MENU')
            print('1 - Lookup Record')
            print('2 - Add Record')
            print('3 - Update Record')
            print('4 - Delete Record')
            print('0 - Back')
            user_input = int(input('Choose an option: '))
            try:
                if user_input == 1:
                    lookup_record()
                elif user_input == 2:
                    add_record()
                elif user_input == 3:
                    update_record()
                elif user_input == 4:
                    delete_record()
                elif user_input == 0:
                    return
                else:
                    print()
                    print('Invalid Entry')
            except:
                print('Invalid Entry')

    def calculate_month_averages():
        for month in months:
            avg_count = 0
            total = 0
            for key, value in month_totals_dict.items():
                record_month = key[5:]
                if month == record_month:
                    avg_count += 1
                    total += int(value)
            average = total / avg_count
            month_averages[month] = average

    def do_linear_regression():
        x = np.array([i for i in range(len(month_totals_dict))]).reshape((-1, 1))
        y = np.array(list(map(int, month_totals_dict.values())))

        model = LinearRegression().fit(x, y)
        return int(model.coef_)


    # Calculating prediction...
    # Predicted background checks next month(2020 - 04): 692511
    # Coefficient of determination: 0.4238052430806428
    # Intercept: 440923.72941176465
    # Slope: [2733.22177117]



    def do_forecast():
        print()
        print('Calculating prediction...')
        calculate_month_averages()
        last = list(month_totals_dict.keys())[-1]

        previous_month = last[5:]
        if int(previous_month) == 12:
            predict_month = '01'
            predict_year = (int(last[:4])) + 1
            predict_year_month = str(predict_year) + '-' + predict_month
        else:
            predict_month = months[int(previous_month)]
            predict_year_month = last[:5] + predict_month

        average = month_averages[predict_month]
        prediction = int(average + do_linear_regression())
        print('Predicted background checks next month(' + predict_year_month + '): ' + str(prediction))







    def main_menu():
        while 1:
            print("\nU.S. Firearms Company\n")
            print("MAIN MENU")
            print("1 - Dashboard")
            print("2 - Forecast next month")
            print("3 - Records")
            print("0 - Exit Application")
            try:
                userInput = int(input("Choose an option: "))
                print()

                if userInput == 1:
                    dashboard()
                elif userInput == 2:
                    do_forecast()
                elif userInput == 3:
                    records()
                elif userInput == 0:
                    return
                else:
                    print("Invalid entry")
            except:
                print('Invalid Entry')

    main_menu()
