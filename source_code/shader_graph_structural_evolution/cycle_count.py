"""
cycle distribution for each frame for directed graph
"""


import os 
import csv 
import pandas as pd
import networkx as nx

path1 = './shaders/fireStrick/combine_all/'

frame_start=510
frame_end=3121
for idx in range(frame_start, frame_end, 10):
    fnum = '_f'+ str(idx)+'_'
    shadertypes = [m for m in os.listdir(path1) if m.startswith('distinct')]
    
    cycle_output= path1  + 'cycle/directed/' + fnum +"FS_cycle_directed_summary.csv"
    cycle_output1= path1  + 'cycle/directed/details/' + fnum +"FS_cycle_directed.csv"

    with open(cycle_output, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["fnum","shadertype","edge", "# cycle"])
                         
    for shadertype in shadertypes:
        print(shadertype)
        edgelists = [i for i in os.listdir(path1 + shadertype +'/edgelist/') if i.find(fnum)!=-1]  

                
        for edge in edgelists:
            #print(edge)
            edge_list = pd.read_csv(path1  + shadertype + '/edgelist/' + edge, header = None)
            node_list = pd.read_csv(path1 + shadertype + '/hash/' + edge.split('_edgelist')[0]+'_nodelist', header = None)
            diG = nx.DiGraph()
            for i, elrow in edge_list.iterrows():
                diG.add_edge(elrow[0], elrow[1])
            for i, nodrow  in node_list.iterrows():
                diG.nodes[i]['value'] =nodrow 
            try:
                cycles = list(nx.simple_cycles(diG))
                print(len(cycles))
                with open(cycle_output, 'a', newline='') as file, open(cycle_output1, 'a', newline='') as file1:
                    writer = csv.writer(file)
                    writer1 = csv.writer(file1)
                    writer.writerow([fnum.split('_')[1].split('f')[1], shadertype.split('_')[1], edge, len(cycles) ])
                    writer1.writerow([fnum.split('_')[1].split('f')[1], shadertype.split('_')[1], edge,cycles])

            except :
                pass 
