import discord as dc
import random as rand
import wikipedia, requests, json # Imports every module needed in this discord bot.

intents = dc.Intents.default() # Basically the config for the bot.
intents.message_content = True # This makes the bot be able to read messages.

class MyClient(dc.Client):
    async def on_ready(self): # When the bot loads up.
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):  
        if message.author == self.user: # This just ensures that if the message is from the bot it wont do anything.
            return
        
        if message.content.startswith("$hello"):  
            await message.channel.send("Hello!")

        if message.content.startswith("$jwordz"):
            await message.channel.send("JWORDZ SUCKS AT BLUE LOCK RIVALS") # this bot is right
    
        if message.content.startswith("$stop"):
            await message.channel.send("Bot is shutting down...")
            await client.close() # This is a kill switch
    
        if message.content.startswith("$wiki"):
            await self.wiki(message) # Calls the wiki function whenever you say $wiki.

        if message.content.startswith("$slot"):
            await self.slot_machine(message) # Same as the wiki function.
        
        if message.content.startswith("$meme"):
            resp = requests.get("https://meme-api.com/gimme") # Requests the data provided by a website
            json_data = json.loads(resp.text) # The information then gets loaded as a dictionary
            await message.channel.send(json_data['url']) # Honestly I got this information from ai and searching, but json_data is a dictionary and url is a key.
            return json_data['url'] # Actually doesn't do anything but I just put it here for safe measures for now.
        
    async def wiki(self, message):
        search = ""
        if message.content.startswith("$wiki"):
            query = message.content[len("$wiki "):].strip() # It gets the text after the "$wiki " message, ':' means range.

            if not query: # If there wasn't anything after "$wiki" then this code gets executed
                    await message.channel.send("Please type in a search query.") 
                    return

            if query:
                try:
                    result = wikipedia.summary(query, sentences=3) # Sends out a summary as a message in the channel, max of 3 sentences from the wiki link.
                    await message.channel.send(result)
                except wikipedia.exceptions.DisambiguationError as d: # This happens when the query goes into a disambiguation page.
                    await message.channel.send(f"Too many results have popped up, try narrowing down the search! {d}")
                except wikipedia.exceptions.PageError as p: # p doesn't actually server any purpose lol, but this is basically if the page aint there.
                    await message.channel.send("Couldn't find page, please try again.")
            
    async def slot_machine(self, message): # Simple slot machine codes, if you get 3 7️⃣s in a row you win.
        symbols = ["🌸","🍒","7️⃣","🪙","🍇","❌"]
        slot_results = rand.choices(symbols, k=3)
        if slot_results[0] == "7️⃣" and slot_results[1] == "7️⃣" and slot_results[2] == "7️⃣":
            await message.channel.send (f"{slot_results[0]} | {slot_results[1]} | {slot_results[2]}")
            await message.channel.send ("You're feeling extra lucky today, buy a lottery ticket!")
        else:
            await message.channel.send(f"{slot_results[0]} | {slot_results[1]} | {slot_results[2]}")
            await message.channel.send("Better luck next time...") 

client = MyClient(intents=intents) # From a class in the program to the client, this connects the dots.
client.run("x")  # This runs it to the correct bot.