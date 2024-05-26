import boto3
import time

# Initialize boto3 client
ec2 = boto3.client('ec2', region_name='eu-central-1')

# Replace with your instance ID
INSTANCE_ID = 'i-0fecbe6979a95a080'


def get_root_volume_id(instance_id):
    response = ec2.describe_instances(InstanceIds=[instance_id])
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            for block_device in instance['BlockDeviceMappings']:
                if block_device['DeviceName'] == '/dev/sda1':  # Root volume device name
                    return block_device['Ebs']['VolumeId']
    raise ValueError("Root volume ID not found")


def create_snapshot(volume_id):
    response = ec2.create_snapshot(VolumeId=volume_id, Description="Initial state snapshot")
    snapshot_id = response['SnapshotId']
    print(f"Snapshot created: {snapshot_id}")
    return snapshot_id


def create_volume(snapshot_id, availability_zone):
    response = ec2.create_volume(SnapshotId=snapshot_id, AvailabilityZone=availability_zone)
    volume_id = response['VolumeId']
    print(f"Volume created: {volume_id}")
    return volume_id


'''

def attach_volume(instance_id, volume_id, device_name):
    ec2.attach_volume(InstanceId=instance_id, VolumeId=volume_id, Device=device_name)
    print(f"Volume {volume_id} attached to instance {instance_id} as {device_name}")

def detach_volume(volume_id):
    ec2.detach_volume(VolumeId=volume_id)
    print(f"Volume {volume_id} detached")

def delete_volume(volume_id):
    ec2.delete_volume(VolumeId=volume_id)
    print(f"Volume {volume_id} deleted")
'''


def main():
    try:
        # Step 1: Stop the EC2 instance
        print("Stopping instance...")
        ec2.stop_instances(InstanceIds=[INSTANCE_ID])
        waiter = ec2.get_waiter('instance_stopped')
        waiter.wait(InstanceIds=[INSTANCE_ID])
        print("Instance stopped")

        # Step 2: Get the root volume ID
        root_volume_id = get_root_volume_id(INSTANCE_ID)
        print(f"Root volume ID: {root_volume_id}")

        # Step 3: Create a snapshot of the current root volume
        snapshot_id = create_snapshot(root_volume_id)

        # Wait for the snapshot to complete
        print("Waiting for snapshot to complete...")
        waiter = ec2.get_waiter('snapshot_completed')
        waiter.wait(SnapshotIds=[snapshot_id])
        print("Snapshot completed")

        # Step 4: Create a new volume from the snapshot
        instance_info = ec2.describe_instances(InstanceIds=[INSTANCE_ID])['Reservations'][0]['Instances'][0]
        availability_zone = instance_info['Placement']['AvailabilityZone']
        new_volume_id = create_volume(snapshot_id, availability_zone)

        # Wait for the volume to become available
        print("Waiting for volume to become available...")
        waiter = ec2.get_waiter('volume_available')
        waiter.wait(VolumeIds=[new_volume_id])
        print("New volume available")
        '''
        # Step 5: Detach the current root volume
        detach_volume(root_volume_id)
        waiter = ec2.get_waiter('volume_available')
        waiter.wait(VolumeIds=[root_volume_id])
        print("Old root volume detached")

        # Step 6: Attach the new volume as the root volume
        attach_volume(INSTANCE_ID, new_volume_id, '/dev/sda1')

        # Step 7: Delete the old volume
        delete_volume(root_volume_id)

        # Step 8: Start the EC2 instance
        print("Starting instance...")
        ec2.start_instances(InstanceIds=[INSTANCE_ID])
        waiter = ec2.get_waiter('instance_running')
        waiter.wait(InstanceIds=[INSTANCE_ID])
        print("Instance started")
        '''
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
