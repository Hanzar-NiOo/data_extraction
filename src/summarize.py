import csv
from collections import Counter

class TransferErrorSummary:
    def __init__(self, result_file):
        self.result_file = result_file
        self.error_counts = Counter()

    def load(self):
        with open(self.result_file, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                error = row.get('Error Message', '').strip()
                if error:
                    self.error_counts[error] += 1
        return self

    def summary(self):
        if not self.error_counts:
            print("No error transactions found.")
            return

        print("\n=== Error Transaction Summary ===\n")
        for error, count in self.error_counts.most_common():
            print(f"  {error} - {count} trns")
        print(f"\n  Total: {sum(self.error_counts.values())} trns")

def	trn_summary(result_file):
	try:
		summary = TransferErrorSummary(result_file).load()
		summary.summary()
	except:
		print("Error in summarize.py")
		print("Something went wrong, try again later.")
