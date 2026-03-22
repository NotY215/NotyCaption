package com.noty215.notycaption.models;

import java.util.List;
import java.util.Map;

/**
 * GPU Information Data Class
 */
public class GPUInfo {
    private String name;
    private GPUType type;
    private String vendor;
    private long memoryTotal;
    private long memoryUsed;
    private long memoryFree;
    private double temperature;
    private double utilization;
    private double powerUsage;
    private int clockCore;
    private int clockMemory;
    private String driverVersion;
    private Integer cudaCores;
    private Integer rocmCores;
    private Integer openclUnits;
    private String vulkanVersion;
    private String directxVersion;
    private String openglVersion;
    private String metalVersion;
    private String pcieVersion;
    private Integer pcieLanes;
    private Integer pcieSpeed;
    private String serial;
    private String uuid;
    private String biosVersion;
    private String vbiosVersion;
    private String subsystemId;
    private String deviceId;
    private String revisionId;
    private String boardId;
    private String busId;
    private String domainId;
    private String slotId;
    private Integer linkWidth;
    private String linkSpeed;
    private Integer maxLinkWidth;
    private String maxLinkSpeed;
    private String performanceState;
    private String throttlingReason;
    private boolean eccEnabled;
    private Map<String, Long> eccErrors;
    private String computeMode;
    private boolean persistenceMode;
    private boolean accountingMode;
    private boolean displayMode;
    private boolean displayActive;
    private Integer fanSpeed;
    private Integer fanRpm;
    private Double voltage;
    private Double current;
    private Double powerLimit;
    private Double powerDefaultLimit;
    private Double powerMinLimit;
    private Double powerMaxLimit;
    private Double thermalLimit;
    private Double memoryTemperature;
    private Double boardTemperature;
    private Double hotspotTemperature;
    private Double gpuSlowdownTemperature;
    private Double shutdownTemperature;

    // Constructors
    public GPUInfo() {}

    public GPUInfo(String name, GPUType type, String vendor, long memoryTotal, long memoryUsed,
                   long memoryFree, double temperature, double utilization, double powerUsage,
                   int clockCore, int clockMemory, String driverVersion) {
        this.name = name;
        this.type = type;
        this.vendor = vendor;
        this.memoryTotal = memoryTotal;
        this.memoryUsed = memoryUsed;
        this.memoryFree = memoryFree;
        this.temperature = temperature;
        this.utilization = utilization;
        this.powerUsage = powerUsage;
        this.clockCore = clockCore;
        this.clockMemory = clockMemory;
        this.driverVersion = driverVersion;
    }

    // Getters and Setters
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public GPUType getType() { return type; }
    public void setType(GPUType type) { this.type = type; }

    public String getVendor() { return vendor; }
    public void setVendor(String vendor) { this.vendor = vendor; }

    public long getMemoryTotal() { return memoryTotal; }
    public void setMemoryTotal(long memoryTotal) { this.memoryTotal = memoryTotal; }

    public long getMemoryUsed() { return memoryUsed; }
    public void setMemoryUsed(long memoryUsed) { this.memoryUsed = memoryUsed; }

    public long getMemoryFree() { return memoryFree; }
    public void setMemoryFree(long memoryFree) { this.memoryFree = memoryFree; }

    public double getTemperature() { return temperature; }
    public void setTemperature(double temperature) { this.temperature = temperature; }

    public double getUtilization() { return utilization; }
    public void setUtilization(double utilization) { this.utilization = utilization; }

    public double getPowerUsage() { return powerUsage; }
    public void setPowerUsage(double powerUsage) { this.powerUsage = powerUsage; }

    public int getClockCore() { return clockCore; }
    public void setClockCore(int clockCore) { this.clockCore = clockCore; }

    public int getClockMemory() { return clockMemory; }
    public void setClockMemory(int clockMemory) { this.clockMemory = clockMemory; }

    public String getDriverVersion() { return driverVersion; }
    public void setDriverVersion(String driverVersion) { this.driverVersion = driverVersion; }

    public Integer getCudaCores() { return cudaCores; }
    public void setCudaCores(Integer cudaCores) { this.cudaCores = cudaCores; }

    public Integer getRocmCores() { return rocmCores; }
    public void setRocmCores(Integer rocmCores) { this.rocmCores = rocmCores; }

    public Integer getOpenclUnits() { return openclUnits; }
    public void setOpenclUnits(Integer openclUnits) { this.openclUnits = openclUnits; }

    public String getVulkanVersion() { return vulkanVersion; }
    public void setVulkanVersion(String vulkanVersion) { this.vulkanVersion = vulkanVersion; }

    public String getDirectxVersion() { return directxVersion; }
    public void setDirectxVersion(String directxVersion) { this.directxVersion = directxVersion; }

    public String getOpenglVersion() { return openglVersion; }
    public void setOpenglVersion(String openglVersion) { this.openglVersion = openglVersion; }

    public String getMetalVersion() { return metalVersion; }
    public void setMetalVersion(String metalVersion) { this.metalVersion = metalVersion; }

    public String getPcieVersion() { return pcieVersion; }
    public void setPcieVersion(String pcieVersion) { this.pcieVersion = pcieVersion; }

    public Integer getPcieLanes() { return pcieLanes; }
    public void setPcieLanes(Integer pcieLanes) { this.pcieLanes = pcieLanes; }

    public Integer getPcieSpeed() { return pcieSpeed; }
    public void setPcieSpeed(Integer pcieSpeed) { this.pcieSpeed = pcieSpeed; }

    public String getSerial() { return serial; }
    public void setSerial(String serial) { this.serial = serial; }

    public String getUuid() { return uuid; }
    public void setUuid(String uuid) { this.uuid = uuid; }

    public String getBiosVersion() { return biosVersion; }
    public void setBiosVersion(String biosVersion) { this.biosVersion = biosVersion; }

    public String getVbiosVersion() { return vbiosVersion; }
    public void setVbiosVersion(String vbiosVersion) { this.vbiosVersion = vbiosVersion; }

    public String getSubsystemId() { return subsystemId; }
    public void setSubsystemId(String subsystemId) { this.subsystemId = subsystemId; }

    public String getDeviceId() { return deviceId; }
    public void setDeviceId(String deviceId) { this.deviceId = deviceId; }

    public String getRevisionId() { return revisionId; }
    public void setRevisionId(String revisionId) { this.revisionId = revisionId; }

    public String getBoardId() { return boardId; }
    public void setBoardId(String boardId) { this.boardId = boardId; }

    public String getBusId() { return busId; }
    public void setBusId(String busId) { this.busId = busId; }

    public String getDomainId() { return domainId; }
    public void setDomainId(String domainId) { this.domainId = domainId; }

    public String getSlotId() { return slotId; }
    public void setSlotId(String slotId) { this.slotId = slotId; }

    public Integer getLinkWidth() { return linkWidth; }
    public void setLinkWidth(Integer linkWidth) { this.linkWidth = linkWidth; }

    public String getLinkSpeed() { return linkSpeed; }
    public void setLinkSpeed(String linkSpeed) { this.linkSpeed = linkSpeed; }

    public Integer getMaxLinkWidth() { return maxLinkWidth; }
    public void setMaxLinkWidth(Integer maxLinkWidth) { this.maxLinkWidth = maxLinkWidth; }

    public String getMaxLinkSpeed() { return maxLinkSpeed; }
    public void setMaxLinkSpeed(String maxLinkSpeed) { this.maxLinkSpeed = maxLinkSpeed; }

    public String getPerformanceState() { return performanceState; }
    public void setPerformanceState(String performanceState) { this.performanceState = performanceState; }

    public String getThrottlingReason() { return throttlingReason; }
    public void setThrottlingReason(String throttlingReason) { this.throttlingReason = throttlingReason; }

    public boolean isEccEnabled() { return eccEnabled; }
    public void setEccEnabled(boolean eccEnabled) { this.eccEnabled = eccEnabled; }

    public Map<String, Long> getEccErrors() { return eccErrors; }
    public void setEccErrors(Map<String, Long> eccErrors) { this.eccErrors = eccErrors; }

    public String getComputeMode() { return computeMode; }
    public void setComputeMode(String computeMode) { this.computeMode = computeMode; }

    public boolean isPersistenceMode() { return persistenceMode; }
    public void setPersistenceMode(boolean persistenceMode) { this.persistenceMode = persistenceMode; }

    public boolean isAccountingMode() { return accountingMode; }
    public void setAccountingMode(boolean accountingMode) { this.accountingMode = accountingMode; }

    public boolean isDisplayMode() { return displayMode; }
    public void setDisplayMode(boolean displayMode) { this.displayMode = displayMode; }

    public boolean isDisplayActive() { return displayActive; }
    public void setDisplayActive(boolean displayActive) { this.displayActive = displayActive; }

    public Integer getFanSpeed() { return fanSpeed; }
    public void setFanSpeed(Integer fanSpeed) { this.fanSpeed = fanSpeed; }

    public Integer getFanRpm() { return fanRpm; }
    public void setFanRpm(Integer fanRpm) { this.fanRpm = fanRpm; }

    public Double getVoltage() { return voltage; }
    public void setVoltage(Double voltage) { this.voltage = voltage; }

    public Double getCurrent() { return current; }
    public void setCurrent(Double current) { this.current = current; }

    public Double getPowerLimit() { return powerLimit; }
    public void setPowerLimit(Double powerLimit) { this.powerLimit = powerLimit; }

    public Double getPowerDefaultLimit() { return powerDefaultLimit; }
    public void setPowerDefaultLimit(Double powerDefaultLimit) { this.powerDefaultLimit = powerDefaultLimit; }

    public Double getPowerMinLimit() { return powerMinLimit; }
    public void setPowerMinLimit(Double powerMinLimit) { this.powerMinLimit = powerMinLimit; }

    public Double getPowerMaxLimit() { return powerMaxLimit; }
    public void setPowerMaxLimit(Double powerMaxLimit) { this.powerMaxLimit = powerMaxLimit; }

    public Double getThermalLimit() { return thermalLimit; }
    public void setThermalLimit(Double thermalLimit) { this.thermalLimit = thermalLimit; }

    public Double getMemoryTemperature() { return memoryTemperature; }
    public void setMemoryTemperature(Double memoryTemperature) { this.memoryTemperature = memoryTemperature; }

    public Double getBoardTemperature() { return boardTemperature; }
    public void setBoardTemperature(Double boardTemperature) { this.boardTemperature = boardTemperature; }

    public Double getHotspotTemperature() { return hotspotTemperature; }
    public void setHotspotTemperature(Double hotspotTemperature) { this.hotspotTemperature = hotspotTemperature; }

    public Double getGpuSlowdownTemperature() { return gpuSlowdownTemperature; }
    public void setGpuSlowdownTemperature(Double gpuSlowdownTemperature) { this.gpuSlowdownTemperature = gpuSlowdownTemperature; }

    public Double getShutdownTemperature() { return shutdownTemperature; }
    public void setShutdownTemperature(Double shutdownTemperature) { this.shutdownTemperature = shutdownTemperature; }

    @Override
    public String toString() {
        return String.format("GPU: %s (%s) - Memory: %.1f/%.1f GB - Temp: %.0f°C - Usage: %.1f%%",
                name, vendor, memoryUsed / 1e9, memoryTotal / 1e9, temperature, utilization);
    }
}