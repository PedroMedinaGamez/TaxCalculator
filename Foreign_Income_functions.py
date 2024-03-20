
def Foreign_Income_Converter (Foreign_Income):
    '''Calculate CAD for EUR income \n
    Use bank of canada rate of conversion: https://www.bankofcanada.ca/rates/exchange/annual-average-exchange-rates/'''
    
    Foreign_Income_CAD = (Foreign_Income * 1.4597 ) # 2023 average rate
    return Foreign_Income_CAD


# LINE 130 - FEDERAL SURTAX ON INCOME EARNED OUTSIDE CANADA (T2203)
def federal_surtax_income_outside (net_income,T4_14, T4RSP_16, Foreign_Income, RRSP_deduction, federal_tax, tax_credit):
    ''' This is the surtax calculation for income obtained out of Canada (T2203):\n
        Asumming the only Canadian income is produced in QC (T4b14, T4RSP)'''
    
    #PART 1
    try:
        Outside_perc = Foreign_Income_Converter(Foreign_Income) / net_income
    except ZeroDivisionError:
        Outside_perc = 0

    #PART 2
    Surtax_out = (federal_tax - tax_credit) * Outside_perc * 0.48

    return(Surtax_out)

# LINE 132 - FEDERAL FOREIGN TAX CREDIT (T2209):

def federal_foreign_tax_credit (Foreign_tax,Foreign_Income, net_income, federal_tax, tax_credit ):
    ''' Use T2209'''
    Foreign_tax_CAD = Foreign_Income_Converter(Foreign_tax)
    calculation = (Foreign_Income_Converter(Foreign_Income) / net_income) * (federal_tax - tax_credit)
    FFTC = (calculation if calculation < Foreign_tax_CAD else Foreign_tax_CAD)
    print(Foreign_tax_CAD)
    print(Foreign_Income_Converter(Foreign_Income) / net_income)
    print(federal_tax - tax_credit)
    print(calculation)
    print(FFTC)
    return FFTC