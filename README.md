
# MultiDB with PandasAI and FastAPI

This project is to use AI from dataframes in multiple sqlite databases



## Installation and execution

#### Create environment

```bash
virtualenv venv
```

#### Install dependencias

```bash
pip install -r requirements.txt
```

#### To execute fastApi

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

#### To send message to AI 
```curl
curl --location 'http://127.0.0.1:8080/api/v1/chat' \
--header 'Content-Type: application/json' \
--data '{
    "msg": ""
}'
```

