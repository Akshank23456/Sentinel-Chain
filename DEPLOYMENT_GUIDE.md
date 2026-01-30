# Device Kill Switch - Smart Contract Implementation

## 📋 Overview

This project implements an automated device security system using blockchain technology. When a threat is detected by a Python monitoring agent, it triggers a smart contract that instantly locks the compromised device on-chain. In a production environment, this would cut internet access to the infected device.

## 🏗️ Architecture

```
┌─────────────────┐
│  Python Agent   │
│ (Threat Monitor)│
└────────┬────────┘
         │ Detects threat
         │
         ▼
┌─────────────────────────┐
│  reportInfection()      │
│  Smart Contract Call    │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Blockchain Update      │
│  Status → LOCKED        │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Real-world Action      │
│  Cut Internet Access    │
└─────────────────────────┘
```

## 📁 Project Structure

```
.
├── DeviceKillSwitch.sol      # Smart contract (Solidity)
├── kill_switch_agent.py      # Python integration agent
├── deployment_guide.md        # This file
└── requirements.txt           # Python dependencies
```

## 🔧 Components

### 1. Smart Contract (`DeviceKillSwitch.sol`)

**Key Features:**
- **Device Registration**: Devices must be registered before monitoring
- **Status Management**: Four states (ACTIVE, LOCKED, SUSPENDED, OFFLINE)
- **Threat Reporting**: Automated infection reporting with details
- **Access Control**: Only authorized agents can trigger kill switch
- **Audit Trail**: Complete history of all threats and status changes
- **Ownership**: Device owners can unlock their own devices

**Core Functions:**
```solidity
registerDevice(deviceId)                    // Register new device
reportInfection(deviceId, type, desc)       // Trigger kill switch
unlockDevice(deviceId)                      // Restore access
getDeviceStatus(deviceId)                   // Check current status
getDeviceThreats(deviceId)                  // View threat history
```

### 2. Python Agent (`kill_switch_agent.py`)

**Key Features:**
- **Web3 Integration**: Connects to any Ethereum-compatible blockchain
- **Transaction Management**: Handles signing, gas, nonces automatically
- **Error Handling**: Robust error catching and reporting
- **Status Monitoring**: Real-time device status queries
- **Threat Tracking**: Complete threat history retrieval

**Core Methods:**
```python
register_device(device_id)                          # Register device
report_infection(device_id, type, description)      # Trigger lockdown
unlock_device(device_id)                            # Unlock after remediation
get_device_status(device_id)                        # Check status
get_threat_history(device_id)                       # View all threats
```

## 🚀 Deployment Guide

### Prerequisites

1. **Blockchain Node**: Ganache, Hardhat, or testnet access
2. **Python 3.8+**: For the agent
3. **Solidity Compiler**: For contract compilation
4. **Web3 Provider**: RPC endpoint to blockchain

### Step 1: Install Dependencies

```bash
# Install Python dependencies
pip install web3 python-dotenv

# Or use requirements.txt
pip install -r requirements.txt
```

### Step 2: Compile the Smart Contract

Using Hardhat:
```bash
npx hardhat compile
```

Using Remix:
1. Open https://remix.ethereum.org
2. Create new file `DeviceKillSwitch.sol`
3. Paste contract code
4. Compile with Solidity 0.8.0+
5. Note the ABI (needed for Python agent)

### Step 3: Deploy the Contract

**Option A: Using Hardhat**
```javascript
// scripts/deploy.js
async function main() {
  const DeviceKillSwitch = await ethers.getContractFactory("DeviceKillSwitch");
  const killSwitch = await DeviceKillSwitch.deploy();
  await killSwitch.deployed();
  console.log("Contract deployed to:", killSwitch.address);
}

main();
```

Run:
```bash
npx hardhat run scripts/deploy.js --network localhost
```

**Option B: Using Remix**
1. Go to "Deploy & Run Transactions"
2. Select environment (Injected Web3 for MetaMask, or VM for testing)
3. Click "Deploy"
4. Copy the contract address

### Step 4: Authorize the Python Agent

After deployment, authorize your agent to report threats:

```javascript
// Using Hardhat console
const killSwitch = await ethers.getContractAt("DeviceKillSwitch", "CONTRACT_ADDRESS");
await killSwitch.authorizeAgent("AGENT_ADDRESS");
```

Or in Remix:
1. Call `authorizeAgent` function
2. Input your agent's Ethereum address
3. Confirm transaction

### Step 5: Configure the Python Agent

Create a `.env` file:
```env
CONTRACT_ADDRESS=0x...
WEB3_PROVIDER=http://127.0.0.1:8545
PRIVATE_KEY=0x...
```

Update `kill_switch_agent.py`:
```python
from dotenv import load_dotenv
import os

load_dotenv()

CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
WEB3_PROVIDER = os.getenv("WEB3_PROVIDER")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
```

### Step 6: Load Contract ABI

Save the compiled ABI to `contract_abi.json`, then:

```python
import json

with open('contract_abi.json', 'r') as f:
    CONTRACT_ABI = json.load(f)

agent = DeviceKillSwitchAgent(
    contract_address=CONTRACT_ADDRESS,
    contract_abi=CONTRACT_ABI,
    web3_provider=WEB3_PROVIDER,
    private_key=PRIVATE_KEY
)
```

## 💻 Usage Examples

### Register a Device

```python
agent = DeviceKillSwitchAgent(...)
agent.register_device("LAPTOP-001")
```

### Simulate Threat Detection and Lockdown

```python
# Monitor for threats (pseudo-code)
if threat_detected():
    agent.report_infection(
        device_id="LAPTOP-001",
        threat_type="ransomware",
        description="WannaCry variant detected encrypting files"
    )
    # Device is now LOCKED on-chain
    # In production: trigger firewall/network disconnect
```

### Check Device Status

```python
status = agent.get_device_status("LAPTOP-001")
# Output: "LOCKED"

is_locked = agent.is_device_locked("LAPTOP-001")
# Output: True
```

### View Threat History

```python
threats = agent.get_threat_history("LAPTOP-001")
for threat in threats:
    print(f"Type: {threat['threat_type']}")
    print(f"Time: {threat['timestamp']}")
    print(f"Description: {threat['description']}")
```

### Unlock After Remediation

```python
# After cleaning the device
agent.unlock_device("LAPTOP-001")
agent.get_device_status("LAPTOP-001")
# Output: "ACTIVE"
```

## 🔐 Security Considerations

1. **Access Control**: Only authorized agents can trigger lockdown
2. **Ownership**: Device owners can unlock their own devices
3. **Admin Powers**: Admin can authorize/revoke agents
4. **Immutable Audit Trail**: All threats recorded on-chain
5. **Private Key Security**: Keep agent private keys secure (use hardware wallets in production)

## 🌐 Network Integration

In production, integrate with network infrastructure:

### Firewall Integration
```python
def cut_internet_access(device_id):
    # Example: Update firewall rules
    os.system(f"iptables -A OUTPUT -s {device_ip} -j DROP")
```

### Router Integration
```python
def disable_device_network(device_mac):
    # Example: Block MAC address on router
    router_api.block_device(mac_address=device_mac)
```

### Complete Workflow
```python
if threat_detected(device_id):
    # 1. Lock on blockchain
    agent.report_infection(device_id, threat_type, description)
    
    # 2. Cut network access
    device_ip = get_device_ip(device_id)
    cut_internet_access(device_ip)
    
    # 3. Send alert
    send_alert_to_admin(device_id, threat_type)
```

## 📊 Monitoring and Events

The contract emits events for all key actions:

```solidity
event DeviceRegistered(string deviceId, address owner, uint256 timestamp)
event ThreatReported(string deviceId, address reporter, string threatType, uint256 timestamp)
event DeviceLocked(string deviceId, address lockedBy, uint256 timestamp)
event DeviceUnlocked(string deviceId, address unlockedBy, uint256 timestamp)
```

Listen to events:
```python
# Monitor for lockdown events
event_filter = agent.contract.events.DeviceLocked.create_filter(fromBlock='latest')

while True:
    for event in event_filter.get_new_entries():
        device_id = event['args']['deviceId']
        print(f"🚨 ALERT: {device_id} has been locked!")
        notify_admin(device_id)
```

## 🧪 Testing

### Local Testing with Ganache

1. Start Ganache:
```bash
ganache-cli
```

2. Deploy contract to local network
3. Run Python agent against localhost:8545

### Test Scenario
```python
# Complete test flow
device_id = "TEST-DEVICE-001"

# 1. Register
agent.register_device(device_id)
assert agent.get_device_status(device_id) == "ACTIVE"

# 2. Trigger lockdown
agent.report_infection(device_id, "malware", "Test infection")
assert agent.is_device_locked(device_id) == True

# 3. Check threat history
threats = agent.get_threat_history(device_id)
assert len(threats) == 1
assert threats[0]['threat_type'] == "malware"

# 4. Unlock
agent.unlock_device(device_id)
assert agent.get_device_status(device_id) == "ACTIVE"
```

## 📈 Gas Costs (Approximate)

- Register Device: ~100,000 gas
- Report Infection: ~150,000 gas
- Unlock Device: ~50,000 gas
- Status Query: Free (read-only)

## 🔄 Upgrade Path

For production systems:

1. **Use Proxy Pattern**: Enable contract upgrades
2. **Add Multi-sig**: Require multiple admins for critical actions
3. **Implement Timelock**: Add delays for unlock operations
4. **Rate Limiting**: Prevent spam attacks
5. **Oracle Integration**: Verify threats from multiple sources

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please submit pull requests or open issues.

## 📧 Support

For questions or issues, please open a GitHub issue or contact the development team.

---

**⚠️ Important**: This is a demonstration implementation. For production use, conduct thorough security audits and testing.
