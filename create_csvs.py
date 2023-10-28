import csv
import os

cors = os.listdir('./CORS_stations')
os.mkdir('CSVs') if not os.path.exists('CSVs') else None

header_rows = [
    ('', '', '', '', '', 'Multipath', '', '', '', ''),
    ('', '', 'Station', 'Cycle slip', '', 'mp1', 'mp2', 'threshold=0.5', 'Data Completeness=95%', ''),
    ('Month', 'Day', 'BAND', 'value', 'threshold', 'value', 'value', 'rmk', '%obs', 'threshold'),
]

for station in cors:
    if not os.path.isfile(f'CSVs/{station}.csv'):
        with open(f'CSVs/{station}.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            writer.writerows(header_rows)
