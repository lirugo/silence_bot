### How to build the Docker image
```bash
docker build --no-cache -t silence-bot .

docker run -e SILENCE_BOT_TOKEN=$SILENCE_BOT_TOKEN silence-bot 
```