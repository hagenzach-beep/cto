"""
PSI Database Module for PowerScale CTO Generator
Provides validation, lookup, and diff capabilities for PSI configurations
Based on plat-psi-conf repository structure
"""

import os
import re
import json
from typing import Dict, List, Optional, Tuple

# PSI Code Database - Populated from plat-psi-conf repository
PSI_DATABASE = {
    "compute": {
        "001-infinity-compute-low-psi": {
            "name": "Low (6x16GB) - 96GB",
            "dram_config": "1x16GB",
            "dram_size": 17179869184,
            "file": "001-1.0-infinity-compute-low-psi.conf"
        },
        "001-infinity-compute-low-64GB-psi": {
            "name": "Low (6x64GB) - 384GB",
            "dram_config": "6x64GB",
            "dram_size": 68719476736,
            "file": "001-1.0-infinity-compute-low-64GB-psi.conf"
        },
        "001-infinity-compute-low-192GB-psi": {
            "name": "Low (6x32GB) - 192GB",
            "dram_config": "6x32GB",
            "dram_size": 34359738368,
            "file": "001-1.0-infinity-compute-low-192GB-psi.conf"
        },
        "001-infinity-compute-low-384GB-psi": {
            "name": "Low (6x64GB) - 384GB",
            "dram_config": "6x64GB",
            "dram_size": 68719476736,
            "file": "001-1.0-infinity-compute-low-384GB-psi.conf"
        },
        "001-infinity-compute-low-768GB-psi": {
            "name": "Low (6x128GB) - 768GB",
            "dram_config": "6x128GB",
            "dram_size": 137438953472,
            "file": "001-1.0-infinity-compute-low-768GB-psi.conf"
        },
        "001-infinity-compute-low-1.5TB-psi": {
            "name": "Low (6x256GB) - 1.5TB",
            "dram_config": "6x256GB",
            "dram_size": 274877906944,
            "file": "001-1.0-infinity-compute-low-1.5TB-psi.conf"
        },
        "001-infinity-compute-low-1536GB-psi": {
            "name": "Low (6x256GB) - 1.5TB",
            "dram_config": "6x256GB",
            "dram_size": 274877906944,
            "file": "001-1.0-infinity-compute-low-1536GB-psi.conf"
        },
        "001-infinity-compute-med-psi": {
            "name": "Medium (6x32GB) - 192GB",
            "dram_config": "6x32GB",
            "dram_size": 34359738368,
            "file": "001-1.0-infinity-compute-med-psi.conf"
        },
        "001-infinity-compute-med-384GB-psi": {
            "name": "Medium (6x64GB) - 384GB",
            "dram_config": "6x64GB",
            "dram_size": 68719476736,
            "file": "001-1.0-infinity-compute-med-384GB-psi.conf"
        },
        "001-infinity-compute-high-psi": {
            "name": "High (6x64GB) - 384GB",
            "dram_config": "6x64GB",
            "dram_size": 68719476736,
            "file": "001-1.0-infinity-compute-high-psi.conf"
        },
        "001-infinity-compute-high-768GB-psi": {
            "name": "High (6x128GB) - 768GB",
            "dram_config": "6x128GB",
            "dram_size": 137438953472,
            "file": "001-1.0-infinity-compute-high-768GB-psi.conf"
        },
        "001-infinity-compute-turbo-psi": {
            "name": "Turbo (6x128GB) - 768GB",
            "dram_config": "6x128GB",
            "dram_size": 137438953472,
            "file": "001-1.0-infinity-compute-turbo-psi.conf"
        },
        "001-infinity-compute-ultra-psi": {
            "name": "Ultra (6x256GB) - 1.5TB",
            "dram_config": "6x256GB",
            "dram_size": 274877906944,
            "file": "001-1.0-infinity-compute-ultra-psi.conf"
        },
        "001-infinity-compute-turbo-mlk-psi": {
            "name": "Turbo MLK (6x128GB) - 768GB",
            "dram_config": "6x128GB",
            "dram_size": 137438953472,
            "file": "001-1.0-infinity-compute-turbo-mlk-psi.conf"
        },
        "001-infinity-compute-turbo-mlk-192GB-psi": {
            "name": "Turbo MLK (6x32GB) - 192GB",
            "dram_config": "6x32GB",
            "dram_size": 34359738368,
            "file": "001-1.0-infinity-compute-turbo-mlk-192GB-psi.conf"
        },
        "001-infinity-compute-low-mlk-psi": {
            "name": "Low MLK (6x16GB) - 96GB",
            "dram_config": "6x16GB",
            "dram_size": 17179869184,
            "file": "001-1.0-infinity-compute-low-mlk-psi.conf"
        },
        "001-infinity-compute-low-cDVT-psi": {
            "name": "Low cDVT (6x16GB) - 96GB",
            "dram_config": "6x16GB",
            "dram_size": 17179869184,
            "file": "001-1.0-infinity-compute-low-cDVT-psi.conf"
        },
        "001-infinity-compute-med-cDVT-psi": {
            "name": "Medium cDVT (6x32GB) - 192GB",
            "dram_config": "6x32GB",
            "dram_size": 34359738368,
            "file": "001-1.0-infinity-compute-med-cDVT-psi.conf"
        },
    },
    "ssd": {
        "001-infinity-ssd-0x400gb-psi": {
            "name": "No SSD",
            "size": 0,
            "count": 0,
            "file": "001-1.0-infinity-ssd-0x400gb-psi.conf"
        },
        "001-infinity-ssd-1x400gb-psi": {
            "name": "400GB (1x400GB)",
            "size": 400,
            "count": 1,
            "file": "001-1.0-infinity-ssd-1x400gb-psi.conf"
        },
        "001-infinity-ssd-1x800gb-psi": {
            "name": "800GB (1x800GB or 2x400GB)",
            "size": 800,
            "count": 1,
            "file": "001-1.0-infinity-ssd-1x800gb-psi.conf"
        },
        "001-infinity-ssd-1x1.6tb-psi": {
            "name": "1.6TB",
            "size": 1600,
            "count": 1,
            "file": "001-1.0-infinity-ssd-1x1.6tb-psi.conf"
        },
        "001-infinity-ssd-1x3.2tb-psi": {
            "name": "3.2TB",
            "size": 3200,
            "count": 1,
            "file": "001-1.0-infinity-ssd-1x3.2tb-psi.conf"
        },
        "001-infinity-ssd-1x6.4tb-psi": {
            "name": "6.4TB",
            "size": 6400,
            "count": 1,
            "file": "001-1.0-infinity-ssd-1x6.4tb-psi.conf"
        },
        "001-infinity-ssd-1x7.68tb-psi": {
            "name": "7.68TB",
            "size": 7680,
            "count": 1,
            "file": "001-1.0-infinity-ssd-1x7.68tb-psi.conf"
        },
        "001-infinity-ssd-1x15.36tb-psi": {
            "name": "15.36TB",
            "size": 15360,
            "count": 1,
            "file": "001-1.0-infinity-ssd-1x15.36tb-psi.conf"
        },
    },
    "nic": {
        "002-iFEIO-10GBE-B-psi": {
            "name": "10GbE 2-port Base-T (Pelican)",
            "speed": "10GbE",
            "ports": 2,
            "type": "Base-T",
            "file": "002-1.0-iFEIO-10GBE-B-psi.conf"
        },
        "002-iFEIO-10GBE-A-psi": {
            "name": "10GbE 2-port",
            "speed": "10GbE",
            "ports": 2,
            "file": "001-1.0-iFEIO-10GBE-A-psi.conf"
        },
        "002-iFEIO-10GBE-psi": {
            "name": "10GbE 2-port",
            "speed": "10GbE",
            "ports": 2,
            "file": "001-1.0-iFEIO-10GBE-psi.conf"
        },
        "002-iFEIO-25GBE-psi": {
            "name": "25GbE 2-port",
            "speed": "25GbE",
            "ports": 2,
            "file": "001-1.0-iFEIO-25GBE-psi.conf"
        },
        "002-iFEIO-40GBE-psi": {
            "name": "40GbE 2-port",
            "speed": "40GbE",
            "ports": 2,
            "file": "001-1.0-iFEIO-40GbE-psi.conf"
        },
        "002-iFEIO-100GBE-psi": {
            "name": "100GbE 2-port",
            "speed": "100GbE",
            "ports": 2,
            "file": "001-1.0-iFEIO-100GBE-psi.conf"
        },
    }
}


class PSIDatabase:
    """PSI Configuration Database and Validation"""
    
    @staticmethod
    def get_all_codes(category: str = None) -> Dict:
        """Get all PSI codes for a category or all categories"""
        if category:
            return PSI_DATABASE.get(category, {})
        return PSI_DATABASE
    
    @staticmethod
    def validate_code(code: str, category: str = None) -> Tuple[bool, Optional[Dict]]:
        """
        Validate a PSI code exists in the database
        Returns: (is_valid, code_info)
        """
        if category:
            info = PSI_DATABASE.get(category, {}).get(code)
            return (info is not None, info)
        
        # Search all categories
        for cat, codes in PSI_DATABASE.items():
            if code in codes:
                return (True, codes[code])
        
        return (False, None)
    
    @staticmethod
    def get_code_details(code: str) -> Optional[Dict]:
        """Get detailed information about a PSI code"""
        is_valid, info = PSIDatabase.validate_code(code)
        if is_valid:
            return info
        return None
    
    @staticmethod
    def suggest_codes(partial: str, category: str = None) -> List[Dict]:
        """Suggest PSI codes based on partial match"""
        suggestions = []
        categories = [category] if category else PSI_DATABASE.keys()
        
        for cat in categories:
            for code, info in PSI_DATABASE.get(cat, {}).items():
                if partial.lower() in code.lower() or partial.lower() in info.get("name", "").lower():
                    suggestions.append({
                        "category": cat,
                        "code": code,
                        **info
                    })
        
        return suggestions
    
    @staticmethod
    def compare_configs(from_code: str, to_code: str, category: str) -> Dict:
        """
        Compare two PSI configurations and return differences
        """
        from_info = PSIDatabase.get_code_details(from_code)
        to_info = PSIDatabase.get_code_details(to_code)
        
        if not from_info or not to_info:
            return {"error": "One or both codes not found"}
        
        differences = {}
        all_keys = set(from_info.keys()) | set(to_info.keys())
        
        for key in all_keys:
            from_val = from_info.get(key)
            to_val = to_info.get(key)
            if from_val != to_val:
                differences[key] = {
                    "from": from_val,
                    "to": to_val
                }
        
        return {
            "category": category,
            "from_code": from_code,
            "to_code": to_code,
            "differences": differences,
            "from_name": from_info.get("name"),
            "to_name": to_info.get("name")
        }
    
    @staticmethod
    def generate_package_info(node_configs: List[Dict]) -> Dict:
        """
        Generate information needed for hardware upgrade package creation
        Based on isi_create_hardware_package tool
        """
        return {
            "package_name": "Isi_Psi_Package_v1.0",
            "description": "Package for PSI repository",
            "destination_dir": "var/psi/patches/psi",
            "config_file": "root/cluster_hardware_upgrade.json",
            "nodes": node_configs,
            "reboot_required": False,
            "install_script": "test-hwupg-install",
            "death_script": "test-hwupg-death"
        }


def get_psi_display_options():
    """
    Generate display options for the web UI
    Returns format: [("Display Name - PSI-CODE", "PSI-CODE"), ...]
    """
    options = {
        "ssd": [],
        "nic": [],
        "compute": []
    }
    
    # SSD Options
    for code, info in PSI_DATABASE["ssd"].items():
        display = f"{info['name']} - {code}"
        options["ssd"].append((display, code))
    
    # Sort SSD by size
    options["ssd"].sort(key=lambda x: PSI_DATABASE["ssd"][x[1]].get("size", 0))
    
    # NIC Options
    for code, info in PSI_DATABASE["nic"].items():
        display = f"{info['name']} - {code}"
        options["nic"].append((display, code))
    
    # Compute Options
    for code, info in PSI_DATABASE["compute"].items():
        display = f"{info['name']} - {code}"
        options["compute"].append((display, code))
    
    return options


# Export for Flask app
psi_db = PSIDatabase()
psi_display_options = get_psi_display_options()
