from fastapi import Fastapi
import uvicorn

app = Fastapi()



if __file__ == "__main__":
    uvicorn.run(app, "0.0.0.0")