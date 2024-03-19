import pymysql
import asyncio
from paymentservice import payment
from dotenv import load_dotenv
import os
load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')



class TimeoutError(Exception):
    pass

class InvalidSeatError(Exception):
    pass

# Connect to the MySQL database
def timeout_function():
    raise TimeoutError("Operation timed out")


async def book_ticket(seat_id,payment_time):
    
    if not (DB_PASSWORD and DB_HOST and DB_USER):
        raise Exception('Invalid/Unavailable Database credentials')
        
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database='bookmyshow')
    cursor = conn.cursor()
    
    try:
        # Begin transaction
        conn.autocommit(False)
        
        cursor.execute("SELECT status from seats where seat_id = %s",(seat_id))
        
        status = cursor.fetchone()
        
        
        if status and status[0]!='available':
            print(status)
            raise InvalidSeatError("Seat not available/already booked")
        
        # Lock the row exclusively
        cursor.execute("SELECT * FROM seats WHERE seat_id = %s FOR UPDATE NOWAIT", (seat_id,))

        #assign unique transaction id
        transaction_id = conn.thread_id()
        
        # time limit for payment to be completed
        PAYMENT_TIMEOUT = 10
        
        response = await asyncio.wait_for(payment(transaction_id,int(payment_time)),PAYMENT_TIMEOUT)
        
        print(response)
        
        cursor.execute('UPDATE seats SET status = %s, booking_id = %s WHERE seat_id = %s',('booked',transaction_id,seat_id))
        
        conn.commit()
        
        return { "booking_id": response["booking_id"] }
        
    except pymysql.Error as e:
        # Rollback transaction in case of an error
        print("Error: Already taken a lock on seat", e)
        conn.rollback()
        raise pymysql.Error(e)
    
    except asyncio.TimeoutError as e:
        print('Booking Session Timed-out')
        conn.rollback()
        raise TimeoutError(e)
    
    except InvalidSeatError as e:
        print('Seat not available/already booked')
        raise InvalidSeatError(e)
    
    except Exception as e:
        raise Exception(e)
        
    finally:
        # Close cursor and connection
        cursor.close()
        conn.close()

    