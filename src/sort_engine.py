import csv
import os

def quick_sort(rows):
	if len(rows) <= 1:
		return rows
	pivot = rows[len(rows) // 2]
	left  = [row for row in rows if row['Time'] < pivot['Time']]
	mid   = [row for row in rows if row['Time'] == pivot['Time']]
	right = [row for row in rows if row['Time'] > pivot['Time']]
	return quick_sort(left) + mid + quick_sort(right)

def Time_Sort(result_file):
	try:
		with open(result_file, mode='r', encoding='utf-8-sig') as f:
			reader = csv.DictReader(f)
			cols = list(reader.fieldnames)
			rows = list(reader)

		sorted_rows = quick_sort(rows)
		for i, row in enumerate(sorted_rows, start=1):
			row['No'] = i
		temp_file = result_file + '.tmp'

		with open(temp_file, mode='w', encoding='utf-8-sig') as f:
			writer = csv.DictWriter(f, fieldnames=cols)
			writer.writeheader()
			writer.writerows(sorted_rows)

		os.replace(temp_file, result_file)
		order = "largest to smallest" if reverse else "smallest to largest"
		print(f"Success: Sorted by Time ({order}).")
	except FileNotFoundError:
		print("Error: The source file was not found.")
	except PermissionError:
		print("Error: File is open in another program. Please close it and try again.")
	except:
		print("Something went wrong, try again later.")
