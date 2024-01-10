
# Time Pattern Cohesion Score

## Introduction

https://pypi.org/project/tpcs/0.0.4/

TPCS is a metric to assess how well time-dependent patterns within a time series signal remain connected over time, with an emphasis on recency. 

![TPCS](https://github.com/karaposu/time-pattern-cohesion-score/blob/main/tpcs_illustration.png)

### We calculate TPCS using 4 main features :

**Consistency** : shows if data collection is consistent with respect to  start and end time of data crawling  , (from  2020-09 to current time)

**Intra Consistency** : shows if data collection was consistent with respect to signal’s own start and end time. 

**Contiguity** : shows how contiguous data is. 5 is fully contiguous which means all existed values are sequential

**Recent Contiguity** : shows how contiguous recent data is. 


## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Dependencies](#dependencies)
- [Documentation](#documentation)
- [Examples](#examples)
- [License](#license)

## Installation

```python
pip install tpcs
```

## How does it work?

###How TPC score is calculated?

We are first extracting relevant attributes from signals with the help of sequentiality package.  These attributes are:

1. total sample size (**n_of_samples**)

2. Longest Consecutive Subsequence of months  (**LCS_m**)

3. Longest Consecutive Subsequence of months with 1 gap month (**LCS_m_1g**)

4. Longest Consecutive Subsequence of months with 2 gap month (**LCS_m_1g**)

5. Longest Consecutive Subsequence of months from last timestamp (**LCS_m_from_last**)

6. Longest Consecutive Subsequence of months from last timestamp  with 1 gap month (**LCS_m_from_last_1g**)

7. Longest Consecutive Subsequence of months from last timestamp  with 2 gap month  (**LCS_m_from_last_2g**)

8. Longest Consecutive Subsequence of months from end time (**LCS_m_from_end**)

9. Longest Consecutive Subsequence of months from end time  with 1 gap month  (**LCS_m_from_end_1g**)

 
And then these attributes are group together into 4 features:

**Consistency** : shows if data collection is consistent with respect to  start and end time of data crawling  , (from  2020-09 to current time)

**Intra Consistency** : shows if data collection was consistent with respect to signal’s own start and end time. 

**Contiguity** : shows how contiguous data is. 5 is fully contiguous which means all existed values are sequential

**Recent Contiguity** : shows how contiguous recent data is. 

Then These features are turned into scores by calculating their ratio to max signal length and normalizing them between 0 and 5. 

And we take weighted avg of these normalized scores to calculate TPC.  

## Features & Usage

TPC score designed as a data quality assesment for time signals. It is really easy to use. 


```python

#Lets assume we have signal of interest. TPC requires dates of this signal as input. 

import datetime
date_list = ['2023-01-01', '2023-02-01', '2023-03-01', '2023-04-01', '2023-05-01', '2023-06-01', '2023-07-01', '2023-08-01', '2023-09-01', '2023-11-01', '2023-12-01', '2024-01-01']
# there are 12 months in this list. '2023-10-01'  is missing.  

date_list = [datetime.datetime.strptime(date_str, "%Y-%m-%d").date() for date_str in specific_dates]

weights={ "contiguity_score":0.5,
                  "recent_contiguity_score":3,
                  "consistency_score":0.8,
                  "intra_consistency_score":1
    
          }
  
MAX_LEN_MONTHS=  13  
END_OF_TIME=  '2024-01-01' 

tpcs =TPCS(date_list, MAX_LEN_MONTHS, END_OF_TIME=END_OF_TIME,  debug=False, return_details=True)
TPC_score, tpcs_details=tpcs.calculate_TPCS(weights=weights, printing=False)
 

```

## Documentation
https://github.com/karaposu/time-pattern-cohesion-score

## License

MIT License

Copyright (c) 2024 Enes Kuzucu

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
