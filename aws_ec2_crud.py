import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def get_credentials():
    print("Por favor, insira suas credenciais AWS:")
    access_key = input("Access Key: ")
    secret_key = input("Secret Key: ")
    region = input("Região AWS (ex: us-east-1): ")
    return access_key, secret_key, region

def create_ec2_instance(ec2):
    print("Criando instância EC2...")
    instances = ec2.create_instances(
        ImageId='ami-0c94855ba95c71c99',  # Exemplo: Amazon Linux 2 AMI
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',
    )
    print(f"Instância criada com ID: {instances[0].id}")

def list_ec2_instances(ec2):
    print("Listando instâncias EC2...")
    for instance in ec2.instances.all():
        print(f"ID: {instance.id}, Estado: {instance.state['Name']}")

def update_ec2_instance(ec2):
    instance_id = input("Insira o ID da instância que deseja parar: ")
    instance = ec2.Instance(instance_id)
    print(f"Parando instância {instance_id}...")
    instance.stop()
    instance.wait_until_stopped()
    print(f"Instância {instance_id} parada.")

def delete_ec2_instance(ec2):
    instance_id = input("Insira o ID da instância que deseja terminar: ")
    instance = ec2.Instance(instance_id)
    print(f"Terminando instância {instance_id}...")
    instance.terminate()
    instance.wait_until_terminated()
    print(f"Instância {instance_id} terminada.")

def main():
    try:
        access_key, secret_key, region = get_credentials()
        ec2 = boto3.resource(
            'ec2',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )
    except (NoCredentialsError, PartialCredentialsError):
        print("Credenciais inválidas. Por favor, tente novamente.")
        return

    while True:
        print("\nEscolha uma operação:")
        print("1. Criar instância EC2")
        print("2. Listar instâncias EC2")
        print("3. Atualizar instância EC2 (Parar)")
        print("4. Deletar instância EC2 (Terminar)")
        print("5. Sair")

        choice = input("Opção: ")

        if choice == '1':
            create_ec2_instance(ec2)
        elif choice == '2':
            list_ec2_instances(ec2)
        elif choice == '3':
            update_ec2_instance(ec2)
        elif choice == '4':
            delete_ec2_instance(ec2)
        elif choice == '5':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
