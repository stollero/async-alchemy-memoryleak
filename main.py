import uvicorn

if __name__ == "__main__":
    config = uvicorn.Config("app:app", host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    server.run()
