#Mute my channel bot
## Бот, который блокирует отправку сообщений в канале

Запуск:

    docker build -t mute_my_chanel:latest . && docker run --env BOT_TOKEN=<token> --name mute_my_channel -d mute_my_chanel:latest 
