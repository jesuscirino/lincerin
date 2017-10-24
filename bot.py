#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# By steemian @jesuscirino
import discord
import asyncio
import random
import pickle
import os
import datetime

BUFFER = 'dat.pkl'

client = discord.Client()

recibe_reporte = ''' ```markdown
# Hola te pediré los siguientes datos: 
    1. la url del post en steemit 
    2. la url de la fuente original
    3. palabra clave de la razón
    4. comentario
> Comienza ahora...
Coloca la url del steemit post:
    (Guardo luego de que des [ENTER])
    ``` '''
ayuda           = '''```markdown
# @lincerin es un bot que recopila reportes.
* Para invocarme porfavor verifica que me encuentre "En línea"

uso: ñ-[comando]

* ñ-?      : muestra este mensaje de ayuda
* ñ-r: recibe un reporte
* ñ-b: genera un body con todos los reportes recibidos
```'''
def ms(text):
    return '```markdown\n'+ text + '```'
def guardar(msg,key, date):
    if not os.path.isfile(BUFFER):
        dic_buffer = {}
    else:
        with open(BUFFER, 'rb') as fb:
            dic_buffer = pickle.load(fb)
    if key == 'post':
        dic_buffer[date] = {}
    dic_buffer[date][key] = msg
    with open(BUFFER, 'wb') as fb:
        pickle.dump(dic_buffer, fb)
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel,ms('calculando mensajes ..') )
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, ms('You have {} messages.').format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

    elif message.content.startswith('ñ-?'):
        await client.send_message(message.channel,ayuda)
    elif message.content.startswith('ñ-r'):
        date = str(datetime.datetime.now())
        tmp = await client.send_message(message.channel, recibe_reporte)
        def check_url(msg):
            return 'http' in msg.content
        def check_clave(msg):
            return 'plagio' in msg.content or 'spam' in msg.content
        def check_comm(msg):
            return 'ñ.' in msg.content
        msg = await client.wait_for_message(author=message.author, check=check_url)
        fmt = '> Datos por recibir: {0} \nIntroduce {1}:'
        guardar(msg.content,'post', date)
        await client.send_message(message.channel, ms(fmt.format(3,\
                'la fuente original (url)')))
        guardar(msg.content, 'font', date)
        msg = await client.wait_for_message(author=message.author, check=check_url)
        await client.send_message(message.channel, ms(fmt.format(2, \
                'razón o motivo (puede ser spam o plagio)')))
        msg = await client.wait_for_message(author=message.author, check=check_clave)
        guardar(msg.content, 'razon', date)
        await client.send_message(message.channel, ms(fmt.format(1, \
                'tu commentario, al terminar coloca [ñ.] en ese mismo mensaje.')))
        msg = await client.wait_for_message(author=message.author, check=check_comm)
        guardar(msg.content, 'comentario', date)
        await client.send_message(message.channel, ms('[Tu reporte está completo, gracias.]'))
    elif message.content.startswith('ñ-body'):
        tmp = await client.send_message(message.channel,ms(' generando body ...') )
        with open(BUFFER, 'rb') as fb:
            dic_buffer = pickle.load(fb)
            await client.send_message(message.channel, ms(str(dic_buffer)))
        lis_filas =[]
        body ='Autor/Author|Post|Acción/Action|Razón/Reason\n' + \
                '--- | --- | --- | ---' 
        for ids, dics in  dic_buffer.items():
            lis_filas.append(dics)
        for dic in lis_filas:
            body = body + '\n' + '[Usuario](steemit.com/' + dic['post'].split('/')[4] + \
                    ')|[Post](' + dic['post']+ ')|Bandera/Flag|' +\
                    dic['razon']

        await client.edit_message(tmp, ms(body))

client.run('MzcxMDI3NzkwNTQ5NjE0NTky.DMx05g._z5wBXEitxMBv7j3zUV89peSJYY')
#client.run('MzcyMTQ4MTI2MzE4MDY3NzE1.DM_9iw.-LLmxYI6GLD2juacQa3wuei4-Cg')
