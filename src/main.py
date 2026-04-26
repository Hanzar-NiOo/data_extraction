import controller
import sort_engine
# import search_engine
import summarize

main_file = '../csv_files/main.csv'
file_A = '../csv_files/Input_file_A.csv'
file_B = '../csv_files/Input_file_B.csv'
result_file = '../csv_files/result.csv'

try:
	Assignee = input("Assignee : ")
	Dispute_side = input("Dispute Side : ")

	controller.handle_main(main_file, result_file, Assignee, Dispute_side)
	controller.handle_errMsg_file(file_A, result_file)
	controller.handle_errMsg_file(file_B, result_file)

	sort_engine.Time_Sort(result_file)
	summarize.trn_summary(result_file)

	# while True:
	# 	find_trn = input("Find with transfer Id, Y/n? ")
	# 	if (find_trn == 'Y'):
	# 		transfer_id = input("Enter Transfer ID to search (or 'q' to quit): ").strip()
	# 		if transfer_id.lower() == 'q':
	# 			break
	# 		search_engine.search_transfer_id(result_file, transfer_id)
	# 	elif (find_trn == 'n'):
	# 		break
	# 	else:
	# 		print ("Invalid input, try again!")

except ValueError as e:
	print(f"Invalid Input: {e}")
except:
	print("Something went wrong, try again later.")
