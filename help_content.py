"""Help tab for the ANTA Web GUI: how to use the interface, what every option
does, and when to use which test.

Kept out of app.py so the (long) text is easy to edit. The two tables below
(TEST_NAMES, NEEDS_VALUES) mirror the checkboxes in "Manage Tests"; the
categories themselves come from app.CATEGORY_KEYS so a test that is added to
the app but not described here still shows up in the reference (by key).
"""
from __future__ import annotations

import pandas as pd

# Generated from the checkboxes in app.py (label -> display name and ANTA class;
# NEEDS_VALUES = tests whose parameters ship with example values).
TEST_NAMES = {
    'chk_aaa_authen': ('Verify Authentication Methods', 'VerifyAuthenMethods'),
    'chk_aaa_authz': ('Verify Authorization Methods', 'VerifyAuthzMethods'),
    'chk_aaa_acct_default': ('Verify Accounting Default', 'VerifyAcctDefaultMethods'),
    'chk_aaa_acct_console': ('Verify Accounting Console', 'VerifyAcctConsoleMethods'),
    'chk_aaa_tacacs_src': ('Verify TACACS Source Intf', 'VerifyTacacsSourceIntf'),
    'chk_aaa_tacacs_servers': ('Verify TACACS Servers', 'VerifyTacacsServers'),
    'chk_aaa_tacacs_groups': ('Verify TACACS Server Groups', 'VerifyTacacsServerGroups'),
    'chk_avt_path': ('Verify AVT Path Health', 'VerifyAVTPathHealth'),
    'chk_avt_role': ('Verify AVT Role', 'VerifyAVTRole'),
    'chk_avt_specific_path': ('Verify AVT Specific Path', 'VerifyAVTSpecificPath'),
    'chk_bfd_health': ('Verify BFD Peers Health', 'VerifyBFDPeersHealth'),
    'chk_bfd_intervals': ('Verify BFD Peers Intervals', 'VerifyBFDPeersIntervals'),
    'chk_bfd_protocols': ('Verify BFD Reg Protocols', 'VerifyBFDPeersRegProtocols'),
    'chk_bfd_specific': ('Verify BFD Specific Peers', 'VerifyBFDSpecificPeers'),
    'chk_cfg_rules': ('Verify Running Config Rules', 'VerifyRunningConfig'),
    'chk_cfg_diff': ('Verify Running Config Diffs', 'VerifyRunningConfigDiffs'),
    'chk_cfg_lines': ('Verify Running Config Lines', 'VerifyRunningConfigLines'),
    'chk_cfg_ztp': ('Verify Zero Touch', 'VerifyZeroTouch'),
    'chk_cfg_banner_login': ('Verify Login Banner', 'VerifyBannerLogin'),
    'chk_cfg_banner_motd': ('Verify MOTD Banner', 'VerifyBannerMotd'),
    'chk_conn_lldp': ('Verify LLDP Neighbors', 'VerifyLLDPNeighbors'),
    'chk_conn_ping': ('Verify Reachability', 'VerifyReachability'),
    'chk_cvx_active': ('Verify Active CVX Connections', 'VerifyActiveCVXConnections'),
    'chk_cvx_cluster': ('Verify CVX Cluster Status', 'VerifyCVXClusterStatus'),
    'chk_cvx_mgmt': ('Verify Management CVX', 'VerifyManagementCVX'),
    'chk_cvx_client_mounts': ('Verify MCS Client Mounts', 'VerifyMcsClientMounts'),
    'chk_cvx_server_mounts': ('Verify MCS Server Mounts', 'VerifyMcsServerMounts'),
    'chk_evpn_type5': ('Verify EVPN Type 5 Routes', 'VerifyEVPNType5Routes'),
    'chk_vxlan_conn': ('Verify VXLAN Conn Settings', 'VerifyVxlan1ConnSettings'),
    'chk_vxlan_intf': ('Verify VXLAN Interface', 'VerifyVxlan1Interface'),
    'chk_vxlan_vvtep': ('Verify VXLAN VVTEP IPs', 'VerifyVxlan1VVTEPIPAddresses'),
    'chk_vxlan_sanity': ('Verify VXLAN Config Sanity', 'VerifyVxlanConfigSanity'),
    'chk_vxlan_vni_binding': ('Verify VXLAN VNI Binding', 'VerifyVxlanVniBinding'),
    'chk_vxlan_vtep': ('Verify VXLAN VTEP', 'VerifyVxlanVtep'),
    'chk_fn_fn44': ('Verify Field Notice 44 Resolution', 'VerifyFieldNotice44Resolution'),
    'chk_fn_fn72': ('Verify Field Notice 72 Resolution', 'VerifyFieldNotice72Resolution'),
    'chk_flow_tracking': ('Verify Hardware Flow Tracker', 'VerifyHardwareFlowTrackerStatus'),
    'chk_greent_policy': ('Verify GreenT Policy', 'VerifyGreenT'),
    'chk_greent_counters': ('Verify GreenT Counters', 'VerifyGreenTCounters'),
    'chk_hw_linecards': ('Verify Linecards Absence', 'VerifyAbsenceOfLinecards'),
    'chk_hw_drops': ('Verify Adverse Drops', 'VerifyAdverseDrops'),
    'chk_hw_chassis': ('Verify Chassis Health', 'VerifyChassisHealth'),
    'chk_hw_cooling_fans': ('Verify Environment Cooling', 'VerifyEnvironmentCooling'),
    'chk_hw_power': ('Verify Environment Power', 'VerifyEnvironmentPower'),
    'chk_hw_sys_cooling': ('Verify Environment System Cooling', 'VerifyEnvironmentSystemCooling'),
    'chk_hw_capacity': ('Verify Hardware Capacity', 'VerifyHardwareCapacityUtilization'),
    'chk_hw_inventory': ('Verify Hardware Inventory', 'VerifyInventory'),
    'chk_hw_module': ('Verify Module Status', 'VerifyModuleStatus'),
    'chk_hw_pcie': ('Verify PCIe Errors', 'VerifyPCIeErrors'),
    'chk_hw_supervisor': ('Verify Supervisor Redundancy', 'VerifySupervisorRedundancy'),
    'chk_hw_temp': ('Verify Temperature', 'VerifyTemperature'),
    'chk_hw_trans': ('Verify Transceivers Manufacturers', 'VerifyTransceiversManufacturers'),
    'chk_hw_trans_temp': ('Verify Transceivers Temperature', 'VerifyTransceiversTemperature'),
    'chk_int_proxy_arp': ('Verify Proxy ARP', 'VerifyIPProxyARP'),
    'chk_int_ill_lacp': ('Verify Illegal LACP', 'VerifyIllegalLACP'),
    'chk_int_disc': ('Verify Interface Discards', 'VerifyInterfaceDiscards'),
    'chk_int_err_dis': ('Verify Interface ErrDisabled', 'VerifyInterfaceErrDisabled'),
    'chk_int_err': ('Verify Interface Errors', 'VerifyInterfaceErrors'),
    'chk_int_ipv4': ('Verify Interface IPv4', 'VerifyInterfaceIPv4'),
    'chk_int_util': ('Verify Interface Utilization', 'VerifyInterfaceUtilization'),
    'chk_int_ber': ('Verify Interfaces BER', 'VerifyInterfacesBER'),
    'chk_int_counter_det': ('Verify Counter Details', 'VerifyInterfacesCounterDetails'),
    'chk_int_ecn': ('Verify ECN Counters', 'VerifyInterfacesECNCounters'),
    'chk_int_egress_drop': ('Verify Egress Queue Drops', 'VerifyInterfacesEgressQueueDrops'),
    'chk_int_optics_rx': ('Verify Optics RX Power', 'VerifyInterfacesOpticsReceivePower'),
    'chk_int_optics_temp': ('Verify Optics Temp', 'VerifyInterfacesOpticsTemperature'),
    'chk_int_pfc': ('Verify PFC Counters', 'VerifyInterfacesPFCCounters'),
    'chk_int_speed': ('Verify Interfaces Speed', 'VerifyInterfacesSpeed'),
    'chk_int_status': ('Verify Interfaces Status', 'VerifyInterfacesStatus'),
    'chk_int_trident': ('Verify Trident Counters', 'VerifyInterfacesTridentCounters'),
    'chk_int_voq': ('Verify VoQ Drops', 'VerifyInterfacesVoqAndEgressQueueDrops'),
    'chk_int_vrrp_mac': ('Verify Virtual Router MAC', 'VerifyIpVirtualRouterMac'),
    'chk_int_l2mtu': ('Verify L2 MTU', 'VerifyL2MTU'),
    'chk_int_l3mtu': ('Verify L3 MTU', 'VerifyL3MTU'),
    'chk_int_lacp_status': ('Verify LACP Status', 'VerifyLACPInterfacesStatus'),
    'chk_int_loopback': ('Verify Loopback Count', 'VerifyLoopbackCount'),
    'chk_int_port_channel': ('Verify Port Channels', 'VerifyPortChannels'),
    'chk_int_svi': ('Verify SVI', 'VerifySVI'),
    'chk_int_storm': ('Verify Storm Control Drops', 'VerifyStormControlDrops'),
    'chk_lanz': ('Verify LANZ Status', 'VerifyLANZ'),
    'chk_log_accounting': ('Verify Logging Accounting', 'VerifyLoggingAccounting'),
    'chk_log_entries': ('Verify Logging Entries', 'VerifyLoggingEntries'),
    'chk_log_errors': ('Verify Logging Errors', 'VerifyLoggingErrors'),
    'chk_log_hostname': ('Verify Logging Hostname', 'VerifyLoggingHostname'),
    'chk_log_hosts': ('Verify Logging Hosts', 'VerifyLoggingHosts'),
    'chk_log_generation': ('Verify Logs Generation', 'VerifyLoggingLogsGeneration'),
    'chk_log_persistent': ('Verify Persistent Logging', 'VerifyLoggingPersistent'),
    'chk_log_source_intf': ('Verify Source Interface', 'VerifyLoggingSourceIntf'),
    'chk_log_timestamp': ('Verify Logging Timestamp', 'VerifyLoggingTimestamp'),
    'chk_log_syslog': ('Verify Syslog Logging', 'VerifySyslogLogging'),
    'chk_mlag_config_sanity': ('Verify MLAG Config Sanity', 'VerifyMlagConfigSanity'),
    'chk_mlag_dual_primary': ('Verify MLAG Dual Primary', 'VerifyMlagDualPrimary'),
    'chk_mlag_interfaces': ('Verify MLAG Interfaces', 'VerifyMlagInterfaces'),
    'chk_mlag_priority': ('Verify MLAG Primary Priority', 'VerifyMlagPrimaryPriority'),
    'chk_mlag_reload_delay': ('Verify MLAG Reload Delay', 'VerifyMlagReloadDelay'),
    'chk_mlag_status': ('Verify MLAG Status', 'VerifyMlagStatus'),
    'chk_igmp_snooping_global': ('Verify IGMP Snooping Global', 'VerifyIGMPSnoopingGlobal'),
    'chk_igmp_snooping_vlans': ('Verify IGMP Snooping VLANs', 'VerifyIGMPSnoopingVlans'),
    'chk_path_sel_health': ('Verify Paths Health', 'VerifyPathsHealth'),
    'chk_path_sel_specific': ('Verify Specific Path', 'VerifySpecificPath'),
    'chk_tcam_profile': ('Verify TCAM Profile', 'VerifyTcamProfile'),
    'chk_uft_mode': ('Verify Unified Forwarding Table Mode', 'VerifyUnifiedForwardingTableMode'),
    'chk_ptp_gm': ('Verify PTP Grandmaster', 'VerifyPtpGMStatus'),
    'chk_ptp_lock': ('Verify PTP Lock Status', 'VerifyPtpLockStatus'),
    'chk_ptp_mode': ('Verify PTP Mode Status', 'VerifyPtpModeStatus'),
    'chk_ptp_offset': ('Verify PTP Offset', 'VerifyPtpOffset'),
    'chk_ptp_port_mode': ('Verify PTP Port Mode', 'VerifyPtpPortModeStatus'),
    'chk_bgp_adv_communities': ('Verify BGP Adv Communities', 'VerifyBGPAdvCommunities'),
    'chk_bgp_exchanged_routes': ('Verify BGP Exchanged Routes', 'VerifyBGPExchangedRoutes'),
    'chk_bgp_nlri': ('Verify BGP NLRI Acceptance', 'VerifyBGPNlriAcceptance'),
    'chk_bgp_asn_cap': ('Verify BGP Peer ASN Cap', 'VerifyBGPPeerASNCap'),
    'chk_bgp_peer_count': ('Verify BGP Peer Count', 'VerifyBGPPeerCount'),
    'chk_bgp_drop_stats': ('Verify BGP Peer Drop Stats', 'VerifyBGPPeerDropStats'),
    'chk_bgp_peer_group': ('Verify BGP Peer Group', 'VerifyBGPPeerGroup'),
    'chk_bgp_md5': ('Verify BGP Peer MD5 Auth', 'VerifyBGPPeerMD5Auth'),
    'chk_bgp_mp_caps': ('Verify BGP Peer MP Caps', 'VerifyBGPPeerMPCaps'),
    'chk_bgp_peer_route_limit': ('Verify BGP Peer Route Limit', 'VerifyBGPPeerRouteLimit'),
    'chk_bgp_refresh_cap': ('Verify BGP Peer Refresh Cap', 'VerifyBGPPeerRouteRefreshCap'),
    'chk_bgp_peer_session': ('Verify BGP Peer Session', 'VerifyBGPPeerSession'),
    'chk_bgp_peer_session_ribd': ('Verify BGP Peer Session RIBD', 'VerifyBGPPeerSessionRibd'),
    'chk_bgp_ttl': ('Verify BGP Peer TTL', 'VerifyBGPPeerTtlMultiHops'),
    'chk_bgp_update_errors': ('Verify BGP Update Errors', 'VerifyBGPPeerUpdateErrors'),
    'chk_bgp_health': ('Verify BGP Peers Health', 'VerifyBGPPeersHealth'),
    'chk_bgp_health_ribd': ('Verify BGP Peers Health RIBD', 'VerifyBGPPeersHealthRibd'),
    'chk_bgp_redistribution': ('Verify BGP Redistribution', 'VerifyBGPRedistribution'),
    'chk_bgp_ecmp': ('Verify BGP Route ECMP', 'VerifyBGPRouteECMP'),
    'chk_bgp_route_paths': ('Verify BGP Route Paths', 'VerifyBGPRoutePaths'),
    'chk_bgp_specific_peers': ('Verify BGP Specific Peers', 'VerifyBGPSpecificPeers'),
    'chk_bgp_timers': ('Verify BGP Timers', 'VerifyBGPTimers'),
    'chk_bgp_route_maps': ('Verify BGP Route Maps', 'VerifyBgpRouteMaps'),
    'chk_bgp_evpn_type2': ('Verify EVPN Type 2 Route', 'VerifyEVPNType2Route'),
    'chk_rt_nexthops': ('Verify IPv4 Route Next Hops', 'VerifyIPv4RouteNextHops'),
    'chk_rt_presence_prefix': ('Verify IPv4 Route Presence Per Prefix', 'VerifyIPv4RoutePresencePerPrefix'),
    'chk_rt_presence_vrf': ('Verify IPv4 Route Presence Per VRF', 'VerifyIPv4RoutePresencePerVRF'),
    'chk_rt_route_type': ('Verify IPv4 Route Type', 'VerifyIPv4RouteType'),
    'chk_rt_model': ('Verify Routing Protocol Model', 'VerifyRoutingProtocolModel'),
    'chk_rt_status': ('Verify Routing Status', 'VerifyRoutingStatus'),
    'chk_rt_size': ('Verify Routing Table Size', 'VerifyRoutingTableSize'),
    'chk_isis_graceful': ('Verify ISIS Graceful Restart', 'VerifyISISGracefulRestart'),
    'chk_isis_intf_mode': ('Verify ISIS Interface Mode', 'VerifyISISInterfaceMode'),
    'chk_isis_neighbor_cnt': ('Verify ISIS Neighbor Count', 'VerifyISISNeighborCount'),
    'chk_isis_neighbor_state': ('Verify ISIS Neighbor State', 'VerifyISISNeighborState'),
    'chk_isis_sr_adj': ('Verify ISIS SR Adj', 'VerifyISISSegmentRoutingAdjacencySegments'),
    'chk_isis_sr_dataplane': ('Verify ISIS SR Dataplane', 'VerifyISISSegmentRoutingDataplane'),
    'chk_isis_sr_tunnels': ('Verify ISIS SR Tunnels', 'VerifyISISSegmentRoutingTunnels'),
    'chk_ospf_max_lsa': ('Verify OSPF Max LSA', 'VerifyOSPFMaxLSA'),
    'chk_ospf_neighbor_cnt': ('Verify OSPF Neighbor Count', 'VerifyOSPFNeighborCount'),
    'chk_ospf_neighbor_state': ('Verify OSPF Neighbor State', 'VerifyOSPFNeighborState'),
    'chk_ospf_specific_neighbors': ('Verify OSPF Specific Neighbors', 'VerifyOSPFSpecificNeighbors'),
    'chk_sec_api_http': ('Verify API HTTP Status', 'VerifyAPIHttpStatus'),
    'chk_sec_api_https_ssl': ('Verify API HTTPS SSL', 'VerifyAPIHttpsSSL'),
    'chk_sec_api_v4_acl': ('Verify API IPv4 ACL', 'VerifyAPIIPv4Acl'),
    'chk_sec_api_v6_acl': ('Verify API IPv6 ACL', 'VerifyAPIIPv6Acl'),
    'chk_sec_ssl_cert': ('Verify SSL Cert', 'VerifyAPISSLCertificate'),
    'chk_sec_banner_login': ('Verify Login Banner', 'VerifyBannerLogin'),
    'chk_sec_banner_motd': ('Verify MOTD Banner', 'VerifyBannerMotd'),
    'chk_sec_entropy': ('Verify Hardware Entropy', 'VerifyHardwareEntropy'),
    'chk_sec_ipsec_health': ('Verify IPSec Health', 'VerifyIPSecConnHealth'),
    'chk_sec_v4_acl': ('Verify IPv4 ACL', 'VerifyIPv4ACL'),
    'chk_sec_fips': ('Verify SSH FIPS', 'VerifySSHFIPSRestrictions'),
    'chk_sec_ssh_v4_acl': ('Verify SSH IPv4 ACL', 'VerifySSHIPv4Acl'),
    'chk_sec_ssh_v6_acl': ('Verify SSH IPv6 ACL', 'VerifySSHIPv6Acl'),
    'chk_ssh_status': ('Verify SSH Status', 'VerifySSHStatus'),
    'chk_sec_ipsec_specific': ('Verify Specific IPSec', 'VerifySpecificIPSecConn'),
    'chk_sec_telnet': ('Verify Telnet Status', 'VerifyTelnetStatus'),
    'chk_svc_dns_lookup': ('Verify DNS Lookup', 'VerifyDNSLookup'),
    'chk_svc_dns_servers': ('Verify DNS Servers', 'VerifyDNSServers'),
    'chk_svc_errdisable_rec': ('Verify Errdisable Recovery', 'VerifyErrdisableRecovery'),
    'chk_hostname': ('Verify Hostname', 'VerifyHostname'),
    'chk_snmp_contact': ('Verify SNMP Contact', 'VerifySnmpContact'),
    'chk_snmp_errors': ('Verify SNMP Errors', 'VerifySnmpErrorCounters'),
    'chk_snmp_group': ('Verify SNMP Group', 'VerifySnmpGroup'),
    'chk_snmp_logging': ('Verify SNMP Logging', 'VerifySnmpHostLogging'),
    'chk_snmp_v4_acl': ('Verify SNMP IPv4 ACL', 'VerifySnmpIPv4Acl'),
    'chk_snmp_v6_acl': ('Verify SNMP IPv6 ACL', 'VerifySnmpIPv6Acl'),
    'chk_snmp_location': ('Verify SNMP Location', 'VerifySnmpLocation'),
    'chk_snmp_notification': ('Verify SNMP Notification', 'VerifySnmpNotificationHost'),
    'chk_snmp_pdu': ('Verify SNMP PDU', 'VerifySnmpPDUCounters'),
    'chk_snmp_source': ('Verify SNMP Source Intf', 'VerifySnmpSourceInterface'),
    'chk_snmp_status': ('Verify SNMP Status', 'VerifySnmpStatus'),
    'chk_snmp_user': ('Verify SNMP User', 'VerifySnmpUser'),
    'chk_sw_extensions': ('Verify EOS Extensions', 'VerifyEOSExtensions'),
    'chk_sw_version': ('Verify EOS Version', 'VerifyEOSVersion'),
    'chk_sw_terminattr': ('Verify TerminAttr Version', 'VerifyTerminAttrVersion'),
    'chk_stp_blocked': ('Verify STP Blocked Ports', 'VerifySTPBlockedPorts'),
    'chk_stp_counters': ('Verify STP Counters', 'VerifySTPCounters'),
    'chk_stp_disabled_vlans': ('Verify STP Disabled VLANs', 'VerifySTPDisabledVlans'),
    'chk_stp_forwarding': ('Verify STP Forwarding Ports', 'VerifySTPForwardingPorts'),
    'chk_stp_mode': ('Verify STP Mode', 'VerifySTPMode'),
    'chk_stp_root_priority': ('Verify STP Root Priority', 'VerifySTPRootPriority'),
    'chk_stp_tc': ('Verify STP Topology Changes', 'VerifyStpTopologyChanges'),
    'chk_stun_client': ('Verify STUN Client', 'VerifyStunClient'),
    'chk_stun_client_trans': ('Verify STUN Client Translation', 'VerifyStunClientTranslation'),
    'chk_stun_status': ('Verify STUN Server', 'VerifyStunServer'),
    'chk_sys_agent_logs': ('Verify Agent Logs', 'VerifyAgentLogs'),
    'chk_sys_cpu': ('Verify CPU Utilization', 'VerifyCPUUtilization'),
    'chk_sys_coredump': ('Verify Coredump', 'VerifyCoredump'),
    'chk_sys_file_presence': ('Verify File Presence', 'VerifyFilePresence'),
    'chk_sys_fs_util': ('Verify File System Util', 'VerifyFileSystemUtilization'),
    'chk_sys_flash_util': ('Verify Flash Util', 'VerifyFlashUtilization'),
    'chk_sys_maintenance': ('Verify Maintenance', 'VerifyMaintenance'),
    'chk_sys_mem': ('Verify Memory Utilization', 'VerifyMemoryUtilization'),
    'chk_sys_ntp': ('Verify NTP', 'VerifyNTP'),
    'chk_sys_ntp_assoc': ('Verify NTP Associations', 'VerifyNTPAssociations'),
    'chk_sys_reload': ('Verify Reload Cause', 'VerifyReloadCause'),
    'chk_sys_uptime': ('Verify Uptime', 'VerifyUptime'),
    'chk_vlan_dynamic': ('Verify Dynamic VLAN Source', 'VerifyDynamicVlanSource'),
    'chk_vlan_internal': ('Verify Internal VLAN Policy', 'VerifyVlanInternalPolicy'),
    'chk_vlan_status': ('Verify VLAN Status', 'VerifyVlanStatus'),
    'chk_adv_sa117': ('Verify Security Advisory 0117 - CVE-2025-0936', 'SA117'),
    'chk_adv_sa140': ('Verify Security Advisory 0140 - CVE-2026-10040', 'SA140'),
    'chk_adv_sa142': ('Verify Security Advisory 0142 - CVE-2026-12546', 'SA142'),
    'chk_adv_sa146': ('Verify Security Advisory 0146', 'SA146'),
    'chk_adv_sa147': ('Verify Security Advisory 0147 - CVE-2026-59995/59996/60001/60002', 'SA147'),
    'chk_adv_sa149': ('Verify Security Advisory 0149 - CVE-2026-73449', 'SA149'),
    'chk_adv_sa150': ('Verify Security Advisory 0150 - CVE-2026-75943/75944/75945/77191', 'SA150'),
    'chk_adv_sa151': ('Verify Security Advisory 0151 - CVE-2026-73451', 'SA151'),
    'chk_adv_sa152': ('Verify Security Advisory 0152 - CVE-2026-19641', 'SA152'),
    'chk_adv_sa153': ('Verify Security Advisory 0153 - CVE-2026-73465/73466/73467', 'SA153'),
    'chk_adv_sa154': ('Verify Security Advisory 0154 - CVE-2026-73458', 'SA154'),
    'chk_adv_sa155': ('Verify Security Advisory 0155 - CVE-2026-19655', 'SA155'),
    'chk_adv_sa156': ('Verify Security Advisory 0156 - CVE-2026-73437', 'SA156'),
    'chk_adv_sa157': ('Verify Security Advisory 0157 - CVE-2026-73442/73443/73444', 'SA157'),
    'chk_adv_sa158': ('Verify Security Advisory 0158 - CVE-2026-73456/73457', 'SA158'),
    'chk_adv_sa159': ('Verify Security Advisory 0159 - CVE-2026-73462', 'SA159'),
    'chk_adv_sa160': ('Verify Security Advisory 0160 - CVE-2026-73446/73459/73460', 'SA160'),
    'chk_adv_sa161': ('Verify Security Advisory 0161 - CVE-2026-73450', 'SA161'),
    'chk_adv_sa162': ('Verify Security Advisory 0162 - CVE-2026-73447', 'SA162'),
    'chk_adv_sa163': ('Verify Security Advisory 0163 - CVE-2026-73461', 'SA163'),
    'chk_adv_sa164': ('Verify Security Advisory 0164 - CVE-2026-73439', 'SA164'),
    'chk_adv_sa165': ('Verify Security Advisory 0165 - CVE-2026-73454', 'SA165'),
    'chk_adv_sa166': ('Verify Security Advisory 0166 - CVE-2026-73464', 'SA166'),
    'chk_adv_sa167': ('Verify Security Advisory 0167 - CVE-2026-73445', 'SA167'),
    'chk_adv_sa168': ('Verify Security Advisory 0168 - CVE-2026-2380', 'SA168'),
    'chk_adv_sa169': ('Verify Security Advisory 0169 - CVE-2026-73463', 'SA169'),
    'chk_adv_sa170': ('Verify Security Advisory 0170 - CVE-2026-19640', 'SA170'),
    'chk_adv_sa171': ('Verify Security Advisory 0171 - CVE-2026-73435/73436', 'SA171'),
    'chk_adv_sa172': ('Verify Security Advisory 0172 - CVE-2026-73438', 'SA172'),
    'chk_adv_sa173': ('Verify Security Advisory 0173 - CVE-2026-73455', 'SA173'),
    'chk_adv_sa174': ('Verify Security Advisory 0174 - CVE-2026-73453', 'SA174'),
    'chk_adv_sa175': ('Verify Security Advisory 0175 - CVE-2026-73468', 'SA175'),
    'chk_adv_sa176': ('Verify Security Advisory 0176 - CVE-2026-73469', 'SA176'),
    'chk_adv_sa177': ('Verify Security Advisory 0177 - CVE-2026-77190', 'SA177'),
    'chk_adv_sa178': ('Verify Security Advisory 0178 - CVE-2026-73440', 'SA178'),
}

NEEDS_VALUES = frozenset({
    'chk_aaa_authen',
    'chk_aaa_authz',
    'chk_aaa_acct_default',
    'chk_aaa_acct_console',
    'chk_aaa_tacacs_src',
    'chk_aaa_tacacs_servers',
    'chk_aaa_tacacs_groups',
    'chk_avt_role',
    'chk_avt_specific_path',
    'chk_bfd_intervals',
    'chk_bfd_protocols',
    'chk_bfd_specific',
    'chk_cfg_rules',
    'chk_cfg_lines',
    'chk_cfg_banner_login',
    'chk_cfg_banner_motd',
    'chk_conn_lldp',
    'chk_conn_ping',
    'chk_cvx_active',
    'chk_cvx_cluster',
    'chk_cvx_mgmt',
    'chk_cvx_server_mounts',
    'chk_evpn_type5',
    'chk_vxlan_conn',
    'chk_vxlan_vvtep',
    'chk_vxlan_vni_binding',
    'chk_vxlan_vtep',
    'chk_flow_tracking',
    'chk_hw_linecards',
    'chk_hw_cooling_fans',
    'chk_hw_power',
    'chk_hw_trans',
    'chk_int_proxy_arp',
    'chk_int_ipv4',
    'chk_int_speed',
    'chk_int_status',
    'chk_int_vrrp_mac',
    'chk_int_l2mtu',
    'chk_int_l3mtu',
    'chk_int_lacp_status',
    'chk_int_loopback',
    'chk_log_entries',
    'chk_log_hosts',
    'chk_log_source_intf',
    'chk_mlag_dual_primary',
    'chk_mlag_priority',
    'chk_mlag_reload_delay',
    'chk_igmp_snooping_global',
    'chk_igmp_snooping_vlans',
    'chk_path_sel_specific',
    'chk_tcam_profile',
    'chk_uft_mode',
    'chk_ptp_gm',
    'chk_bgp_adv_communities',
    'chk_bgp_exchanged_routes',
    'chk_bgp_nlri',
    'chk_bgp_asn_cap',
    'chk_bgp_peer_count',
    'chk_bgp_drop_stats',
    'chk_bgp_peer_group',
    'chk_bgp_md5',
    'chk_bgp_mp_caps',
    'chk_bgp_peer_route_limit',
    'chk_bgp_refresh_cap',
    'chk_bgp_peer_session',
    'chk_bgp_peer_session_ribd',
    'chk_bgp_ttl',
    'chk_bgp_update_errors',
    'chk_bgp_health',
    'chk_bgp_redistribution',
    'chk_bgp_ecmp',
    'chk_bgp_route_paths',
    'chk_bgp_specific_peers',
    'chk_bgp_timers',
    'chk_bgp_route_maps',
    'chk_bgp_evpn_type2',
    'chk_rt_nexthops',
    'chk_rt_presence_prefix',
    'chk_rt_presence_vrf',
    'chk_rt_route_type',
    'chk_rt_size',
    'chk_isis_graceful',
    'chk_isis_intf_mode',
    'chk_isis_neighbor_cnt',
    'chk_isis_sr_adj',
    'chk_isis_sr_dataplane',
    'chk_isis_sr_tunnels',
    'chk_ospf_neighbor_cnt',
    'chk_ospf_specific_neighbors',
    'chk_sec_api_https_ssl',
    'chk_sec_api_v4_acl',
    'chk_sec_api_v6_acl',
    'chk_sec_ssl_cert',
    'chk_sec_banner_login',
    'chk_sec_banner_motd',
    'chk_sec_v4_acl',
    'chk_sec_ssh_v4_acl',
    'chk_sec_ssh_v6_acl',
    'chk_sec_ipsec_specific',
    'chk_svc_dns_lookup',
    'chk_svc_dns_servers',
    'chk_svc_errdisable_rec',
    'chk_hostname',
    'chk_snmp_contact',
    'chk_snmp_group',
    'chk_snmp_logging',
    'chk_snmp_v4_acl',
    'chk_snmp_v6_acl',
    'chk_snmp_location',
    'chk_snmp_notification',
    'chk_snmp_source',
    'chk_snmp_status',
    'chk_snmp_user',
    'chk_sw_version',
    'chk_sw_terminattr',
    'chk_stp_disabled_vlans',
    'chk_stp_forwarding',
    'chk_stp_mode',
    'chk_stp_root_priority',
    'chk_stp_tc',
    'chk_stun_client',
    'chk_stun_client_trans',
    'chk_sys_file_presence',
    'chk_sys_ntp_assoc',
    'chk_sys_uptime',
    'chk_vlan_dynamic',
    'chk_vlan_internal',
    'chk_vlan_status',
})

# Display order for the category guide: everyday health first, niche features last.
CATEGORY_ORDER = [
    "System", "Hardware", "Interfaces", "Connectivity", "Configuration", "Software",
    "BGP", "Routing_Generic", "EVPN_VXLAN", "MLAG_Multicast", "STP", "VLAN",
    "Logging", "Services", "SNMP", "AAA", "Security", "Advisories", "FieldNotices",
    "PTP", "AVT_BFD", "Path_Profiles", "Flow_GreenT", "CVX", "STUN",
]

# category id -> (title, what it covers, use it when, notes)
CATEGORY_GUIDE = {
    "System": (
        "System",
        "Device health basics: CPU, memory, flash and file-system usage, uptime, last reload cause, core dumps, agent crash logs, NTP sync, maintenance mode, and the presence of specific files.",
        "Every routine health check, after a maintenance window, and whenever someone says \"the switch rebooted\" or \"it feels slow\".",
        "Most of these need no values. **Uptime** takes a minimum number of seconds, and **File Presence** takes the file names to look for. A failing **Reload Cause** or **Coredump** is worth investigating even if the switch looks fine now.",
    ),
    "Hardware": (
        "Hardware",
        "Environment and physical health: power supplies, fans and cooling, temperatures, transceivers (manufacturer and temperature), PCIe errors, adverse hardware drops, hardware resource capacity, and modular-chassis checks (supervisors, linecards, modules).",
        "Daily health checks, after any physical work (new optics, PSU or fan swap), and before relying on a switch for new traffic.",
        "Chassis, supervisor, linecard and module tests are meant for modular platforms; on fixed-form switches expect them to be skipped or not applicable. **Transceivers Manufacturers** needs the list of manufacturers you accept; the default is only an example.",
    ),
    "Interfaces": (
        "Interfaces",
        "The largest group (26 tests): interface status and speed, error/discard counters, utilization, MTU, LACP and port-channels, IPv4 addresses, SVIs, loopbacks, optics quality (RX power, temperature, BER), and queue/QoS drop counters (ECN, PFC, VoQ, egress queue, storm control).",
        "Daily checks, before/after a change, and when troubleshooting packet loss, slowness or flapping links.",
        "**Interfaces Status** needs the list of interfaces that should be `up`. Error and discard counters are cumulative since they were last cleared, so an old problem keeps failing the test until the counters are cleared on the switch. The QoS/queue tests only make sense on platforms and designs that use those features.",
    ),
    "Connectivity": (
        "Connectivity",
        "**LLDP Neighbors** (the expected port, neighbor name and neighbor port) and **Reachability** (ping from the switch to chosen destinations).",
        "After cabling or maintenance (does the wiring match the design?), and to prove the switch can reach its gateway, loopbacks or other devices.",
        "Both need your values. Reachability runs *from the switch*, so it shows the switch's view of the network, not yours. LLDP names must match what the neighbor advertises.",
    ),
    "Configuration": (
        "Configuration",
        "Running-config checks: **Running Config Diffs** (running vs startup config), **Running Config Lines** (regex patterns that must be present), **Running Config Rules** (your own rule table: section, match text, mode, and whether the line must be present or absent), Zero Touch status, and login/MOTD banner text.",
        "Compliance checks, and right after a change window to catch a forgotten `write memory`.",
        "**Running Config Diffs** needs no values and is a cheap, high-value check. Rules and Lines are only as good as the patterns you give them; the example rules shipped with the app are just examples.",
    ),
    "Software": (
        "Software",
        "EOS version, TerminAttr (CloudVision agent) version, and installed EOS extensions.",
        "After upgrades and for fleet-wide version compliance.",
        "**EOS Version** takes the version you expect. The default (`4.30.2F`) is only an example, so edit it or every switch will fail.",
    ),
    "BGP": (
        "Routing BGP",
        "24 tests: peer health and counts, specific peers, session details, exchanged routes, paths and ECMP, redistribution, communities, route maps, NLRI acceptance, route limits, ASN cap, MD5 authentication, TTL/multihop, timers, update errors and drop statistics, capabilities, plus EVPN Type 2 routes.",
        "Any BGP or EVPN fabric. Start with **BGP Peers Health** and **BGP Peer Count**; add the specific tests when you need strict validation of one behaviour.",
        "Almost all of these need values (address families, peers, VRFs). The **RIBD** variants are only for switches running the `ribd` routing protocol model; use the normal ones on multi-agent switches. For an EVPN fabric, check both the `ipv4 unicast` and `evpn` address families.",
    ),
    "Routing_Generic": (
        "Routing Generic, OSPF & IS-IS",
        "Routing table checks (route presence per prefix or VRF, route type, next hops, table size, routing protocol model and status), OSPF (neighbor count and state, max LSA, specific neighbors), and IS-IS (neighbor count and state, graceful restart, interface mode, segment routing).",
        "To validate the underlay: neighbors in the expected state, key prefixes (such as a default route) present, and routing table size inside the range you expect.",
        "OSPF and IS-IS tests only apply if that protocol is configured; the result is usually skipped when it is not. Route and table-size tests need your prefixes or limits.",
    ),
    "EVPN_VXLAN": (
        "EVPN & VXLAN",
        "The Vxlan1 interface, VXLAN configuration sanity, VNI-to-VLAN bindings, remote VTEPs, virtual VTEP addresses, connection settings, and EVPN Type 5 routes.",
        "EVPN/VXLAN fabrics: after adding a leaf, a VNI or a tenant, and when overlay traffic does not work.",
        "Pair these with BGP peer health for the `evpn` address family: VXLAN can look healthy while the control plane is down, and the other way round. Not applicable on switches without VXLAN.",
    ),
    "MLAG_Multicast": (
        "MLAG & Multicast",
        "MLAG status, interfaces, config sanity, dual-primary detection, primary priority and reload delay, plus IGMP snooping (global and per VLAN).",
        "On MLAG pairs, especially before and after maintenance on one peer, and after any MLAG or port-channel change.",
        "**MLAG Status** needs no values and is the first one to run. Skip the MLAG tests on switches that are not part of an MLAG pair. IGMP tests only matter where multicast is used.",
    ),
    "STP": (
        "STP",
        "Spanning-tree mode, root priority, blocked and forwarding ports, disabled VLANs, BPDU counters and topology changes.",
        "Layer 2 domains, after changes, and when you suspect loops or instability.",
        "A rising topology-change count is a classic sign of a flapping link. Most of these need the VLANs/ports or expected values.",
    ),
    "VLAN": (
        "VLAN",
        "VLAN status, dynamic VLAN source, and the internal VLAN allocation policy.",
        "After VLAN changes, and to confirm that the VLANs a design depends on exist and are active.",
        "VLAN Status needs the VLAN IDs and the status you expect.",
    ),
    "Logging": (
        "LANZ & Logging",
        "Syslog configuration (hosts, source interface, timestamps, persistent logging, accounting, hostname) and log content (recent errors, whether logs are being generated), plus LANZ status.",
        "Logging compliance, and after an incident (**Logging Errors** surfaces recent error-level messages).",
        "Configuration-type tests need your syslog hosts and settings. LANZ only matters if you use it.",
    ),
    "Services": (
        "Services",
        "DNS servers and lookups, errdisable recovery, and the device hostname.",
        "Day-0 acceptance of a new switch and basic compliance.",
        "All of these need your values (DNS servers, expected hostname, recovery settings).",
    ),
    "SNMP": (
        "SNMP",
        "SNMP status, contact and location, users and groups, ACLs, source interface, notification hosts, host logging, and PDU/error counters.",
        "Monitoring-standard compliance, and when the monitoring system cannot poll a switch.",
        "Nearly all need your values, since they compare the switch to *your* SNMP standard.",
    ),
    "AAA": (
        "AAA",
        "Authentication, authorization and accounting method lists, and TACACS+ settings (source interface, servers, server groups).",
        "Access-control audits, after changing AAA or TACACS+ settings, and compliance checks.",
        "All need values. Method lists must match your configuration exactly (for example `group tacacs+, local`).",
    ),
    "Security": (
        "Security",
        "Management-plane hardening: eAPI (HTTP/HTTPS status, SSL, certificates, ACLs), SSH (status, ACLs, FIPS restrictions), Telnet status, banners, IPv4 ACL, IPsec, and hardware entropy.",
        "Hardening audits and compliance: telnet off, eAPI on HTTPS only, management ACLs applied, certificates not about to expire.",
        "Decide what your policy says before reading a result: for example a failing **Telnet Status** means telnet is enabled. Several tests need your ACL names or IPsec peers.",
    ),
    "Advisories": (
        "Security Advisories",
        "35 tests, one per published Arista Security Advisory (SA117 and up). Each checks whether the switch is exposed to that advisory.",
        "Periodic vulnerability review, after upgrades, and when a new advisory is published.",
        "No values needed. A failure means the switch looks exposed; the message and the advisory itself say what to do. Advisories that do not apply to a platform may be skipped.",
    ),
    "FieldNotices": (
        "Field Notices",
        "Checks whether the known issues described in Arista Field Notices 44 and 72 apply to the device and whether they are resolved.",
        "Periodic review and after hardware or boot-loader changes.",
        "No values needed.",
    ),
    "PTP": (
        "PTP",
        "Precision Time Protocol: grandmaster status, lock status, mode, offset and port mode.",
        "Time-sensitive networks (media, finance, telecom).",
        "Skip entirely if you do not use PTP. For ordinary NTP checks use **NTP** and **NTP Associations** in the System category.",
    ),
    "AVT_BFD": (
        "AVT & BFD",
        "Adaptive Virtual Topology (WAN) path health and role, and BFD peer health, intervals, registered protocols and specific peers.",
        "WAN edge devices using AVT, and any routing that depends on BFD for fast failure detection.",
        "Select only if the feature is configured; otherwise the tests have nothing to check.",
    ),
    "Path_Profiles": (
        "Path Selection & Profiles",
        "WAN path selection (health, specific path), the TCAM profile, and the unified forwarding table (UFT) mode.",
        "Platforms that need a specific forwarding profile (TCAM/UFT), and WAN path-selection deployments.",
        "UFT and TCAM checks need the value you expect. Path selection tests only apply to WAN deployments.",
    ),
    "Flow_GreenT": (
        "Flow Tracking & GreenT",
        "Hardware flow tracker status, and GreenT policy and counters.",
        "Only where flow tracking or GreenT is configured.",
        "Skip otherwise.",
    ),
    "CVX": (
        "CVX",
        "CloudVision eXchange (CVX): active connections, cluster status, management CVX, and MCS client/server mounts.",
        "Only if you run CVX (for example as a VXLAN control service).",
        "Skip otherwise.",
    ),
    "STUN": (
        "STUN",
        "STUN client, client translation and server status.",
        "WAN deployments that use STUN.",
        "Skip otherwise.",
    ),
}

# (title, when to run it, what to select)
SCENARIOS = [
    (
        "Quick daily health check",
        "A fast look at every switch, a few minutes.",
        "Start with the ** Basic NRFU (Quick Check)** profile: transceiver manufacturers, power, temperature, uptime, NTP, interface errors, interface status and running-config diffs. Edit the ones that need values (the transceiver manufacturers list, the interface list, and the minimum uptime if 60 seconds is not what you want), then add **CPU**, **Memory**, **Reload Cause**, **Coredump**, **Agent Logs** and **Logging Errors** from the System and Logging categories.",
    ),
    (
        "Before and after a change window",
        "Prove that a change did what you wanted and nothing else.",
        "Run the *same* selection before and after. Good building blocks: Interfaces Status and Errors, BGP Peers Health and Peer Count, OSPF/IS-IS neighbor state, MLAG Status, STP Topology Changes and Blocked Ports, Routing Table Size, LLDP Neighbors, Reachability, and **Running Config Diffs** (catches a forgotten `write memory`). Note the Run ID of each run so you can tell them apart.",
    ),
    (
        "After an upgrade",
        "Confirm the new software is healthy.",
        "EOS Version, TerminAttr Version, EOS Extensions, Reload Cause, Uptime, Coredump, Agent Logs, Logging Errors, Hardware Module Status and Environment tests, the protocols you run (BGP, MLAG, OSPF/IS-IS), then Field Notices and Security Advisories.",
    ),
    (
        "New switch or site acceptance",
        "Day-0 checks before a switch carries traffic.",
        "Hostname, DNS, NTP, SNMP, Logging hosts, AAA/TACACS, SSH and Telnet status, banners, Zero Touch status, LLDP Neighbors (cabling), Interfaces Status/Speed/MTU, EOS Version, Transceivers Manufacturers and the Hardware environment tests.",
    ),
    (
        "Security and compliance audit",
        "Check hardening and standards.",
        "The Security, AAA and SNMP categories, Security Advisories and Field Notices, EOS Version, plus **Running Config Lines/Rules** for any line your standard requires or forbids.",
    ),
    (
        "EVPN/VXLAN fabric validation",
        "Underlay and overlay together.",
        "BGP Peers Health for both `ipv4 unicast` and `evpn`, BGP Peer Count, VXLAN Interface, VXLAN Config Sanity, VNI Binding and VTEP checks, EVPN Type 2/5 routes, MLAG Status on leaf pairs, Routing Table Size and LLDP Neighbors.",
    ),
]

# symptom -> what to run
SYMPTOMS = [
    ("Packet loss or a slow link", "Interface Errors, Discards, Utilization, Optics RX Power, Egress Queue / VoQ Drops, Adverse Drops, CPU Utilization"),
    ("A switch rebooted or is unstable", "Reload Cause, Uptime, Coredump, Agent Logs, Logging Errors, Interface ErrDisabled, STP Topology Changes"),
    ("A neighbor is down", "BGP Peers Health or Specific Peers, OSPF/IS-IS Neighbor State, BFD Peers Health, LLDP Neighbors, Interfaces Status"),
    ("Users on one side cannot reach the other", "Reachability, Routing Table Size, IPv4 Route Presence, VLAN Status, MLAG Status, VXLAN Config Sanity"),
    ("Clocks are wrong or logs do not line up", "NTP, NTP Associations, Logging Timestamp (and the PTP tests if you use PTP)"),
    ("A switch is missing from the results", "Run it from the Raw CLI tab (`show version`); check Credentials, eAPI and the Filter Tags (see Troubleshooting)"),
]

FAQ = [
    (
        "The first full audit shows hundreds of failures",
        "That is expected. Many tests ship with **example values** (for example EOS version `4.30.2F`, interface `Ethernet1`, LLDP neighbor `switch2`). They fail until you replace them with values from your network. Tests marked ⚙️ in the Test reference need your values; the others are plain health checks. Start with the Basic profile, fix the ⚙️ values, and add areas gradually.",
    ),
    (
        "The Execute Tests button is missing and I see \"Inventory is empty\"",
        "Add at least one device, network or IP range in **Manage Inventory** and click **Save Inventory**.",
    ),
    (
        "A switch shows a connectivity error (or an error row for the whole switch)",
        "ANTA could not reach its eAPI, so it was left out of every test. Check that the IP/name is right, that eAPI is enabled on the switch (`management api http-commands`, `no shutdown`), that the username and password are right, and that the machine running this app can reach the switch on HTTPS. If the app runs in Docker on a Mac or Windows PC, remember the container reaches the network through Docker's NAT.",
    ),
    (
        "\"ANTA skipped running tests because a tag filter does not match any device\"",
        "A tag is set in **Filter Tags**, but no device in the inventory has that tag. Clear the filter, or add the tag to the device's `tags` column in Manage Inventory.",
    ),
    (
        "A row says \"skipped\"",
        "The test is not applicable to that switch, for example an OSPF test on a switch that does not run OSPF. It is not a failure.",
    ),
    (
        "A row named \"Catalog Pre-Validator\" with an error",
        "A selected test has invalid or missing parameters, so it was not run at all. Open **Manage Tests**, find that test and fix its values.",
    ),
    (
        "The run stopped after 10 minutes",
        "A whole run is limited to 600 seconds. Run fewer tests or fewer switches at a time (use Filter Tags to split the fleet), and check for switches that do not answer.",
    ),
    (
        "My Save button overwrote a profile",
        "**Save** uses the name in the **Save as** box (it starts as the selected profile's name). If that name already exists you must tick *Overwrite existing …* first; type a different name to create a new profile instead. Use **Load** first if you want to start from a profile, change the selection, then Save.",
    ),
    (
        "My settings and inventory are different on another computer",
        "They are private to each browser. Another browser or computer starts with its own inventory and saved credentials. Use the CSV export/import in Manage Inventory to move an inventory.",
    ),
    (
        "Can I save or export the results?",
        "Yes. After a run, use ** Download CSV** or ** Download JSON** above the results table. Results stay on the Dashboard only until the next run, so download first if you need a record.",
    ),
]


def _needs_label(key: str) -> str:
    return "⚙️ needs your values" if key in NEEDS_VALUES else "✅ no values needed"


def _name(key: str) -> str:
    return TEST_NAMES.get(key, (key, key))[0]


def _cls(key: str) -> str:
    return TEST_NAMES.get(key, (key, key))[1]


def build_test_table(category_keys: dict[str, list[str]]) -> pd.DataFrame:
    """One row per test, used by the "Find a test" search."""
    rows = []
    titles = {cid: CATEGORY_GUIDE.get(cid, (cid,))[0] for cid in category_keys}
    for cid, keys in category_keys.items():
        for key in keys:
            rows.append({
                "Test": _name(key),
                "ANTA class": _cls(key),
                "Category": titles[cid],
                "Values": _needs_label(key),
            })
    return pd.DataFrame(rows, columns=["Test", "ANTA class", "Category", "Values"])


def render_help(st, category_keys: dict[str, list[str]]) -> None:
    """Draw the whole Help tab. ``category_keys`` is app.CATEGORY_KEYS."""
    total = sum(len(v) for v in category_keys.values())
    st.subheader(" Help & User Guide")
    st.caption(
        f"How to use this interface, what every option does, and when to use which test "
        f"({total} tests in {len(category_keys)} categories)."
    )

    t_start, t_ext, t_ui, t_opts, t_which, t_ref, t_faq = st.tabs([
        "Quick start", "External catalogs", "The interface", "Options", "Which tests?", "Test reference", "Troubleshooting",
    ])

    # ------------------------------------------------------------------ quick start
    with t_start:
        st.markdown(
            """
> **Already have ready-made test catalogs (for example generated by Arista AVD)?** Skip steps 3-4 and follow the **External catalogs** tab: you point the app at a folder of catalog files and run them without ticking anything.

### Run your first check in five steps

1. ** Credentials** – enter the username and password of your switches. ANTA talks to them over **eAPI (HTTPS)**, so eAPI must be enabled on every switch (`management api http-commands` → `no shutdown`). Click *Save as Default Credentials* if you want this browser to remember them.
2. ** Manage Inventory** – add your switches. In *Specific Hosts* put the IP or DNS name in **host**, a friendly name in **name**, and optionally **tags** such as `leaf` or `spine`. Click ** Save Inventory**.
3. **Pick what to test** – in the sidebar choose ** Basic NRFU (Quick Check)** and click ** Load**. This selects eight everyday health checks.
4. *(Optional)* ** Manage Tests** – review the selection and fill in the values the tests need (interfaces, versions, neighbors…).
5. ** Dashboard** → **Execute Tests**. When it finishes you get a summary, a table with one row per test per switch, and expandable details for every failure.

> **Tip:** start small. Get the Basic profile green on one or two switches, then add test areas and more switches. Running everything at once on default values produces a wall of failures that mostly means "values not filled in yet".
            """
        )

    # ------------------------------------------------------------------ external catalogs
    with t_ext:
        st.markdown(
            """
### Running tests from an external catalog folder

Instead of ticking tests in Manage Tests, the app can run **one ready-made catalog file per switch**. This is the way to use the catalogs that Arista **AVD** generates (`anta_runner`, folder `avd/anta/avd_catalogs/`), or any catalog files you wrote yourself. The tests come from the files, so they always match what AVD designed for that switch.

#### 1. What the folder must look like

```
/catalogs/
  leaf1.json
  leaf2.json
  spine1.yaml
```

- One file per switch, named after the switch: `<name>.json`, `<name>.yaml` or `<name>.yml`.
- The file content is a normal ANTA catalog (the same format ANTA documents for `anta nrfu --catalog`).
- The part before the extension (`leaf1`) is the **switch name** and must match the **name** column in Manage Inventory exactly, including capital letters.

#### 2. Make the folder visible to the app (done once, by whoever starts the container)

The app only looks at a folder when the environment variable `ANTA_DEVICE_CATALOGS_DIR` is set. With Docker you mount the folder (read-only is enough) and set the variable to the path **inside** the container:

```
docker run -d --name anta-gui -p 8501:8501 \\
  -e ANTA_DEVICE_CATALOGS_DIR=/catalogs \\
  -v /path/to/avd/anta/avd_catalogs:/catalogs:ro \\
  anta-gui
```

After the container starts, an extra profile named **AVD design catalogs** appears in the sidebar. If it does not, the variable is not set (restart the container with `-e`). New or changed files in the folder are picked up on the next page refresh; no restart is needed for that.

#### 3. Describe the switches

1. **Credentials**: enter the eAPI username and password (same for every switch in the run).
2. **Manage Inventory** > *Specific Hosts*: add each switch with its IP in **host** and the catalog name in **name** (`leaf1`). Click **Save Inventory**.

#### 4. Run it

1. In the sidebar, **Select Active Profile** > **AVD design catalogs**. The sidebar lists how many catalog files were found and their names. You do not need Load.
2. Open the **Dashboard**. It says *Ready to execute device catalogs for N switch(es)*.
3. Click **Execute Tests**. Switches run in parallel and the progress line shows which one just finished.
4. Read the summary, the table (one row per test per switch) and the failure details grouped by switch. **Download CSV / JSON** saves the result.

#### 5. Good to know

- **Only switches that have a catalog file are tested.** A switch that is in the inventory but has no file is simply not run.
- A catalog file with **no matching inventory name** shows an error row that lists the inventory names, so you can see the mismatch (usually a spelling or capital-letter difference).
- **Manage Tests is greyed out** while this profile is selected, and **Filter Tags** do not apply, because every file is already scoped to its own switch. Select another profile to go back to ticking tests.
- A switch that does not answer shows as an error row and does not hold up the others.
- Optional settings (environment variables, same place as `ANTA_DEVICE_CATALOGS_DIR`):

| Variable | Default | Meaning |
|---|---|---|
| `ANTA_DEVICE_CATALOG_WORKERS` | 4 | Switches tested in parallel |
| `ANTA_DEVICE_CATALOG_TIMEOUT` | 300 | Seconds allowed per switch |
| `ANTA_DEVICE_CATALOG_ENABLE` | off | Set to `1` to run with `--enable` |
| `ANTA_CATALOG_PROFILE_NAME` | AVD design catalogs | Name of the sidebar profile |

#### When to use this instead of the checkboxes

| Situation | Use |
|---|---|
| AVD manages your fabric and you want to verify the network matches the design | External catalogs |
| Each switch needs different expected values (its own interfaces, neighbors, ASN) | External catalogs |
| Quick health check of unmanaged or unknown switches | Basic / Deep profile |
| One-off test of a few checks | Ticked tests, or Custom YAML |
            """
        )


    # ------------------------------------------------------------------ interface
    with t_ui:
        st.markdown(
            """
### The sidebar (always visible)

| Control | What it does |
|---|---|
| **Select Active Profile** | A named set of ticked tests. The two built-in ones are *Basic NRFU (Quick Check)* and *Deep NRFU (Full Audit)*. If your administrator configured a catalog directory, a third profile, *AVD design catalogs*, appears (see the External catalogs tab). |
| ** Load** | Ticks the tests stored in the selected profile (and replaces the config rules with the profile's). |
| **Save as** + ** Save** | Stores your *current* selection (and Custom YAML) under the name in the box. Same name as an existing profile = overwrite (needs the confirmation tick); a new name creates a new profile. |
| ** Filter Tags** | Limits both the tests and the devices to a tag (see Options). Leave empty to use every device. |
| ** Selected Tests** | How many of the tests are ticked. |
| **Select All / Deselect All** | Ticks or clears every test at once. |

### The tabs

| Tab | Use it to |
|---|---|
| ** Dashboard** | Run the selected tests and read the results. |
| ** Credentials** | Set the switch username and password. |
| ** Manage Inventory** | Add, edit, import and export the switches to test. |
| ** Manage Tests** | Tick tests and fill in their values, one category at a time. The last category, ** Custom YAML**, takes tests written in ANTA catalog format; they are added to every run on top of the ticks (invalid YAML or an unknown test shows up as a *Catalog Pre-Validator* error row). |
| ** Raw CLI** | Run a one-off `show` command on one switch. |
| ** Help** | This guide. |
            """
        )

    # ------------------------------------------------------------------ options
    with t_opts:
        with st.expander(" Profiles: Basic, Deep and your own", expanded=True):
            st.markdown(
                """
A profile is just a saved list of ticked tests.

- ** Basic NRFU (Quick Check)** – eight everyday checks: transceiver manufacturers, power, temperature, uptime, NTP, interface errors, interface status, running-config diffs. Good for a daily look.
- ** Deep NRFU (Full Audit)** – ticks **every** test and includes example config rules. Use it as a starting point for a thorough audit, **not** as a ready-to-run check: many tests need your values (see *Which tests?*).
- **Your own** – tick what you want, then **Save**. Type a new name in **Save as** to keep the original profile untouched; reusing a name overwrites it (after you confirm).
- A profile must be **Loaded** before it affects Manage Tests and the Dashboard. Just selecting it in the dropdown does not change the ticks.
                """
            )
        with st.expander(" Filter Tags"):
            st.markdown(
                """
Tags let you test part of the fleet. Put tags in the **tags** column of **Manage Inventory** (for example `leaf`, `spine`, `site-a`), then type one or more (comma-separated) into **Filter Tags**.

- The tag is added to every test in the catalog **and** used to filter which devices are tested.
- A device is tested only if it carries at least one of the tags you typed.
- If a tag is set that no device has, nothing runs and you get a warning.
- Empty filter = all devices.
                """
            )
        with st.expander(" Manage Inventory"):
            st.markdown(
                """
There are three ways to say which switches to test, each on its own sub-tab:

- **Specific Hosts** – `host` (IP or DNS name), `name` (the label used in results), `tags`.
- **Networks (CIDR)** – a whole subnet, for example `192.0.2.0/24`.
- **IP Ranges** – a `start` and `end` address.

You can type in the table, or use ** Export to CSV** / ** Import from CSV** to edit an inventory in a spreadsheet (separate multiple tags with `;`). Importing only fills the table: click ** Save Inventory** to keep it. The inventory is private to your browser.

The **Raw CLI** tab can only use *Specific Hosts*, not networks or ranges.
                """
            )
        with st.expander(" Credentials"):
            st.markdown(
                """
The username and password are used for every switch in a run. They apply to your current session straight away; **Save as Default Credentials** also stores them for this browser so they are filled in next time. Other people using the app from a different browser do not see them.
                """
            )
        with st.expander(" Manage Tests"):
            st.markdown(
                """
The left column lists the categories; pick one to see its tests on the right.

- **Tick a test** to include it. Ticking reveals the *values* that test needs (interfaces, versions, peers…). Unticked tests are not run.
- **Select Section / Deselect Section** ticks or clears the whole category.
- **Running Config Rules** (in *Configuration*) opens a table where each row is a rule: the config section, the text to match, the mode (`exact` is the default), whether the line must be absent instead of present, and a description.
- Invalid values are caught **before** the run and shown as a *Catalog Pre-Validator* error row, so a typo never silently disappears.
                """
            )
        with st.expander(" Dashboard and reading results"):
            st.markdown(
                """
**Execute Tests** runs the selected tests on the devices that match your inventory and Filter Tags. Each run has a **Run ID**.

The **Test Summary** counts:

| Count | Meaning |
|---|---|
| **Passed** | The switch matched what the test expected. |
| **Failed** | The test ran and the switch did **not** match. Read the message. |
| **Error / Exception** | The test could not complete, for example invalid values, or the switch could not be reached. |
| **Skipped** | Not applicable to that switch (a feature that is not configured). Not a failure. |

Below it, the table lists every test per switch, and **Failed Tests Details** groups the failures by switch with the full message. A switch that cannot be reached appears as an error row instead of vanishing. A whole run is limited to 10 minutes.
                """
            )
        with st.expander(" Raw CLI"):
            st.markdown(
                """
Pick one switch from your *Specific Hosts*, type an EOS command (for example `show mac address-table`) and click **Run Command**. If the output contains tables they are shown as sortable tables, followed by the full text. Use it for quick questions, to double-check a failed test, or to confirm a switch answers at all. It is intended for `show` commands; there is a 60-second limit.
                """
            )

    # ------------------------------------------------------------------ which tests
    with t_which:
        st.markdown(
            """
### How to choose

1. **Know what you are checking for.** A test only means something if you know what a good result looks like for *your* network.
2. **Two kinds of test.** ✅ *Health checks* need no values: they ask the switch whether something is wrong (temperature, errors, core dumps, advisories). ⚙️ *Configuration checks* compare the switch with **your** values (versions, interfaces, neighbors, SNMP settings). They fail until you fill the values in.
3. **Only select what applies.** A switch that does not run OSPF, MLAG or PTP has nothing to check there. Skipped results are harmless, but every extra test makes a run longer and the results harder to read.
4. **Same selection, same switches, before and after.** Comparing two runs is more useful than any single run.
            """
        )
        st.markdown("### Recommended sets for common situations")
        for title, when, what in SCENARIOS:
            with st.expander(title):
                st.markdown(f"**When:** {when}\n\n**Select:** {what}")

        st.markdown("### Troubleshooting by symptom")
        st.table(pd.DataFrame(SYMPTOMS, columns=["Symptom", "Tests worth running"]))

    # ------------------------------------------------------------------ test reference
    with t_ref:
        st.markdown(
            "Every test in **Manage Tests**, grouped by category, with what the group covers and when to use it. "
            "**✅** = health check, no values needed. **⚙️** = compares with your values, so fill them in under *Manage Tests*."
        )

        query = st.text_input(" Find a test", placeholder="e.g. bgp, temperature, ntp, vxlan", key="help_find_test")
        if query.strip():
            table = build_test_table(category_keys)
            q = query.strip().lower()
            mask = (
                table["Test"].str.lower().str.contains(q, regex=False)
                | table["ANTA class"].str.lower().str.contains(q, regex=False)
                | table["Category"].str.lower().str.contains(q, regex=False)
            )
            hits = table[mask]
            if hits.empty:
                st.info("No test matches that text.")
            else:
                st.caption(f"{len(hits)} match(es)")
                st.dataframe(hits, use_container_width=True, hide_index=True)

        ordered = [c for c in CATEGORY_ORDER if c in category_keys] + [c for c in category_keys if c not in CATEGORY_ORDER]
        for cid in ordered:
            keys = category_keys[cid]
            title, covers, use_when, notes = CATEGORY_GUIDE.get(
                cid, (cid, "No description yet.", "", "")
            )
            n_val = sum(1 for k in keys if k in NEEDS_VALUES)
            with st.expander(f"{title} — {len(keys)} tests ({n_val} need your values)"):
                st.markdown(f"**Covers:** {covers}")
                if use_when:
                    st.markdown(f"**Use it when:** {use_when}")
                if notes:
                    st.markdown(f"**Good to know:** {notes}")
                st.markdown(
                    "\n".join(
                        f"- {'⚙️' if k in NEEDS_VALUES else '✅'} **{_name(k)}** · `{_cls(k)}`" for k in keys
                    )
                )

    # ------------------------------------------------------------------ faq
    with t_faq:
        st.markdown("### Common problems")
        for question, answer in FAQ:
            with st.expander(question):
                st.markdown(answer)
        st.caption("This tool is a graphical front end for Arista's open-source ANTA project; the tests and their behaviour come from ANTA.")
