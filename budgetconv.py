import csv
import re

def is_header_row(line): # Returns True if the input line is determined to be a header
    if 'Period' and 'Account' and 'Debit' in line:
            return True
        
def is_main_info_row(line):
    month = r'\w\w\w-\d\d'
    account =  r'\d-\d\d-\d\d\d\d\d-\d\d\d\d-\d\d\d\d-\d\d\d\d\d\d\d\d\d'
    match = re.search(month and account, line)
    if match:
        return True
    
def line_as_list(l):
    info_list = [l[3:9],
                 l[13:44],
                 l[44:59],
                 l[59:75],
                 l[76:99],
                 l[100:113],
                 l[114:130],
                 l[143:]]

    stripped_list = [i.strip() for i in info_list]

    stripped_list[2] = convert_to_float(stripped_list[2])
    stripped_list[3] = convert_to_float(stripped_list[3])
   
    return stripped_list

def convert_to_float(num):
    n = num.replace(',', '')
    try:
        float_n = float(n)
        return float_n
    except ValueError:
        return n

def processed_line(l):
    global header_written
    if header_written == False and is_header_row(l):
        header_written = True
        return line_as_list(l)
    elif is_main_info_row(line):
        return line_as_list(l)

def write_to_csv(l, output_file):
    with open(output_file, 'w') as outputFile:
        wr = csv.writer(outputFile, dialect='excel')
        wr.writerows(l)

def generateOutputName(inputFile):
    fullName = inputFile
    noExt = inputFile[:inputFile.index('.')]
    ext = fullName[inputFile.index('.'):]
    return noExt + '.csv'
    

      
def main(input_file, output_file):
    main_list = []
    header_written = False
    with open(input_file, 'r') as input_file_obj:
        for line in input_file_obj:
            if (is_header_row(line) and header_written == False) or is_main_info_row(line):
                main_list.append(line_as_list(line))
                if is_header_row(line):
                    header_written = True
    write_to_csv(main_list, output_file)

##### Main stuff starts here

print('''
-------------------------------------------------
| Convert Budget .TXT files to CSV Spreadsheets |
| Press Ctrl + C to quit at any time            |
|                                               |
| **Only works on the 'with PO' budgets**       |
-------------------------------------------------

''')

while True:
    inputFile = input('''Drag & drop budget .txt file below, then press Enter\n>> ''')
    inputFile = inputFile.replace('\\','')
    if inputFile[-1] == ' ':
            inputFile = inputFile[:-1]
    main(inputFile, generateOutputName(inputFile))

    print('''

Success!!
You'll find it in the same directory as the original .TXT file.

Need to do another?
''')
                    
                    
                
            



                        
