import csv
import os.path
from bs4 import BeautifulSoup



def parse_htm(file):
    if file:
        with open(file, 'r') as htm_file:
            content = htm_file.read()
        return content


def start_process(htm_file, csv_file, month, day):
    data_in = parse_htm(htm_file)
    bs_object = BeautifulSoup(data_in, 'html.parser')
    parent_table = bs_object.find('table', attrs={'border': 0})

    tables = parent_table.find_all('table')

    csv_file_data = [month, day, station]

    if tables:
        for table in tables:
            if "GPS Specific Tests" in str(table):
                with open(csv_file, 'a', newline='\n') as csvfile:
                    writer = csv.writer(csvfile)

                    # Write the table rows
                    for row_data in table.find_all('tr')[1:]:

                        row = [td.get_text(strip=True) for td in row_data.find_all('td')]
                        if row[0] == 'Cycle Slips:':
                            try:
                                value, threshold = row[2].split(' ')[1], row[2].split(' ')[4]
                                csv_file_data.append(value)
                                csv_file_data.append(threshold)
                                print(f'Cycle Slips [value, threshold]: {value}, {threshold}')
                            except:
                                pass
                        elif row[0] == 'Multipath:':
                            try:
                                mp1, mp2, threshold = row[2].split(' ')[1][:-1], row[2].split(' ')[4][:-1], \
                                    row[2].split(' ')[7]
                                csv_file_data.append(mp1)
                                csv_file_data.append(mp2)
                                csv_file_data.append(threshold)
                                print(f'Multipath [mp1, mp2, threshold]: {mp1}, {mp2}, {threshold}')
                            except:
                                pass
                        elif row[0] == 'Data Completeness:':
                            try:
                                value, threshold = row[2].split(' ')[1], row[2].split(' ')[4]
                                csv_file_data.append(value)
                                csv_file_data.append(threshold)
                                print(f'Data Completeness [value, threshold]: {value}, {threshold}')
                            except:
                                pass
                    writer.writerow(csv_file_data)
    else:
        print('No table was found with that criteria')


def main(station):
    current_dir = os.path.normpath(rf'CORS_stations/{station}')
    trail = current_dir.split('/')[-1]

    months = ['MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER', ]
    for current_month in months:
        month_dir = os.path.join(current_dir, current_month)
        days = sorted(int(d) for d in os.listdir(month_dir))

        current_csv_file = f'CSVs/{station}.csv'
        for day in days:
            day_dir = os.path.join(month_dir, f"{day}")
            
            file = [file for file in os.listdir(day_dir) if file.endswith('.htm')]

            if len(file) != 0:
                current_htm_file = os.path.join(month_dir, os.path.join(f"{day}", f"{file[0]}"))
                print(f"Current htm file: {current_htm_file}")
                start_process(current_htm_file, current_csv_file, current_month, day)
            else:
                csv_file_data = [current_month, day, station, '', '', '', '', '', '']
                with open(current_csv_file, 'a', newline='\n') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(csv_file_data)


if __name__ == '__main__':
    for station in sorted(os.listdir('CORS_stations')):
        main(station)
