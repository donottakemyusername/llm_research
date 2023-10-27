import time
import psutil
import openai
import pandas as pd

# Set your OpenAI API key
openai.api_key = "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"

# question_list = [
#     # message 1
#     "@NJTRANSIT_MBPJ @NJTRANSIT @aew1776 @FuckNjTransit "
#     "8:45am……approaching AN HOUR WAITING"
#     "STILL no shuttle bus has shown up at Salisbury Mills…."
#     "We’re LITERALLY 1 stop from Harriman and nothing……",
#
#     # message 2
#     "somebody said dr. strange is the the best of the mcu",
#
#     # message 3
#     "bus out of service. engine off, lights out. not allowed to disembark as still on the highway, approaching the bronx, near lafayette avenue. bus driver already called for assistance, waiting quietly and patiently for the next bus https: and and t.co and 6sxouvhg1v"
# ]

messages = [
    {"role": "system", "content": "Assistant is an intelligent chatbot. First read the twitter post, then identify the travel mode and the person's sentiment. If the sentiment is negative, identify the reason."},
    {"role": "system", "content": "Please write in the following format: Travel Mode: xxx, Sentiment: xxx, Reason: xxx."},
    {"role": "user", "content": "I've been waiting a long time for the subway. I have been waiting for half an hour already there is no subway coming."},
    {"role": "assistant", "content": "Travel Mode: subway"
                                     "Sentiment: negative"
                                     "Reason: long waiting time"},
    {"role": "user", "content": "I like eating noodles"},
    {"role": "assistant", "content": "not related content"},
    {"role": "user", "content": "I want to give credit to the bus service in New York. There was flood last week but the bus service was still running. I was able to make it to work on time."},
    {"role": "assistant", "content": "Travel Mode: bus"
                                     "Sentiment: positive"},
    {"role": "user", "content": "I was so disappointed. I got a flight to Seattle last week. It was overbooked and I was bumped from the airplane with little compensation."},
    {"role": "assistant", "content": "Travel Mode: airplane"
                                     "Sentiment: negative"
                                     "Reason: bumped from the airplane and received little compensation"}
]

df = pd.read_excel('sample.xlsx')
reply = ''
reply_list = []

for index, row in df.iterrows():
    messages.append({
        "role": "user", "content": row['processed_txt']
    })
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.2
    )
    reply = response['choices'][0]['message']['content']
    print(reply)
    reply_list.append(reply)
    messages.pop()

df['response'] = reply_list
df.to_excel('output.xlsx', index=False)

# reply = ''
# reply_list = []
#
# for question in question_list:
#     if reply != '':
#         messages.append(reply)
#     messages.append(
#         {
#             "role": "user", "content": question
#         }
#     )
#
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=messages,
#         temperature=0.2
#     )
#     reply = response['choices'][0]['message']
#     reply_list.append(reply['content'])
#
# print(reply_list)

