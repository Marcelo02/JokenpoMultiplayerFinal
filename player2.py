import pika

url = 'amqps://hgglhdrq:PCCHVDRLB-NiZeJyAiHwnmu5dNUliGNg@jackal.rmq.cloudamqp.com/hgglhdrq'
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='fila')
channel.queue_declare(queue='vencedor')


def callback(ch, method, properties, body):
    p1_move = body.decode()
    p2_move = get_player_move()
    result = determine_winner(p1_move, p2_move)
    print(result)
    channel.basic_publish(exchange='', routing_key='vencedor', body=result)



def get_player_move():
    while True:
        print("Hello player 2!")
        move = input("Enter your move (rock, paper, or scissors): ").lower()
        if move in ['rock', 'paper', 'scissors']:
            return move
        else:
            print("Invalid move. Please try again.")


def determine_winner(p1_move, p2_move):
    if p1_move == p2_move:
        return "It's a tie!"
    elif (p1_move == 'rock' and p2_move == 'scissors') or \
            (p1_move == 'paper' and p2_move == 'rock') or \
            (p1_move == 'scissors' and p2_move == 'paper'):
        return "Player 1 wins!"
    else:
        return "Player 2 wins!"


def play_game():
    print("Welcome to Rock, Paper, Scissors!")

    channel.basic_consume(queue='fila', on_message_callback=callback, auto_ack=True)
    print("Waiting for opponent...")
    channel.start_consuming()


play_game()
