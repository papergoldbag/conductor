import uvicorn

if __name__ == '__main__':
    uvicorn.run('conductor.core.asgi:app', reload=True, workers=1, port=8081, host='127.0.0.1')
