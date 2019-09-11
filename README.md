# oci-resource-switchboard

Usage:

```bash
app.py --config <CONFIGURATION_FILE_PATH> --action <ACTION>
```

> Where action may be `start`, `stop` or `status` (default).

Sample configuration file:

```json
{
    "configFile": "~/.oci/config",
    "profile": "DEFAULT",
    "computes": [
        {
            "instance_id": "ocid1.instance.oc1.xxxxx"
        },
        {
            "instance_id": "ocid1.instance.oc1.xxxxx"
        }
    ],
    "databases": [
        { 
            "compartment_id": "ocid1.compartment.oc1..xxxxx",
            "db_system_id": "ocid1.dbsystem.oc1.us-ashburn-1.xxxxx" 
        },
        { 
            "compartment_id": "ocid1.compartment.oc1..xxxxx",
            "db_system_id": "ocid1.dbsystem.oc1.us-ashburn-1.xxxxx" 
        }
    ]
}
```