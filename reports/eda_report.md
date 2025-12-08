# Tartu Bike Data - Exploratory Data Analysis Report

**Generated**: 2025-12-08 10:08:12


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




## Machine Learning Analysis


### Demand Prediction

**Predicted Peak Hour**: 17:00

**Predicted Peak Demand**: 1532 trips

**Average Hourly Demand**: 803 trips




### User Behavior Clustering

**Number of Clusters**: 3

**Silhouette Score**: 0.307 (higher is better)

**Davies-Bouldin Index**: 1.347 (lower is better)



**Cluster 0**:

- Users: 233

- Avg trips: 23.9

- Avg duration: 16.6 min

- Avg distance: 2.27 km



**Cluster 1**:

- Users: 74

- Avg trips: 37.7

- Avg duration: 33.9 min

- Avg distance: 3.70 km



**Cluster 2**:

- Users: 208

- Avg trips: 52.6

- Avg duration: 22.8 min

- Avg distance: 3.30 km




### Route Clustering

**Number of Clusters**: 5

**Total OD Pairs Analyzed**: 1256



**Cluster 0**:

- Routes: 185

- Avg trips/route: 23.7

- Avg distance: 2.21 km



**Cluster 1**:

- Routes: 387

- Avg trips/route: 7.9

- Avg distance: 4.36 km



**Cluster 2**:

- Routes: 626

- Avg trips/route: 8.5

- Avg distance: 2.07 km



**Cluster 3**:

- Routes: 38

- Avg trips/route: 8.1

- Avg distance: 4.83 km



**Cluster 4**:

- Routes: 20

- Avg trips/route: 62.5

- Avg distance: 2.84 km




### Anomaly Detection

**Total Trips**: 19,307

**Anomalies Detected**: 966 (5.00%)

**Normal Trips**: 18,341 (95.00%)



**Anomaly Characteristics**:

- Avg duration: 84.4 min (vs 18.9 normal)

- Avg distance: 7.58 km (vs 2.77 normal)

- Most anomalies at hour: 0:00


## Interactive Visualizations


### Station Map

**Total Stations Mapped**: 73

**Map Center**: (58.3740, 26.7253)

**Total Trips Visualized**: 38,614




### Trip Flow Map

**Top Routes Visualized**: 20

**Most Popular Route**: EMÜ spordihoone → EMÜ spordihoone

**Most Popular Route Trips**: 6




### GPS Density Heatmap

**GPS Points Visualized**: 15,255

**Sampling Rate**: 1 in 100 points

**Map Center**: (58.3755, 26.7299)




### Interactive Hourly Analysis

**Peak Hour**: 17:00

**Peak Hour Trips**: 1,639

**Quietest Hour**: 5:00




### Interactive Station Analysis

**Top Station**: Uueturu

**Top Station Starts**: 1,176

**Top Station Ends**: 1,146




## Network Analysis


### Network Structure

**Total Stations (Nodes)**: 73

**Total Routes (Edges)**: 3520

**Network Density**: 0.6697

**Strongly Connected**: Yes

**Weakly Connected**: Yes

**Network Diameter**: 3

**Average Shortest Path**: 1.21




### Top 10 Stations by Centrality

**PageRank (Overall Importance):**

1. Uueturu: 0.0538

2. Soola: 0.0380

3. Pirogovi plats: 0.0266

4. Eeden: 0.0257

5. Vabadussild: 0.0229

6. Roosi: 0.0228

7. Veeriku: 0.0220

8. Aleksandri: 0.0218

9. Lõunakeskus: 0.0208

10. Turusild: 0.0203




### Community Detection

**Number of Communities**: 3

**Modularity Score**: 0.1772




### Shortest Paths (Top Stations)

**Sample Shortest Paths:**

- Veeriku → ERM: 1 hops

- Veeriku → Turusild: 1 hops

- Eeden → Vabadussild: 2 hops

- Eeden → Roosi: 2 hops

- Eeden → Veeriku: 1 hops


