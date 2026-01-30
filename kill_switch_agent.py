"""
Python Agent for interacting with DeviceKillSwitch Smart Contract
This script demonstrates how a threat detection agent would report infections
and trigger the kill switch on the blockchain.
"""

from web3 import Web3
from web3.middleware import geth_poa_middleware
import json
import time
from typing import Optional, Dict, Any
from datetime import datetime

class DeviceKillSwitchAgent:
    """
    Agent for monitoring devices and reporting threats to the blockchain
    """
    
    def __init__(
        self, 
        contract_address: str, 
        contract_abi: list,
        web3_provider: str,
        private_key: str
    ):
        """
        Initialize the agent
        
        Args:
            contract_address: Deployed contract address
            contract_abi: Contract ABI (JSON)
            web3_provider: Web3 provider URL (e.g., HTTP, WebSocket)
            private_key: Private key for the authorized agent account
        """
        # Connect to blockchain
        self.w3 = Web3(Web3.HTTPProvider(web3_provider))
        
        # For POA chains (like some testnets)
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        
        # Verify connection
        if not self.w3.is_connected():
            raise ConnectionError("Failed to connect to blockchain")
        
        # Set up account
        self.account = self.w3.eth.account.from_key(private_key)
        self.w3.eth.default_account = self.account.address
        
        # Load contract
        self.contract_address = Web3.to_checksum_address(contract_address)
        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=contract_abi
        )
        
        print(f"✓ Connected to blockchain")
        print(f"✓ Agent address: {self.account.address}")
        print(f"✓ Contract address: {self.contract_address}")
    
    def register_device(self, device_id: str) -> Dict[str, Any]:
        """
        Register a new device on the blockchain
        
        Args:
            device_id: Unique device identifier
            
        Returns:
            Transaction receipt
        """
        print(f"\n📱 Registering device: {device_id}")
        
        try:
            # Build transaction
            tx = self.contract.functions.registerDevice(device_id).build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gas': 200000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            # Sign and send
            signed_tx = self.w3.eth.account.sign_transaction(tx, self.account.key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            
            # Wait for confirmation
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            print(f"✓ Device registered. TX: {tx_hash.hex()}")
            return receipt
            
        except Exception as e:
            print(f"✗ Error registering device: {e}")
            raise
    
    def report_infection(
        self, 
        device_id: str, 
        threat_type: str, 
        description: str
    ) -> Dict[str, Any]:
        """
        Report a threat and trigger the kill switch
        
        Args:
            device_id: Device that has been compromised
            threat_type: Type of threat (e.g., "malware", "ransomware")
            description: Detailed description of the threat
            
        Returns:
            Transaction receipt
        """
        print(f"\n🚨 THREAT DETECTED!")
        print(f"   Device: {device_id}")
        print(f"   Type: {threat_type}")
        print(f"   Description: {description}")
        print(f"   Triggering kill switch...")
        
        try:
            # Build transaction
            tx = self.contract.functions.reportInfection(
                device_id,
                threat_type,
                description
            ).build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gas': 300000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            # Sign and send
            signed_tx = self.w3.eth.account.sign_transaction(tx, self.account.key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            
            # Wait for confirmation
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            print(f"✓ DEVICE LOCKED! TX: {tx_hash.hex()}")
            print(f"✓ Internet access would be cut in real-world deployment")
            
            return receipt
            
        except Exception as e:
            print(f"✗ Error reporting infection: {e}")
            raise
    
    def unlock_device(self, device_id: str) -> Dict[str, Any]:
        """
        Unlock a device after threat remediation
        
        Args:
            device_id: Device to unlock
            
        Returns:
            Transaction receipt
        """
        print(f"\n🔓 Unlocking device: {device_id}")
        
        try:
            tx = self.contract.functions.unlockDevice(device_id).build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gas': 200000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            signed_tx = self.w3.eth.account.sign_transaction(tx, self.account.key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            print(f"✓ Device unlocked. TX: {tx_hash.hex()}")
            return receipt
            
        except Exception as e:
            print(f"✗ Error unlocking device: {e}")
            raise
    
    def get_device_status(self, device_id: str) -> str:
        """
        Get the current status of a device
        
        Args:
            device_id: Device to query
            
        Returns:
            Device status as string
        """
        status_map = {
            0: "ACTIVE",
            1: "LOCKED",
            2: "SUSPENDED",
            3: "OFFLINE"
        }
        
        try:
            status_code = self.contract.functions.getDeviceStatus(device_id).call()
            status = status_map.get(status_code, "UNKNOWN")
            print(f"📊 Device {device_id} status: {status}")
            return status
        except Exception as e:
            print(f"✗ Error getting device status: {e}")
            raise
    
    def get_device_info(self, device_id: str) -> Dict[str, Any]:
        """
        Get detailed device information
        
        Args:
            device_id: Device to query
            
        Returns:
            Device information dictionary
        """
        try:
            info = self.contract.functions.getDeviceInfo(device_id).call()
            
            device_info = {
                'owner': info[0],
                'status': ['ACTIVE', 'LOCKED', 'SUSPENDED', 'OFFLINE'][info[1]],
                'registered_at': datetime.fromtimestamp(info[2]).isoformat(),
                'last_updated': datetime.fromtimestamp(info[3]).isoformat(),
                'threat_count': info[4]
            }
            
            print(f"\n📋 Device Information for {device_id}:")
            for key, value in device_info.items():
                print(f"   {key}: {value}")
            
            return device_info
            
        except Exception as e:
            print(f"✗ Error getting device info: {e}")
            raise
    
    def get_threat_history(self, device_id: str) -> list:
        """
        Get all threat reports for a device
        
        Args:
            device_id: Device to query
            
        Returns:
            List of threat reports
        """
        try:
            threats = self.contract.functions.getDeviceThreats(device_id).call()
            
            threat_list = []
            for threat in threats:
                threat_data = {
                    'device_id': threat[0],
                    'reporter': threat[1],
                    'threat_type': threat[2],
                    'timestamp': datetime.fromtimestamp(threat[3]).isoformat(),
                    'description': threat[4]
                }
                threat_list.append(threat_data)
            
            print(f"\n🔍 Threat History for {device_id}:")
            print(f"   Total threats: {len(threat_list)}")
            for i, threat in enumerate(threat_list, 1):
                print(f"\n   Threat #{i}:")
                print(f"      Type: {threat['threat_type']}")
                print(f"      Time: {threat['timestamp']}")
                print(f"      Description: {threat['description']}")
            
            return threat_list
            
        except Exception as e:
            print(f"✗ Error getting threat history: {e}")
            raise
    
    def is_device_locked(self, device_id: str) -> bool:
        """
        Check if a device is currently locked
        
        Args:
            device_id: Device to check
            
        Returns:
            True if locked, False otherwise
        """
        try:
            locked = self.contract.functions.isDeviceLocked(device_id).call()
            status = "🔒 LOCKED" if locked else "🔓 UNLOCKED"
            print(f"{status}: {device_id}")
            return locked
        except Exception as e:
            print(f"✗ Error checking lock status: {e}")
            raise


def demo_threat_detection():
    """
    Demonstration of the kill switch in action
    """
    print("=" * 60)
    print("DEVICE KILL SWITCH - THREAT DETECTION DEMO")
    print("=" * 60)
    
    # Configuration (replace with your actual values)
    CONTRACT_ADDRESS = "0x..."  # Your deployed contract address
    WEB3_PROVIDER = "http://127.0.0.1:8545"  # Your blockchain node
    PRIVATE_KEY = "0x..."  # Your authorized agent private key
    
    # Contract ABI (simplified - use full ABI from compilation)
    CONTRACT_ABI = []  # Load from compiled contract JSON
    
    # Initialize agent
    # agent = DeviceKillSwitchAgent(
    #     contract_address=CONTRACT_ADDRESS,
    #     contract_abi=CONTRACT_ABI,
    #     web3_provider=WEB3_PROVIDER,
    #     private_key=PRIVATE_KEY
    # )
    
    # Example workflow
    device_id = "DEVICE-001"
    
    # Step 1: Register device
    # agent.register_device(device_id)
    
    # Step 2: Check initial status
    # agent.get_device_status(device_id)
    
    # Step 3: Simulate threat detection
    print("\n" + "=" * 60)
    print("SIMULATING THREAT DETECTION...")
    print("=" * 60)
    time.sleep(2)
    
    # Step 4: Report infection (TRIGGER KILL SWITCH)
    # agent.report_infection(
    #     device_id=device_id,
    #     threat_type="ransomware",
    #     description="WannaCry ransomware variant detected. Files being encrypted."
    # )
    
    # Step 5: Verify device is locked
    # agent.is_device_locked(device_id)
    # agent.get_device_info(device_id)
    
    # Step 6: View threat history
    # agent.get_threat_history(device_id)
    
    # Step 7: After remediation, unlock device
    # time.sleep(5)
    # agent.unlock_device(device_id)
    # agent.get_device_status(device_id)
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║        DEVICE KILL SWITCH - BLOCKCHAIN INTEGRATION        ║
    ║                                                           ║
    ║  This script demonstrates automated threat response       ║
    ║  using blockchain-based device lockdown.                  ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Uncomment to run demo
    # demo_threat_detection()
    
    print("\n💡 To use this script:")
    print("   1. Deploy the DeviceKillSwitch.sol contract")
    print("   2. Update CONTRACT_ADDRESS, WEB3_PROVIDER, PRIVATE_KEY")
    print("   3. Load the contract ABI from compilation")
    print("   4. Authorize your agent address on the contract")
    print("   5. Run demo_threat_detection()")
