import csv
import os
import re
from datetime import datetime

def handle_main(input_file, output_file, assignee, dispute_side):
	try:
		with open(input_file, mode='r', encoding='utf-8-sig') as infile:
			reader = csv.DictReader(infile)
			if reader.fieldnames and reader.fieldnames[0].startswith('sep='):
				reader.fieldnames = next(csv.reader([next(infile)]))
			with open(output_file, mode='w', encoding='utf-8-sig') as outfile:
				cols = ['No', 'Transfer_ID', 'Date', 'Time', 'Error Message', 'Assignee', 'Dispute Side']
				writer = csv.DictWriter(outfile, fieldnames=cols)
				writer.writeheader()
				num = 1
				for row in reader:
					dt = datetime.strptime(row['Time'], '%Y-%m-%d %H:%M:%S')
					writer.writerow({
						'No': num,
						'Transfer_ID': row['Transfer_ID'],
						'Date': dt.strftime('%#m/%d/%Y'),
						'Time': dt.strftime('%H:%M:%S'),
						'Error Message': '',
						'Assignee': assignee,
						'Dispute Side': dispute_side,
					})
					num += 1
		print(f"Success: Cleaned data saved to {output_file}")
	except FileNotFoundError:
		print("Error: The source file was not found.")
	except ValueError as e:
		print(f"Error parsing date/time: {e}")

def handle_errMsg_file(input_file, result_file):
	def extract_fields(log_text):
		transfer_id = (re.search(r'transferId=([A-Z0-9]+)', log_text) or type('', (), {'group': lambda s, x: None})()).group(1)
		err_msg = (
			(re.search(r'"([^"]+)"$', log_text.strip()) or re.search(r'"exec_msg"\s*:\s*"([^"]+)"', log_text))
		)
		msg = err_msg.group(1) if err_msg else None
		if msg in skip_messages:
			return transfer_id, None
		return transfer_id, msg

	skip_messages = {'5100:Payee or Payee FSP rejected the request.'}
	try:
		with open(input_file, mode='r', encoding='utf-8-sig') as f:
			reader = csv.DictReader(f)
			if reader.fieldnames[0].startswith('sep='):
				reader.fieldnames = next(csv.reader([next(f)]))
			extracted = {}
			for row in reader:
				tid, msg = extract_fields(row['Line'])
				if tid and msg:
					extracted[tid] = msg

		with open(result_file, mode='r', encoding='utf-8-sig') as f:
			reader = csv.DictReader(f)
			cols = list(reader.fieldnames)
			rows = [{**row, 'Error Message': extracted.get(row['Transfer_ID'], row.get('Error Message', ''))} for row in reader]

		temp_file = result_file + '.tmp'
		with open(temp_file, mode='w', encoding='utf-8-sig') as f:
			writer = csv.DictWriter(f, fieldnames=cols)
			writer.writeheader()
			writer.writerows(rows)
		os.replace(temp_file, result_file)

		print(f"Success: Error messages mapped into {result_file}.")
	except FileNotFoundError:
		print("Error: The source file was not found.")
	except PermissionError:
		print("Error: File is open in another program. Please close it and try again.")
