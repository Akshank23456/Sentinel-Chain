// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title DeviceKillSwitch
 * @dev Smart contract for automated device lockdown in response to security threats
 */
contract DeviceKillSwitch {
    
    // Device status enumeration
    enum DeviceStatus {
        ACTIVE,      // Device is operational
        LOCKED,      // Device is locked due to threat
        SUSPENDED,   // Device is temporarily suspended
        OFFLINE      // Device is offline
    }
    
    // Device information structure
    struct Device {
        address owner;
        DeviceStatus status;
        string deviceId;
        uint256 registeredAt;
        uint256 lastUpdated;
        uint256 threatCount;
        bool exists;
    }
    
    // Threat report structure
    struct ThreatReport {
        string deviceId;
        address reporter;
        string threatType;
        uint256 timestamp;
        string description;
    }
    
    // State variables
    mapping(string => Device) public devices;
    mapping(string => ThreatReport[]) public deviceThreats;
    mapping(address => bool) public authorizedAgents;
    address public admin;
    
    // Events
    event DeviceRegistered(string deviceId, address owner, uint256 timestamp);
    event DeviceStatusChanged(string deviceId, DeviceStatus oldStatus, DeviceStatus newStatus, uint256 timestamp);
    event ThreatReported(string deviceId, address reporter, string threatType, uint256 timestamp);
    event DeviceLocked(string deviceId, address lockedBy, uint256 timestamp);
    event DeviceUnlocked(string deviceId, address unlockedBy, uint256 timestamp);
    event AgentAuthorized(address agent, uint256 timestamp);
    event AgentRevoked(address agent, uint256 timestamp);
    
    // Modifiers
    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can perform this action");
        _;
    }
    
    modifier onlyAuthorizedAgent() {
        require(authorizedAgents[msg.sender] || msg.sender == admin, "Not authorized");
        _;
    }
    
    modifier onlyDeviceOwner(string memory deviceId) {
        require(devices[deviceId].owner == msg.sender, "Not device owner");
        _;
    }
    
    modifier deviceExists(string memory deviceId) {
        require(devices[deviceId].exists, "Device not registered");
        _;
    }
    
    // Constructor
    constructor() {
        admin = msg.sender;
        authorizedAgents[msg.sender] = true;
    }
    
    /**
     * @dev Register a new device
     * @param deviceId Unique identifier for the device
     */
    function registerDevice(string memory deviceId) external {
        require(!devices[deviceId].exists, "Device already registered");
        require(bytes(deviceId).length > 0, "Device ID cannot be empty");
        
        devices[deviceId] = Device({
            owner: msg.sender,
            status: DeviceStatus.ACTIVE,
            deviceId: deviceId,
            registeredAt: block.timestamp,
            lastUpdated: block.timestamp,
            threatCount: 0,
            exists: true
        });
        
        emit DeviceRegistered(deviceId, msg.sender, block.timestamp);
    }
    
    /**
     * @dev Report an infection/threat detected on a device
     * @param deviceId The device that has been compromised
     * @param threatType Type of threat detected (e.g., "malware", "ransomware", "phishing")
     * @param description Detailed description of the threat
     */
    function reportInfection(
        string memory deviceId,
        string memory threatType,
        string memory description
    ) external onlyAuthorizedAgent deviceExists(deviceId) {
        Device storage device = devices[deviceId];
        
        // Store the old status for event
        DeviceStatus oldStatus = device.status;
        
        // Lock the device
        device.status = DeviceStatus.LOCKED;
        device.lastUpdated = block.timestamp;
        device.threatCount++;
        
        // Record the threat
        deviceThreats[deviceId].push(ThreatReport({
            deviceId: deviceId,
            reporter: msg.sender,
            threatType: threatType,
            timestamp: block.timestamp,
            description: description
        }));
        
        emit ThreatReported(deviceId, msg.sender, threatType, block.timestamp);
        emit DeviceLocked(deviceId, msg.sender, block.timestamp);
        emit DeviceStatusChanged(deviceId, oldStatus, DeviceStatus.LOCKED, block.timestamp);
    }
    
    /**
     * @dev Unlock a device after threat remediation
     * @param deviceId The device to unlock
     */
    function unlockDevice(string memory deviceId) 
        external 
        deviceExists(deviceId) 
    {
        require(
            msg.sender == devices[deviceId].owner || 
            authorizedAgents[msg.sender] || 
            msg.sender == admin,
            "Not authorized to unlock"
        );
        
        Device storage device = devices[deviceId];
        require(device.status == DeviceStatus.LOCKED, "Device is not locked");
        
        DeviceStatus oldStatus = device.status;
        device.status = DeviceStatus.ACTIVE;
        device.lastUpdated = block.timestamp;
        
        emit DeviceUnlocked(deviceId, msg.sender, block.timestamp);
        emit DeviceStatusChanged(deviceId, oldStatus, DeviceStatus.ACTIVE, block.timestamp);
    }
    
    /**
     * @dev Manually change device status
     * @param deviceId The device to update
     * @param newStatus The new status to set
     */
    function updateDeviceStatus(string memory deviceId, DeviceStatus newStatus) 
        external 
        deviceExists(deviceId) 
    {
        require(
            msg.sender == devices[deviceId].owner || 
            msg.sender == admin,
            "Not authorized"
        );
        
        Device storage device = devices[deviceId];
        DeviceStatus oldStatus = device.status;
        
        device.status = newStatus;
        device.lastUpdated = block.timestamp;
        
        emit DeviceStatusChanged(deviceId, oldStatus, newStatus, block.timestamp);
    }
    
    /**
     * @dev Authorize an agent (Python script/backend) to report threats
     * @param agent Address of the agent to authorize
     */
    function authorizeAgent(address agent) external onlyAdmin {
        require(!authorizedAgents[agent], "Agent already authorized");
        authorizedAgents[agent] = true;
        emit AgentAuthorized(agent, block.timestamp);
    }
    
    /**
     * @dev Revoke agent authorization
     * @param agent Address of the agent to revoke
     */
    function revokeAgent(address agent) external onlyAdmin {
        require(authorizedAgents[agent], "Agent not authorized");
        require(agent != admin, "Cannot revoke admin");
        authorizedAgents[agent] = false;
        emit AgentRevoked(agent, block.timestamp);
    }
    
    /**
     * @dev Get device information
     * @param deviceId The device to query
     */
    function getDeviceInfo(string memory deviceId) 
        external 
        view 
        deviceExists(deviceId) 
        returns (
            address owner,
            DeviceStatus status,
            uint256 registeredAt,
            uint256 lastUpdated,
            uint256 threatCount
        ) 
    {
        Device memory device = devices[deviceId];
        return (
            device.owner,
            device.status,
            device.registeredAt,
            device.lastUpdated,
            device.threatCount
        );
    }
    
    /**
     * @dev Get all threat reports for a device
     * @param deviceId The device to query
     */
    function getDeviceThreats(string memory deviceId) 
        external 
        view 
        deviceExists(deviceId) 
        returns (ThreatReport[] memory) 
    {
        return deviceThreats[deviceId];
    }
    
    /**
     * @dev Get device status
     * @param deviceId The device to query
     */
    function getDeviceStatus(string memory deviceId) 
        external 
        view 
        deviceExists(deviceId) 
        returns (DeviceStatus) 
    {
        return devices[deviceId].status;
    }
    
    /**
     * @dev Check if device is locked
     * @param deviceId The device to query
     */
    function isDeviceLocked(string memory deviceId) 
        external 
        view 
        deviceExists(deviceId) 
        returns (bool) 
    {
        return devices[deviceId].status == DeviceStatus.LOCKED;
    }
    
    /**
     * @dev Transfer device ownership
     * @param deviceId The device to transfer
     * @param newOwner Address of the new owner
     */
    function transferOwnership(string memory deviceId, address newOwner) 
        external 
        onlyDeviceOwner(deviceId) 
    {
        require(newOwner != address(0), "Invalid new owner");
        devices[deviceId].owner = newOwner;
        devices[deviceId].lastUpdated = block.timestamp;
    }
}
