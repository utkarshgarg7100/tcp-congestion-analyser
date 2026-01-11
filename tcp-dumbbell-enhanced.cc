#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/flow-monitor-module.h"
#include <fstream>
#include <iostream>

using namespace ns3;

NS_LOG_COMPONENT_DEFINE("TcpDumbbellEnhanced");

int main(int argc, char *argv[])
{
  double simulationTime = 20.0; // seconds
  CommandLine cmd;
  cmd.AddValue("simulationTime", "Simulation time (s)", simulationTime);
  cmd.Parse(argc, argv);

  // TCP Variants to test
  std::vector<std::string> tcpVariants = {"TcpNewReno", "TcpCubic", "TcpBbr"};

  // Test scenarios (bandwidth, delay, buffer, numFlows)
  struct Scenario
  {
    std::string bandwidth;
    std::string delay;
    uint32_t bufferPackets;
    uint32_t numFlows;
    std::string description;
  };

  std::vector<Scenario> scenarios = {
      {"2Mbps", "10ms", 10, 2, "Low-bandwidth, Low-latency"},
      {"2Mbps", "100ms", 20, 3, "Low-bandwidth, High-latency"},
      {"10Mbps", "10ms", 20, 3, "High-bandwidth, Low-latency"},
      {"10Mbps", "100ms", 50, 3, "High-bandwidth, High-latency"}
  };

  std::ofstream out("results.csv");
  out << "Variant,Scenario,Description,Bandwidth,Delay,BufferPackets,NumFlows,FlowId,Source,Destination,Throughput_Mbps,Delay_s,LostPackets,TxPackets,RxPackets\n";

  // Loop through all variants and scenarios
  for (auto variant : tcpVariants)
  {
    TypeId tcpTid;
    
    // Try to lookup the TCP variant, skip if not available
    try
    {
      if (variant == "TcpNewReno")
        tcpTid = TypeId::LookupByName("ns3::TcpNewReno");
      else if (variant == "TcpCubic")
        tcpTid = TypeId::LookupByName("ns3::TcpCubic");
      else if (variant == "TcpBbr")
        tcpTid = TypeId::LookupByName("ns3::TcpBbr");
      else
        continue;
    }
    catch (...)
    {
      std::cout << "\n⚠️  " << variant << " not available in this NS-3 version, skipping...\n";
      continue;
    }

    Config::SetDefault("ns3::TcpL4Protocol::SocketType", TypeIdValue(tcpTid));

    for (size_t i = 0; i < scenarios.size(); ++i)
    {
      std::cout << "\n=== Running " << variant << " - Scenario " << (i + 1) 
                << ": " << scenarios[i].description << " ===" << std::endl;

      // Create nodes
      NodeContainer senders, receivers, routers;
      senders.Create(scenarios[i].numFlows);
      receivers.Create(scenarios[i].numFlows);
      routers.Create(2);

      // Install internet stack
      InternetStackHelper stack;
      stack.Install(senders);
      stack.Install(receivers);
      stack.Install(routers);

      // Access links (fast connections)
      PointToPointHelper access;
      access.SetDeviceAttribute("DataRate", StringValue("100Mbps"));
      access.SetChannelAttribute("Delay", StringValue("2ms"));

      // Bottleneck link (varies by scenario)
      PointToPointHelper bottleneck;
      bottleneck.SetDeviceAttribute("DataRate", StringValue(scenarios[i].bandwidth));
      bottleneck.SetChannelAttribute("Delay", StringValue(scenarios[i].delay));

      // Set queue size for bottleneck
      Config::SetDefault("ns3::DropTailQueue<Packet>::MaxSize", 
                         QueueSizeValue(QueueSize(QueueSizeUnit::PACKETS, scenarios[i].bufferPackets)));

      // Connect routers with bottleneck link
      NetDeviceContainer bottleneckDevices = bottleneck.Install(routers.Get(0), routers.Get(1));

      // Connect senders and receivers to routers
      std::vector<NetDeviceContainer> senderDevices(scenarios[i].numFlows);
      std::vector<NetDeviceContainer> receiverDevices(scenarios[i].numFlows);

      for (uint32_t j = 0; j < scenarios[i].numFlows; ++j)
      {
        senderDevices[j] = access.Install(senders.Get(j), routers.Get(0));
        receiverDevices[j] = access.Install(routers.Get(1), receivers.Get(j));
      }

      // Assign IP addresses
      Ipv4AddressHelper address;
      
      // Bottleneck link
      address.SetBase("10.1.1.0", "255.255.255.0");
      Ipv4InterfaceContainer bottleneckInterfaces = address.Assign(bottleneckDevices);

      // Sender links
      std::vector<Ipv4InterfaceContainer> senderInterfaces(scenarios[i].numFlows);
      for (uint32_t j = 0; j < scenarios[i].numFlows; ++j)
      {
        std::ostringstream subnet;
        subnet << "10.2." << (j + 1) << ".0";
        address.SetBase(subnet.str().c_str(), "255.255.255.0");
        senderInterfaces[j] = address.Assign(senderDevices[j]);
      }

      // Receiver links
      std::vector<Ipv4InterfaceContainer> receiverInterfaces(scenarios[i].numFlows);
      for (uint32_t j = 0; j < scenarios[i].numFlows; ++j)
      {
        std::ostringstream subnet;
        subnet << "10.3." << (j + 1) << ".0";
        address.SetBase(subnet.str().c_str(), "255.255.255.0");
        receiverInterfaces[j] = address.Assign(receiverDevices[j]);
      }

      // Populate routing tables
      Ipv4GlobalRoutingHelper::PopulateRoutingTables();

      // Create applications
      uint16_t port = 9;
      ApplicationContainer apps;

      for (uint32_t j = 0; j < scenarios[i].numFlows; ++j)
      {
        // OnOff application on sender
        Address receiverAddr = InetSocketAddress(receiverInterfaces[j].GetAddress(1), port);
        OnOffHelper onoff("ns3::TcpSocketFactory", receiverAddr);
        onoff.SetConstantRate(DataRate("5Mbps"));
        onoff.SetAttribute("StartTime", TimeValue(Seconds(1.0 + 0.2 * j)));
        onoff.SetAttribute("StopTime", TimeValue(Seconds(simulationTime)));
        apps.Add(onoff.Install(senders.Get(j)));

        // Packet sink on receiver
        PacketSinkHelper sink("ns3::TcpSocketFactory", 
                              InetSocketAddress(Ipv4Address::GetAny(), port));
        apps.Add(sink.Install(receivers.Get(j)));
      }

      // Flow monitor
      FlowMonitorHelper flowmon;
      Ptr<FlowMonitor> monitor = flowmon.InstallAll();

      // Run simulation
      Simulator::Stop(Seconds(simulationTime + 1.0));
      Simulator::Run();

      // Collect and save results
      monitor->CheckForLostPackets();
      Ptr<Ipv4FlowClassifier> classifier = DynamicCast<Ipv4FlowClassifier>(flowmon.GetClassifier());
      std::map<FlowId, FlowMonitor::FlowStats> stats = monitor->GetFlowStats();

      for (auto &flow : stats)
      {
        Ipv4FlowClassifier::FiveTuple t = classifier->FindFlow(flow.first);
        double throughput = flow.second.rxBytes * 8.0 / (simulationTime * 1e6); // Mbps
        double avgDelay = (flow.second.rxPackets > 0)
                              ? (flow.second.delaySum.GetSeconds() / flow.second.rxPackets)
                              : 0;

        out << variant << "," 
            << (i + 1) << ","
            << scenarios[i].description << ","
            << scenarios[i].bandwidth << ","
            << scenarios[i].delay << ","
            << scenarios[i].bufferPackets << ","
            << scenarios[i].numFlows << ","
            << flow.first << ","
            << t.sourceAddress << ","
            << t.destinationAddress << ","
            << throughput << ","
            << avgDelay << ","
            << flow.second.lostPackets << ","
            << flow.second.txPackets << ","
            << flow.second.rxPackets << "\n";

        std::cout << "  Flow " << flow.first << ": "
                  << "Throughput=" << throughput << " Mbps, "
                  << "Delay=" << avgDelay << " s, "
                  << "Lost=" << flow.second.lostPackets << std::endl;
      }

      Simulator::Destroy();
    }
  }

  out.close();
  std::cout << "\n✅ All simulations completed! Results saved to results.csv ✅\n";
  return 0;
}