from controllers.processor import jobDistributor as commandProcessor

# Write tests here for testing the bot

bot = commandProcessor('remember hwyyou')
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