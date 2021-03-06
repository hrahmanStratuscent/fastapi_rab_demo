import pika
from fastapi import FastAPI, HTTPException, Body

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to RabbitMQ-FastAPI"}

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    message = body.decode("utf-8")
    if message == "hey":
        print("hey there")
    elif message == "hello":
        print("well hello there")
    else:
        print(f"sorry i did not understand {message}")
    print(" [x] Done")


@app.post("/message")
def get_message():
    try:
        connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq-0.rabbitmq-headless.keda.svc.cluster.local", port=5672, 
        credentials=pika.PlainCredentials("user", "PASSWORD")))
        channel = connection.channel()
        channel.queue_declare(queue='hello')
        
        channel.basic_consume(on_message_callback=callback, queue="hello", auto_ack=True)
        print(" [*] Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        

# @app.get("/error")
# async def post_message():
#     try:
#         connection = pika.BlockingConnection(
#             pika.ConnectionParameters(host="localhost")
#             )
#         channel = connection.channel()
#         channel.exchange_declare(exchange='logs', exchange_type='direct')
#         result = channel.queue_declare(exclusive=True, queue="")
#         queue_name = result.method.queue
#         channel.queue_bind(exchange='logs', queue=queue_name, routing_key='error')

#         def callback(ch, method, properties, body):
#             print(" [x] %r:%r" % (method.routing_key, body))
#         channel.basic_consume(on_message_callback=callback, queue=queue_name, auto_ack=True)
#         await channel.start_consuming()

#         return {"message": "Message received"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @app.get("/hello")
# async def post_message():
#     try:
#         connection = pika.BlockingConnection(
#             pika.ConnectionParameters(host="localhost")
#             )
#         channel = connection.channel()
#         channel.exchange_declare(exchange='logs', exchange_type='direct')
#         result = channel.queue_declare(exclusive=True, queue="")
#         queue_name = result.method.queue
#         channel.queue_bind(exchange='logs', queue=queue_name, routing_key='hello')

#         def callback(ch, method, properties, body):
#             print(" [x] %r:%r" % (method.routing_key, body))
#         channel.basic_consume(on_message_callback=callback, queue=queue_name, auto_ack=True)
#         await channel.start_consuming()

#         return {"message": "Message received"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
