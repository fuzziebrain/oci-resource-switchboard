import oci
import json
import sys
import argparse

VALID_ACTIONS = ['START', 'STOP', 'STATUS']
START_ACTION = 'START'
STOP_ACTION = 'STOP'
STATUS_ACTION = 'STATUS'
CAN_START = ['STOPPED']
CAN_STOP = ['AVAILABLE']

def executeDatabaseCommand(config, action):
    databaseClient = oci.database.DatabaseClient(config)

    print('Processing Database Systems...')

    for db in workspace['databases']:
        response = databaseClient.list_db_nodes(
            compartment_id=db['compartment_id']
            , db_system_id=db['db_system_id'])
        for dbNode in response.data:
            if (action == START_ACTION and dbNode.lifecycle_state in CAN_START) \
            or (action == STOP_ACTION and dbNode.lifecycle_state in CAN_STOP):
                databaseClient.db_node_action(db_node_id=dbNode.id, action = action)
                print('[ACTION] Starting...' if action == START_ACTION else '[ACTION] Stopping...' + dbNode.id)
            else:
                if action != STATUS_ACTION:
                    print('[ACTION] Skipping...' + dbNode.id)
            
            print('ocid: ' + dbNode.id + '. Current state: ' + dbNode.lifecycle_state)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Manage OCI resources.')
    parser.add_argument('-c', '--config', metavar='Configuration file path', required=True)
    parser.add_argument('-x', '--action', metavar='Action', choices=['status', 'start', 'stop'], default=STATUS_ACTION)
    args = parser.parse_args()

    try:
        workspaceFilePath = args.config
        action = args.action.upper()

        with open(workspaceFilePath, 'r') as workspaceFile:
            workspace = json.load(workspaceFile)

        config = oci.config.from_file(workspace['configFile'], workspace['profile'])
        
        executeDatabaseCommand(config, action)
    except:
        parser.usage()
        sys.exit(1)