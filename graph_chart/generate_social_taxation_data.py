"""
Reminder: Social Taxation split used in this work is the following:

Donator    Receiver     Percentage
90-100 ==>   0-30  ==>    7%
70-90  ==>  30-50  ==>    5%
60-70  ==>  50-60  ==>    3%

"""
def pre_tax_file(file, new_file, year):
	"""Creates new file containg only (year, low, share, cumul) records which 
	corresponds to input year in input file.

	Params:
	file: str, name of tsv file of income taken from WID (World Inequality Datasert).
	year: int, year of the records to keep from input file.
	new_file: str, name of new generated tsv file.
    """
	with open(file, 'r') as f:
		lines = [line.strip() for line in f.readlines() if (line.startswith('year') or line.startswith(str(year)))]
		share_99 = 0.0
		with open(new_file, 'w') as out:
			record = lines[0].split('\t')
			record = record[:2] + record[4:6]
			record = '\t'.join(record)
			out.write(record+'\n')
			for i,line in enumerate(lines[1:]):
				record = line.split('\t')
				record = record[:2] + record[4:6]
				if (float(record[1])>0.98):
					share_99 += float(record[2])
					if i==len(lines)-2:
						record[1] = '0.99'
						record[2] = str(share_99)
						record = '\t'.join(record)
						out.write(record+'\n')
				else:
					record = '\t'.join(record)
					out.write(record+'\n')
	return

def get_percentage(x, list_shares):
	"""Returns percentage of increase/decrease of income after applying 'social taxation' for input x.
	"""
	if x>=0.9:
		percentage = -7
	elif x>=0.7:
		percentage = -5
	elif x>=0.6:
		percentage = -3
	elif x>=0.5:
		percentage = (3*list_shares[3])/list_shares[2]		# i.e. (3*Share_60_70)/Share_50_60)
	elif x>=0.3:
		percentage = (5*list_shares[4])/list_shares[1]		# i.e. (5*Share_70_90)/Share_30_50)
	else: # i.e. x>=0
		percentage = (7*list_shares[5])/list_shares[0]		# i.e. (7*Share_90_100)/Share_0_30)

	return percentage

def get_list_shares(file):
	"""Returns list of share quantity per class of Donator/Receiver in 'Social Taxation'.

	Params:
	file: str, name of file created by 'pre_tax_file' function.
	
	Returns:
	list, [Shares_0_30, Shares_30_50, .... , Shares_90_100] (of size 6 and sum=1)
	"""
	with open(file, 'r') as f:
		lines = [line.strip() for line in f.readlines()]
		list_shares = []
		class_delimiters = [0.3, 0.5, 0.6, 0.7, 0.9, 1.0]
		delimiter_index = 0
		prev_share_qtty = 0.0
		for i, line in enumerate(lines[1:]):
			record = line.split('\t')
			record[1],record[3] = float(record[1]), float(record[3])
			# record[1]=low & record[3]=cumul
			if record[1]>class_delimiters[delimiter_index]:
				curr_share_qtty = float(lines[i-1].split('\t')[3])
				list_shares.append(curr_share_qtty-prev_share_qtty)
				prev_share_qtty = curr_share_qtty
				delimiter_index += 1
			elif i==len(lines)-2:
				list_shares.append(record[3]-prev_share_qtty)
	print("list_shares=", list_shares)

	return list_shares

'''
def update_perc_file(file, new_file):
	"""Creates new file containg (year, low, perc) records from input file, perc
	is the percentage of increase/decrease of income after applying 'social taxation'.

	Params:
	file: str, name of file created by 'pre_tax_file' function.
	new_file: str, name of new generated tsv file.
    """
	list_shares = get_list_shares(file)
	class_number = 1
	with open(file, 'r') as f:
		lines = [line.strip() for line in f.readlines()]
		prev_perc = 0.0
		with open(new_file, 'w') as out:
			out.write('year\tclass\tperc\n')
			for line in lines[1:]:
				record = line.split('\t')[0:3]
				x = float(record[1])
				# percentage of increase/decrease will be stored in record[2] 
				curr_perc = get_percentage(x, list_shares)
				if curr_perc!=prev_perc:
					record[1] = str(class_number)
					record[2] = str(int(curr_perc))
					record = '\t'.join(record)
					out.write(record+'\n')
					prev_perc = curr_perc
					class_number += 1
	return 
'''

def update_perc_file(file, new_file):
	"""Creates new file containg (year, low, perc) records from input file, perc
	is the percentage of increase/decrease of income after applying 'social taxation'.
	Params:
	file: str, name of file created by 'pre_tax_file' function.
	new_file: str, name of new generated tsv file.
    """
	list_shares = get_list_shares(file)
	with open(file, 'r') as f:
		lines = [line.strip() for line in f.readlines()]

		with open(new_file, 'w') as out:
			out.write('year\tlow\tperc\n')
			for line in lines[1:]:
				record = line.split('\t')[0:3]
				x = float(record[1])
				# percentage of increase/decrease will be stored in record[2] 
				record[2] = str(get_percentage(x, list_shares))
				record = '\t'.join(record)
				out.write(record+'\n')
	return 


def get_class_counts(file):
	"""Returns list of records per class of Receiver in 'Social Taxation'.

	Params:
	file: str, name of file created by 'pre_tax_file' function.
	
	Returns:
	list, [Count_records_0_30, Count_records_30_50, Count_records_50_60] 
	"""
	with open(file, 'r') as f:
		lines = [line.strip() for line in f.readlines()]
		list_counts = []
		class_delimiters = [0.3, 0.5, 0.6]
		delimiter_index = 0
		counter= 0
		for line in lines[1:]:
			record = line.split('\t')
			record[1] = float(record[1])
			# record[1]=low
			if record[1]<=class_delimiters[delimiter_index]:
				counter += 1
			else: #record[1]>class_delimiters[delimiter_index]
				list_counts.append(counter)
				counter = 1
				if delimiter_index==2:
					break
				delimiter_index += 1
	print("list_counts= ", list_counts)

	return list_counts

def post_tax_file(file, new_file):
	"""Creates new file containg new (year, low, cumul) values after applying 'social
	taxation' to input file.

	Params:
	file: str, name of file created by 'pre_tax_file' function.
	new_file: str, name of new generated tsv file.
    """
	list_shares = get_list_shares(file)
	list_counts = get_class_counts(file)

	with open(file, 'r') as f:
		lines = [line.strip() for line in f.readlines()]
		cumul = 0.0
		with open(new_file, 'w') as out:
			out.write(lines[0]+'\n')
			for line in lines[1:]:
				record = line.split('\t')
				record[2] = float(record[2])
				x = float(record[1])
				# compute new cumul income after 'Social Taxation'
				if x>0.9:
					record[2] -= 0.07*record[2]
				elif x>0.7:
					record[2] -= 0.05*record[2]
				elif x>0.6:
					record[2] -= 0.03*record[2]
				elif x>0.5:
					record[2] += (0.03*list_shares[3])/list_counts[2]
				elif x>0.3:
					record[2] += (0.05*list_shares[4])/list_counts[1]
				else: # i.e. x>=0
					record[2] += (0.07*list_shares[5])/list_counts[0]
				cumul += record[2]
				record[3] = str(cumul)
				record[2] = str(record[2])
				record = '\t'.join(record)
				out.write(record+'\n')
	return 

def generate_all_files(file, year):
	pre_tax_file_name = file[:-4]+"_"+str(year)+"_pre_tax.tsv"
	post_tax_file_name = file[:-4]+"_"+str(year)+"_post_tax.tsv"
	perc_file_name = file[:-4]+"_"+str(year)+"_update_perc.tsv"
	pre_tax_file(file, pre_tax_file_name, year)
	post_tax_file(pre_tax_file_name, post_tax_file_name)
	update_perc_file(pre_tax_file_name, perc_file_name)

if __name__ == "__main__":
	generate_all_files("social_taxation_data/CN.tsv", 2014)
	generate_all_files("social_taxation_data/US.tsv", 2014)
	generate_all_files("social_taxation_data/FR.tsv", 2014)
	

