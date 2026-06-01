# PowerScale CTO JSON Generator - User Manual

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Quick Start Guide](#quick-start-guide)
4. [Understanding PSI Codes](#understanding-psi-codes)
5. [Creating Hardware Upgrades](#creating-hardware-upgrades)
6. [PSI Configuration Tools](#psi-configuration-tools)
7. [Advanced Features](#advanced-features)
8. [Troubleshooting](#troubleshooting)
9. [Examples & Workflows](#examples--workflows)
10. [Reference](#reference)

---

## Introduction

### What is the PowerScale CTO JSON Generator?

The **PowerScale CTO JSON Generator** is a comprehensive web-based tool designed for Dell Technologies support engineers and field personnel who need to create hardware upgrade configurations for PowerScale storage systems.

### Key Capabilities

- **CTO JSON Generation**: Create properly formatted hardware upgrade blueprints
- **PSI Code Management**: Browse, validate, and compare PSI (PowerScale Inventory) codes
- **Multi-Generation Support**: Works with Gen 6/MLK, Gen 6.5, and Gen 16 hardware
- **File Management**: Bundled PSI configuration files (.conf) ready for download
- **Package Generation**: Integration with `isi_create_hardware_package` tool

### Who Should Use This Tool?

- Support Engineers creating hardware upgrade packages
- Field Technicians validating configuration changes
- CTO Validation Team members processing upgrade requests
- Anyone needing to generate PowerScale hardware configuration files

---

## Getting Started

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Python | 3.8 | 3.10+ |
| RAM | 512 MB | 1 GB |
| Disk Space | 100 MB | 200 MB |
| Browser | Any modern | Chrome/Firefox latest |

### Supported Operating Systems

- **Windows**: 10, 11
- **Linux**: Ubuntu 20.04+, Debian 10+, RHEL 8+, CentOS 8+, Fedora 35+
- **macOS**: 10.15+ (with Python installed)

### Installation

#### Windows Installation

**Method 1: Manual Installation**
```cmd
# Navigate to the tool directory
cd PowerScale-CTO-Generator

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

**Method 2: Using run.bat**
```cmd
# Double-click run.bat or run from command line
run.bat
```

#### Ubuntu/Linux Installation

**Method 1: Using install.sh (Recommended)**
```bash
cd PowerScale-CTO-Generator
chmod +x install.sh run.sh
./install.sh
```

**Method 2: Using Makefile**
```bash
cd PowerScale-CTO-Generator
make install
make run
```

**Method 3: Manual Installation**
```bash
cd PowerScale-CTO-Generator

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
python3 -m pip install -r requirements.txt

# Run the application
python3 app.py
```

#### macOS Installation

```bash
cd PowerScale-CTO-Generator

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### First Run

After starting the application:

1. Open your web browser
2. Navigate to `http://localhost:5000`
3. You should see the PowerScale CTO JSON Generator interface

---

## Quick Start Guide

### Creating Your First Hardware Upgrade

**Scenario**: You need to upgrade RAM on a Gen 6 PowerScale node from Low to High configuration.

**Steps**:

1. **Start the Application**
   ```bash
   ./run.sh  # Linux/Mac
   # or
   run.bat   # Windows
   ```

2. **Open Browser**
   - Go to `http://localhost:5000`

3. **Configure Node Group**
   - Click "Add Node Group"
   - Set Generation: "Gen 6 / MLK"
   - Enter Serial Numbers: `ABCD1234, EFGH5678`
   
4. **Select PSI Codes**
   - **Compute**: Current = "Low (96GB)" → Target = "High (384GB)"
   - **SSD**: Select "No SSD Change"
   - **NIC**: Select "No NIC Change"

5. **Generate JSON**
   - Click "Generate JSON"
   - Review the preview
   - Click "Download JSON"

6. **Done!** 
   - The file is saved as `CTO_hardware_ABC123_YYYYMMDD_HHMMSS.json`
   - Attach this to your SR email

---

## Understanding PSI Codes

### What are PSI Codes?

**PSI (PowerScale Inventory)** codes are unique identifiers that define specific hardware configurations for PowerScale nodes. Each code represents a specific combination of:

- Memory (DRAM) configuration
- SSD cache drives
- Network interface cards (NICs)

### PSI Code Format

```
001-infinity-compute-low-psi
│   │        │      │   │
│   │        │      │   └── Type identifier
│   │        │      └────── Configuration level
│   │        └────────────── Category
│   └───────────────────────── Platform
└───────────────────────────── Version/ID
```

### Categories

#### 1. Compute PSI Codes (Memory/DRAM)

| PSI Code | Description | Total DRAM |
|----------|-------------|------------|
| `001-infinity-compute-low-psi` | Low (2x16GB DIMMs) | 96GB |
| `001-infinity-compute-low-64GB-psi` | Low w/ 64GB DIMMs | 384GB |
| `001-infinity-compute-med-psi` | Medium | 384GB |
| `001-infinity-compute-high-psi` | High | 384GB |
| `001-infinity-compute-turbo-psi` | Turbo | 768GB |
| `001-infinity-compute-ultra-psi` | Ultra | 1536GB |

**Use Case**: Memory upgrades, performance improvements

#### 2. SSD PSI Codes (Cache Drives)

| PSI Code | Description | Capacity |
|----------|-------------|----------|
| `001-infinity-ssd-0x400gb-psi` | No SSD | N/A |
| `001-infinity-ssd-1x400gb-psi` | 1x 400GB SSD | 400GB |
| `001-infinity-ssd-1x800gb-psi` | 1x 800GB SSD | 800GB |
| `001-infinity-ssd-1x1.6tb-psi` | 1x 1.6TB SSD | 1.6TB |
| `001-infinity-ssd-1x3.2tb-psi` | 1x 3.2TB SSD | 3.2TB |
| `001-infinity-ssd-1x7.68tb-psi` | 1x 7.68TB SSD | 7.68TB |
| `001-infinity-ssd-2x7.68tb-psi` | 2x 7.68TB SSD | 15.36TB |

**Important**: Dual 400GB SSDs (`2x400gb`) is NOT a valid configuration.

#### 3. NIC PSI Codes (Front-End Networking)

| PSI Code | Description | Speed |
|----------|-------------|-------|
| `002-iFEIO-10GBE-B-psi` | 10GbE Base-T | 10 Gbps |
| `001-iFEIO-25GBE-psi` | 25GbE SFP28 | 25 Gbps |
| `001-iFEIO-100GBE-psi` | 100GbE QSFP28 | 100 Gbps |
| `001-iFEIO-200GBE-psi` | 200GbE | 200 Gbps |

**Note**: Gen 6.5/Gen 16 nodes only support NIC upgrades.

---

## Creating Hardware Upgrades

### Node Generation Selection

The tool supports three hardware generations:

#### Gen 6 / MLK
- **Identifier**: Serial Numbers (e.g., `ABCD1234`)
- **Upgrade Options**: SSD, NIC, Compute
- **Use Case**: Traditional PowerScale nodes

#### Gen 6.5 / Gen 16
- **Identifier**: Service Tags (e.g., `ABC1234`)
- **Platform**: B100, P100, F200, F600, F210, F710, F900, F910
- **Upgrade Options**: NIC only
- **Use Case**: PowerEdge-based PowerScale

### Working with Node Groups

A **Node Group** represents a set of nodes that will receive the same hardware upgrade.

#### Adding a Node Group

1. Click **"Add Node Group"**
2. Select the **Node Generation**
3. Enter **Serial Numbers** or **Service Tags**
   - Comma-separated: `ABCD1234, EFGH5678, IJKL9012`
   - Space-separated: `ABCD1234 EFGH5678`
   - One per line: Supported in the text area
4. Select **PSI Codes** for each component

#### Managing Multiple Node Groups

You can create multiple node groups for different upgrade scenarios:

**Example Scenario**:
- **Group 1**: 3 nodes getting RAM upgrade only
- **Group 2**: 2 nodes getting SSD upgrade only
- **Group 3**: 1 node getting both RAM and NIC upgrades

Each group generates separate entries in the JSON output.

### Serial Number / Service Tag Entry

#### Gen 6 Nodes - Serial Numbers
- Format: Alphanumeric, 8 characters
- Example: `ABCD1234`, `EFGH5678`
- Case insensitive: `abcd1234` works the same

**Quick Entry Tips**:
- Paste from Excel/csv files
- The tool auto-parses comma, space, and newline separated values
- Duplicate entries are automatically handled

#### Gen 6.5/Gen 16 - Service Tags
- Format: 7-character alphanumeric
- Example: `ABC1234`, `XYZ5678`
- Platform model is required

---

## PSI Configuration Tools

The tool includes a comprehensive suite for managing PSI configurations.

### PSI Code Browser

Browse the complete database of valid PSI codes.

**How to Use**:
1. Scroll to **"PSI Code Browser"** section
2. Click a category button:
   - **Compute** - Shows memory configurations
   - **SSD** - Shows cache drive options
   - **NIC** - Shows network interface options
3. Review the list of available codes

**What You'll See**:
- PSI Code (e.g., `001-infinity-compute-low-psi`)
- Human-readable name (e.g., "Low (96GB)")
- Source configuration file path

### PSI Configuration Comparison

Compare two PSI codes to see exactly what changes between configurations.

**Use Case**: Verify an upgrade path before implementing it.

**How to Use**:
1. Select **Category** (SSD, NIC, or Compute)
2. Enter **From PSI Code** (current configuration)
3. Enter **To PSI Code** (target configuration)
4. Click **"Compare Configurations"**

**Example**: Compare `001-infinity-compute-low-psi` vs `001-infinity-compute-low-64GB-psi`

```
Differences:
  - dram_1: 16GB → 64GB
  - dram_2: 16GB → 64GB
```

This shows you're upgrading from 16GB DIMMs to 64GB DIMMs.

### PSI Code Validator

Validate that a PSI code exists in the database.

**How to Use**:
1. Enter a PSI code in the text field
2. (Optional) Select a category to narrow the search
3. Click **"Validate"**

**Results**:
- **Valid**: Shows configuration details
- **Invalid**: Code not found in database

**Example**:
```
Valid PSI Code: 001-infinity-ssd-1x400gb-psi
Category: ssd
Name: 400GB SSD
Description: Single 400GB cache SSD
```

### PSI Configuration File Browser

Access and download actual PSI configuration files (.conf) that are bundled with the tool.

**Categories**:
- **Compute Files** - Memory/DRAM configurations
- **SSD Files** - Cache SSD configurations
- **NIC Files** - Front-end NIC configurations

**Features**:
- **View**: Display file contents directly in browser
- **Download**: Save .conf files locally
- **Browse**: Navigate through all bundled files

**Why Use This?**
The `isi_create_hardware_package` tool requires these .conf files. Instead of manually copying them from the plat-psi-conf repository, you can download them directly from this interface.

### Hardware Upgrade Package Generator

Generate complete package information for the `isi_create_hardware_package` tool.

**How to Use**:
1. Configure your node groups with current/target PSI codes
2. Click **"Generate Package Information"**
3. Review the generated information:
   - Package name
   - Package description
   - Number of nodes
   - Destination directory
   - Command syntax

**Output Example**:
```json
{
  "package_name": "hardware_upgrade_ABC123_20250129",
  "nodes_affected": 5,
  "components": ["compute", "ssd"],
  "command": "isi_create_hardware_package -f hardware_upgrade.json"
}
```

**Next Steps**:
1. Save the CTO JSON to a file (e.g., `hardware_upgrade.json`)
2. Run `isi_create_hardware_package -f hardware_upgrade.json`
3. Sign the resulting `.pkg` file
4. Attach to your Service Request

---

## Advanced Features

### JSON Output Format

The generated JSON follows the flat structure matching `isi_psi_tool -v` output:

```json
{
  "nodes": [
    {
      "serial_number": "ABCD1234",
      "compute": {
        "from_psi": "001-infinity-compute-low-psi",
        "to_psi": "001-infinity-compute-high-psi"
      },
      "ssd": {
        "from_psi": "001-infinity-ssd-1x400gb-psi",
        "to_psi": "001-infinity-ssd-1x800gb-psi"
      },
      "nic": {
        "from_psi": "002-iFEIO-10GBE-B-psi",
        "to_psi": "001-iFEIO-25GBE-psi"
      }
    }
  ]
}
```

### Multi-Node Support

The tool supports configuring multiple nodes with the same or different upgrades.

**Same Upgrade for Multiple Nodes**:
- Enter all serials in one node group
- Single PSI code selection applies to all

**Different Upgrades**:
- Create multiple node groups
- Each group has its own PSI code configuration

### Validation Rules

The tool enforces these rules:

1. **At least one hardware component** must be configured (SSD, NIC, or Compute)
2. **Serial numbers required** for Gen 6/MLK nodes
3. **Service tags required** for Gen 6.5/Gen 16 nodes
4. **Platform model required** for Gen 6.5/Gen 16 nodes
5. **No dual 400GB SSDs** - This is not a valid configuration

---

## Troubleshooting

### Installation Issues

#### "externally-managed-environment" Error (Ubuntu 22.04+)

**Problem**: Ubuntu prevents direct pip installs.

**Solution**: Use the install script which handles this:
```bash
./install.sh
```

Or manually use the virtual environment:
```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

#### Missing Python

**Windows**: Download from [python.org](https://python.org)
**Ubuntu**: `sudo apt install python3 python3-venv python3-pip`
**RHEL/CentOS**: `sudo yum install python3 python3-virtualenv`

#### Port Already in Use

**Error**: `Address already in use`

**Solution**: Either:
1. Stop the other application using port 5000
2. Change the port in `app.py`: `app.run(port=5001)`

### Runtime Issues

#### "Validation Error: At least one hardware component must be configured"

**Cause**: No PSI codes selected for SSD, NIC, or Compute

**Solution**: Select at least one:
- If only doing RAM upgrade: Select Compute codes
- If only doing SSD upgrade: Select SSD codes
- If only doing NIC upgrade: Select NIC codes

#### "Missing Required Fields"

**Cause**: 
- Gen 6 nodes without serial numbers
- Gen 6.5 nodes without service tags or platform

**Solution**: Fill in all required fields for the selected generation.

#### PSI Code Not in Dropdown

**Cause**: Code not in the bundled database

**Solution**:
1. Check your `isi_psi_tool -v` output for the exact code
2. Contact the tool developer to add missing PSI codes
3. Use the PSI Code Validator to confirm the code exists

### File Issues

#### Missing psi_database.py

**Error**: `ModuleNotFoundError: No module named 'psi_database'`

**Solution**: Ensure `psi_database.py` is in the same directory as `app.py`

#### Missing psi_configs Directory

**Warning**: `psi_configs/ directory not found`

**Solution**: The PSI File Browser won't work, but JSON generation will. Re-install to get bundled files.

---

## Examples & Workflows

### Example 1: Simple RAM Upgrade (Gen 6)

**Scenario**: Upgrade 2 nodes from Low to High memory

**Steps**:
1. Add Node Group
2. Generation: Gen 6 / MLK
3. Serials: `ABCD1234, EFGH5678`
4. Compute: Current = "Low (96GB)", Target = "High (384GB)"
5. SSD: "No SSD Change"
6. NIC: "No NIC Change"
7. Generate & Download

**Result**: JSON with 2 nodes, compute upgrades only

### Example 2: SSD Upgrade (Gen 6)

**Scenario**: Upgrade cache from 400GB to 1.6TB

**Steps**:
1. Add Node Group
2. Generation: Gen 6 / MLK
3. Serials: `ABCD1234`
4. Compute: "No Compute Change"
5. SSD: Current = "400GB", Target = "1.6TB"
6. NIC: "No NIC Change"
7. Generate & Download

**Result**: JSON with SSD upgrade only

### Example 3: Mixed Upgrades

**Scenario**: Different nodes need different upgrades

**Group 1 - RAM Upgrade**:
- Serials: `ABCD1234, EFGH5678`
- Compute: Low → High
- SSD: No Change
- NIC: No Change

**Group 2 - SSD Upgrade**:
- Serials: `IJKL9012, MNOP3456`
- Compute: No Change
- SSD: 400GB → 800GB
- NIC: No Change

**Group 3 - NIC Upgrade**:
- Serials: `QRST7890`
- Compute: No Change
- SSD: No Change
- NIC: 10GbE → 25GbE

**Result**: Single JSON with 3 separate node configurations

### Example 4: Gen 6.5 NIC Upgrade

**Scenario**: Upgrade F600 platform from 10GbE to 100GbE

**Steps**:
1. Add Node Group
2. Generation: Gen 6.5 / Gen 16
3. Platform: F600
4. Service Tags: `ABC1234`
5. NIC: Current = "10GbE Base-T", Target = "100GbE"
6. Generate & Download

**Result**: JSON formatted for Gen 6.5 platform

### Example 5: Using PSI File Browser for Package Creation

**Scenario**: Create a hardware package using `isi_create_hardware_package`

**Steps**:
1. Configure your node groups
2. Click "Generate Package Information"
3. Note the destination directory shown
4. Click "Download JSON"
5. Go to PSI File Browser section
6. Download required .conf files:
   - Click "Compute Files" → Download target compute config
   - Click "SSD Files" → Download target SSD config
   - Click "NIC Files" → Download target NIC config
7. Run the command shown in Package Info

---

## Reference

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + Enter` | Generate JSON |
| `Tab` | Navigate between fields |
| `Esc` | Close modal dialogs |

### File Locations

| File | Purpose |
|------|---------|
| `app.py` | Main Flask application |
| `psi_database.py` | PSI code definitions |
| `requirements.txt` | Python dependencies |
| `templates/index.html` | Web interface |
| `psi_configs/` | Bundled .conf files |
| `install.sh` | Linux installer |
| `run.sh` | Linux launcher |
| `run.bat` | Windows launcher |

### API Endpoints

The tool exposes these REST API endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main web interface |
| `/api/generate` | POST | Generate CTO JSON |
| `/api/validate-serials` | POST | Validate serial/tag format |
| `/api/validate-psi` | POST | Validate PSI code |
| `/api/psi-suggest` | POST | Get PSI code suggestions |
| `/api/psi-compare` | POST | Compare two PSI codes |
| `/api/psi-browser` | GET | Browse PSI codes |
| `/api/psi-configs` | GET | List bundled .conf files |
| `/api/psi-configs/download/<path>` | GET | Download .conf file |
| `/api/psi-configs/view/<path>` | GET | View .conf file contents |
| `/api/package-info` | POST | Generate package metadata |

### PSI Code Quick Reference

**Compute (Memory)**:
- Low: 96GB (2x16GB)
- Low-64GB: 384GB (2x64GB)
- Med: 384GB
- High: 384GB
- Turbo: 768GB
- Ultra: 1536GB

**SSD (Cache)**:
- 400GB, 800GB, 1.6TB, 3.2TB, 7.68TB, 15.36TB

**NIC (Front-End)**:
- 10GbE, 25GbE, 100GbE, 200GbE

---

## Support

For issues, questions, or feature requests:

1. Check this manual first
2. Review the README.md
3. Run `make test` to verify installation
4. Check browser console for JavaScript errors
5. Check terminal output for Python errors

### Common Validation Commands

```bash
# Verify installation
make test

# Check bundled files
make verify

# Check Python version
python3 --version

# Check virtual environment
source venv/bin/activate
which python3
```

---

**Version**: 1.2  
**Last Updated**: 2024  
**Compatible With**: PowerScale OneFS 9.0+
