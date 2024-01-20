# How to Work Shifa BotP0

## Functions
If I say "hello bot", it responds "sup". If any other user or bot says "hello bot", the bot does nothing. 

If any user (not bot) says good morning, good night, or tell me a joke, the bot responds good morning {name}, good night {name}, or with a random dad joke depending on what the sender said. It does not reply to bots (itself included).

# Running it
It works by reading the last message sent every 3 seconds. If the last message sent is "hello bot" from a sender that is not me, nothing happens, but if another sender types good morning while it is running, it will respond. 
