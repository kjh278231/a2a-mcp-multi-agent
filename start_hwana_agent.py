import uvicorn
from hwana.agent import app

uvicorn.run(app=app, port=8002, host="localhost")
