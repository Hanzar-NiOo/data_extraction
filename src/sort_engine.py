import csv
import os

def quick_sort(rows, reverse=False):
	if len(rows) <= 1:
		return rows
	pivot = rows[len(rows) // 2]
	left  = [row for row in rows if row['Time'] < pivot['Time']]
	mid   = [row for row in rows if row['Time'] == pivot['Time']]
	right = [row for row in rows if row['Time'] > pivot['Time']]
	if reverse:
		return quick_sort(right, reverse) + mid + quick_sort(left, reverse)
	else:
		return quick_sort(left, reverse) + mid + quick_sort(right, reverse)

def Time_Sort(result_file, reverse=False):
	try:
		with open(result_file, mode='r', encoding='utf-8-sig') as f:
			reader = csv.DictReader(f)
			cols = list(reader.fieldnames)
			rows = list(reader)

		sorted_rows = quick_sort(rows, reverse)
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
		print(f"Something went wrong, try again later.")
