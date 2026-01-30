"""
Practical Integration Example: Kill Switch with Threat Detection
This shows how to integrate the kill switch with actual threat detection logic
"""

import time
import psutil
import os
import json
from dotenv import load_dotenv
from kill_switch_agent import DeviceKillSwitchAgent

class ThreatDetector:
    """
    Simulated threat detection system that monitors for suspicious activity
    In production, this would integrate with antivirus, IDS/IPS, etc.
    """
    
    def __init__(self, agent: DeviceKillSwitchAgent, device_id: str):
        self.agent = agent
        self.device_id = device_id
        self.known_threats = {
            'ransomware': ['wannacry', 'locky', 'cryptolocker'],
            'malware': ['trojan', 'backdoor', 'rootkit'],
            'phishing': ['credential_stealer', 'browser_hijack']
        }
    
    def check_running_processes(self):
        """
        Monitor running processes for suspicious behavior
        """
        print("🔍 Scanning running processes...")
        
        suspicious_processes = []
        for proc in psutil.process_iter(['name', 'cmdline']):
            try:
                proc_name = proc.info['name'].lower()
                
                # Check against known threat signatures
                for threat_type, signatures in self.known_threats.items():
                    for signature in signatures:
                        if signature in proc_name:
                            suspicious_processes.append({
                                'name': proc.info['name'],
                                'type': threat_type,
                                'signature': signature
                            })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        return suspicious_processes
    
    def check_network_connections(self):
        """
        Monitor for suspicious network connections
        """
        print("🌐 Scanning network connections...")
        
        suspicious_connections = []
        known_malicious_ips = ['192.0.2.1', '198.51.100.1']  # Example IPs
        
        for conn in psutil.net_connections(kind='inet'):
            if conn.raddr:
                remote_ip = conn.raddr.ip
                if remote_ip in known_malicious_ips:
                    suspicious_connections.append({
                        'ip': remote_ip,
                        'port': conn.raddr.port,
                        'status': conn.status
                    })
        
        return suspicious_connections
    
    def check_file_modifications(self):
        """
        Monitor for rapid file modifications (ransomware behavior)
        In production, use a proper file system watcher
        """
        print("📁 Checking for suspicious file activity...")
        
        # This is a simplified example
        # Real implementation would use watchdog or similar
        suspicious_activity = False
        
        # Check for rapid file changes in critical directories
        # (simplified for demo)
        
        return suspicious_activity
    
    def trigger_lockdown(self, threat_type: str, description: str):
        """
        Trigger the blockchain kill switch
        """
        print(f"\n{'='*60}")
        print(f"🚨 CRITICAL THREAT DETECTED - INITIATING LOCKDOWN")
        print(f"{'='*60}")
        
        try:
            # Report to blockchain
            receipt = self.agent.report_infection(
                device_id=self.device_id,
                threat_type=threat_type,
                description=description
            )
            
            # In production: Cut network access here
            self.cut_network_access()
            
            # Alert admin
            self.send_alert(threat_type, description)
            
            print(f"\n✓ Device locked on blockchain")
            print(f"✓ Network access disabled")
            print(f"✓ Administrator notified")
            
            return True
            
        except Exception as e:
            print(f"\n✗ Failed to trigger lockdown: {e}")
            return False
    
    def cut_network_access(self):
        """
        Disable network access for the device
        PLACEHOLDER - implement based on your infrastructure
        """
        print("🔌 Cutting network access...")
        
        # Option 1: Firewall rules (Linux)
        # import subprocess
        # subprocess.run(['iptables', '-A', 'OUTPUT', '-j', 'DROP'])
        
        # Option 2: Disable network interface
        # subprocess.run(['ifconfig', 'eth0', 'down'])
        
        # Option 3: Router API call
        # router.block_device(mac_address=get_mac_address())
        
        print("   [SIMULATED] Network access would be cut in production")
    
    def send_alert(self, threat_type: str, description: str):
        """
        Send alert to security team
        """
        print("📧 Sending alert to security team...")
        
        # In production: Send email, SMS, Slack notification, etc.
        alert_message = f"""
        🚨 SECURITY ALERT
        
        Device: {self.device_id}
        Threat Type: {threat_type}
        Description: {description}
        Time: {time.strftime('%Y-%m-%d %H:%M:%S')}
        Status: LOCKED
        
        Immediate action required!
        """
        
        print(f"   [SIMULATED] Alert sent:\n{alert_message}")
    
    def run_continuous_monitoring(self, interval: int = 60):
        """
        Continuously monitor for threats
        
        Args:
            interval: Seconds between scans
        """
        print(f"\n🛡️  Starting continuous threat monitoring")
        print(f"   Scan interval: {interval} seconds")
        print(f"   Device ID: {self.device_id}")
        print(f"   Press Ctrl+C to stop\n")
        
        try:
            while True:
                print(f"\n[{time.strftime('%H:%M:%S')}] Running security scan...")
                
                # Check for threats
                suspicious_procs = self.check_running_processes()
                suspicious_conns = self.check_network_connections()
                suspicious_files = self.check_file_modifications()
                
                # Evaluate threat level
                threat_detected = False
                threat_info = None
                
                if suspicious_procs:
                    threat_detected = True
                    proc = suspicious_procs[0]
                    threat_info = {
                        'type': proc['type'],
                        'description': f"Malicious process detected: {proc['name']} (signature: {proc['signature']})"
                    }
                
                elif suspicious_conns:
                    threat_detected = True
                    conn = suspicious_conns[0]
                    threat_info = {
                        'type': 'network_threat',
                        'description': f"Connection to malicious IP detected: {conn['ip']}:{conn['port']}"
                    }
                
                elif suspicious_files:
                    threat_detected = True
                    threat_info = {
                        'type': 'ransomware',
                        'description': "Suspicious rapid file modification detected"
                    }
                
                if threat_detected:
                    # TRIGGER KILL SWITCH
                    self.trigger_lockdown(
                        threat_type=threat_info['type'],
                        description=threat_info['description']
                    )
                    
                    print("\n🔒 System is now in lockdown mode")
                    print("   Monitoring paused. Manual intervention required.")
                    break
                else:
                    print("✓ No threats detected")
                
                # Wait for next scan
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n⏹️  Monitoring stopped by user")


def main():
    """
    Main execution: Set up and run the integrated threat detection + kill switch
    """
    
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║         INTEGRATED THREAT DETECTION + KILL SWITCH         ║
    ║                                                           ║
    ║  Automated security monitoring with blockchain lockdown   ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    load_dotenv()

    # Configuration
    DEVICE_ID = os.getenv("DEVICE_ID", "WORKSTATION-001")
    CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
    WEB3_PROVIDER = os.getenv("WEB3_PROVIDER", "http://127.0.0.1:8545")
    PRIVATE_KEY = os.getenv("PRIVATE_KEY")
    CONTRACT_ABI = []
    if os.path.exists('DeviceKillSwitch.json'):
        with open('DeviceKillSwitch.json', 'r') as f:
            contract_data = json.load(f)
            CONTRACT_ABI = contract_data.get('abi', [])

    if not CONTRACT_ADDRESS or not PRIVATE_KEY:
        raise ValueError("Missing required environment variables: CONTRACT_ADDRESS, PRIVATE_KEY")
    
    # Initialize kill switch agent
    print("Initializing blockchain agent...")
    agent = DeviceKillSwitchAgent(
        contract_address=CONTRACT_ADDRESS,
        contract_abi=CONTRACT_ABI,
        web3_provider=WEB3_PROVIDER,
        private_key=PRIVATE_KEY
    )

    # Register device if not already registered
    try:
        agent.get_device_status(DEVICE_ID)
    except:
        print(f"Registering device {DEVICE_ID}...")
        agent.register_device(DEVICE_ID)

    # Initialize threat detector
    detector = ThreatDetector(agent=agent, device_id=DEVICE_ID)

    # Start monitoring
    detector.run_continuous_monitoring(interval=30)  # Scan every 30 seconds
    
    print("\n💡 Setup Instructions:")
    print("   1. Deploy DeviceKillSwitch.sol contract")
    print("   2. Update CONTRACT_ADDRESS, WEB3_PROVIDER, PRIVATE_KEY")
    print("   3. Authorize your agent address on the contract")
    print("   4. Uncomment the code above and run")
    print("\n   Then the system will continuously monitor for threats")
    print("   and automatically trigger the kill switch when detected!")


if __name__ == "__main__":
    main()
