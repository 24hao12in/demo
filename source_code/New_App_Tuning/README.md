# ShaderNet New App Tuning
<!-- TABLE OF CONTENTS -->

<!-- ABOUT THE PROJECT -->


<!-- Graph creation -->


<!-- Scripts Explanation -->
## Graph  
The sample graphs of disassembly shaders can be found in  [Link to the folder](../sample_graph/)

## Scripts Explanation

All the scripts are written in python 3.8. To run the script, please lunch a python tools like Anaconda or directly run "python xx.py" 
1. Frequent subgraph result analysis 

    Frequent subgraph mining utilized the library of gSpan in the link listed in useful link. 

    An example to convert gSpan output text to edgelist and nodelist: 
    
    Scripts:[convert gSpan result to graph format](fsm_file_to_edgelist_hash.py)

    An example to select longest distinct subgraphs from gSpan result: 
    
    Scripts: [select longest patterns from gSpan result ](select_distinct_subgraph_labelgame.py)


2. Game clustering 
	
    There are 2 steps in community detection

    Step1: Dataset preparation 
    
	[Find max similarity for each pair of games' fsm](graph_similarity_measure.py)
   
  	[Prepare train dataset] (prepare_dataset_clustering.py)


    Step2:clustering with PCA feature reduction
    
	[Clutering](Kmeans_3dplot.py)
	
	This script using Kmenas with PCA feature reduction. The clustering result will be plotted in 3d as table3 figure.  



<!-- Useful linkes -->
## Useful linkes
1. [gSpan](https://github.com/betterenvi/gSpan)




<!-- Reference -->
## Reference

