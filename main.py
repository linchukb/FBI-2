import csv
import datetime
import matplotlib.pyplot as plt

if __name__ == '__main__':

    monthTotalsDict = {}
    totals_by_month_list = []
    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']

    with open('monthlyTotals.csv', newline='') as file:
        for row in file:
            date = row[:7]
            total = row[8:]
            monthTotalsDict[date] = total
    file.close()
    monthAverages = {}

    def update_totals_by_month():
        global total_by_month_dict
        total_by_month_dict = {'01': 0, '02': 0, '03': 0, '04': 0, '05': 0, '06': 0, '07': 0, '08': 0, '09': 0, '10': 0,
                               '11': 0, '12': 0}
        with open('monthlyTotals.csv') as file:
            for row in file:
                month = row[5:7]
                value = row[8:]
                thisTotal = total_by_month_dict[month]
                thisTotal += int(value)
                total_by_month_dict[month] = thisTotal

    def lookupRecord():
        print()
        print('LOOKUP RECORD')
        print('Enter a year-month to lookup in the format yyyy-mm')
        var = input('Enter a year-month: ')
        try:
            record = monthTotalsDict[var]
            print('Background Checks:' + record)
        except:
            print('Invalid Entry')
        print()

    def addRecord():
        print()
        print('ADD RECORD')
        last = max(monthTotalsDict.keys())
        if last[5:] == '12':
            next = str(int(last[:4]) + 1) + '-01'
        else:
            next = last[:5] + months[int(last[5:])]
        print('Year-Month: ' + next)
        try:
            value = int(input('Value: '))
            value = str(value)
            monthTotalsDict[next] = value
        except:
            print()
            print('Invalid Entry')

    def updateRecord():
        print()
        print('UPDATE RECORD')
        print('Select a record to update')
        key = input('Enter a year-month(yyyy-mm): ')
        try:
            value = monthTotalsDict[key]
            print('Old record:')
            print(key + ' : ' + value)
            newValue = int(input('Enter new value: '))
            newValue = str(newValue)
            monthTotalsDict[key] = newValue
            print('New Record: ')
            print(key + ' : ' + monthTotalsDict[key])
        except:
            print('Invalid Entry')
        print()

    def deleteRecord():
        print()
        print('DELETE RECORD')
        print('Select a record to update')
        key = input('Enter a year-month(yyyy-mm): ')
        try:
            monthTotalsDict.pop(key)
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

    def dashBoard():
        print()
        print('Dashboard')
        calculateMonthAverages()
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
        for date_i in list(monthTotalsDict.keys()):
            temp_date = datetime.date(int(date_i[:4]), int(date_i[5:]), 1)
            Dates.append(temp_date)
        for check_i in list(monthTotalsDict.values()):
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
        plt.bar(range(len(monthAverages)), list(monthAverages.values()), align='center')
        plt.title('Average Background Checks by Month')
        plt.xlabel('Month of Year (e.g., 01 = January)')
        plt.ylabel('Average Background Checks Submitted')
        plt.ticklabel_format(style='plain')
        plt.xticks(range(len(monthAverages)), list(monthAverages.keys()))
        plt.savefig('averages.jpg')

    def percentages_figure():
        plt.figure(1, facecolor='tan')
        explode = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
        centre_circle = plt.Circle((0, 0), 0.70, fc='tan')
        plt.gcf()
        plt.gca().add_artist(centre_circle)
        plt.pie(percentages, labels=monthNames, autopct='%.2f%%', pctdistance=0.85, explode=explode)
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
            userInput = int(input('Choose an option: '))
            try:
                if userInput == 1:
                    lookupRecord()
                elif userInput == 2:
                    addRecord()
                elif userInput == 3:
                    updateRecord()
                elif userInput == 4:
                    deleteRecord()
                elif userInput == 0:
                    return
                else:
                    print()
                    print('Invalid Entry')
            except:
                print('Invalid Entry')

    def calculateMonthAverages():
        for month in months:
            avgCount = 0
            total = 0
            for key, value in monthTotalsDict.items():
                recordMonth = key[5:]
                if month == recordMonth:
                    avgCount += 1
                    total += int(value)
            average = total / avgCount
            monthAverages[month] = average

    def forecastingMenu():
        print()
        print('Calculating prediction...')
        calculateMonthAverages()
        last = list(monthTotalsDict.keys())[-1]

        previous_month = last[5:]
        if int(previous_month) == 12:
            predict_month = '01'
            predict_year = (int(last[:4])) + 1
            predict_year_month = str(predict_year) + '-' + predict_month
        else:
            predict_month = months[int(previous_month)]
            predict_year_month = last[:5] + predict_month

        average = monthAverages[predict_month]
        trend = 0.0015651785
        prediction = int(average + (average * trend))
        print('Predicted background checks next month(' + predict_year_month + '): ' + str(prediction))

    def mainMenu():
        while 1:
            print("\nU.S. Firearm Company\n")
            print("MAIN MENU")
            print("1 - Dashboard")
            print("2 - Forecast next month")
            print("3 - Records")
            print("0 - Exit Application")
            try:
                userInput = int(input("Choose an option: "))
                print()

                if userInput == 1:
                    dashBoard()
                elif userInput == 2:
                    forecastingMenu()
                elif userInput == 3:
                    records()
                elif userInput == 0:
                    return
                else:
                    print("Invalid entry")
            except:
                print('Invalid Entry')

    mainMenu()
