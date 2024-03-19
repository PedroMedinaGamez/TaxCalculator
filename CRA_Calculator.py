import CRA_functions as cf
import csv
import os

# Define the path to the CSV files
path = r'C:\Users\pedro\OneDrive\Desktop\Cursos\Python\Results_of_TaxCalculator'
csv_file_name = 'RRSP_Extraction_no_income.csv'
csv_file_path = os.path.join(path,csv_file_name)
############
#    T4    #
############
T4_14 = 82424.62
T4_17 = 4038.4 #4.8%
T4_18 = 781.05 # 0.94%
T4_55 = 407.18 # 4.9%

############
#   RRSP   #
############
T4RSP_16 = 0  # Money extracted from RRSP
RRSP_deduction = 0 # Money inserted in RRSP

############
#  Others  #
############
interest = 100
medical_exp = 0
Foreign_Income = 0
    # Write the row data to the CSV file




# File extension
#csv_extension = '.csv'

# Check if the first CSV file exists


# Open the CSV file in write mode
with open(csv_file_path, 'w', newline='') as csvfile:
    # Create a CSV writer object
    csv_writer = csv.writer(csvfile)

    # Write header
    csv_writer.writerow(["T4_14", "T4_17", "T4_18", "T4_55", "T4RSP_16", "RRSP_deduction", "interest", "medical_exp","Total_Income", "Net_Income", "Taxable_Income", "Federal_Tax","Tax_Credit", "Net_Federal_Tax"])
   
    #Write row

    # CALCULATIN NO RRSP EXTRACTION
    # for T4_14 in range(0,120000,1000):
    #     T4_17 = T4_14 * 0.048
    #     T4_18 = T4_14 * 0.0094
    #     T4_55 = T4_14 * 0.0048
        
    #     #for T4RSP_16 in range(0,10000,100):

    #     for RRSP_deduction in range(0,10000,100):
    #             input_data = [T4_14, T4_17, T4_18, T4_55, T4RSP_16, RRSP_deduction, interest, medical_exp]
    #             value = cf.total_calculation (T4_14, T4_17, T4_18, T4_55, T4RSP_16, RRSP_deduction, interest, medical_exp)
    #             csv_writer.writerow(input_data + value)


    # CALCULATE RRSP EXTRACTION NO INCOME
    T4_14 = 0
    T4_17 = T4_14 * 0.048
    T4_18 = T4_14 * 0.0094
    T4_55 = T4_14 * 0.0048
    RRSP_deduction = 0

    for T4RSP_16 in range (0,50000,10):
                input_data = [T4_14, T4_17, T4_18, T4_55, T4RSP_16, RRSP_deduction, interest, medical_exp]
                value = cf.total_calculation (T4_14, T4_17, T4_18, T4_55, T4RSP_16, Foreign_Income, RRSP_deduction, interest, medical_exp)
                csv_writer.writerow(input_data + value)  

print(f"Row has been written to the CSV file '{csv_file_path}' successfully.")
