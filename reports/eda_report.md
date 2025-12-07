# Tartu Bike Data - Exploratory Data Analysis Report

**Generated**: 2025-12-07 23:34:49

---

## 1. Dataset Overview

- **Total trips**: 19,307

- **Total GPS points**: 1,525,424

- **Date range**: 2019-07-18 to 2019-07-26

- **Unique bikes**: 515

- **Unique stations**: 73


## 2. Temporal Analysis

### 2.1 Hourly Patterns

- **Peak hour**: 17:00 (1639 trips)

- **Quietest hour**: 5:00 (159 trips)

- **Average trips/hour**: 965.4


### 2.2 Day of Week Patterns

- **Busiest day**: Thursday (10320 trips)

- **Quietest day**: Friday (8987 trips)


### 2.3 Weekend vs Weekday

- **Weekday trips**: 19,307

- **Weekend trips**: 0

- **Weekday avg duration**: 22.18 minutes

- **Weekend avg duration**: 0.00 minutes


### 2.4 Time Period Analysis

```

             Trip Count  Avg Duration (min)  Avg Distance (km)
time_period                                                   
Afternoon          7570               22.52               2.89
Evening            5679               24.51               3.21
Morning            3225               15.80               2.66
Night              2833               23.85               3.33

```


## 3. Spatial Analysis

### 3.1 Most Popular Stations

**Top 5 Start Stations:**

1. Uueturu: 1,176 trips

2. Soola: 807 trips

3. Eeden: 536 trips

4. Pirogovi plats: 517 trips

5. Vabadussild: 479 trips


**Top 5 End Stations:**

1. Uueturu: 1,146 trips

2. Soola: 832 trips

3. Eeden: 547 trips

4. Pirogovi plats: 539 trips

5. Vabadussild: 491 trips



### 3.2 Trip Types

- **Round trips**: 2,288 (11.9%)

- **One-way trips**: 17,019 (88.1%)


### 3.3 Most Popular Routes

1. Veeriku → Kannikese: 60 trips

2. Uueturu → Soola: 47 trips

3. Annelinna keskus → Annelinna kiir: 46 trips

4. Aparaaditehas → Uueturu: 43 trips

5. Pirogovi plats → Uueturu: 42 trips



## 4. User Behavior Analysis

### 4.1 Membership Analysis

**Top 5 Membership Types:**

1. Free Membership (with bus card): 5,334 trips

2. 3-Month Free Membership: 5,105 trips

3. 3 month free membership: 4,824 trips

4. 1 month free membership: 753 trips

5. 1-month Free Membership: 730 trips



### 4.2 Bike Type Analysis

**Bike:**

- Trips: 3,334

- Avg Duration: 14.60 min

- Avg Distance: 1.92 km


**Pedelec:**

- Trips: 15,973

- Avg Duration: 23.76 min

- Avg Distance: 3.24 km


## 5. Trip Characteristics

### 5.1 Duration Statistics

- Mean: 22.18 minutes

- Median: 13.93 minutes

- Std Dev: 30.18 minutes

- Min: 0.50 minutes

- Max: 1366.18 minutes


### 5.2 Distance Statistics

- Mean: 3.01 km

- Median: 2.38 km

- Std Dev: 2.62 km

- Min: 0.00 km

- Max: 37.95 km


### 5.3 Duration vs Distance Correlation

- **Correlation coefficient**: 0.489


## 6. Statistical Analysis

### 6.1 Correlation Matrix

Key correlations:

- duration_minutes_calculated vs length: 0.489

- duration_minutes_calculated vs costs: 0.767

- length vs costs: 0.293



### 6.2 Cost Analysis

- **Free trips**: 18,680 (96.8%)

- **Paid trips**: 627 (3.2%)

- **Average cost (all)**: €0.05

- **Average cost (paid only)**: €1.49


## 7. GPS Data Analysis

- **Average GPS points per trip**: 79.1

- **Median GPS points per trip**: 52.0

- **Latitude range**: 58.293123° to 58.436823°

- **Longitude range**: 26.606762° to 26.895897°

- **Coverage area**: ~0.1437° × 0.2891°


## 8. Summary Statistics

```

       duration_minutes_calculated        length         costs
count                 19307.000000  19307.000000  19307.000000
mean                     22.178545      3.011318      0.048428
std                      30.175379      2.623038      0.305660
min                       0.500000      0.000000      0.000000
25%                       7.050000      1.200000      0.000000
50%                      13.933333      2.380000      0.000000
75%                      30.191667      4.040000      0.000000
max                    1366.183333     37.950000      4.000000

```

