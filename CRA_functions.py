
def total_income (T4_14, interest, T4RSP_16, Foreign_Income,conversion="No"):
    ''' Total income will sum:
        - Work income : Sum of all T4 box 14
        - Interest earned: Bank should provide
        - RRSP amount withdrawal: T4RSP Box 16
        - Foreign income - Use bank of canada rate of conversion: https://www.bankofcanada.ca/rates/exchange/annual-average-exchange-rates/'''
    
    # Converting foreign income
    Foreign_Income_CAD = (Foreign_Income if conversion=="No" else Foreign_Income * 1.4597 ) # 2023 average rate

    TI = T4_14 + interest + T4RSP_16 + Foreign_Income_CAD
    return (TI)


def net_income (total_income, RRSP_deduction, T4_17):
    ''' Net income will be total income minus:
        - RRSP deduction: Amount added to RRSP
        - QCC contribution: Calculated from T4 box 17 '''
    QCC_max = 631 #Could change in future
    QCC_cont = (T4_17 if T4_17<QCC_max else QCC_max)

    NI = total_income - RRSP_deduction - QCC_cont
    return (NI)


def taxable_income (net_income):
    '''No exception applies to me for variation between
    taxable income and net income so TI = NI'''
    return(net_income)

def federal_tax (taxable_income):
    ''' Calculate federal tax in steps 
    (Didn't add for more than 165,430 $)'''
    ti = taxable_income
    if ti <= 53359:
        ft = ti * 0.15
    elif 53359 < ti <= 106717:
        ft = (ti-53359)*0.205 + 8003.85
    else:
        ft = (ti-106717)*26 + 18942.24
    return (ft)



def tax_credits (taxable_income, T4_17, T4_18, T4_55, total_income,medical_exp, net_income, donations=0):
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

    return (tax_credit)


def net_federal_tax (federal_tax, tax_credit):
    ''' Federal tax minus tax credit - No other benefit applies'''
    NFT = (federal_tax - tax_credit if federal_tax - tax_credit > 0 else 0)
    return(NFT)


def total_calculation (T4_14, T4_17, T4_18, T4_55, T4RSP_16, Foreign_Income, conversion, RRSP_deduction, interest, medical_exp):
    ''' Consolidates the calculation and return list with all main values in return form'''
    total_income_value = total_income (T4_14, interest, T4RSP_16, Foreign_Income, conversion)
    net_income_value = net_income (total_income_value, RRSP_deduction, T4_17)
    taxable_income_value = taxable_income (net_income_value)
    federal_tax_value = federal_tax (taxable_income_value)
    tax_credit_value = tax_credits (taxable_income_value, T4_17, T4_18, T4_55, total_income_value,medical_exp, net_income_value)
    net_federal_tax_value = net_federal_tax (federal_tax_value, tax_credit_value)

    return ([total_income_value, net_income_value, taxable_income_value, federal_tax_value, tax_credit_value, net_federal_tax_value])