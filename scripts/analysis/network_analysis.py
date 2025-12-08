"""
Network Analysis
================

Station network analysis using NetworkX.
"""

import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import os
from . import config
from .utils import plotting


def create_station_network(routes):
    """
    Create a directed network graph of bike stations.

    Args:
        routes (pd.DataFrame): Routes dataframe

    Returns:
        tuple: (NetworkX DiGraph, network_stats dict)
    """
    # Create directed graph
    G = nx.DiGraph()

    # Add edges with weights (trip counts)
    route_counts = routes.groupby(['startstationname', 'endstationname']).agg({
        'route_code': 'count',
        'duration_minutes_calculated': 'mean',
        'length': 'mean'
    }).reset_index()
    route_counts.columns = ['source', 'target', 'weight', 'avg_duration', 'avg_distance']

    # Add edges
    for _, row in route_counts.iterrows():
        if row['source'] != row['target']:  # Skip self-loops
            G.add_edge(
                row['source'],
                row['target'],
                weight=row['weight'],
                duration=row['avg_duration'],
                distance=row['avg_distance']
            )

    # Network statistics
    network_stats = {
        'nodes': G.number_of_nodes(),
        'edges': G.number_of_edges(),
        'density': nx.density(G),
        'is_strongly_connected': nx.is_strongly_connected(G),
        'is_weakly_connected': nx.is_weakly_connected(G)
    }

    if nx.is_weakly_connected(G):
        network_stats['diameter'] = nx.diameter(G.to_undirected())
        network_stats['avg_shortest_path'] = nx.average_shortest_path_length(G.to_undirected())

    return G, network_stats


def calculate_centrality_metrics(G):
    """
    Calculate various centrality metrics for the network.

    Args:
        G (nx.DiGraph): Network graph

    Returns:
        pd.DataFrame: Centrality metrics for each station
    """
    # Degree centrality (in and out)
    in_degree = dict(G.in_degree())
    out_degree = dict(G.out_degree())
    degree_centrality = nx.degree_centrality(G)

    # Betweenness centrality
    betweenness = nx.betweenness_centrality(G, weight='weight')

    # Closeness centrality
    closeness = nx.closeness_centrality(G, distance='weight')

    # PageRank
    pagerank = nx.pagerank(G, weight='weight')

    # Eigenvector centrality (if possible)
    try:
        eigenvector = nx.eigenvector_centrality(G, weight='weight', max_iter=1000)
    except:
        eigenvector = {node: 0 for node in G.nodes()}

    # Combine into dataframe
    centrality_df = pd.DataFrame({
        'station': list(G.nodes()),
        'in_degree': [in_degree[n] for n in G.nodes()],
        'out_degree': [out_degree[n] for n in G.nodes()],
        'degree_centrality': [degree_centrality[n] for n in G.nodes()],
        'betweenness_centrality': [betweenness[n] for n in G.nodes()],
        'closeness_centrality': [closeness[n] for n in G.nodes()],
        'pagerank': [pagerank[n] for n in G.nodes()],
        'eigenvector_centrality': [eigenvector[n] for n in G.nodes()]
    })

    # Sort by PageRank
    centrality_df = centrality_df.sort_values('pagerank', ascending=False).reset_index(drop=True)

    return centrality_df


def detect_communities(G):
    """
    Detect communities in the station network.

    Args:
        G (nx.DiGraph): Network graph

    Returns:
        tuple: (community assignments dict, modularity score)
    """
    # Convert to undirected for community detection
    G_undirected = G.to_undirected()

    # Use Louvain method (greedy modularity)
    try:
        from networkx.algorithms import community
        communities = community.greedy_modularity_communities(G_undirected, weight='weight')

        # Convert to dict
        community_dict = {}
        for i, comm in enumerate(communities):
            for node in comm:
                community_dict[node] = i

        # Calculate modularity
        modularity = community.modularity(G_undirected, communities, weight='weight')

        return community_dict, modularity
    except:
        # Fallback: simple connected components
        components = list(nx.connected_components(G_undirected))
        community_dict = {}
        for i, comp in enumerate(components):
            for node in comp:
                community_dict[node] = i

        return community_dict, 0.0


def analyze_shortest_paths(G, top_stations):
    """
    Analyze shortest paths between top stations.

    Args:
        G (nx.DiGraph): Network graph
        top_stations (list): List of top station names

    Returns:
        pd.DataFrame: Shortest path analysis
    """
    # Get undirected graph for path analysis
    G_undirected = G.to_undirected()

    paths_data = []

    # Calculate paths between top stations
    for i, source in enumerate(top_stations[:10]):
        for target in top_stations[i+1:11]:
            if source != target and source in G_undirected and target in G_undirected:
                try:
                    # Shortest path
                    path = nx.shortest_path(G_undirected, source, target, weight='weight')
                    path_length = nx.shortest_path_length(G_undirected, source, target, weight='weight')

                    paths_data.append({
                        'source': source,
                        'target': target,
                        'path_length': len(path) - 1,  # Number of hops
                        'weighted_distance': path_length,
                        'path': ' → '.join(path[:3]) + ('...' if len(path) > 3 else '')
                    })
                except nx.NetworkXNoPath:
                    continue

    paths_df = pd.DataFrame(paths_data)
    if len(paths_df) > 0:
        paths_df = paths_df.sort_values('weighted_distance').reset_index(drop=True)

    return paths_df


def visualize_network(G, centrality_df, community_dict, top_n=30):
    """
    Visualize the station network.

    Args:
        G (nx.DiGraph): Network graph
        centrality_df (pd.DataFrame): Centrality metrics
        community_dict (dict): Community assignments
        top_n (int): Number of top stations to show

    Returns:
        list: Visualization file paths
    """
    filepaths = []

    # Get top stations by PageRank
    top_stations = centrality_df.head(top_n)['station'].tolist()
    G_sub = G.subgraph(top_stations).copy()

    # Figure 1: Network with node sizes by PageRank
    fig, ax = plt.subplots(figsize=(16, 12))

    # Layout
    pos = nx.spring_layout(G_sub, k=2, iterations=50, seed=42)

    # Node sizes by PageRank
    node_sizes = [centrality_df[centrality_df['station'] == n]['pagerank'].values[0] * 10000
                  for n in G_sub.nodes()]

    # Node colors by community
    node_colors = [community_dict.get(n, 0) for n in G_sub.nodes()]

    # Draw network
    nx.draw_networkx_nodes(
        G_sub, pos,
        node_size=node_sizes,
        node_color=node_colors,
        cmap='Set3',
        alpha=0.8,
        ax=ax
    )

    # Draw edges with varying widths
    edges = G_sub.edges()
    weights = [G_sub[u][v]['weight'] for u, v in edges]
    max_weight = max(weights) if weights else 1
    edge_widths = [w / max_weight * 3 for w in weights]

    nx.draw_networkx_edges(
        G_sub, pos,
        width=edge_widths,
        alpha=0.3,
        edge_color='gray',
        arrows=True,
        arrowsize=10,
        ax=ax
    )

    # Draw labels
    nx.draw_networkx_labels(
        G_sub, pos,
        font_size=8,
        font_weight='bold',
        ax=ax
    )

    ax.set_title(f'Station Network - Top {top_n} Stations by PageRank\n(Node size = Importance, Color = Community)',
                 fontsize=14, fontweight='bold', pad=20)
    ax.axis('off')

    plt.tight_layout()
    filepath = plotting.save_figure(fig, 'station_network.png', 'statistical')
    filepaths.append(filepath)
    plt.close()

    # Figure 2: Centrality comparison
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    top_10 = centrality_df.head(10)

    # Degree Centrality
    axes[0, 0].barh(top_10['station'], top_10['degree_centrality'], color='steelblue', edgecolor='black')
    axes[0, 0].set_title('Top 10 Stations - Degree Centrality', fontweight='bold')
    axes[0, 0].set_xlabel('Degree Centrality')
    axes[0, 0].invert_yaxis()
    axes[0, 0].grid(axis='x', alpha=0.3)

    # Betweenness Centrality
    axes[0, 1].barh(top_10['station'], top_10['betweenness_centrality'], color='coral', edgecolor='black')
    axes[0, 1].set_title('Top 10 Stations - Betweenness Centrality', fontweight='bold')
    axes[0, 1].set_xlabel('Betweenness Centrality')
    axes[0, 1].invert_yaxis()
    axes[0, 1].grid(axis='x', alpha=0.3)

    # Closeness Centrality
    axes[1, 0].barh(top_10['station'], top_10['closeness_centrality'], color='green', edgecolor='black')
    axes[1, 0].set_title('Top 10 Stations - Closeness Centrality', fontweight='bold')
    axes[1, 0].set_xlabel('Closeness Centrality')
    axes[1, 0].invert_yaxis()
    axes[1, 0].grid(axis='x', alpha=0.3)

    # PageRank
    axes[1, 1].barh(top_10['station'], top_10['pagerank'], color='purple', edgecolor='black')
    axes[1, 1].set_title('Top 10 Stations - PageRank', fontweight='bold')
    axes[1, 1].set_xlabel('PageRank Score')
    axes[1, 1].invert_yaxis()
    axes[1, 1].grid(axis='x', alpha=0.3)

    plt.tight_layout()
    filepath = plotting.save_figure(fig, 'centrality_metrics.png', 'statistical')
    filepaths.append(filepath)
    plt.close()

    # Figure 3: Community visualization
    fig, ax = plt.subplots(figsize=(14, 10))

    # Count communities
    community_sizes = pd.Series(community_dict).value_counts().sort_index()

    ax.bar(community_sizes.index, community_sizes.values, color='teal', edgecolor='black', alpha=0.7)
    ax.set_title('Station Communities - Size Distribution', fontsize=14, fontweight='bold')
    ax.set_xlabel('Community ID', fontsize=12)
    ax.set_ylabel('Number of Stations', fontsize=12)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    filepath = plotting.save_figure(fig, 'community_distribution.png', 'statistical')
    filepaths.append(filepath)
    plt.close()

    return filepaths


def run_network_analysis(routes, report):
    """
    Run all network analyses.

    Args:
        routes (pd.DataFrame): Routes dataframe
        report (MarkdownReport): Report object

    Returns:
        dict: Analysis results
    """
    print("\n[Network Analysis]")
    print("-" * 80)

    results = {}

    # Create network
    print("  • Building station network...")
    G, network_stats = create_station_network(routes)
    results['network'] = {'graph': G, 'stats': network_stats}

    report.add_section("Network Analysis")
    report.add_subsection("Network Structure")
    report.add_line(f"**Total Stations (Nodes)**: {network_stats['nodes']}")
    report.add_line(f"**Total Routes (Edges)**: {network_stats['edges']}")
    report.add_line(f"**Network Density**: {network_stats['density']:.4f}")
    report.add_line(f"**Strongly Connected**: {'Yes' if network_stats['is_strongly_connected'] else 'No'}")
    report.add_line(f"**Weakly Connected**: {'Yes' if network_stats['is_weakly_connected'] else 'No'}")
    if 'diameter' in network_stats:
        report.add_line(f"**Network Diameter**: {network_stats['diameter']}")
        report.add_line(f"**Average Shortest Path**: {network_stats['avg_shortest_path']:.2f}")
    report.add_line("")

    # Centrality metrics
    print("  • Calculating centrality metrics...")
    centrality_df = calculate_centrality_metrics(G)
    results['centrality'] = centrality_df

    report.add_subsection("Top 10 Stations by Centrality")
    report.add_line("**PageRank (Overall Importance):**")
    for i, row in centrality_df.head(10).iterrows():
        report.add_line(f"{i+1}. {row['station']}: {row['pagerank']:.4f}")
    report.add_line("")

    # Community detection
    print("  • Detecting communities...")
    community_dict, modularity = detect_communities(G)
    results['communities'] = {'assignments': community_dict, 'modularity': modularity}

    report.add_subsection("Community Detection")
    report.add_line(f"**Number of Communities**: {len(set(community_dict.values()))}")
    report.add_line(f"**Modularity Score**: {modularity:.4f}")
    report.add_line("")

    # Shortest paths
    print("  • Analyzing shortest paths...")
    top_stations = centrality_df.head(15)['station'].tolist()
    paths_df = analyze_shortest_paths(G, top_stations)
    results['paths'] = paths_df

    if len(paths_df) > 0:
        report.add_subsection("Shortest Paths (Top Stations)")
        report.add_line("**Sample Shortest Paths:**")
        for i, row in paths_df.head(5).iterrows():
            report.add_line(f"- {row['source']} → {row['target']}: {row['path_length']} hops")
        report.add_line("")

    # Visualizations
    print("  • Creating network visualizations...")
    viz_files = visualize_network(G, centrality_df, community_dict, top_n=30)
    results['visualizations'] = viz_files

    print(f"  ✓ Network analysis complete")
    print(f"  ✓ Analyzed {network_stats['nodes']} stations, {network_stats['edges']} routes")

    return results
