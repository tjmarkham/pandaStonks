# pandaStonks :panda_face: :chart_with_upwards_trend: 
Investment Data Analysis w/ Pandas

## Objective
Given data from `top100.json` and `companies.csv`, determine what five stocks to retroactively invest $1,000 in.

Show:
- ROI of stock selection
- best/worst companies by dollar value and percent (full time range)
- best/worst gain/loss by dollar value and percent in a day

## Dependencies
- Python 3
- pandas - https://pandas.pydata.org
```
pip install pandas
```
- matplotlib - https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html
```
pip install matplotlib
```

## Run Instructions
`pandaStonks.py` must be in the same folder as `top100.json` and `companies.csv`.

Run from the command line:
```
$ python3 pandaStonks.py
```

## Example output
Files:
- `top100.csv`
- `top100withCompanies.csv`
- `roi_over_time.png`

Command line:
```
$ python3 pandaStonks.py

 reading top100.json ...
 creating top100.csv ...
 reading companies.csv ...
 creating top100withCompanies.csv ...
 analyzing data .......................................................................
 .............................

=======================================================================================
                                 ROI of Chosen Stocks
=======================================================================================

Top 5 Picks:
                                                  Investment  |    Close    |   Profit

1)  Align Technology Inc.                          $ 200.00   |  $ 460.55   |  $ 260.55
2)  Vertex Pharmaceuticals Incorporated            $ 200.00   |  $ 402.69   |  $ 202.69
3)  Wynn Resorts Limited                           $ 200.00   |  $ 386.67   |  $ 186.67
4)  The Boeing Company                             $ 200.00   |  $ 377.36   |  $ 177.36
5)  NVIDIA Corporation                             $ 200.00   |  $ 370.69   |  $ 170.69

    Total                                          $ 1000.00  |  $ 1997.96  |  $ 997.96

                                     ROI   99.80 %


=======================================================================================
                                  Ticker Performance
=======================================================================================

                               -------------------------
                                    By Dollar value
                               -------------------------

Best:
1)  Amazon.com Inc.                                $ 411.55   |   54.30 %
2)  Alphabet Inc.                                  $ 267.59   |   34.36 %
3)  PCLN                                           $ 260.83   |   17.66 %
4)  Alphabet Inc.                                  $ 252.78   |   31.57 %
5)  Mettler-Toledo International Inc.              $ 197.59   |   46.83 %

Worst:
1)  Chipotle Mexican Grill Inc.                    $ -90.08   |  -23.76 %
2)  AutoZone Inc.                                  $ -84.21   |  -10.58 %
3)  Acuity Brands Inc.                             $ -56.89   |  -24.43 %
4)  Allergan plc                                   $ -50.57   |  -23.61 %
5)  O'Reilly Automotive Inc.                       $ -39.46   |  -14.09 %

                               -------------------------
                                      By Percent
                               -------------------------

Best:
1)  Align Technology Inc.                          130.27 %  |  $ 125.70
2)  Vertex Pharmaceuticals Incorporated            101.34 %  |  $ 75.43
3)  Wynn Resorts Limited                            93.34 %  |  $ 81.39
4)  The Boeing Company                              88.68 %  |  $ 138.61
5)  NVIDIA Corporation                              85.34 %  |  $ 89.10

Worst:
1)  Acuity Brands Inc.                             -24.43 %  |  $ -56.89
2)  Chipotle Mexican Grill Inc.                    -23.76 %  |  $ -90.08
3)  Allergan plc                                   -23.61 %  |  $ -50.57
4)  O'Reilly Automotive Inc.                       -14.09 %  |  $ -39.46
5)  Ulta Beauty Inc.                               -12.70 %  |  $ -32.54


=======================================================================================
                        Ticker best/worst Single-Day Gain/Loss
=======================================================================================

                               -------------------------
                                    By Dollar value
                               -------------------------
Best:
Company         |   PCLN
Date            |   2017-11-09
Dollar delta    |   $ 46.21

Worst:
Company         |   PCLN
Date            |   2017-11-07
Dollar delta    |   $ -100.98

                               -------------------------
                                      By Percent
                               -------------------------
Best:
Company         |    AET
Date            |    2017-10-26
Dollar delta    |    11.53 %

Worst:
Company         |    Align Technology Inc.
Date            |    2017-12-04
Dollar delta    |   -12.42 %


=======================================================================================
```
