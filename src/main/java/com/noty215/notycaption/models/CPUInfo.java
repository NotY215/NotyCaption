package com.noty215.notycaption.models;

import java.util.List;

/**
 * CPU Information Data Class
 */
public class CPUInfo {
    private String name;
    private String vendor;
    private String architecture;
    private int coresPhysical;
    private int coresLogical;
    private int threads;
    private double baseFrequency;
    private double maxFrequency;
    private double currentFrequency;
    private double temperature;
    private double utilization;
    private double powerUsage;
    private long cacheL1;
    private long cacheL2;
    private long cacheL3;
    private List<String> instructionSets;
    private boolean virtualization;
    private boolean hypervisor;
    private boolean smtEnabled;
    private boolean turboEnabled;
    private boolean overclocked;
    private Double voltage;
    private Integer tdp;
    private String socket;
    private Integer stepping;
    private Integer model;
    private Integer family;
    private Integer extFamily;
    private Integer extModel;
    private String microcode;
    private String cpuid;
    private String serial;

    // Constructors
    public CPUInfo() {}

    public CPUInfo(String name, String vendor, String architecture, int coresPhysical, int coresLogical,
                   int threads, double baseFrequency, double maxFrequency, double currentFrequency,
                   double temperature, double utilization, double powerUsage, long cacheL1, long cacheL2,
                   long cacheL3, List<String> instructionSets, boolean virtualization, boolean hypervisor,
                   boolean smtEnabled, boolean turboEnabled, boolean overclocked) {
        this.name = name;
        this.vendor = vendor;
        this.architecture = architecture;
        this.coresPhysical = coresPhysical;
        this.coresLogical = coresLogical;
        this.threads = threads;
        this.baseFrequency = baseFrequency;
        this.maxFrequency = maxFrequency;
        this.currentFrequency = currentFrequency;
        this.temperature = temperature;
        this.utilization = utilization;
        this.powerUsage = powerUsage;
        this.cacheL1 = cacheL1;
        this.cacheL2 = cacheL2;
        this.cacheL3 = cacheL3;
        this.instructionSets = instructionSets;
        this.virtualization = virtualization;
        this.hypervisor = hypervisor;
        this.smtEnabled = smtEnabled;
        this.turboEnabled = turboEnabled;
        this.overclocked = overclocked;
    }

    // Getters and Setters
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getVendor() { return vendor; }
    public void setVendor(String vendor) { this.vendor = vendor; }

    public String getArchitecture() { return architecture; }
    public void setArchitecture(String architecture) { this.architecture = architecture; }

    public int getCoresPhysical() { return coresPhysical; }
    public void setCoresPhysical(int coresPhysical) { this.coresPhysical = coresPhysical; }

    public int getCoresLogical() { return coresLogical; }
    public void setCoresLogical(int coresLogical) { this.coresLogical = coresLogical; }

    public int getThreads() { return threads; }
    public void setThreads(int threads) { this.threads = threads; }

    public double getBaseFrequency() { return baseFrequency; }
    public void setBaseFrequency(double baseFrequency) { this.baseFrequency = baseFrequency; }

    public double getMaxFrequency() { return maxFrequency; }
    public void setMaxFrequency(double maxFrequency) { this.maxFrequency = maxFrequency; }

    public double getCurrentFrequency() { return currentFrequency; }
    public void setCurrentFrequency(double currentFrequency) { this.currentFrequency = currentFrequency; }

    public double getTemperature() { return temperature; }
    public void setTemperature(double temperature) { this.temperature = temperature; }

    public double getUtilization() { return utilization; }
    public void setUtilization(double utilization) { this.utilization = utilization; }

    public double getPowerUsage() { return powerUsage; }
    public void setPowerUsage(double powerUsage) { this.powerUsage = powerUsage; }

    public long getCacheL1() { return cacheL1; }
    public void setCacheL1(long cacheL1) { this.cacheL1 = cacheL1; }

    public long getCacheL2() { return cacheL2; }
    public void setCacheL2(long cacheL2) { this.cacheL2 = cacheL2; }

    public long getCacheL3() { return cacheL3; }
    public void setCacheL3(long cacheL3) { this.cacheL3 = cacheL3; }

    public List<String> getInstructionSets() { return instructionSets; }
    public void setInstructionSets(List<String> instructionSets) { this.instructionSets = instructionSets; }

    public boolean isVirtualization() { return virtualization; }
    public void setVirtualization(boolean virtualization) { this.virtualization = virtualization; }

    public boolean isHypervisor() { return hypervisor; }
    public void setHypervisor(boolean hypervisor) { this.hypervisor = hypervisor; }

    public boolean isSmtEnabled() { return smtEnabled; }
    public void setSmtEnabled(boolean smtEnabled) { this.smtEnabled = smtEnabled; }

    public boolean isTurboEnabled() { return turboEnabled; }
    public void setTurboEnabled(boolean turboEnabled) { this.turboEnabled = turboEnabled; }

    public boolean isOverclocked() { return overclocked; }
    public void setOverclocked(boolean overclocked) { this.overclocked = overclocked; }

    public Double getVoltage() { return voltage; }
    public void setVoltage(Double voltage) { this.voltage = voltage; }

    public Integer getTdp() { return tdp; }
    public void setTdp(Integer tdp) { this.tdp = tdp; }

    public String getSocket() { return socket; }
    public void setSocket(String socket) { this.socket = socket; }

    public Integer getStepping() { return stepping; }
    public void setStepping(Integer stepping) { this.stepping = stepping; }

    public Integer getModel() { return model; }
    public void setModel(Integer model) { this.model = model; }

    public Integer getFamily() { return family; }
    public void setFamily(Integer family) { this.family = family; }

    public Integer getExtFamily() { return extFamily; }
    public void setExtFamily(Integer extFamily) { this.extFamily = extFamily; }

    public Integer getExtModel() { return extModel; }
    public void setExtModel(Integer extModel) { this.extModel = extModel; }

    public String getMicrocode() { return microcode; }
    public void setMicrocode(String microcode) { this.microcode = microcode; }

    public String getCpuid() { return cpuid; }
    public void setCpuid(String cpuid) { this.cpuid = cpuid; }

    public String getSerial() { return serial; }
    public void setSerial(String serial) { this.serial = serial; }

    @Override
    public String toString() {
        return String.format("CPU: %s (%d cores) - Usage: %.1f%% - Temp: %.0f°C",
                name, coresPhysical, utilization, temperature);
    }
}