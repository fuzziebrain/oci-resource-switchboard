import oci
import json
import sys
import argparse

VALID_ACTIONS = ['START', 'STOP', 'STATUS']
START_ACTION = 'START'
STOP_ACTION = 'STOP'
STATUS_ACTION = 'STATUS'
CAN_START = ['STOPPED']
CAN_STOP = ['AVAILABLE', 'RUNNING']

def executeComputeCommand(computes, config, action):
    computeClient = oci.core.ComputeClient(config)

    print('Processing Compute Instances...')

    for c in computes:
        response = computeClient.get_instance(instance_id=c['instance_id'])
        instance = response.data
        print(instance.display_name + ' status: ' + instance.lifecycle_state)

        if (action == START_ACTION and instance.lifecycle_state in CAN_START) \
            or (action == STOP_ACTION and instance.lifecycle_state in CAN_STOP):
            response = computeClient.instance_action(
                instance_id=c['instance_id']
                , action=action
            )

            print(
                ('[ACTION] Starting...' if action == START_ACTION else '[ACTION] Stopping...')
                + instance.display_name
            )
        else:
            print('[ACTION] Skipping...' + instance.display_name)

def executeDatabaseCommand(databases, config, action):
    databaseClient = oci.database.DatabaseClient(config)

    print('Processing Database Systems...')

    for db in databases:
        response = databaseClient.list_db_nodes(
            compartment_id=db['compartment_id']
            , db_system_id=db['db_system_id'])
        for dbNode in response.data:
            if (action == START_ACTION and dbNode.lifecycle_state in CAN_START) \
            or (action == STOP_ACTION and dbNode.lifecycle_state in CAN_STOP):
                databaseClient.db_node_action(db_node_id=dbNode.id, action = action)
                print(
                    ('[ACTION] Starting...' if action == START_ACTION else '[ACTION] Stopping...') 
                    + dbNode.hostname)
            else:
                if action != STATUS_ACTION:
                    print('[ACTION] Skipping...' + dbNode.hostname)
            
            print('DB hostname: ' + dbNode.hostname + '. Current state: ' + dbNode.lifecycle_state)

def main():
    parser = argparse.ArgumentParser(description='Manage OCI resources.')
    parser.add_argument('-c', '--config', metavar='<CONFIGURATION_FILE_PATH>', required=True)
    parser.add_argument('-x', '--action', metavar='<ACTION>', choices=['status', 'start', 'stop'], default=STATUS_ACTION)
    args = parser.parse_args()

    try:
        workspaceFilePath = args.config
        action = args.action.upper()

        with open(workspaceFilePath, 'r') as workspaceFile:
            workspace = json.load(workspaceFile)

        config = oci.config.from_file(workspace['configFile'], workspace['profile'])
        
        executeComputeCommand(workspace['computes'], config, action)
        executeDatabaseCommand(workspace['databases'], config, action)
    except:
        parser.usage()
        sys.exit(1)

if __name__ == "__main__":
    main()