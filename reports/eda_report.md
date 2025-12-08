# Tartu Bike Data - Exploratory Data Analysis Report

**Generated**: 2025-12-08 09:32:27


---


## Dataset Overview

- **Total trips**: 19,307

- **Total GPS points**: 1,525,424

- **Date range**: 2019-07-18 to 2019-07-26

- **Unique bikes**: 515

- **Unique stations**: 73




## Temporal Analysis


### Hourly Patterns

- **Peak hour**: 17:00 (1639 trips)

- **Quietest hour**: 5:00 (159 trips)

- **Average trips/hour**: 965.4




### Day of Week Patterns

- **Busiest day**: Thursday (10320 trips)

- **Quietest day**: Friday (8987 trips)




### Weekend vs Weekday

- **Weekday trips**: 19,307

- **Weekend trips**: 0

- **Weekday avg duration**: 22.18 minutes

- **Weekend avg duration**: 0.00 minutes




### Time Period Analysis

```

             Trip Count  Avg Duration (min)  Avg Distance (km)
time_period                                                   
Afternoon          7570               22.52               2.89
Evening            5679               24.51               3.21
Morning            3225               15.80               2.66
Night              2833               23.85               3.33

```




## Spatial Analysis


### Most Popular Stations

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




### Trip Types

- **Round trips**: 2,288 (11.9%)

- **One-way trips**: 17,019 (88.1%)




### Most Popular Routes

1. Veeriku → Kannikese: 60 trips

2. Uueturu → Soola: 47 trips

3. Annelinna keskus → Annelinna kiir: 46 trips

4. Aparaaditehas → Uueturu: 43 trips

5. Pirogovi plats → Uueturu: 42 trips




## Statistical Analysis


### Weekend vs Weekday Comparison

Note: No weekend data available for comparison




### Bike Type Comparison

**Comparing**: Pedelec vs Bike



**Duration:**

- Pedelec mean: 23.76 minutes

- Bike mean: 14.60 minutes

- p-value: 0.0000

- Significant difference: Yes



**Distance:**

- Pedelec mean: 3.24 km

- Bike mean: 1.92 km

- p-value: 0.0000

- Significant difference: Yes




### Time Period Comparison (ANOVA)

**Time Periods Tested**: Night, Morning, Afternoon, Evening



**Duration ANOVA:**

- F-statistic: 63.14

- p-value: 0.0000

- Significant difference: Yes



**Distance ANOVA:**

- F-statistic: 49.19

- p-value: 0.0000

- Significant difference: Yes




### User Segmentation Analysis

**Total Users Analyzed**: 515



**Segment Distribution**:

- Heavy: 456 users (88.5%)

- Regular: 42 users (8.2%)

- Occasional: 17 users (3.3%)


