# Transfer Reconciliation Tool

A command-line tool for processing and reconciling transfer transaction records from multiple CSV sources, mapping error messages, sorting by time, and summarizing error transactions.

---

## Project Structure

```
project/
├── main.py           # Entry point
├── controller.py     # File handling and data processing
├── sort_engine.py    # Sorting logic
├── summarize.py      # Error summary report
└── csv_files/
    ├── main.csv          # Main transaction input file
    ├── Input_file_A.csv  # Error log source A
    ├── Input_file_B.csv  # Error log source B
    └── result.csv        # Output result file
```

---

## How It Works

1. **Load main transactions** — Reads `main.csv`, cleans and formats date/time fields, and writes them to `result.csv` with assignee and dispute side metadata.
2. **Map error messages** — Reads error logs from `Input_file_A.csv` and `Input_file_B.csv`, extracts `Transfer_ID` and error messages using regex, and maps them into `result.csv`.
3. **Sort by time** — Sorts all records in `result.csv` by the `Time` column using quicksort, then re-numbers the `No` column.
4. **Summarize errors** *(optional)* — Displays a grouped count of all error messages found in the result file.

---

## Usage

```bash
python main.py
```

You will be prompted to enter:

```
Assignee     : <your name>
Dispute Side : <dispute side>
```

Then optionally:

```
Do you want summary for error transaction, Y/n?
```

### Example Output

```
Success: Cleaned data saved to result.csv
Success: Error messages from Input_file_A mapped into result.csv.
Success: Error messages from Input_file_B mapped into result.csv.
Success: Sorted by Time (Smallest to Largest).

Do you want summary for error transaction, Y/n? Y

***** Error Transaction Summary *****

Socket Timeout   - 10 trns
UNKNOWN MISSION  - 7 trns
========================================
Total            - 17 trns
```

---

## Input File Formats

### `main.csv`
Must contain the following columns:

| Column      | Format                  |
|-------------|-------------------------|
| Transfer_ID | Alphanumeric (e.g. TXN001234) |
| Time        | `YYYY-MM-DD HH:MM:SS`   |

### `Input_file_A.csv` / `Input_file_B.csv`
Must contain a `Line` column with log text entries that include:
- `transferId=<ID>` — to identify the transaction
- An error message either as a trailing quoted string or under `"exec_msg"` key

---

## Output File

### `result.csv`

| Column        | Description                        |
|---------------|------------------------------------|
| No            | Row number (re-indexed after sort) |
| Transfer_ID   | Transaction identifier             |
| Date          | Formatted as `M/DD/YYYY`          |
| Time          | Formatted as `HH:MM:SS`           |
| Error Message | Mapped from input log files        |
| Assignee      | Entered at runtime                 |
| Dispute Side  | Entered at runtime                 |

---

## Modules

### `controller.py`
| Function | Description |
|---|---|
| `handle_main(input_file, output_file, assignee, dispute_side)` | Reads main CSV, formats records, writes to result file |
| `handle_errMsg_file(input_file, result_file)` | Extracts error messages from log CSV and maps them to result file |

### `sort_engine.py`
| Function | Description |
|---|---|
| `quick_sort(rows)` | Recursively sorts rows by `Time` field |
| `Time_Sort(result_file)` | Reads result file, sorts it, re-numbers rows, and saves |

### `summarize.py`
| Class / Function | Description |
|---|---|
| `TransferErrorSummary` | OOP class that loads and counts error messages using `Counter` |
| `TransferErrorSummary.load()` | Reads result file and tallies errors; returns `self` for chaining |
| `TransferErrorSummary.summary()` | Prints grouped error counts sorted by frequency |
| `trn_summary(result_file)` | Wrapper function called from `main.py` |

---

## Error Handling

All modules handle these common errors gracefully:

- `FileNotFoundError` — source file not found
- `PermissionError` — file is open in another program
- `ValueError` — invalid date/time format in main file
- General exceptions — caught with a fallback message

---

## Requirements

- Python 3.x
- No external libraries required (uses `csv`, `os`, `re`, `datetime`, `collections` from the standard library)
