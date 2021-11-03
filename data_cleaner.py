import csv

with open('FBI_Test.csv', newline='') as file:
    meta_list = []
    date = ''
    for row in file:
        split_row = row.split(',')  # split_row is array of date, state,total
        current_date = split_row[0]
        temp_total = split_row[2]
        if current_date != date:
            if date != '':
                meta_list.append([date, total])
            date = current_date
            total = 0
        total += int(temp_total)
    meta_list.reverse()

with open('monthlyTotals.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerows(meta_list)
file.close()
csvfile.close()
