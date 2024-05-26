import boto3
import time

# Initialize boto3 client
ec2 = boto3.client('ec2', region_name='eu-central-1')

# Replace with your instance ID and the fixed volume ID
INSTANCE_ID = 'i-0312ba672f0c27e69'
FIXED_VOLUME_ID = 'vol-017a374b9f273f130'


def get_root_volume_id(instance_id):
    response = ec2.describe_instances(InstanceIds=[instance_id])
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            for block_device in instance['BlockDeviceMappings']:
                if block_device['DeviceName'] == '/dev/sda1':  # Root volume device name
                    return block_device['Ebs']['VolumeId']
    raise ValueError("Root volume ID not found")


def attach_volume(instance_id, volume_id, device_name):
    ec2.attach_volume(InstanceId=instance_id, VolumeId=volume_id, Device=device_name)
    print(f"Volume {volume_id} attached to instance {instance_id} as {device_name}")


def detach_volume(volume_id):
    ec2.detach_volume(VolumeId=volume_id)
    print(f"Volume {volume_id} detached")


def delete_volume(volume_id):
    ec2.delete_volume(VolumeId=volume_id)
    print(f"Volume {volume_id} deleted")


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

        # Step 3: Detach the current root volume
        detach_volume(root_volume_id)
        waiter = ec2.get_waiter('volume_available')
        waiter.wait(VolumeIds=[root_volume_id])
        print("Old root volume detached")

        # Step 4: Attach the fixed volume as the root volume
        attach_volume(INSTANCE_ID, FIXED_VOLUME_ID, '/dev/sda1')

        # Step 5: Delete the old volume
        delete_volume(root_volume_id)

        # Step 6: Start the EC2 instance
        print("Starting instance...")
        ec2.start_instances(InstanceIds=[INSTANCE_ID])
        waiter = ec2.get_waiter('instance_running')
        waiter.wait(InstanceIds=[INSTANCE_ID])
        print("Instance started")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
