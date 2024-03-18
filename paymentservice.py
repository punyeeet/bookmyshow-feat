import asyncio

# simulating payment gateway time consumption

async def payment(transaction_id,payment_time):
    
    await asyncio.sleep(payment_time)
    
    print("Payment Successfull")
    return {"message":f"Payment for transID:{transaction_id} Successfull"}