# PowerScale CTO JSON Generator

A comprehensive, cross-platform web application for generating Configure-To-Order (CTO) hardware upgrade JSON blueprints for Dell PowerScale storage systems. Features include JSON generation, PSI code validation, configuration comparison, and bundled PSI configuration files.

**Platforms:** Windows 10/11 | Ubuntu 20.04+ | Debian 10+ | RHEL 8+ | CentOS 8+ | Fedora 35+

**📖 Full Documentation: [USER_MANUAL.md](USER_MANUAL.md)**

## System Requirements

- **Python:** 3.8 or higher
- **Memory:** 512 MB RAM minimum
- **Disk:** 100 MB free space
- **Browser:** Any modern web browser (Chrome, Firefox, Edge, Safari)
- **Network:** Local access only (runs on localhost:5000)

## What This Tool Does

The PowerScale CTO JSON Generator helps you:

1. **Create Hardware Upgrade Configurations**: Generate JSON blueprints for PowerScale node hardware upgrades (RAM, NIC, SSD)
2. **PSI Code Management**: Browse, validate, and compare PSI (PowerScale Inventory) codes
3. **Bundled Configuration Files**: Download actual PSI .conf files for use with `isi_create_hardware_package`
4. **Package Generation**: Integration with hardware upgrade packaging workflow
5. **Support Multiple Node Groups**: Configure different hardware specifications for different nodes in the same pool
6. **Export JSON Files**: Download timestamped JSON files ready to attach to SR emails

### Supported Hardware Generations

- **Gen 6 / MLK**: Traditional PowerScale nodes with serial numbers
  - SSD upgrades (400GB, 800GB, 1.6TB, 3.2TB, etc.)
  - Front-End NIC upgrades (10GbE, 25GbE, 40GbE, 100GbE)
  - Memory/Compute upgrades (Low, Medium, High configurations)
  
- **Gen 6.5 / Gen 16**: PowerEdge-based PowerScale nodes with service tags
  - Platform: B100, P100, F200, F600, F210, F710, F900, F910
  - Front-End NIC upgrades only
  - Auto-display NIC slot information

## Installation

### Windows

**Requirements:** Python 3.8 or higher

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

**Or use the batch script:**
```bash
run.bat
```

### Ubuntu/Linux

#### Quick Install (Recommended)

```bash
# Clone or extract the project
cd PowerScale-CTO-Generator

# Run the installer (installs system deps + Python packages)
chmod +x install.sh
./install.sh

# Start the application
./run.sh
```

#### Manual Install

**1. Install system dependencies:**

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

**RHEL/CentOS/Fedora:**
```bash
sudo yum install python3 python3-pip
```

**2. Create virtual environment and install:**
```bash
cd PowerScale-CTO-Generator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**3. Run the application:**
```bash
./run.sh
# Or manually:
python3 app.py
```

#### Using Make (Ubuntu/Linux)

```bash
# Install everything
make install

# Run the application
make run

# Run tests
make test

# Clean up
make clean
```

### All Platforms

After starting the server, open your browser to: **http://localhost:5000**

The application will be accessible:
- **Local:** http://localhost:5000
- **Network:** http://YOUR_IP_ADDRESS:5000

### Step-by-Step Workflow

#### 1. Read the Warning Banner

**CRITICAL**: The red banner at the top states:
> "PSI receipt configurations MUST be sourced from `isi_psi_tool -v` output, NOT `isi_hw_status`"

Always run `isi_psi_tool -v` on the node to get accurate PSI codes for current configuration.

#### 2. Add a Node Group

Click the **"Add Node Group"** button to create a configuration group. Each group represents nodes with identical hardware specifications.

**Why multiple groups?** You need separate groups if nodes have different:
- Current hardware configurations
- Target upgrade specifications
- Node generations (Gen 6 vs Gen 6.5)

#### 3. Select Node Generation

Choose the generation for this group:

- **Gen 6 / MLK**: Traditional PowerScale nodes (e.g., H400, H500, H5600, F200, F600)
- **Gen 6.5 / Gen 16**: PowerEdge-based nodes (e.g., B100, P100, F900)

The form fields will change dynamically based on your selection.

#### 4. Enter Node Identifiers

**For Gen 6 / MLK:**
- Enter **Serial Numbers** (comma-separated)
- Example: `JACNM194040851, JACNM194040866, JWXNM190900360`

**For Gen 6.5 / Gen 16:**
- Select **Platform Model** (B100, P100, F200, etc.)
- Enter **Service Tags** (comma-separated)
- The NIC slot will auto-display based on model

#### 5. Select Current Configuration

From the dropdown menus, select the **Current** PSI codes for:
- Cache SSD
- Front-End NIC
- Compute/Memory

These should match your `isi_psi_tool -v` output.

#### 6. Select Target Configuration

Select the **Target** PSI codes for the hardware you want to upgrade to.

**PSI Code Format:**
Dropdowns show: `Description - PSI-Code`
- Example: `400GB (1x400GB) - 001-infinity-ssd-1x400gb-psi`
- Example: `Low (6x64GB) - 384GB - 001-infinity-compute-low-64GB-psi`

#### 7. Generate JSON

Click **"Generate JSON"** to preview the output.

The preview pane shows the formatted JSON. Verify:
- All serial numbers are correct
- PSI codes match your requirements
- Format matches `isi_psi_tool -v` structure

#### 8. Download the JSON File

Click **"Save & Download JSON"** to save the file locally.

The file will be named: `powerscale_cto_config_YYYYMMDD_HHMMSS.json`

#### 9. Attach to SR

Attach the downloaded JSON file to your Service Request (SR) email for the CTO Validation Team.

## JSON Output Format

The tool generates JSON in the flat `nodes` array format:

```json
{
  "nodes": [
    {
      "serial_number": "JACNM194040851",
      "ssd": {
        "from": "001-infinity-ssd-1x400gb-psi",
        "to": "001-infinity-ssd-1x400gb-psi"
      },
      "nic": {
        "from": "002-iFEIO-10GBE-B-psi",
        "to": "002-iFEIO-10GBE-B-psi"
      },
      "compute": {
        "from": "001-infinity-compute-low-psi",
        "to": "001-infinity-compute-low-64GB-psi"
      }
    }
  ]
}
```

This format matches the output of `isi_psi_tool -v` and is compatible with:
- CTO Validation Team workflows
- PSI package generation tools
- Hardware upgrade automation

## PSI Code Reference

### SSD (Cache) PSI Codes

| Configuration | PSI Code |
|--------------|----------|
| 400GB (1x400GB) | `001-infinity-ssd-1x400gb-psi` |
| 800GB (2x400GB) | `001-infinity-ssd-1x400gb-psi` |
| 1.6TB | `001-infinity-ssd-1.6tb-psi` |
| 3.2TB | `001-infinity-ssd-3.2tb-psi` |
| 6.4TB | `001-infinity-ssd-6.4tb-psi` |
| 15.36TB | `001-infinity-ssd-15.36tb-psi` |
| 1.92TB | `001-infinity-ssd-1.92tb-psi` |
| 3.84TB | `001-infinity-ssd-3.84tb-psi` |
| 7.68TB | `001-infinity-ssd-7.68tb-psi` |
| 15.36TB NVMe | `001-infinity-ssd-15.36tb-nvme-psi` |

**Note:** For dual 400GB SSDs, use `001-infinity-ssd-1x400gb-psi` even if the system shows 800GB total.

### NIC (Front-End) PSI Codes

| Configuration | PSI Code |
|--------------|----------|
| 10GbE 2-port Base-T | `002-iFEIO-10GBE-B-psi` |
| 10GbE 2-port SFP+ | `002-iFEIO-10GBE-SF-psi` |
| 10GbE 4-port | `002-iFEIO-10GBE-4P-psi` |
| 25GbE 2-port | `002-iFEIO-25GBE-psi` |
| 25GbE 2-port SFP28 | `002-iFEIO-25GBE-SF-psi` |
| 40GbE 2-port | `002-iFEIO-40GBE-psi` |
| 100GbE 2-port | `002-iFEIO-100GBE-psi` |
| 100GbE 2-port QSFP28 | `002-iFEIO-100GBE-QS-psi` |
| 100GbE 4-port | `002-iFEIO-100GBE-4P-psi` |
| 200GbE 2-port | `002-iFEIO-200GBE-psi` |

### Compute/Memory PSI Codes

| Configuration | PSI Code |
|--------------|----------|
| Low (6x16GB) - 96GB | `001-infinity-compute-low-psi` |
| Low (6x32GB) - 192GB | `001-infinity-compute-low-192GB-psi` |
| Low (6x32GB) - 192GB | `001-infinity-compute-low-6x32GB-psi` |
| Low (6x32GB) - 192GB | `001-infinity-compute-low-6x32g-psi` |
| Low (6x64GB) - 384GB | `001-infinity-compute-low-64GB-psi` |
| Low (6x64GB) - 384GB | `001-infinity-compute-low-384GB-psi` |
| Low (6x128GB) - 768GB | `001-infinity-compute-low-768GB-psi` |
| Low (6x256GB) - 1.5TB | `001-infinity-compute-low-1.5TB-psi` |
| Low (6x256GB) - 1.5TB | `001-infinity-compute-low-1536GB-psi` |
| Medium (6x32GB) - 192GB | `001-infinity-compute-medium-psi` |
| Medium (6x64GB) - 384GB | `001-infinity-compute-medium-384GB-psi` |
| High (6x64GB) - 384GB | `001-infinity-compute-high-psi` |
| High (6x128GB) - 768GB | `001-infinity-compute-high-768GB-psi` |

## Gen 6.5 NIC Slot Mapping

When you select a platform model, the tool displays the correct NIC slot:

| Platform Model | NIC Slot |
|---------------|----------|
| B100, P100, F600, F710 | Slot 3 |
| F200, F210 | Slot 2 |
| F900 | Slot 8 |
| F910 | Slot 7 |

## Common Workflows

### RAM Upgrade Only (No SSD/NIC Change)

1. Select current SSD PSI code for both Current and Target
2. Select current NIC PSI code for both Current and Target
3. Select current Compute for Current
4. Select target Compute (higher memory) for Target

### SSD Upgrade

1. Select current SSD PSI code for Current
2. Select target SSD PSI code for Target
3. Keep NIC and Compute the same (Current = Target)

### NIC Upgrade

1. Keep SSD the same (Current = Target)
2. Select current NIC for Current
3. Select target NIC for Target
4. Keep Compute the same (Current = Target)

### Mixed Upgrades

Create multiple node groups if different nodes need different upgrades:

- **Group 1**: Nodes getting RAM upgrade only
- **Group 2**: Nodes getting SSD upgrade only
- **Group 3**: Nodes getting both RAM and NIC upgrades

## PSI Configuration Tools

The application includes advanced tools for working with PSI (PowerScale Inventory) configurations:

### PSI Code Browser

Browse the complete database of valid PSI codes:
- **SSD Configurations**: All available SSD options (400GB to 15.36TB)
- **NIC Configurations**: Front-end NIC options (10GbE to 200GbE)
- **Compute Configurations**: Memory/compute profiles (Low to Ultra)

Click any category button to see all available PSI codes with their descriptions and configuration files.

### PSI Configuration Comparison

Compare two PSI codes to see what changes between configurations:
1. Select the category (SSD, NIC, or Compute)
2. Enter the "From" PSI code (current configuration)
3. Enter the "To" PSI code (target configuration)
4. Click "Compare" to see differences

Example: Compare `001-infinity-compute-low-psi` vs `001-infinity-compute-low-64GB-psi` to see the memory difference (16GB → 64GB DIMMs).

### PSI Code Validator

Validate that a PSI code exists in the database:
- Enter any PSI code (e.g., `001-infinity-ssd-1x400gb-psi`)
- Click "Validate" to check if it's a known configuration
- Displays configuration details if valid

### PSI Configuration File Browser

Browse and download actual PSI configuration files (.conf) that are bundled with the tool:

**Categories:**
- **Compute Files**: Memory/DRAM configurations (low, med, high, turbo, ultra profiles)
- **SSD Files**: Cache SSD configurations (400GB to 15.36TB)
- **NIC Files**: Front-end NIC configurations (10GbE to 200GbE)

**Features:**
- View file contents directly in the browser
- Download individual .conf files
- Files are from the plat-psi-conf repository
- Used by `isi_create_hardware_package` tool

This eliminates the need to manually locate and copy PSI configuration files from the repository.

### Hardware Upgrade Package Generator

Generate complete package information for the `isi_create_hardware_package` tool:
1. Configure your node groups with current/target PSI codes
2. Click "Generate Package Information"
3. View package details including:
   - Package name and description
   - Number of nodes
   - Destination directory
   - Command-line syntax

This helps you prepare the files needed for the PSI packaging workflow.

## Quick Reference

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + Enter` | Generate JSON |
| `Tab` | Navigate between fields |

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

## Validation Rules

The tool enforces these rules:

1. **At least one hardware component** must be configured (SSD, NIC, or Compute)
2. **Serial numbers required** for Gen 6/MLK nodes
3. **Service tags required** for Gen 6.5/Gen 16 nodes
4. **Platform model required** for Gen 6.5/Gen 16 nodes
5. **No dual 400GB SSDs** - Not a valid configuration

## Documentation

**For detailed documentation, see: [USER_MANUAL.md](USER_MANUAL.md)**

The user manual includes:
- Complete installation instructions for all platforms
- Step-by-step usage guides
- PSI code reference tables
- Example workflows and scenarios
- Troubleshooting guide
- API reference

## Troubleshooting

### "Validation Error: At least one hardware component must be configured"

- Select a PSI code for at least one of: SSD, NIC, or Compute
- Can select "No SSD" if only doing NIC or Compute upgrades

### PSI Code Not in Dropdown

- Check your `isi_psi_tool -v` output for the exact PSI code
- Contact the tool developer to add missing PSI codes

### JSON Format Doesn't Match Expected

- Ensure you're using the latest version of the tool
- The tool outputs flat `nodes` array format
- Verify with the "Generate JSON" preview before downloading

### Ubuntu: "externally-managed-environment" Error

**Problem:** Ubuntu 22.04+ and newer Debian systems prevent direct pip installs.

**Solution 1 - Use the install script (Recommended):**
```bash
./install.sh
```

**Solution 2 - Manual virtual environment:**
```bash
# Remove any partial venv
rm -rf venv

# Create fresh venv
python3 -m venv venv

# Activate and install using venv python
source venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# Run
python3 app.py
```

**Solution 3 - Use pipx (system-wide install):**
```bash
# Install pipx
sudo apt install pipx

# Install the application
pipx install flask

# Run manually with dependencies
pipx run --spec requirements.txt flask --app app.py run
```

**Note:** Never use `sudo pip install` on Ubuntu 22.04+. Always use a virtual environment.

## Important Notes

1. **Always use `isi_psi_tool -v` output** for current configuration values
2. **Never use `isi_hw_status`** for PSI configuration data
3. **Dual 400GB SSDs**: Use `001-infinity-ssd-1x400gb-psi` (not 800GB variant)
4. **Test the JSON** with the preview before downloading
5. **Keep the JSON file** until the upgrade is complete

## Support

For issues or feature requests:
- Contact the internal PowerScale tools team
- File a ticket with the CTO Validation Team
- Reference your SR number when reporting issues

## Version History

- **v1.2** (2024): Bundled PSI Configuration Files
  - Actual .conf files from plat-psi-conf repository included
  - PSI Configuration File Browser with view/download capabilities
  - Files organized by category (compute, ssd, nic)
  - Integration with isi_create_hardware_package workflow

- **v1.1** (2024): Enhanced with PSI Tools
  - PSI Code Browser - browse all available PSI configurations
  - PSI Configuration Comparison - compare two PSI codes side-by-side
  - PSI Code Validator - validate PSI codes against database
  - Hardware Upgrade Package Generator - integration with isi_create_hardware_package
  - Cross-platform support (Windows, Ubuntu, RHEL)
  
- **v1.0** (2024): Initial release with PSI code support
  - Gen 6/MLK support
  - Gen 6.5/Gen 16 support
  - PSI code dropdowns
  - Flat JSON output format
  - Multi-node group support

---

**For Internal Use Only** - Dell Technologies PowerScale CTO Validation Team Tool
