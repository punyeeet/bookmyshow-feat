from fastapi import FastAPI,HTTPException
import pymysql
from bookingservice import book_ticket,TimeoutError,InvalidSeatError


# Create an instance of FastAPI
app = FastAPI()
    
@app.get("/book/params")
async def handle_booking(seat_id:str,payment_time:str):
    print('enetered')
    try:
        response = await book_ticket(seat_id=seat_id,payment_time=payment_time)
        
    except pymysql.Error as e:
        raise HTTPException(400,"Seat already Reserved")
    
    except TimeoutError as e:
        raise HTTPException(408,"timeout")
    
    except InvalidSeatError as e:
        raise HTTPException(404,"Seat not available/already booked")
    
    except Exception as e:
        raise HTTPException(500,e)
    
    return {"mssg":" Acquired and released lock, booking successfull.", "booking_id": response["booking_id"] }


