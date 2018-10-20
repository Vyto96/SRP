#!/bash/bin

ps aux | grep gunicorn | grep SRP | awk '{ print $2 }' | xargs kill

#ps axjf

