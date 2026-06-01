"""
PowerScale CTO JSON Generator
A lightweight Flask application for generating CTO hardware upgrade configurations.
Generates JSON in PSI hardware upgrade format with PSI codes.
"""

from flask import Flask, render_template, request, jsonify, send_file
import json
import io
import re
from datetime import datetime

# Import PSI database and validation
from psi_database import psi_db, psi_display_options, PSI_DATABASE

app = Flask(__name__)

# PSI SSD Options (Cache SSD) - Maps display names to PSI codes
PSI_SSD_OPTIONS = [
    ("", ""),
    ("No SSD", ""),
    ("400GB (1x400GB) - 001-infinity-ssd-1x400gb-psi", "001-infinity-ssd-1x400gb-psi"),
    ("800GB (2x400GB) - 001-infinity-ssd-1x400gb-psi", "001-infinity-ssd-1x400gb-psi"),
    ("1.6TB - 001-infinity-ssd-1.6tb-psi", "001-infinity-ssd-1.6tb-psi"),
    ("3.2TB - 001-infinity-ssd-3.2tb-psi", "001-infinity-ssd-3.2tb-psi"),
    ("6.4TB - 001-infinity-ssd-6.4tb-psi", "001-infinity-ssd-6.4tb-psi"),
    ("15.36TB - 001-infinity-ssd-15.36tb-psi", "001-infinity-ssd-15.36tb-psi"),
    ("1.92TB - 001-infinity-ssd-1.92tb-psi", "001-infinity-ssd-1.92tb-psi"),
    ("3.84TB - 001-infinity-ssd-3.84tb-psi", "001-infinity-ssd-3.84tb-psi"),
    ("7.68TB - 001-infinity-ssd-7.68tb-psi", "001-infinity-ssd-7.68tb-psi"),
    ("15.36TB NVMe - 001-infinity-ssd-15.36tb-nvme-psi", "001-infinity-ssd-15.36tb-nvme-psi")
]

# PSI NIC Options (Front-End NIC) - Maps display names to PSI codes
PSI_NIC_OPTIONS = [
    ("", ""),
    ("10GbE 2-port Base-T - 002-iFEIO-10GBE-B-psi", "002-iFEIO-10GBE-B-psi"),
    ("10GbE 2-port SFP+ - 002-iFEIO-10GBE-SF-psi", "002-iFEIO-10GBE-SF-psi"),
    ("10GbE 4-port - 002-iFEIO-10GBE-4P-psi", "002-iFEIO-10GBE-4P-psi"),
    ("25GbE 2-port - 002-iFEIO-25GBE-psi", "002-iFEIO-25GBE-psi"),
    ("25GbE 2-port SFP28 - 002-iFEIO-25GBE-SF-psi", "002-iFEIO-25GBE-SF-psi"),
    ("40GbE 2-port - 002-iFEIO-40GBE-psi", "002-iFEIO-40GBE-psi"),
    ("100GbE 2-port - 002-iFEIO-100GBE-psi", "002-iFEIO-100GBE-psi"),
    ("100GbE 2-port QSFP28 - 002-iFEIO-100GBE-QS-psi", "002-iFEIO-100GBE-QS-psi"),
    ("100GbE 4-port - 002-iFEIO-100GBE-4P-psi", "002-iFEIO-100GBE-4P-psi"),
    ("200GbE 2-port - 002-iFEIO-200GBE-psi", "002-iFEIO-200GBE-psi")
]

# PSI Compute/Memory Options - Maps display names to PSI codes
PSI_COMPUTE_OPTIONS = [
    ("", ""),
    ("Low (6x16GB) - 96GB - 001-infinity-compute-low-psi", "001-infinity-compute-low-psi"),
    ("Low (6x32GB) - 192GB - 001-infinity-compute-low-192GB-psi", "001-infinity-compute-low-192GB-psi"),
    ("Low (6x32GB) - 192GB - 001-infinity-compute-low-6x32GB-psi", "001-infinity-compute-low-6x32GB-psi"),
    ("Low (6x64GB) - 384GB - 001-infinity-compute-low-64GB-psi", "001-infinity-compute-low-64GB-psi"),
    ("Low (6x64GB) - 384GB - 001-infinity-compute-low-384GB-psi", "001-infinity-compute-low-384GB-psi"),
    ("Low (6x128GB) - 768GB - 001-infinity-compute-low-768GB-psi", "001-infinity-compute-low-768GB-psi"),
    ("Low (6x256GB) - 1.5TB - 001-infinity-compute-low-1.5TB-psi", "001-infinity-compute-low-1.5TB-psi"),
    ("Low (6x256GB) - 1.5TB - 001-infinity-compute-low-1536GB-psi", "001-infinity-compute-low-1536GB-psi"),
    ("Low (6x32GB) - 192GB - 001-infinity-compute-low-6x32g-psi", "001-infinity-compute-low-6x32g-psi"),
    ("Medium (6x32GB) - 192GB - 001-infinity-compute-medium-psi", "001-infinity-compute-medium-psi"),
    ("Medium (6x64GB) - 384GB - 001-infinity-compute-medium-384GB-psi", "001-infinity-compute-medium-384GB-psi"),
    ("High (6x64GB) - 384GB - 001-infinity-compute-high-psi", "001-infinity-compute-high-psi"),
    ("High (6x128GB) - 768GB - 001-infinity-compute-high-768GB-psi", "001-infinity-compute-high-768GB-psi")
]

# Extract display names for dropdowns
GEN6_CACHE_SSD_OPTIONS = [opt[0] for opt in PSI_SSD_OPTIONS]
GEN6_FE_NIC_OPTIONS = [opt[0] for opt in PSI_NIC_OPTIONS]
GEN6_MEMORY_OPTIONS = [opt[0] for opt in PSI_COMPUTE_OPTIONS]

# Create lookup dictionaries for PSI codes
SSD_PSI_CODES = {opt[0]: opt[1] for opt in PSI_SSD_OPTIONS}
NIC_PSI_CODES = {opt[0]: opt[1] for opt in PSI_NIC_OPTIONS}
COMPUTE_PSI_CODES = {opt[0]: opt[1] for opt in PSI_COMPUTE_OPTIONS}

# Gen 6.5/Gen 16 Configuration Options - Also uses PSI codes
GEN65_PLATFORM_MODELS = [
    "B100",
    "P100",
    "F200",
    "F600",
    "F210",
    "F710",
    "F900",
    "F910"
]

# Gen 6.5 uses same PSI NIC codes
GEN65_FE_NIC_OPTIONS = GEN6_FE_NIC_OPTIONS

# Platform to NIC slot mapping
PLATFORM_NIC_SLOTS = {
    "B100": "Slot 3",
    "P100": "Slot 3",
    "F600": "Slot 3",
    "F710": "Slot 3",
    "F200": "Slot 2",
    "F210": "Slot 2",
    "F900": "Slot 8",
    "F910": "Slot 7"
}

# Gen 6 models with no SSD support (F800/F810 series)
GEN6_NO_SSD_MODELS = ["F800", "F810", "H800", "H810"]


def parse_serial_numbers(serial_text):
    """Parse comma-separated serial numbers or service tags."""
    if not serial_text:
        return []
    # Split by comma and clean up whitespace
    serials = [s.strip() for s in serial_text.split(',')]
    return [s for s in serials if s]


def validate_node_group(group_data):
    """Validate a node group configuration."""
    errors = []
    
    node_gen = group_data.get('nodeGeneration')
    
    if not node_gen:
        errors.append("Node Generation is required")
        return errors
    
    if node_gen == 'gen6':
        serials = parse_serial_numbers(group_data.get('serialNumbers', ''))
        if not serials:
            errors.append("Serial Numbers are required for Gen 6/MLK")
        
        # Validate at least one upgrade field is selected
        has_upgrade = (
            group_data.get('currentCacheSSD') or group_data.get('targetCacheSSD') or
            group_data.get('currentFENIC') or group_data.get('targetFENIC') or
            group_data.get('currentMemory') or group_data.get('targetMemory')
        )
        if not has_upgrade:
            errors.append("At least one hardware component (SSD, NIC, or Compute) must be configured")
    
    elif node_gen == 'gen65':
        service_tags = parse_serial_numbers(group_data.get('serviceTags', ''))
        if not service_tags:
            errors.append("Service Tags are required for Gen 6.5/Gen 16")
        
        platform_model = group_data.get('platformModel')
        if not platform_model:
            errors.append("Platform Model is required for Gen 6.5/Gen 16")
    
    return errors


def generate_cto_json(node_groups):
    """
    Generate the CTO JSON blueprint in PSI hardware upgrade format.
    Returns flat structure: {"nodes": [...]} matching isi_psi_tool output format.
    """
    output = {
        "nodes": []
    }
    
    for group in node_groups:
        node_gen = group.get('nodeGeneration')
        
        if node_gen == 'gen6':
            serials = parse_serial_numbers(group.get('serialNumbers', ''))
            
            # Get PSI codes from display values
            current_cache_display = group.get('currentCacheSSD', '')
            target_cache_display = group.get('targetCacheSSD', '')
            current_fe_display = group.get('currentFENIC', '')
            target_fe_display = group.get('targetFENIC', '')
            current_mem_display = group.get('currentMemory', '')
            target_mem_display = group.get('targetMemory', '')
            
            # Convert display values to PSI codes
            current_cache = SSD_PSI_CODES.get(current_cache_display, '')
            target_cache = SSD_PSI_CODES.get(target_cache_display, '')
            current_fe = NIC_PSI_CODES.get(current_fe_display, '')
            target_fe = NIC_PSI_CODES.get(target_fe_display, '')
            current_compute = COMPUTE_PSI_CODES.get(current_mem_display, '')
            target_compute = COMPUTE_PSI_CODES.get(target_mem_display, '')
            
            for serial in serials:
                node_config = {
                    "serial_number": serial
                }
                
                # Add SSD config if present
                if current_cache or target_cache:
                    node_config["ssd"] = {
                        "from": current_cache if current_cache else target_cache,
                        "to": target_cache if target_cache else current_cache
                    }
                
                # Add NIC config if present
                if current_fe or target_fe:
                    node_config["nic"] = {
                        "from": current_fe if current_fe else target_fe,
                        "to": target_fe if target_fe else current_fe
                    }
                
                # Add Compute config if present
                if current_compute or target_compute:
                    node_config["compute"] = {
                        "from": current_compute if current_compute else target_compute,
                        "to": target_compute if target_compute else current_compute
                    }
                
                output["nodes"].append(node_config)
                
        elif node_gen == 'gen65':
            service_tags = parse_serial_numbers(group.get('serviceTags', ''))
            
            current_fe_display = group.get('currentFENIC65', '')
            target_fe_display = group.get('targetFENIC65', '')
            current_fe = NIC_PSI_CODES.get(current_fe_display, '')
            target_fe = NIC_PSI_CODES.get(target_fe_display, '')
            
            for tag in service_tags:
                node_config = {
                    "service_tag": tag
                }
                
                # For Gen 6.5, use service_tag instead of serial_number
                # Note: Some systems may still use serial_number field
                node_config["serial_number"] = tag
                
                # Add NIC config if present
                if current_fe or target_fe:
                    node_config["nic"] = {
                        "from": current_fe if current_fe else target_fe,
                        "to": target_fe if target_fe else current_fe
                    }
                
                output["nodes"].append(node_config)
    
    return output


@app.route('/')
def index():
    """Render the main application page."""
    return render_template('index.html',
                         gen6_cache_options=GEN6_CACHE_SSD_OPTIONS,
                         gen6_fe_options=GEN6_FE_NIC_OPTIONS,
                         gen6_memory_options=GEN6_MEMORY_OPTIONS,
                         gen65_platform_models=GEN65_PLATFORM_MODELS,
                         gen65_fe_options=GEN65_FE_NIC_OPTIONS,
                         platform_nic_slots=PLATFORM_NIC_SLOTS,
                         gen6_no_ssd_models=GEN6_NO_SSD_MODELS,
                         psi_database=PSI_DATABASE,
                         psi_display_options=psi_display_options)


@app.route('/api/generate', methods=['POST'])
def generate_json():
    """Generate CTO JSON from form data."""
    data = request.get_json()
    node_groups = data.get('nodeGroups', [])
    
    # Validate all groups
    all_errors = []
    for idx, group in enumerate(node_groups):
        errors = validate_node_group(group)
        if errors:
            all_errors.append({
                "group_index": idx,
                "errors": errors
            })
    
    if all_errors:
        return jsonify({
            "success": False,
            "errors": all_errors
        }), 400
    
    # Generate JSON
    cto_json = generate_cto_json(node_groups)
    
    return jsonify({
        "success": True,
        "data": cto_json
    })


@app.route('/api/download', methods=['POST'])
def download_json():
    """Generate and download CTO JSON file."""
    data = request.get_json()
    node_groups = data.get('nodeGroups', [])
    
    # Validate all groups
    all_errors = []
    for idx, group in enumerate(node_groups):
        errors = validate_node_group(group)
        if errors:
            all_errors.append({
                "group_index": idx,
                "errors": errors
            })
    
    if all_errors:
        return jsonify({
            "success": False,
            "errors": all_errors
        }), 400
    
    # Generate JSON
    cto_json = generate_cto_json(node_groups)
    
    # Create file in memory (compact format - single line, no spaces)
    json_str = json.dumps(cto_json, separators=(',', ':'))
    mem_file = io.BytesIO()
    mem_file.write(json_str.encode('utf-8'))
    mem_file.seek(0)
    
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"powerscale_cto_config_{timestamp}.json"
    
    return send_file(
        mem_file,
        mimetype='application/json',
        as_attachment=True,
        download_name=filename
    )


@app.route('/api/validate-serials', methods=['POST'])
def validate_serials():
    """Validate serial numbers or service tags format."""
    data = request.get_json()
    serial_text = data.get('serials', '')
    serials = parse_serial_numbers(serial_text)
    
    return jsonify({
        "count": len(serials),
        "serials": serials,
        "valid": len(serials) > 0
    })


@app.route('/api/validate-psi', methods=['POST'])
def validate_psi():
    """Validate PSI codes against database"""
    data = request.get_json()
    code = data.get('code', '')
    category = data.get('category')  # 'ssd', 'nic', 'compute'
    
    is_valid, info = psi_db.validate_code(code, category)
    
    return jsonify({
        "valid": is_valid,
        "code": code,
        "category": category,
        "info": info
    })


@app.route('/api/psi-suggest', methods=['POST'])
def psi_suggest():
    """Get PSI code suggestions based on partial match"""
    data = request.get_json()
    partial = data.get('partial', '')
    category = data.get('category')  # optional
    
    suggestions = psi_db.suggest_codes(partial, category)
    
    return jsonify({
        "suggestions": suggestions,
        "count": len(suggestions)
    })


@app.route('/api/psi-compare', methods=['POST'])
def psi_compare():
    """Compare two PSI configurations and show differences"""
    data = request.get_json()
    from_code = data.get('from', '')
    to_code = data.get('to', '')
    category = data.get('category', '')
    
    if not all([from_code, to_code, category]):
        return jsonify({
            "error": "Missing required fields: from, to, category"
        }), 400
    
    comparison = psi_db.compare_configs(from_code, to_code, category)
    
    return jsonify(comparison)


@app.route('/api/psi-browser')
def psi_browser():
    """Browse all available PSI codes"""
    category = request.args.get('category')  # 'ssd', 'nic', 'compute'
    
    if category:
        codes = psi_db.get_all_codes(category)
        return jsonify({
            "category": category,
            "codes": codes
        })
    
    return jsonify(PSI_DATABASE)


@app.route('/api/package-info', methods=['POST'])
def package_info():
    """Generate hardware upgrade package information"""
    data = request.get_json()
    node_groups = data.get('nodeGroups', [])
    
    # Generate CTO JSON first
    cto_json = generate_cto_json(node_groups)
    
    # Generate package info
    pkg_info = psi_db.generate_package_info(cto_json.get('nodes', []))
    
    return jsonify({
        "cto_json": cto_json,
        "package_info": pkg_info,
        "instructions": {
            "step1": "Save the CTO JSON to hardware_upgrade.json",
            "step2": "Use isi_create_hardware_package tool with -f hardware_upgrade.json",
            "step3": "Sign the resulting .pkg file",
            "step4": "Attach signed package to SR"
        }
    })


# PSI Configuration File Serving
import os

PSI_CONFIGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'psi_configs')


@app.route('/api/psi-configs')
def list_psi_configs():
    """List all bundled PSI configuration files"""
    configs = {
        "compute": [],
        "ssd": [],
        "nic": []
    }
    
    # List compute configs
    compute_dir = os.path.join(PSI_CONFIGS_DIR, 'infinity', 'compute')
    if os.path.exists(compute_dir):
        for f in sorted(os.listdir(compute_dir)):
            if f.endswith('.conf'):
                configs["compute"].append({
                    "filename": f,
                    "path": f"infinity/compute/{f}",
                    "download_url": f"/api/psi-configs/download/infinity/compute/{f}"
                })
    
    # List SSD configs
    ssd_dir = os.path.join(PSI_CONFIGS_DIR, 'infinity', 'ssd')
    if os.path.exists(ssd_dir):
        for f in sorted(os.listdir(ssd_dir)):
            if f.endswith('.conf'):
                configs["ssd"].append({
                    "filename": f,
                    "path": f"infinity/ssd/{f}",
                    "download_url": f"/api/psi-configs/download/infinity/ssd/{f}"
                })
    
    # List NIC (FE) configs
    fe_dir = os.path.join(PSI_CONFIGS_DIR, 'FE')
    if os.path.exists(fe_dir):
        for f in sorted(os.listdir(fe_dir)):
            if f.endswith('.conf'):
                configs["nic"].append({
                    "filename": f,
                    "path": f"FE/{f}",
                    "download_url": f"/api/psi-configs/download/FE/{f}"
                })
    
    return jsonify({
        "configs": configs,
        "total": len(configs["compute"]) + len(configs["ssd"]) + len(configs["nic"]),
        "basedir": PSI_CONFIGS_DIR
    })


@app.route('/api/psi-configs/download/<path:filename>')
def download_psi_config(filename):
    """Download a specific PSI configuration file"""
    # Security: ensure the path is within PSI_CONFIGS_DIR
    safe_path = os.path.normpath(os.path.join(PSI_CONFIGS_DIR, filename))
    
    # Check for path traversal attacks
    if not safe_path.startswith(PSI_CONFIGS_DIR):
        return jsonify({"error": "Invalid file path"}), 403
    
    if not os.path.exists(safe_path):
        return jsonify({"error": "File not found"}), 404
    
    return send_file(
        safe_path,
        mimetype='text/plain',
        as_attachment=True,
        download_name=os.path.basename(filename)
    )


@app.route('/api/psi-configs/view/<path:filename>')
def view_psi_config(filename):
    """View contents of a PSI configuration file"""
    # Security: ensure the path is within PSI_CONFIGS_DIR
    safe_path = os.path.normpath(os.path.join(PSI_CONFIGS_DIR, filename))
    
    # Check for path traversal attacks
    if not safe_path.startswith(PSI_CONFIGS_DIR):
        return jsonify({"error": "Invalid file path"}), 403
    
    if not os.path.exists(safe_path):
        return jsonify({"error": "File not found"}), 404
    
    try:
        with open(safe_path, 'r') as f:
            content = f.read()
        
        return jsonify({
            "filename": os.path.basename(filename),
            "path": filename,
            "content": content,
            "size": len(content)
        })
    except Exception as e:
        return jsonify({"error": f"Error reading file: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
