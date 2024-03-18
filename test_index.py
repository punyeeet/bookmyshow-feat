import pymysql
import pytest
import httpx
from main import app
import asyncio
from dotenv import load_dotenv
import os
load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')





def setup_function():
    if not (DB_PASSWORD and DB_HOST and DB_USER):
        raise Exception('Invalid/Unavailable Database credentials')
    
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database='bookmyshow')
    cursor = conn.cursor() 
       
    cursor.execute('UPDATE `bookmyshow`.`seats` SET `status` = %s, `booking_id` = NULL WHERE `seat_id` = %s', ('available', 1))
    cursor.execute('UPDATE `bookmyshow`.`seats` SET `status` = %s, `booking_id` = NULL WHERE `seat_id` = %s', ('available', 2))
    conn.commit()
        
# test case to book two different tickets at a time and pyament time '<' time limit hence successfull
@pytest.mark.asyncio
async def test_two_async_requests():
    async with httpx.AsyncClient(app=app, base_url="http://localhost:8000") as client:
        tasks = [client.get("/book/params?seat_id=1&payment_time=9"), client.get("/book/params?seat_id=2&payment_time=9")]
        responses = await asyncio.gather(*tasks)
        
    for response in responses:
        assert response.status_code == 200
        
        
# test case where two users try to book same seat concurrently and only one succeeds
@pytest.mark.asyncio
async def test_two_async_requests_same_seat():
    async with httpx.AsyncClient(app=app, base_url="http://localhost:8000") as client:
        tasks = [client.get("/book/params?seat_id=2&payment_time=9"),client.get("/book/params?seat_id=2&payment_time=9")]
        responses = await asyncio.gather(*tasks)
        
    for response in responses:
        assert (response.status_code == 200 or response.status_code == 400)
        
        
# test case where two users try to book same seat and only one proceeds to the payments and then fails due to timeout.
# Then a third request comes to book the same seat which succeeds as the seat is now free.
@pytest.mark.asyncio
async def test_three_async_requests():
    async with httpx.AsyncClient(app=app, base_url="http://localhost:8000") as client:
        tasks = [client.get("/book/params?seat_id=2&payment_time=11"),client.get("/book/params?seat_id=2&payment_time=11")]
        responses_one = await asyncio.gather(*tasks)
        
        tasks = [client.get("/book/params?seat_id=2&payment_time=5")]
        
        responses_two = await asyncio.gather(*tasks)
        
    for response in responses_one:
        assert (response.status_code == 408 or response.status_code == 400)
        
    for response in responses_two:
        assert response.status_code == 200
        
        
# test case where two users try to book same seat and only one succeeds.
# And a third user comes to book a different seat which also succeeds. All users come concurrently.
@pytest.mark.asyncio
async def test_three_async_requests_():
    async with httpx.AsyncClient(app=app, base_url="http://localhost:8000") as client:
        tasks = [client.get("/book/params?seat_id=2&payment_time=5"), client.get("/book/params?seat_id=2&payment_time=5"), client.get("/book/params?seat_id=1&payment_time=5")]
        responses = await asyncio.gather(*tasks)
        
        codes = []
        
        for response in responses:
            codes.append(response.status_code)
            
        assert codes.count(200) == 2
        assert codes.count(400) == 1
        
    
        
        

        

