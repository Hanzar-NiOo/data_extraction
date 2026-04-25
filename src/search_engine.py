import csv
import os

class TransferRecord:
    def __init__(self, no, transfer_id, date, time, error_message, assignee, dispute_side):
        self.no             = no
        self.transfer_id    = transfer_id
        self.date           = date
        self.time           = time
        self.error_message  = error_message
        self.assignee       = assignee
        self.dispute_side   = dispute_side

    def print_details(self):
        print(f"No             : {self.no}")
        print(f"Transfer ID    : {self.transfer_id}")
        print(f"Date           : {self.date}")
        print(f"Time           : {self.time}")
        print(f"Error Message  : {self.error_message}")
        print(f"Assignee       : {self.assignee}")
        print(f"Dispute Side   : {self.dispute_side}")

def binary_search(rows, target_id):
    left, right = 0, len(rows) - 1
    while left <= right:
        mid = (left + right) // 2
        mid_id = int(rows[mid]['Transfer_ID'])
        if mid_id == target_id:
            row = rows[mid]
            record = TransferRecord(
                no            = row.get('No', ''),
                transfer_id   = row.get('Transfer_ID', ''),
                date          = row.get('Date', ''),
                time          = row.get('Time', ''),
                error_message = row.get('Error Message', ''),
                assignee      = row.get('Assignee', ''),
                dispute_side  = row.get('Dispute Side', ''),
            )
            return record
        elif mid_id < target_id:
            left = mid + 1
        else:
            right = mid - 1
    return None

def search_transfer_id(result_file):
    try:
        with open(result_file, mode='r', newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            rows = sorted(list(reader), key=lambda r: int(r['Transfer_ID']))
        while True:
            target_input = input("\nEnter Transfer ID to search (or 'q' to quit): ").strip()
            if target_input.lower() == 'q':
                break
            try:
                target_id = int(target_input)
            except ValueError:
                print("Invalid input. Please enter a numeric Transfer ID.")
                continue
            record = binary_search(rows, target_id)
            if record:
                print("\n--- Transfer Record Found ---")
                record.print_details()
            else:
                print(f"Transfer ID '{target_id}' not found.")
    except FileNotFoundError:
        print(f"Error: '{result_file}' was not found.")
    except KeyError:
        print("Error: 'Transfer_ID' column not found. Check your CSV headers.")
