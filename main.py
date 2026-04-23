import controller
import sort_engine
# import search_engine

main_file = 'csv_files/main.csv'
file_A = 'csv_files/Input_file_A.csv'
file_B = 'csv_files/Input_file_B.csv'
result_file = 'csv_files/result.csv'

try:
	Assignee = input("Assignee : ")
	Dispute_side = input("Dispute Side : ")

	controller.handle_main(main_file, result_file)
	controller.handle_errMsg_file(file_A, result_file)
	controller.handle_errMsg_file(file_B, result_file)
	controller.add_cols(result_file, Assignee, Dispute_side)
	sorting_loop = True
	while (sorting_loop):
		time_sort = input("Sort by time, Y/n? ")
		if (time_sort == 'Y'):
			sort_type_loop = True
			while (sort_type_loop):
				sort_type = input ("1 for smallest to largest.\n2 for largest to smallest.\nq for back\n> ")
				sort_type_loop = False
				if (sort_type == '1'):
					sort_engine.Time_Sort(result_file, reverse=False)
					break
				elif (sort_type == '2'):
					sort_engine.Time_Sort(result_file, reverse=True)
					break
				elif (sort_type == 'q'):
					break
				else:
					sort_type_loop = True
					print ("Invalid input, try again!")
			sorting_loop = False
			break
		elif (time_sort == 'n'):
			sorting_loop = False
			break
except ValueError as e:
	print(f"Invalid Input: {e}")
except ValueError as e:
	print(f"Something went wrong, try again later.")
