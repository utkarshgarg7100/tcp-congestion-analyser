# TCP Congestion Control Analysis

A comprehensive network simulation project analyzing TCP congestion control algorithms using NS-3 network simulator. This project compares the performance of different TCP variants in various network conditions.

## 🚀 Features

- **Multi-TCP Variant Analysis**: Compares TCP NewReno, Cubic, BBR, and other algorithms
- **Comprehensive Metrics**: Throughput, delay, packet loss, link utilization, and fairness analysis
- **Automated Visualization**: Python scripts for generating performance charts
- **Statistical Analysis**: Detailed CSV reports with summary statistics

## 📁 Project Structure

```
├── tcp-dumbbell-enhanced.cc    # Main NS-3 simulation (C++)
├── visualize_tcp_results.py    # Results visualization script
├── test.py                     # Automated testing framework
├── utils.py                    # Utility functions for data processing
├── results*.csv                # Simulation output data
├── fairness_analysis.csv       # TCP fairness metrics
├── summary_statistics.csv      # Statistical summary
└── *.png                       # Generated performance charts
```

## 🛠️ Technologies Used

- **NS-3 Network Simulator** - Network simulation framework
- **C++** - Core simulation logic
- **Python** - Data analysis and visualization
- **Matplotlib/Pandas** - Chart generation and data processing

## 📊 Results

The project generates comprehensive analysis including:

1. **Throughput Comparison** - Performance across TCP variants
2. **Delay Analysis** - Latency characteristics 
3. **Packet Loss Metrics** - Loss rates under different conditions
4. **Link Utilization** - Network efficiency analysis
5. **Fairness Index** - Resource sharing fairness between flows
6. **Throughput-Delay Tradeoffs** - Performance optimization insights

## 🚀 Quick Start

1. **Setup NS-3 Environment**
   ```bash
   # Download and build NS-3
   git clone https://gitlab.com/nsnam/ns-3-dev.git ns-3
   cd ns-3
   ./ns3 configure --enable-examples --enable-tests
   ./ns3 build
   ```

2. **Run Simulation**
   ```bash
   # Copy simulation file to NS-3 scratch directory
   cp tcp-dumbbell-enhanced.cc ns-3/scratch/
   cd ns-3
   ./ns3 run scratch/tcp-dumbbell-enhanced
   ```

3. **Generate Visualizations**
   ```bash
   python3 visualize_tcp_results.py
   python3 test.py  # Run automated analysis
   ```

## 📈 Sample Results

The simulation analyzes network performance under various conditions:
- Multiple TCP congestion control algorithms
- Different network topologies (dumbbell topology)
- Varying bandwidth and delay parameters
- Statistical significance testing

## 🎯 Key Insights

- Comparative performance analysis of modern TCP variants
- Impact of network conditions on congestion control effectiveness
- Fairness implications in multi-flow scenarios
- Optimization recommendations for different use cases

## 📋 Requirements

- NS-3 Network Simulator (v3.35+)
- C++17 compatible compiler
- Python 3.7+ with matplotlib, pandas, numpy
- Git for version control

## 🤝 Contributing

This project demonstrates network simulation and analysis capabilities. Feel free to explore the code and suggest improvements!

---
*This project showcases skills in network simulation, C++ programming, Python data analysis, and performance evaluation methodologies.*