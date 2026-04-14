"""
Script to populate the database with sample cloud resources
Run this to get some example data for testing
"""

import requests
import json

BASE_URL = "http://localhost:8000"

sample_resources = [
    {
        "resource_id": "vm-eastus-001",
        "resource_type": "virtual_machine",
        "region": "eastus",
        "status": "active",
        "tags": {
            "size": "Standard_D2s_v3",
            "os": "Ubuntu 22.04",
            "owner": "engineering-team",
            "cost_center": "ENG-001"
        }
    },
    {
        "resource_id": "storage-westus-001",
        "resource_type": "storage_account",
        "region": "westus",
        "status": "active",
        "tags": {
            "capacity_gb": 1000,
            "replication": "GRS",
            "tier": "Standard"
        }
    },
    {
        "resource_id": "db-centralus-001",
        "resource_type": "database",
        "region": "centralus",
        "status": "provisioning",
        "tags": {
            "engine": "PostgreSQL",
            "version": "14.5",
            "size": "Standard_D4s_v3"
        }
    },
    {
        "resource_id": "vm-eastus-002",
        "resource_type": "virtual_machine",
        "region": "eastus",
        "status": "active",
        "tags": {
            "size": "Standard_B2s",
            "os": "Windows Server 2022",
            "owner": "operations-team"
        }
    },
    {
        "resource_id": "lb-northeurope-001",
        "resource_type": "load_balancer",
        "region": "northeurope",
        "status": "active",
        "tags": {
            "sku": "Standard",
            "frontend_ips": 2,
            "backend_pools": 3
        }
    },
    {
        "resource_id": "vm-westus-001",
        "resource_type": "virtual_machine",
        "region": "westus",
        "status": "terminated",
        "tags": {
            "size": "Standard_D2s_v3",
            "os": "Ubuntu 20.04",
            "terminated_at": "2026-04-10T14:30:00Z",
            "reason": "Cost optimization"
        }
    }
]

def populate_database():
    """Create sample resources in the database"""
    print("Populating database with sample resources...")
    print(f"Target API: {BASE_URL}\n")
    
    for resource in sample_resources:
        try:
            response = requests.post(
                f"{BASE_URL}/resources/",
                json=resource,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 201:
                print(f"✓ Created: {resource['resource_id']}")
            elif response.status_code == 400:
                print(f"⚠ Already exists: {resource['resource_id']}")
            else:
                print(f"✗ Failed to create {resource['resource_id']}: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"\n✗ Error: Could not connect to API at {BASE_URL}")
            print("Make sure the API is running with: uvicorn app.main:app --reload")
            return
    
    print("\n" + "="*50)
    print("Sample data population complete!")
    print("="*50)
    
    # Show statistics
    try:
        stats_response = requests.get(f"{BASE_URL}/stats/summary")
        if stats_response.status_code == 200:
            stats = stats_response.json()
            print(f"\nTotal Resources: {stats['total_resources']}")
            print(f"\nBy Type: {json.dumps(stats['by_type'], indent=2)}")
            print(f"\nBy Region: {json.dumps(stats['by_region'], indent=2)}")
            print(f"\nBy Status: {json.dumps(stats['by_status'], indent=2)}")
    except:
        pass
    
    print(f"\nView all resources at: {BASE_URL}/docs")

if __name__ == "__main__":
    populate_database()