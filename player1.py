import pika

url = 'amqps://hgglhdrq:PCCHVDRLB-NiZeJyAiHwnmu5dNUliGNg@jackal.rmq.cloudamqp.com/hgglhdrq'
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='fila')
channel.queue_declare(queue='vencedor')

def callback(ch, method, properties, body):
    resultado = body.decode()
    print(resultado)


def send():
    print("Hello player 1!")
    move = input("Enter your move (rock, paper, or scissors): ").lower()
    while move not in ['rock', 'paper', 'scissors']:
        print("Invalid move. Please try again.")
        move = input("Enter your move (rock, paper, or scissors): ").lower()
    channel.basic_publish(exchange='', routing_key='fila', body=move)
    
    channel.basic_consume(queue='vencedor', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
    
    print('Sent:', move)


send()
