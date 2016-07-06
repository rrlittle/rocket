import csv
with open ('../source_datafiles/coinsExport2016_06_29-13_54_47_0.tsv') as csv_file:
	template_file = csv.DictReader(csv_file,  delimiter='\t')
	template_list = []
	for i, row in enumerate(template_file):
		if i == 0 :
			print(row)
			pass
		else:
			template_list.append(row)


