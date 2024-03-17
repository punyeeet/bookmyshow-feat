import asyncio
import aiohttp

# Assuming FastAPI app is defined in another file named app.py
from main import app

# Define the base URL of your FastAPI server
BASE_URL = "http://localhost:8000"

async def fetch(url, headers):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.text()

async def test_multiple_origins_async():
    # Define two different origins
    origin1 = "http://example1.com"
    origin2 = "http://example2.com"

    # Define the headers for each request
    headers1 = {"Origin": origin1}
    headers2 = {"Origin": origin2}

    # Send requests to your FastAPI server asynchronously from different origins
    tasks = [
        fetch(f"{BASE_URL}/2", headers1),
        fetch(f"{BASE_URL}/2", headers2)
    ]
    responses = await asyncio.gather(*tasks)

    # Assert that both responses were received successfully
    for res in responses:
        print(res)
        
    assert len(responses) == 2
    # You can perform further assertions on response content if needed
    # assert "expected_response_content" in responses[0]
    # assert "expected_response_content" in responses[1]

# Run the asynchronous test
asyncio.run(test_multiple_origins_async())
