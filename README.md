# Websploit
- searchsploit can install locally, but there are some problems like getting caught by AV.
- Use vuls module, so I can search poc on github,inthewild too!

### Check it out... https://websploit-pbkqosy7ya-uc.a.run.app/
![mmmm](img/websploit.svg)



## Start with docker
```sh
cd websploit
docker compose up -d
# Stop container
#docker compose down
```

## Start locally to develop 
```sh
cd websploit
rye sync
rye run pytest                                                                                         
rye run streamlit run src/websploit/app.py
```
#### If you not install rye
```sh
curl -sSf https://rye-up.com/get | bash
# brew install rye
echo 'source "$HOME/.rye/env"' >> ~/.zshrc
source ~/.zshrc
```

## Deploy websploit to Cloud Run
When you push to GitHub, it automatically deploys to Cloud Run via Cloud Build!

## Deploy AWS environment by Terraform
Ensure you have access to the target resources via AWSCLI beforehand.
```sh
terraform apply
```

## memo
- python&cloud run→streamlitがwebsocketを使うのでlambdaは使えないのでcloud runで
  - https://chatgpt.com/share/e06aafe8-551b-42de-80dd-6cf3d49a0189
- google cloud endpointでレート制限→429エラーになれば以降は料金発生しない。
- billing alertでコンテナ停止　↑があればこれはとりあえず急ぎではない
- Will add lastupdate, Total number of records.