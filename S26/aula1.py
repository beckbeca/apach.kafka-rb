import boto3

# Inicialize o cliente do SQS
sqs = boto3.client('sqs', region_name='us-east-1')

# Crie uma fila padrão
standard_queue = sqs.create_queue(QueueName='StandardQueue')

# Crie uma fila FIFO
fifo_queue = sqs.create_queue(QueueName='FIFOQueue-Rebeca.fifo', Attributes={'FifoQueue': 'true'})

# Enviando mensagens para a fila padrão
for i in range(5):
    sqs.send_message(QueueUrl=standard_queue['QueueUrl'], MessageBody=f'Pedido {i}')

# Enviando mensagens para a fila FIFO
for i in range(5):
    sqs.send_message(
        QueueUrl=fifo_queue['QueueUrl'],
        MessageBody=f'Pedido {i}',
        MessageGroupId='pedido',
        MessageDeduplicationId=str(i)
    )

# Recebendo mensagens da fila padrão
print("Mensagens recebidas da fila padrão:")
msgs = sqs.receive_message(QueueUrl=standard_queue['QueueUrl'], MaxNumberOfMessages=5)
for msg in msgs.get('Messages', []):
    print(msg['Body'])

# Recebendo mensagens da fila FIFO
print("Mensagens recebidas da fila FIFO:")
msgs = sqs.receive_message(QueueUrl=fifo_queue['QueueUrl'], MaxNumberOfMessages=5)
for msg in msgs.get('Messages', []):
    print(msg['Body'])

# Apague as filas para limpeza
#sqs.delete_queue(QueueUrl=standard_queue['QueueUrl'])
#sqs.delete_queue(QueueUrl=fifo_queue['QueueUrl'])