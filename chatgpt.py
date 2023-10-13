import time
import psutil
import openai

# Set your OpenAI API key
openai.api_key = "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"

question_list = [
    # message 1
    "@NJTRANSIT_MBPJ @NJTRANSIT @aew1776 @FuckNjTransit "
    "8:45am……approaching AN HOUR WAITING"
    "STILL no shuttle bus has shown up at Salisbury Mills…."
    "We’re LITERALLY 1 stop from Harriman and nothing……",

    # message 2
    "somebody said dr. strange is the the best of the mcu",
    
    # message 3
    "bus out of service. engine off, lights out. not allowed to disembark as still on the highway, approaching the bronx, near lafayette avenue. bus driver already called for assistance, waiting quietly and patiently for the next bus https: and and t.co and 6sxouvhg1v"
]

def get_memory_usage():
    process = psutil.Process()
    return process.memory_info().rss

before_memory = get_memory_usage() # get initial memory usage
start_time = time.time() # start message execution time
messages = [
    {"role": "system", "content": "Assistant is an intelligent chatbot that based on a twitter post, finds the travel mode, people's sentiment, as well as the reason behind if the sentiment is negative."},
    {"role": "user", "content": "I've been waiting a long time for the subway. I have been waiting for half an hour already there is no subway coming."},
    {"role": "assistant", "content": "In the context, the user says he has been waiting for the subway, so the travel mode is subway. He complained about the long waiting time, so the sentiment is negative and the rason is the long waiting time."
                                     "Thus, the answer should be the following:"
                                     "Travel Mode: subway"
                                     "Sentiment: negative"
                                     "Reason: long waiting time"},
    {"role": "user", "content": "I like eating noodles"},
    {"role": "assistant", "content": "In the context, the user mentioned nothing about the travel mode, nor about his sentiment."
                                     "Thus, the answer should be the following:"
                                     "not related content"},
    {"role": "user", "content": "I want to give credit to the bus service in New York. There was flood last week but the bus service was still running. I was able to make it to work on time."},
    {"role": "assistant", "content": "In the context, the user mentioned he likes the bus service in New York, so the travel mode should be bus and the sentiment is positive."
                                     "Thus, the answer should be the following:"
                                     "Travel Mode: bus"
                                     "Sentiment: positive"},
    {"role": "user", "content": "I was so disappointed. I got a flight to Seattle last week. It was overbooked and I was bumped from the airplane with little compensation."},
    {"role": "assistant", "content": "In the context, the user mentioned he took a flight last week, so the travel mode should be airplane. The user said he was bumped from the airplane with little compensation, so the sentiment is negative and that should be the reason."
                                     "Thus, the answer should be the following:"
                                     "Travel Mode: airplane"
                                     "Sentiment: negative"
                                     "Reason: bumped from the airplane and received little compensation"}
]

reply = ''
reply_list = []

for question in question_list:
    if reply != '':
        messages.append(reply)
    messages.append(
        {
            "role": "user", "content": question
        }
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.2
    )
    reply = response['choices'][0]['message']
    reply_list.append(reply['content'])

end_time = time.time()
after_memory = get_memory_usage()
execution_time = end_time - start_time
memory_increase = after_memory - before_memory
print(reply_list)
print(f'Execution Time: {execution_time} seconds')
print(f'Memory Usage: {memory_increase} bytes')

# result:
# Q1: Travel Mode: shuttle bus; Sentiment: negative; Reason: Long waiting time and no shuttle bus showing up
# Q2: not related content
# Q3: Travel Mode: bus; Sentiment: negative; Reason: Bus out of service, engine off, lights out, unable to disembark on the highway
