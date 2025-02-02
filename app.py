import argparse
from fastapi import FastAPI, HTTPException, Request
import uvicorn

from bucket_token_algorithm import BucketTokenAlgorithm

app = FastAPI()

rate_limiting_strategy = BucketTokenAlgorithm(100)


@app.get('/unlimited')
def default():
    return "this api is not rate limited!!"

@app.get('/limited')
def default(request: Request):
    client_ip = request.client.host
    if rate_limiting_strategy.is_valid(client_ip):
        return "this api is rate limited"
    else:
        raise HTTPException(status_code=429, detail="too many requests, wait for some time")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the app with specified port.')
    parser.add_argument('--port', type=str, default=8000, help='Port number (default: 8000)')
    parser.add_argument('--rate', type=int, default=10, help='Rate')
    args = parser.parse_args()
    print(args)
    rate = args.rate - 1


    uvicorn.run(app, host="0.0.0.0", port=args.port)

# bucket size (10), rate of token addition (1 per second)
# a bucket for each unique ip address 