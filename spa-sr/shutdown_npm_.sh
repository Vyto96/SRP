#!/bash/bin

ps aux | grep npm | awk '{ print $2 }' | xargs kill
ps aux | grep node | awk '{ print $2 }' | xargs kill


