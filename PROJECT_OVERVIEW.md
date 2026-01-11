# Project Overview: TCP Congestion Control Analysis

## 🎯 Problem Statement
Modern networks use different TCP congestion control algorithms, but their relative performance under various conditions isn't well understood. This project provides a comprehensive comparison of TCP variants using network simulation.

## 🔬 Methodology

### Simulation Framework
- **Tool**: NS-3 Network Simulator
- **Language**: C++ for simulation core
- **Topology**: Dumbbell network (realistic bottleneck scenario)

### TCP Variants Tested
1. **TCP NewReno** - Traditional loss-based algorithm
2. **TCP Cubic** - Improved cubic window growth
3. **TCP BBR** - Google's bottleneck bandwidth and RTT algorithm

### Test Scenarios
| Scenario | Bandwidth | Delay | Buffer | Flows | Description |
|----------|-----------|-------|--------|-------|-------------|
| 1 | 2 Mbps | 10ms | 10 packets | 2 | Low BW, Low latency |
| 2 | 2 Mbps | 100ms | 20 packets | 3 | Low BW, High latency |
| 3 | 10 Mbps | 10ms | 20 packets | 3 | High BW, Low latency |
| 4 | 10 Mbps | 100ms | 50 packets | 3 | High BW, High latency |

## 📊 Key Metrics
- **Throughput**: Data transfer rate (Mbps)
- **Delay**: End-to-end latency (seconds)
- **Packet Loss**: Loss rate percentage
- **Link Utilization**: Bottleneck efficiency
- **Fairness Index**: Resource sharing fairness
- **Throughput-Delay Tradeoff**: Performance optimization

## 🎨 Visualization Pipeline
Python scripts generate publication-quality charts:
1. Throughput comparison across variants
2. Delay analysis by scenario
3. Packet loss characteristics
4. Link utilization efficiency
5. Fairness index calculation
6. Performance tradeoff analysis

## 🏆 Key Findings
*(Based on simulation results)*
- BBR shows superior performance in high-latency scenarios
- Cubic provides good balance across different conditions
- NewReno remains competitive in low-latency environments
- Buffer sizing significantly impacts fairness metrics

## 💻 Technical Skills Demonstrated
- **Network Simulation**: NS-3 framework expertise
- **C++ Programming**: Complex simulation logic
- **Python Data Analysis**: Pandas, NumPy, Matplotlib
- **Statistical Analysis**: Performance metrics and fairness
- **Visualization**: Publication-quality charts
- **Version Control**: Git best practices

## 🚀 Running the Project
```bash
# 1. Setup NS-3 and run simulation
cp tcp-dumbbell-enhanced.cc ns-3/scratch/
cd ns-3 && ./ns3 run scratch/tcp-dumbbell-enhanced

# 2. Generate analysis
python3 run_analysis.py

# 3. View results
ls *.png  # Performance charts
cat summary_statistics.csv  # Statistical summary
```

This project demonstrates end-to-end network performance analysis capabilities, from simulation design to statistical evaluation.