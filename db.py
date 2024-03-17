import pymysql
import time
import cryptography
import asyncio
import threading

class TimeoutError(Exception):
    pass

# Connect to the MySQL database
def timeout_function():
    raise TimeoutError("Operation timed out")

async def payment(transaction_id,payment_time):
    await asyncio.sleep(payment_time)
    print("Payment Successfull")
    return {"message":"Payment Successfull"}


async def getLock(seat_id,id):
    conn = pymysql.connect(host='localhost', user='root', password='1234', database='bookmyshow')
    cursor = conn.cursor()
    
    try:
        # Begin transaction
        conn.autocommit(False)
        # Lock the row exclusively
        cursor.execute("SELECT * FROM seats WHERE seat_id = %s FOR UPDATE NOWAIT", (seat_id,))
        # timer
        print(f'User {id} got the lock')

        #assign unique transaction id
        transaction_id = conn.thread_id()
        
        # limit for payment to be completed
        timeout = 10
        
        # random time taken by payment to get executed
        payment_time = 6
        
        
        response = await asyncio.wait_for(payment(transaction_id,payment_time),timeout)
        
        
        row = cursor.fetchone()
        print(row)
        
        # await asyncio.sleep(20)
        
        
        
        conn.commit()
        
    except pymysql.Error as e:
        # Rollback transaction in case of an error
        print("Error: Already taken a lock on seat ---", e)
        conn.rollback()
        raise pymysql.Error(e)
    
    except asyncio.TimeoutError as e:
        print('Timeout exception caught')
        conn.rollback()
        raise TimeoutError(e)

    finally:
        # Close cursor and connection
        cursor.close()
        conn.close()
    