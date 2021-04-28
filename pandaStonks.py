import pandas as pd

#-------------------------------------------------------------------------------
# Problem - If I had $1000 to retroactively invest, what basket of 5 tickers
#           should I have purchased?
#-------------------------------------------------------------------------------

# data constants
INVEST_SPEND = 1000 # US Dollars $

# formatting constants
OUTPUT_WIDTH = 87
LOADING_WIDTH = OUTPUT_WIDTH - 1 # for loading rows after the first row
SUB_SECTION_WIDTH = 25
LOADING_SYMBOL = '.'
NAME_FORMAT = '{: <45}'
PERCENT_FORMAT = ' {:>7.2f} %'
DOLLAR_FORMAT = '  $ {:<7.2f}'
TITLE_FORMAT = '{: ^' + str(OUTPUT_WIDTH) + '}'
COLUMN_DIVIDER = '  |'
INDEX_DIVIDER = ')  '
BEST_LABEL = 'Best:'
WORST_LABEL = 'Worst:'
SECTION_DIVIDER = '=' * OUTPUT_WIDTH
SUB_SECTION_DIVIDER = '-' * SUB_SECTION_WIDTH

print()
print(' reading top100.json ...')
top100df = pd.read_json('top100.json')

# rename 'name' to 'ticker' to join with companies.csv later
top100df = top100df.rename(columns = {'Name' : 'ticker'})

print(' creating top100.csv ...')
top100df.to_csv('top100.csv', index = False)

print(' reading companies.csv ...')
companiesDf = pd.read_csv('companies.csv')

# only keep most recent company name
companiesDf = companiesDf[companiesDf['name change effective date'].isna()]

print(' creating top100withCompanies.csv ...')
# join top100 and companies on 'ticker'
# use left join to retain all data from top100 (companies.csv is incomplete)
top100wCompaniesDf = top100df.merge(companiesDf, how = 'left', on = 'ticker')

# ouptut the data
top100wCompaniesDf.to_csv('top100withCompanies.csv', index = False)

# validate number of companies
#print('number of companies: ',len(pd.unique(top100wCompaniesDf['ticker'])))

loadingString = ' analyzing data '
print(loadingString, end = '', flush = True)

roiDollar = {}
roiPercent = {}
tickerToName = {}

bestDollarDayInfo = {}
bestDollarDayInfo['value'] = 0;
worstDollarDayInfo = {}
worstDollarDayInfo['value'] = 0;

bestPercentDayInfo = {}
bestPercentDayInfo['value'] = 0;
worstPercentDayInfo = {}
worstPercentDayInfo['value'] = 0;

tickers = pd.unique(top100wCompaniesDf['ticker'])
count = 1
firstLoadRow = True
for ticker in tickers :
    print(LOADING_SYMBOL, end = '', flush = True)
    # the first row has loadingSting at the start, so it has fewer spots
    # for LOADING_SYMBOL
    if firstLoadRow and (count % (OUTPUT_WIDTH - len(loadingString))) == 0:
        print()
        print(' ', end = '', flush = True)
        firstLoadRow = False
    elif count > LOADING_WIDTH and count % LOADING_WIDTH == 0:
        print(OUTPUT_WIDTH - 1)
        print(' ', end = '', flush = True)
    count += 1

    tickerData = top100wCompaniesDf[top100wCompaniesDf['ticker'] == ticker]

    firstDateData = {}
    lastDateData = {}
    dates = tickerData['date']
    firstDate = str(dates.iloc[0]).split(' ', 1)[0]
    lastDate = str(dates.iloc[len(dates) - 1]).split(' ', 1)[0]

    for date in dates:
        dateData = tickerData[tickerData['date'] == date]
        open = float(dateData['open'].iloc[0])
        close = float(dateData['close'].iloc[0])
        dollarDiff = close - open
        percentDiff = dollarDiff / open

        if bestDollarDayInfo['value'] < dollarDiff:
            bestDollarDayInfo['value'] = dollarDiff
            bestDollarDayInfo['ticker'] = ticker
            bestDollarDayInfo['date'] = date

        if worstDollarDayInfo['value'] > dollarDiff:
            worstDollarDayInfo['value'] = dollarDiff
            worstDollarDayInfo['ticker'] = ticker
            worstDollarDayInfo['date'] = date

        if bestPercentDayInfo['value'] < percentDiff:
            bestPercentDayInfo['value'] = percentDiff
            bestPercentDayInfo['ticker'] = ticker
            bestPercentDayInfo['date'] = date

        if worstPercentDayInfo['value'] > percentDiff:
            worstPercentDayInfo['value'] = percentDiff
            worstPercentDayInfo['ticker'] = ticker
            worstPercentDayInfo['date'] = date

        dateString = str(date).split(' ', 1)[0]
        if dateString == firstDate:
            firstDateData = dateData
        elif dateString == lastDate:
            lastDateData = dateData

    companyName = str(firstDateData['company name'].iloc[0])
    firstPrice = float(firstDateData['open'].iloc[0])
    lastPrice = float(lastDateData['close'].iloc[0])
    roiDollarData = lastPrice - firstPrice

    # if company name is missing, use ticker instead
    tickerToName[ticker] = companyName if companyName != 'nan' else ticker
    roiDollar[ticker] = roiDollarData
    roiPercent[ticker] = roiDollarData / firstPrice

print()
print()

#-------------------------------------------------------------------------------
# 1. Visually show ROI of the selected basket
#-------------------------------------------------------------------------------

print(SECTION_DIVIDER)
print(TITLE_FORMAT.format('ROI of Chosen Stocks'))
print(SECTION_DIVIDER)
print()

sortedByPercent = sorted(roiPercent, key = roiPercent.get, reverse = True)
topFiveByPercent = sortedByPercent[:5]

dollarsPerStock = INVEST_SPEND / 5

print('Top 5 Picks:')
print('    ', NAME_FORMAT.format(''), ' Investment', COLUMN_DIVIDER,
'    Close  ', COLUMN_DIVIDER, '   Profit', sep='')
print()

count = 1
totalProfit = 0
totalClose = 0
for ticker in topFiveByPercent:
    profit = dollarsPerStock * roiPercent[ticker]
    totalProfit += profit
    close = dollarsPerStock + profit
    totalClose += close

    print(count, INDEX_DIVIDER, NAME_FORMAT.format(tickerToName[ticker]),
    DOLLAR_FORMAT.format(dollarsPerStock), COLUMN_DIVIDER,
    DOLLAR_FORMAT.format(close), COLUMN_DIVIDER, DOLLAR_FORMAT.format(profit),
    sep='')

    count += 1

print()
print('    ', NAME_FORMAT.format('Total'), DOLLAR_FORMAT.format(INVEST_SPEND),
COLUMN_DIVIDER, DOLLAR_FORMAT.format(totalClose), COLUMN_DIVIDER,
DOLLAR_FORMAT.format(totalProfit), sep='')
print()

roiString = 'ROI' + PERCENT_FORMAT.format((totalProfit / INVEST_SPEND) * 100)
print(TITLE_FORMAT.format(roiString))

print()
print()

#-------------------------------------------------------------------------------
# 2. Which tickers performed best/worst by dollar value and percent in the
#    time period?
#-------------------------------------------------------------------------------

print(SECTION_DIVIDER)
print(TITLE_FORMAT.format('Ticker Performance'))
print(SECTION_DIVIDER)
print()

print(TITLE_FORMAT.format(SUB_SECTION_DIVIDER))
print(TITLE_FORMAT.format('By Dollar value'))
print(TITLE_FORMAT.format(SUB_SECTION_DIVIDER))
print()

sortedByDollar = sorted(roiDollar, key = roiDollar.get, reverse = True)

print(BEST_LABEL)
topFiveByDollar = sortedByDollar[:5]
count = 1
for ticker in topFiveByDollar:
    print(count, INDEX_DIVIDER, NAME_FORMAT.format(tickerToName[ticker]),
    DOLLAR_FORMAT.format(roiDollar[ticker]), '  |',
    PERCENT_FORMAT.format(roiPercent[ticker] * 100), sep='')
    count += 1
print()

print(WORST_LABEL)
bottomFiveByDollar = sortedByDollar[-5:]
count = 1
for ticker in reversed(bottomFiveByDollar):
    print(count, INDEX_DIVIDER, NAME_FORMAT.format(tickerToName[ticker]),
    DOLLAR_FORMAT.format(roiDollar[ticker]), COLUMN_DIVIDER,
    PERCENT_FORMAT.format(roiPercent[ticker] * 100), sep='')
    count += 1
print()

print(TITLE_FORMAT.format(SUB_SECTION_DIVIDER))
print(TITLE_FORMAT.format('By Percent'))
print(TITLE_FORMAT.format(SUB_SECTION_DIVIDER))
print()

print(BEST_LABEL)
count = 1
for ticker in topFiveByPercent:
    print(count, INDEX_DIVIDER, NAME_FORMAT.format(tickerToName[ticker]),
    PERCENT_FORMAT.format(roiPercent[ticker] * 100), COLUMN_DIVIDER,
    DOLLAR_FORMAT.format(roiDollar[ticker]), sep='')
    count += 1
print()

print(WORST_LABEL)
bottomFiveByPercent = sortedByPercent[-5:]
count = 1
for ticker in reversed(bottomFiveByPercent):
    print(count, INDEX_DIVIDER, NAME_FORMAT.format(tickerToName[ticker]),
    PERCENT_FORMAT.format(roiPercent[ticker] * 100), COLUMN_DIVIDER,
    DOLLAR_FORMAT.format(roiDollar[ticker]), sep='')
    count += 1
print()

print()

#-------------------------------------------------------------------------------
# 3. Which ticker had the single best/worst gain/loss by dollar value and
#    percent in a day?
#-------------------------------------------------------------------------------

print(SECTION_DIVIDER)
print(TITLE_FORMAT.format('Ticker best/worst Single-Day Gain/Loss'))
print(SECTION_DIVIDER)
print()

print(TITLE_FORMAT.format(SUB_SECTION_DIVIDER))
print(TITLE_FORMAT.format('By Dollar value'))
print(TITLE_FORMAT.format(SUB_SECTION_DIVIDER))

print(BEST_LABEL)
print('Company      ', COLUMN_DIVIDER, ' ',
NAME_FORMAT.format(tickerToName[bestDollarDayInfo['ticker']]))

bestDollarDayDate = str(bestDollarDayInfo['date']).split(' ', 1)[0]
print('Date         ', COLUMN_DIVIDER, ' ', bestDollarDayDate)
print('Dollar delta ', COLUMN_DIVIDER,
DOLLAR_FORMAT.format(bestDollarDayInfo['value']))
print()

print(WORST_LABEL)
print('Company      ', COLUMN_DIVIDER, ' ',
NAME_FORMAT.format(tickerToName[worstDollarDayInfo['ticker']]))

worstDollarDayDate = str(worstDollarDayInfo['date']).split(' ', 1)[0]
print('Date         ', COLUMN_DIVIDER, ' ', worstDollarDayDate)
print('Dollar delta ', COLUMN_DIVIDER,
DOLLAR_FORMAT.format(worstDollarDayInfo['value']))
print()

print(TITLE_FORMAT.format(SUB_SECTION_DIVIDER))
print(TITLE_FORMAT.format('By Percent'))
print(TITLE_FORMAT.format(SUB_SECTION_DIVIDER))

print(BEST_LABEL)
print('Company      ', COLUMN_DIVIDER, '  ',
NAME_FORMAT.format(tickerToName[bestPercentDayInfo['ticker']]))

bestPercentDayDate = str(bestPercentDayInfo['date']).split(' ', 1)[0]
print('Date         ', COLUMN_DIVIDER, '  ', bestPercentDayDate)
print('Dollar delta ', COLUMN_DIVIDER,
PERCENT_FORMAT.format(bestPercentDayInfo['value'] * 100))
print()

print(WORST_LABEL)
print('Company      ', COLUMN_DIVIDER, '  ',
NAME_FORMAT.format(tickerToName[worstPercentDayInfo['ticker']]))

worstPercentDayDate = str(worstPercentDayInfo['date']).split(' ', 1)[0]
print('Date         ', COLUMN_DIVIDER, '  ', worstPercentDayDate)
print('Dollar delta ', COLUMN_DIVIDER,
PERCENT_FORMAT.format(worstPercentDayInfo['value'] * 100))
print()

print()

print(SECTION_DIVIDER)
print()
