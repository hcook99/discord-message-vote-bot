import discord
import time

TOKEN = 'NTI4MDgxNTgxNzY4ODM1MDgy.DwdSvA.QRw6VzST0xSilX0vBp7BwIYxXvc'

client = discord.Client()
timeMap = {}
numVote = 0


@client.event
async def on_message(message):


    if message.author == client.user:
        return

    if message.content.startswith('!delete'):
        global numVote
        numVote += 1
        messageD = message.content.split(" ")
        if(len(messageD)>1):
            messageToAlertVoting = 'Beginning Vote for ' + str(numVote)
            await client.send_message(message.channel, messageToAlertVoting)
            channelID = message.channel
            messageIDDelete = messageD[1]
            saveCurrentTime = time.time()
            timeMap[numVote] = [messageIDDelete, saveCurrentTime, 0, channelID]

    if message.content.startswith('!vote'):
        breakUpMessage = message.content.split(" ")

        if(len(breakUpMessage)==2):
            if int(breakUpMessage[1]) in timeMap.keys():
                listOfDel = timeMap.get(int(breakUpMessage[1]))
                if (time.time() - listOfDel[1] < 29):
                    valueToIncrease = listOfDel[2]
                    valueToIncrease += 1
                    listOfDel[2] = valueToIncrease
                    print(listOfDel[2])
                    await client.send_message(message.channel, ('Current vote count for '+breakUpMessage[1]+' is '+str(valueToIncrease)))
                    await check_delete(breakUpMessage[1])
                else:
                    timeMap.pop(int(breakUpMessage[1]))
                    await client.send_message(message.channel, ('Time up for ' + breakUpMessage[1]))



async def check_delete(key):
    global timeMap
    listOfDel = timeMap.get(int(key))
    online = 0
    for x in client.get_all_members():
        if x.status == discord.Status.online:
            online += 1
    if(listOfDel[2]>=int(online/2)):
        msg = await client.get_message(listOfDel[3], listOfDel[0])
        await  client.delete_message(msg)
        timeMap.pop(int(key))
    else:
        timeMap.pop(int(key))


client.run(TOKEN)