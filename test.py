from worker.bot import commandProcessor
from time import sleep

#Write tests here for testing the bot

bot = commandProcessor('Heyyyyyy')
print(bot.find_and_execute_command())

bot = commandProcessor('rate 235 tourist')
print(bot.find_and_execute_command())

bot = commandProcessor('rate 1408', 4430672097006727)
print(bot.find_and_execute_command())

bot = commandProcessor('rate', 4430672097006727)
print(bot.find_and_execute_command())

bot = commandProcessor('help', 4430672097006727)
print(bot.find_and_execute_command())
































print('\n===========================\nAll test passed')