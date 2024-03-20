import Foreign_Income_functions as fi

def total_income (T4_14, interest, T4RSP_16, Foreign_Income, printing):
    ''' Total income will sum:
        - Work income : Sum of all T4 box 14
        - Interest earned: Bank should provide
        - RRSP amount withdrawal: T4RSP Box 16
        - Foreign income '''
    # Converting foreign income
    Foreign_Income_CAD = fi.Foreign_Income_Converter(Foreign_Income)
    TI = T4_14 + interest + T4RSP_16 + Foreign_Income_CAD

    #Priting
    if printing == True:
        printer(["Step 2 - Total Income",(10100,T4_14),(10400,Foreign_Income),(12100,interest),(12900,T4RSP_16),("15000 (Total Income)",TI)])
    
    return (TI)





def net_income (total_income, RRSP_deduction, T4_17, printing):
    ''' Net income will be total income minus:
        - RRSP deduction: Amount added to RRSP
        - QCC contribution: Calculated from T4 box 17 '''
    QCC_max = 631 #Could change in future
    QCC_cont = (T4_17 if T4_17<QCC_max else QCC_max)

    NI = total_income - RRSP_deduction - QCC_cont

    if printing == True:
        printer(["Step 3 - Net Income", (20800,RRSP_deduction),(22215, QCC_cont), ("23400 (Net Income)",NI)])
        
    return (NI)


def taxable_income (net_income, printing):
    '''No exception applies to me for variation between
    taxable income and net income so TI = NI'''

    TI = net_income

    if printing == True:
        printer(["Step 4 - Taxable Income", ("23600 (Taxable Income)",TI)])     
    
    return(TI)


def federal_tax (taxable_income, printing):
    ''' Calculate federal tax in steps 
    (Didn't add for more than 165,430 $)'''
    ti = taxable_income
    if ti <= 53359:
        ft = ti * 0.15
    elif 53359 < ti <= 106717:
        ft = (ti-53359)*0.205 + 8003.85
    else:
        ft = (ti-106717)*26 + 18942.24
    
    if printing == True:
        printer(["Step 5 - Federal Tax", ("76 (Federal Tax)", ft)])      
     
    return (ft)


def tax_credits (taxable_income, T4_17, T4_18, T4_55, total_income,medical_exp, net_income, printing, donations=0):
    ''' Initial value = 15000 (Unless income over 165,430$) 
        \nAdded:\n
        - QQC Contribution: Calculated from T4 box 17 - Max 3407$
        - EI Premium: Calculated from T4 box 18 - Max 781$
        - PPIP Premium: Calculated from T4 box 55 - Max 449$
        - Canada Employment amount: Based on total work income - Max 1368$
        - Medical expenses: Enter value - Has to be higher than 3% of net income
        - Donations: If any, complete schedule 9 - Default is 0'''

    tc_ini = (15000 if taxable_income < 165430 else 13520)

    # Line 30800 - QCC Contribution
    QCC_cont = (T4_17 if T4_17 < 3407.4 else 3407.4)

    # Line 31200 - EI premiums (Box 18 T4)
    EI_prem = (T4_18 if T4_18 < 781.05 else 781.05)

    # Line 31205 - PPIP Premiums (Box 55 T4)
    PPIP_prem = (T4_55 if T4_55 < 449.54 else 449.54)

    # Line 31260 - Canada employment amount (based on work income):
    CEA = (total_income if total_income < 1368 else 1368)
    
    # Line 33099 and 33200 - Medical expenses (Box 85 T4 is medical expense)
    total = medical_exp - net_income*0.03
    medical_deduction = (total if total > 0 else 0)

    # Donations (Complete Schedule 9)
    # Setting default value as 0

    tax_credit = (tc_ini + QCC_cont + EI_prem + PPIP_prem + CEA + medical_deduction)*0.15 + donations

    if printing == True:
        printer(["Step 5B - Non Refundable Tax Credits",(30000,tc_ini),(30800,QCC_cont),(31200,EI_prem),(31205,PPIP_prem),(31260,CEA),(33099,medical_exp),(33200,medical_deduction)])
  
    return (tax_credit)



def net_federal_tax (federal_tax, tax_credit, net_income,T4_14, T4RSP_16, Foreign_Income, RRSP_deduction, Foreign_tax, printing):
    ''' Federal tax : \n
    - Tax Credits
    - Federal surtax on foreign income - Line 130'''

    basic_federal_tax =federal_tax - tax_credit
    # Line 130, 132
    if Foreign_Income != 0:
        Surtax_out = fi.federal_surtax_income_outside(net_income,T4_14, T4RSP_16, Foreign_Income, RRSP_deduction, federal_tax, tax_credit)
        Foreign_Tax_Credit = fi.federal_foreign_tax_credit (Foreign_tax,Foreign_Income, net_income, federal_tax, tax_credit )
    else:
        Surtax_out = 0
        Foreign_Tax_Credit = 0

    Quebec_abatement = (federal_tax - tax_credit) * 0.165

    calculation = basic_federal_tax - Foreign_Tax_Credit - Quebec_abatement # + Surtax_out
    
    NFT = (calculation if calculation > 0 else 0)

    if printing == True:
        printer(["Step 5C - Net federal Tax", (40400,federal_tax),(128,tax_credit),(42900,basic_federal_tax),("130: Federal Surtax removed", Surtax_out),(44000,Quebec_abatement), (48200, NFT)])
    return(NFT)






def total_calculation (T4_14, T4_17, T4_18, T4_55, T4RSP_16, Foreign_Income, Foreign_tax, RRSP_deduction, interest, medical_exp, printing=True):
    ''' Consolidates the calculation and return list with all main values in return form'''
    total_income_value = total_income (T4_14, interest, T4RSP_16, Foreign_Income,printing)
    net_income_value = net_income (total_income_value, RRSP_deduction, T4_17,printing)
    taxable_income_value = taxable_income (net_income_value,printing)
    federal_tax_value = federal_tax (taxable_income_value, printing)
    tax_credit_value = tax_credits (taxable_income_value, T4_17, T4_18, T4_55, total_income_value,medical_exp, net_income_value, printing)
    net_federal_tax_value = net_federal_tax (federal_tax_value, tax_credit_value, net_income_value,T4_14, T4RSP_16, Foreign_Income, RRSP_deduction, Foreign_tax, printing)


    

    return ([total_income_value, net_income_value, taxable_income_value, federal_tax_value, tax_credit_value, net_federal_tax_value])



def printer (value):
    ''' Printing values corresponding to each line in following way\n
    ----------------
    Header
    ----------------
    Line x : value
    
    to insert it --> printer(["Header",(x,value)])'''

    print (f"----------------------\n{value[0]}\n----------------------")
    for i in value[1:]:
        print(f'Line {i[0]}: {i[1]}')
        if i == value[-1] : print("")