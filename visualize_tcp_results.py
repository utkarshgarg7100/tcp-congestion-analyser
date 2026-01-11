
#!/usr/bin/env python3
"""
TCP Congestion Control Performance Visualization
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set publication-quality style
plt.style.use('seaborn-v0_8-paper')
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 11

# Load results
print("Loading results_corrected.csv...")
df = pd.read_csv('results_corrected.csv')

print("\nFirst 5 rows of data:")
print(df.head())

# Filter out ACK flows (keep only forward data flows)
df_forward = df[df['Throughput_Mbps'] > 0.1].copy()

print(f"\nTotal flows: {len(df)}")
print(f"Forward flows (data): {len(df_forward)}")

# Get unique variants and scenarios
variants = sorted(df_forward['Variant'].unique())
scenarios = sorted(df_forward['Scenario'].unique())

print(f"\nDetected TCP Variants: {variants}")
print(f"Detected Scenarios: {scenarios}")

# Generate colors dynamically
colors = plt.cm.Set2(np.linspace(0, 1, len(variants)))

# ============================================================================
# GRAPH 1: THROUGHPUT COMPARISON
# ============================================================================
print("\n[1/8] Creating Throughput Comparison graph...")

throughput_agg = df_forward.groupby(['Variant', 'Scenario'])['Throughput_Mbps'].sum().reset_index()

plt.figure(figsize=(12, 6))
bar_width = 0.8 / len(variants)
x = np.arange(len(scenarios))

for i, variant in enumerate(variants):
    variant_data = throughput_agg[throughput_agg['Variant'] == variant]
    # Make sure data is sorted by scenario
    variant_data = variant_data.sort_values('Scenario')
    
    plt.bar(x + i*bar_width, variant_data['Throughput_Mbps'], 
            bar_width, label=variant, color=colors[i], alpha=0.8)

plt.xlabel('Scenario', fontsize=12, fontweight='bold')
plt.ylabel('Aggregate Throughput (Mbps)', fontsize=12, fontweight='bold')
plt.title('TCP Variant Throughput Comparison Across Scenarios', 
          fontsize=14, fontweight='bold', pad=20)
plt.xticks(x + bar_width * (len(variants)-1) / 2, [f'Scenario {s}' for s in scenarios])
plt.legend(title='TCP Variant', fontsize=10)
plt.grid(axis='y', alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig('1_throughput_comparison.png', bbox_inches='tight')
print("✓ Saved: 1_throughput_comparison.png")
plt.close()

# ============================================================================
# GRAPH 2: AVERAGE DELAY COMPARISON
# ============================================================================
print("[2/8] Creating Delay Comparison graph...")

delay_agg = df_forward.groupby(['Variant', 'Scenario'])['Delay_s'].mean().reset_index()
delay_agg['Delay_ms'] = delay_agg['Delay_s'] * 1000

plt.figure(figsize=(12, 6))
for i, variant in enumerate(variants):
    variant_data = delay_agg[delay_agg['Variant'] == variant]
    variant_data = variant_data.sort_values('Scenario')
    
    plt.bar(x + i*bar_width, variant_data['Delay_ms'], 
            bar_width, label=variant, color=colors[i], alpha=0.8)

plt.xlabel('Scenario', fontsize=12, fontweight='bold')
plt.ylabel('Average End-to-End Delay (ms)', fontsize=12, fontweight='bold')
plt.title('TCP Variant Delay Comparison Across Scenarios', 
          fontsize=14, fontweight='bold', pad=20)
plt.xticks(x + bar_width * (len(variants)-1) / 2, [f'Scenario {s}' for s in scenarios])
plt.legend(title='TCP Variant', fontsize=10)
plt.grid(axis='y', alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig('2_delay_comparison.png', bbox_inches='tight')
print("✓ Saved: 2_delay_comparison.png")
plt.close()

# ============================================================================
# GRAPH 3: PACKET LOSS COMPARISON
# ============================================================================
print("[3/8] Creating Packet Loss Comparison graph...")

loss_agg = df_forward.groupby(['Variant', 'Scenario'])['LostPackets'].sum().reset_index()

plt.figure(figsize=(12, 6))
for i, variant in enumerate(variants):
    variant_data = loss_agg[loss_agg['Variant'] == variant]
    variant_data = variant_data.sort_values('Scenario')
    
    plt.bar(x + i*bar_width, variant_data['LostPackets'], 
            bar_width, label=variant, color=colors[i], alpha=0.8)

plt.xlabel('Scenario', fontsize=12, fontweight='bold')
plt.ylabel('Total Lost Packets', fontsize=12, fontweight='bold')
plt.title('TCP Variant Packet Loss Comparison', 
          fontsize=14, fontweight='bold', pad=20)
plt.xticks(x + bar_width * (len(variants)-1) / 2, [f'Scenario {s}' for s in scenarios])
plt.legend(title='TCP Variant', fontsize=10)
plt.grid(axis='y', alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig('3_packet_loss_comparison.png', bbox_inches='tight')
print("✓ Saved: 3_packet_loss_comparison.png")
plt.close()

# ============================================================================
# GRAPH 4: LINK UTILIZATION
# ============================================================================
print("[4/8] Creating Link Utilization graph...")

scenario_capacity = {1: 2, 2: 2, 3: 10, 4: 10}  # Mbps
throughput_agg['Capacity'] = throughput_agg['Scenario'].map(scenario_capacity)
throughput_agg['Utilization_%'] = (throughput_agg['Throughput_Mbps'] / 
                                    throughput_agg['Capacity']) * 100

plt.figure(figsize=(12, 6))
for i, variant in enumerate(variants):
    variant_data = throughput_agg[throughput_agg['Variant'] == variant]
    variant_data = variant_data.sort_values('Scenario')
    
    plt.bar(x + i*bar_width, variant_data['Utilization_%'], 
            bar_width, label=variant, color=colors[i], alpha=0.8)

plt.axhline(y=100, color='red', linestyle='--', linewidth=2, 
            label='100% Capacity', alpha=0.7)
plt.xlabel('Scenario', fontsize=12, fontweight='bold')
plt.ylabel('Link Utilization (%)', fontsize=12, fontweight='bold')
plt.title('Bottleneck Link Utilization by TCP Variant', 
          fontsize=14, fontweight='bold', pad=20)
plt.xticks(x + bar_width * (len(variants)-1) / 2, [f'Scenario {s}' for s in scenarios])
plt.legend(fontsize=10)
plt.ylim(0, 110)
plt.grid(axis='y', alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig('4_link_utilization.png', bbox_inches='tight')
print("✓ Saved: 4_link_utilization.png")
plt.close()

# ============================================================================
# GRAPH 5: THROUGHPUT-DELAY SCATTER PLOT
# ============================================================================
print("[5/8] Creating Throughput vs Delay scatter plot...")

plt.figure(figsize=(10, 7))
markers = ['o', 's', '^', 'D', 'v', '<', '>', 'p']

for i, variant in enumerate(variants):
    variant_data = df_forward[df_forward['Variant'] == variant]
    
    plt.scatter(variant_data['Delay_s'] * 1000, 
               variant_data['Throughput_Mbps'],
               s=100, alpha=0.6, marker=markers[i % len(markers)], 
               color=colors[i],
               label=variant)

plt.xlabel('Average Delay (ms)', fontsize=12, fontweight='bold')
plt.ylabel('Throughput (Mbps)', fontsize=12, fontweight='bold')
plt.title('Throughput-Delay Trade-off Analysis', 
          fontsize=14, fontweight='bold', pad=20)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig('5_throughput_delay_tradeoff.png', bbox_inches='tight')
print("✓ Saved: 5_throughput_delay_tradeoff.png")
plt.close()

# ============================================================================
# GRAPH 6: FAIRNESS INDEX
# ============================================================================
print("[6/8] Creating Fairness Index graph...")

def jains_fairness(throughputs):
    """Calculate Jain's Fairness Index"""
    n = len(throughputs)
    if n == 0 or n == 1:
        return 1.0
    sum_x = sum(throughputs)
    sum_x_squared = sum(x**2 for x in throughputs)
    if sum_x_squared == 0:
        return 0
    return (sum_x ** 2) / (n * sum_x_squared)

fairness_data = []
for scenario in scenarios:
    for variant in variants:
        flows = df_forward[(df_forward['Scenario'] == scenario) & 
                           (df_forward['Variant'] == variant)]['Throughput_Mbps'].values
        if len(flows) > 0:
            fairness = jains_fairness(flows)
            fairness_data.append({
                'Scenario': scenario,
                'Variant': variant,
                'Fairness': fairness
            })

fairness_df = pd.DataFrame(fairness_data)

plt.figure(figsize=(12, 6))
for i, variant in enumerate(variants):
    variant_data = fairness_df[fairness_df['Variant'] == variant]
    variant_data = variant_data.sort_values('Scenario')
    
    plt.bar(x + i*bar_width, variant_data['Fairness'], 
            bar_width, label=variant, color=colors[i], alpha=0.8)

plt.axhline(y=1.0, color='green', linestyle='--', linewidth=2, 
            label='Perfect Fairness', alpha=0.7)
plt.xlabel('Scenario', fontsize=12, fontweight='bold')
plt.ylabel("Jain's Fairness Index", fontsize=12, fontweight='bold')
plt.title('Fairness Index Comparison (1.0 = Perfect Fairness)', 
          fontsize=14, fontweight='bold', pad=20)
plt.xticks(x + bar_width * (len(variants)-1) / 2, [f'Scenario {s}' for s in scenarios])
plt.legend(fontsize=10)
plt.ylim(0, 1.1)
plt.grid(axis='y', alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig('6_fairness_index.png', bbox_inches='tight')
print("✓ Saved: 6_fairness_index.png")
plt.close()

# ============================================================================
# SUMMARY TABLE
# ============================================================================
print("\n" + "="*70)
print("SUMMARY STATISTICS")
print("="*70)

summary = df_forward.groupby(['Variant', 'Scenario']).agg({
    'Throughput_Mbps': ['sum', 'mean'],
    'Delay_s': 'mean',
    'LostPackets': 'sum'
}).round(3)

print("\n", summary)

summary.to_csv('summary_statistics.csv')
fairness_df.to_csv('fairness_analysis.csv', index=False)

print("\n" + "="*70)
print("ALL VISUALIZATIONS COMPLETED SUCCESSFULLY!")
print("="*70)
print("\nGenerated files:")
print("  1. 1_throughput_comparison.png")
print("  2. 2_delay_comparison.png")
print("  3. 3_packet_loss_comparison.png")
print("  4. 4_link_utilization.png")
print("  5. 5_throughput_delay_tradeoff.png")
print("  6. 6_fairness_index.png")
print("  7. summary_statistics.csv")
print("  8. fairness_analysis.csv")
print("\nUse these graphs in your research paper! 📊🎉")