# guest@24.147.205.252 -p 8022

# /Users/home/Documents/nycbikes/201406-citibike-tripdata.csv

import os, sys, time, pandas as pd, matplotlib.pyplot as plt, networkx as nx, numpy as np, scipy
from scipy.io import mmread

data = pd.read_csv('/Users/home/Documents/nycbikes/201412-citibike-tripdata.csv')
df = pd.DataFrame(data)

#--- Computed Data ---
#1765 stations 
#Center Axis: 40.748465362034544 -73.9514614600538
#Max Deviation Axis: 0.13375645596545382 0.07536153994618644 --> 0.134 0.0754

def draw_network(start, end):  
    start_time = time.time()
    DG = nx.DiGraph()
    station_names = []
    edge_count = 0
    for i in range(start, end):
        if df.loc[i]['start station name'] not in station_names:
            DG.add_node(df.loc[i]['start station name'], pos=(df.loc[i]['start station latitude'], df.loc[i]['start station longitude']))
            station_names.append(df.loc[i]['start station name'])
        if df.loc[i]['end station name'] not in station_names:
            DG.add_node(df.loc[i]['end station name'], pos=(df.loc[i]['end station latitude'], df.loc[i]['end station longitude']))
            station_names.append(df.loc[i]['end station name'])
        if DG.has_edge(df.loc[i]['start station name'], df.loc[i]['end station name']):
            DG[df.loc[i]['start station name']][df.loc[i]['end station name']]['weight'] += 1
        else:
            DG.add_edge(df.loc[i]['start station name'], df.loc[i]['end station name'], weight=1)
            edge_count += 1
    print(f'{len(station_names)} nodes, {edge_count} edges.')
    plt.figure("Jan 2023", figsize=(14, 7))
    nx.draw_networkx(DG, pos=nx.get_node_attributes(DG, 'pos'), width=[e[2]['weight']*50/edge_count for e in DG.edges(data=True)], 
                     node_size=10, font_size=2, arrowsize=5, node_color=list(DG.degree(n) for n in DG.nodes), cmap=plt.cm.jet, with_labels=True)
    print('--> Graph Created in', f'{(time.time() - start_time)} seconds' if time.time() - start_time < 60.0 else f'{(time.time() - start_time) / 60.0} minutes')
    plt.show()

def deg_dist(start, end):
    start_time = time.time()
    DG = nx.DiGraph()
    station_names = []
    for i in range(start, end):
        if df.loc[i]['start station name'] not in station_names:
            DG.add_node(df.loc[i]['start station name'], pos=(df.loc[i]['start station latitude'], df.loc[i]['start station longitude']), weight=0)
            station_names.append(df.loc[i]['start station name'])
        if df.loc[i]['end station name'] not in station_names:
            DG.add_node(df.loc[i]['end station name'], pos=(df.loc[i]['end station latitude'], df.loc[i]['end station longitude']), weight=0)
            station_names.append(df.loc[i]['end station name'])
        DG.nodes[df.loc[i]['start station name']]['weight'] += 1
        DG.nodes[df.loc[i]['end station name']]['weight'] += 1
    axs = plt.subplots(1, 1, figsize=(10, 5))
    axs[1].hist([DG.nodes[n]['weight'] for n in DG.nodes], density=True, bins=len(station_names), width=25)
    print('--> Graph Created in', f'{(time.time() - start_time)} seconds' if time.time() - start_time < 60.0 else f'{(time.time() - start_time) / 60.0} minutes')
    plt.show()
    
def number_of_stations(start, end):
    start_time = time.time()
    station_names = []
    for i in range(start, end):
        if df.loc[i]['start station name'] not in station_names:
            station_names.append(df.loc[i]['start station name'])
        if df.loc[i]['end station name'] not in station_names:
            station_names.append(df.loc[i]['end station name'])
    print('--> Calculated in', f'{(time.time() - start_time)} seconds' if time.time() - start_time < 60.0 else f'{(time.time() - start_time) / 60.0} minutes')
    print(f'{len(station_names)} stations')

def find_center_axis(start, end):
    station_ids = []
    lat_sum, lng_sum, count = 0, 0, 0
    for i in range(start, end):
        if df.loc[i]['start station name'] not in station_ids:
            lat_sum += df.loc[i]['start station latitude']
            lng_sum += df.loc[i]['start station longitude']
            count += 1
            station_ids.append(df.loc[i]['start station name'])
    print(lat_sum/count, lng_sum/count, count)

def find_concentration_axis(start, end):
    station_ids = []
    lat_sum, lng_sum, count = 0, 0, 0
    for i in range(start, end):
        if df.loc[i]['start station name'] not in station_ids:
            lat_sum += df.loc[i]['start station latitude']
            lng_sum += df.loc[i]['start station longitude']
            count += 1
    print(lat_sum/count, lng_sum/count, count)
    
def find_max_deviation_axis(center_lat, center_lng, start, end):
    station_ids = []
    max_lat = 0.0
    max_lng = 0.0
    for i in range(start, end):
        if df.loc[i]['start station name'] not in station_ids:
            if abs(float(df.loc[i]['start station latitude']) - center_lat) > max_lat:
                max_lat = abs(float(df.loc[i]['start station latitude']) - center_lat)
            if abs(float(df.loc[i]['start station longitude']) - center_lng) > max_lng:
                max_lng = abs(float(df.loc[i]['start station longitude']) - center_lng)
            station_ids.append(df.loc[i]['start station name'])
    print(max_lat, max_lng) 

#number_of_stations(0, len(df))
deg_dist(0, len(df))