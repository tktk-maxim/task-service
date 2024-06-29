from fastapi import FastAPI


app = FastAPI(title="Task service")


@app.get("/")
async def root():
    return {"message": "Hello world"}
