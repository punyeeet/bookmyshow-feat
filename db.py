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

async def getLock(seat_id):
    conn = pymysql.connect(host='localhost', user='root', password='1234', database='bookmyshow')
    cursor = conn.cursor()
    
    try:
        # Begin transaction
        conn.begin()
        # Lock the row exclusively
        cursor.execute("SELECT * FROM seats WHERE seat_id = %s FOR UPDATE NOWAIT", (seat_id,))
        # timer
        timer = threading.Timer(10, timeout_function)
        timer.start()
        
        row = cursor.fetchone()
        print(row)
        
        await asyncio.sleep(20)
        
        timer.cancel()
        
        conn.commit()
        
    except pymysql.Error as e:
        # Rollback transaction in case of an error
        print("Error: Already taken a lock on seat ---", e)
        conn.rollback()
        raise pymysql.Error(e)
    
    except TimeoutError as e:
        print('TImeout exception caught')
        conn.rollback()
        raise TimeoutError(e)

    finally:
        # Close cursor and connection
        cursor.close()
        conn.close()
    