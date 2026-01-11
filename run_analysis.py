#!/usr/bin/env python3
"""
TCP Analysis Demo Script

Quick demonstration of the TCP congestion control analysis project.
This script shows how to run the complete analysis pipeline.

Usage: python3 run_analysis.py
"""

import os
import sys
import subprocess
import pandas as pd

def main():
    print("🚀 TCP Congestion Control Analysis Demo")
    print("=" * 50)
    
    # Check if results exist
    if not os.path.exists('results_corrected.csv'):
        print("❌ Results file not found!")
        print("📝 To generate results:")
        print("   1. Copy tcp-dumbbell-enhanced.cc to ns-3/scratch/")
        print("   2. Run: ./ns3 run scratch/tcp-dumbbell-enhanced")
        print("   3. Copy results back to this directory")
        return
    
    # Load and display basic stats
    print("\n📊 Loading simulation results...")
    df = pd.read_csv('results_corrected.csv')
    
    print(f"✅ Found {len(df)} flow measurements")
    print(f"🔬 TCP Variants: {', '.join(df['Variant'].unique())}")
    print(f"🌐 Test Scenarios: {len(df['Scenario'].unique())}")
    
    # Show sample data
    print("\n📋 Sample Results:")
    print(df.groupby('Variant')['Throughput_Mbps'].agg(['mean', 'std']).round(2))
    
    # Generate visualizations
    print("\n🎨 Generating visualizations...")
    try:
        subprocess.run([sys.executable, 'visualize_tcp_results.py'], check=True)
        print("✅ Charts generated successfully!")
        
        # List generated files
        charts = [f for f in os.listdir('.') if f.endswith('.png')]
        print(f"📈 Generated {len(charts)} charts:")
        for chart in sorted(charts):
            print(f"   - {chart}")
            
    except subprocess.CalledProcessError:
        print("❌ Error generating charts")
        return
    
    print("\n🎯 Analysis Complete!")
    print("📁 Check the PNG files for performance visualizations")
    print("📊 Review CSV files for detailed metrics")

if __name__ == "__main__":
    main()