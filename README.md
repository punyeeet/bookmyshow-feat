# APP: BookMyShow 
## Feature: Real time booking and Handling concurrent booking requests for the same/diiferent seats by multiple users.

## Setup
### Virtual Environment
1. Extract the folder `SeatBooking` from the in the local machine.
2. Open the `SeatBooking` directory in the Terminal (UNIX) 
3. Load the dependencies using the following command:
   `pipenv install -r requirements.txt`
   This loads all the dependencies that's required to run the program.

### MySQL:
To set up MySQL for your application, you'll need to follow these general steps:

1. **Install MySQL Server**: Install **MySQL Community Server** on your system. You can download MySQL Server from the official website or use a package manager specific to your operating system.

2. **Start MySQL Server**: After installation, start the MySQL Server service. The commands to start the service may vary depending on your operating system.

3. **Access MySQL Shell**: Access the MySQL shell using a MySQL client. You can use the command-line client (`mysql` command) or a graphical user interface (GUI) tool like MySQL Workbench .

4. **Create Database**: Create a new database for your application using the `CREATE DATABASE` command. For example:
   ```sql
   CREATE DATABASE bookmyshow;
   ```

5. **Create Tables**: Define the tables required for your application schema. You can use the `CREATE TABLE` command to create tables with appropriate columns and constraints. For our program the SQL queries to create the required table(i.e. `seats`) is given:
   ```sql
   CREATE TABLE seats (
       seat_id INT PRIMARY KEY,
       booking_id VARCHAR(10),
       seat_status ENUM('available', 'reserved', 'booked')
   );
   ```

6. **Modifying Environment Variable Values for Database Configuration**

	In the provided application setup, environment variables such as `DB_HOST`, `DB_USER`, and `DB_PASSWORD` are used to configure database connection details. These variables allow for flexible configuration and enhance security by keeping sensitive information separate from the application code.
	
	To edit the values of these environment variables according to specific requirements, you can follow these steps:
	
	1. **Locate the .env File**:
	   - The .env file contains key-value pairs of environment variables used by the application.
	   - It is typically located in the root directory of the project.
	
	2. **Open the .env File**:
	   - You can use a text editor or an integrated development environment (IDE) to open the .env file.
	
	3. **Modify Environment Variable Values**:
	   - Locate the lines corresponding to the database configuration variables (`DB_HOST`, `DB_USER`, `DB_PASSWORD`).
	   - Edit the values assigned to these variables according to the desired database configuration.
	   - For example:
	     ```python
	     DB_HOST=your_mysql_host_address
	     DB_USER=your_mysql_username
	     DB_PASSWORD=your_mysql_user_password
	     ```
	
	4. **Save the Changes**:
	   - After modifying the environment variable values, you should save the changes to the .env file.
	
	5. **Reload the Application**:
	   - If the application is already running, you may need to reload or restart the application for the changes to take effect.
	   - You can restart the application server or reload the environment variables depending on the deployment environment.

 7. **Insert Values into the `seats` table:** 
	The requires values of the seats for proper testing can be inserted using the following SQL statements:
```sql
	-- Inserting values into the seats table
	INSERT INTO seats (seat_id, booking_id, seat_status) VALUES
	(1, NULL, 'available'),
	(2, NULL, 'available');

```
## Usage
### Usage Details

##### Prerequisites:
- Ensure that you have Python 3.x installed on your system.
- Install the required Python packages by running `pip install -r requirements.txt`.
- Set up a MySQL database and configure the connection details in the `.env` file.

##### Running the Application:
1. Start the FastAPI server by running the command:
   ```
   uvicorn main:app --host 127.0.0.1 --port 8000
   ```
   This command will launch the FastAPI server, and the application will be accessible at `http://localhost:8000`.

##### Testing the Application:
1. Execute the provided test script `test_index.py` to run the test cases against the application:
   ```
   pytest test_index.py
   ```
   This command will execute all the test cases defined in the script and display the test results.

##### Using the API Endpoints:
- Once the application is running, you can access the API endpoints using an HTTP client (e.g., Postman, cURL) or by sending HTTP requests programmatically.
- The main API endpoint for booking seats is `/book/params`, which accepts seat ID and payment time as query parameters. Example usage:
  ```
  GET http://localhost:8000/book/params?seat_id=1&payment_time=9
  ```
  This request attempts to book the seat with ID 1 with a payment time of 9 units.
- The application will return appropriate responses based on the outcome of the booking attempt, including success, seat already reserved, timeout, or invalid seat.

Following these usage details will enable you to effectively run the application, test its functionality, and interact with the API endpoints to perform seat bookings.

### Testing Details 

The provided `test_index.py` script contains test cases for testing the functionality of the booking endpoint implemented in the `handle_booking` function of the FastAPI application. Below are the testing details along with a write-up for each test case:

1. **Setup and Teardown Fixture**:
   - The `setup_function` fixture is used to set up the database environment before each test case by updating the seat statuses and booking IDs accordingly. After each test case, the database state is reverted back to its initial state.
   - This fixture ensures that each test case operates on a clean and consistent database environment.

2. **Test Case: `test_two_async_requests`**:
   - This test case simulates two different users attempting to book two different seats simultaneously.
   - Both booking requests have payment times less than the time limit, ensuring successful bookings.
   - Expected Behavior: Both requests should return a status code of 200 (OK), indicating successful bookings.

3. **Test Case: `test_two_async_requests_same_seat`**:
   - This test case simulates two users attempting to book the same seat concurrently.
   - Only one of the booking requests should succeed, while the other should fail due to the seat already being reserved.
   - Expected Behavior: One request should return a status code of 200 (OK), indicating a successful booking, and the other should return a status code of 400 (Bad Request), indicating that the seat is already reserved.

4. **Test Case: `test_three_async_requests`**:
   - This test case simulates two users attempting to book the same seat concurrently, followed by a third user attempting to book the same seat after a timeout occurs for one of the previous bookings.
   - The first two booking requests should fail due to either one or both exceeding the payment time limit, resulting in a timeout or the seat already being reserved.
   - The third booking request should succeed since the seat becomes available after the timeout occurs for one of the previous bookings.
   - Expected Behavior: The first two requests should return a status code of 408 (Request Timeout) or 400 (Bad Request), and the third request should return a status code of 200 (OK).

5. **Test Case: `test_three_async_requests_`**:
   - This test case simulates three users attempting to book seats concurrently, with two users attempting to book the same seat and one user attempting to book a different seat.
   - One of the users attempting to book the same seat should succeed, while the other should fail due to the seat already being reserved. The user attempting to book the different seat should succeed.
   - Expected Behavior: Two requests should return a status code of 200 (OK) for successful bookings, and one request should return a status code of 400 (Bad Request) for a failed booking attempt.

These test cases cover various scenarios to ensure the correct behavior of the booking endpoint under different conditions, including concurrent requests, seat availability, and payment time limits. They help validate the robustness and reliability of the booking functionality implemented in the FastAPI application.

## Endpoint Details

Here are the details for the `/book/params` endpoint:

- **HTTP Method**: GET
- **Path**: /book/params
- **Query Parameters**:
  - `seat_id`: Represents the identifier of the seat to be booked. (Type: String)
  - `payment_time`: Represents the time allocated for payment processing. (Type: String)
- **Description**: This endpoint is used to handle booking requests for a specific seat. 
	- It takes the seat ID and payment time as query parameters to simulate different scenarios during testing. 
	- In a real-world scenario, the payment time parameter would not be included as it is not typically provided by clients during booking. 
	- The endpoint attempts to book the seat using the `book_ticket` function. 
	- If the booking process is successful, it returns a success message. If any errors occur during the booking process, appropriate HTTP responses are returned.
- **Responses**:
  - Success (Status Code: 200):
    - Body: `{"message": "Acquired and released lock, booking successful." , "booking_id": Booking ID}`
    - Description: Indicates that the seat was successfully booked, and the lock on the seat was released.
  - Seat Already Reserved (Status Code: 400):
    - Body: `{"detail": "Seat already Reserved"}`
    - Description: Indicates that the seat is already reserved and cannot be booked.
  - Timeout (Status Code: 408):
    - Body: `{"detail": "Timeout"}`
    - Description: Indicates that the booking process timed out before completion.
  - Invalid Seat (Status Code: 404):
    - Body: `{"detail": "Seat not available/already booked"}`
    - Description: Indicates that the specified seat is not available or already booked.
  - Internal Server Error (Status Code: 500):
    - Body: `{"detail": "Internal Server Error"}`
    - Description: Indicates that an unexpected error occurred during the booking process.

This endpoint follows the RESTful principles and accepts query parameters to specify the seat ID and payment time. It provides clear and concise responses to indicate the outcome of the booking attempt, enabling clients to handle different scenarios appropriately.

## Database Schema
Schema for the `Seats` table:

```sql
   CREATE TABLE seats (
       seat_id INT PRIMARY KEY,
       booking_id VARCHAR(10),
       seat_status ENUM('available', 'reserved', 'booked')
   );
```

Explanation of the schema:

- `seat_id`: An integer column serving as the primary key for identifying each seat.
  
- `booking_id`: A variable character column (VARCHAR) used to store the booking ID associated with a booked seat. It can hold up to 10 characters. This field can be NULL if the seat is available or reserved. Once booked, it will contain the ID of the user who booked the seat.
  
- `seat_status`: An `ENUM` field to represent the status of the seat. It can have three possible values: 'available', 'reserved', or 'booked'. This field indicates whether the seat is available for booking, reserved by a user, or already booked by a user.

This schema provides a basic structure to manage seat information, including its ID, the user who booked it (if any), and its current status. 

## Challenges Faced
### **Challenge 1: Communication Between Threads**

**Problem**: Ensuring _immediate_ communication between threads to allow either the ``seat_booking`` function or the `timeout` function to stop the other's operation depending on which one finishes first was a problem. 

**Solution**:
- We implemented asynchronous execution using `asyncio` instead of threads. 
- By utilizing asynchronous programming with `asyncio`, the code can efficiently manage and coordinate the execution of tasks without the need for explicit thread communication. 
- The `get_lock` function now uses `await` to wait for asynchronous operations such as `payment` and `asyncio.wait_for()` to handle timeouts.

By leveraging `asyncio`'s features and carefully orchestrating the interactions between the booking and timeout functions, We successfully implemented a robust communication mechanism that allowed either function to terminate the other's operation as needed.

---

### **Challenge 2: Simultaneous Requests from SwaggerUI**

**Problem:** It was difficult to simulate simultaneous requests from the SwaggerUI, which necessitated the creation of a custom test script.

**Solution:**
To overcome this challenge, we employed a custom Python script named `test.py` to simulate concurrent requests and test the system's behaviour under load. This script utilized Python's `asyncio` and `aiohttp` libraries to send HTTP requests asynchronously and analyze the system's response.

1. **Using `asyncio` and `aiohttp`:** We utilized `asyncio` and `aiohttp` to create asynchronous HTTP requests, enabling the script to send multiple requests concurrently without blocking the execution flow. This allowed us to simulate simultaneous user interactions and evaluate the system's performance under load.

2. **Creating Automated Tests:** The `test.py` script served as an automated testing tool to validate the system's behaviour under various scenarios, including concurrency and scalability testing. By defining test scenarios and executing them programmatic-ally, we could identify potential bottlenecks, performance issues, or concurrency-related bugs in the system.

By developing and utilizing the `test.py` script, we effectively addressed the challenge of simulating simultaneous requests from the Swagger UI, enabling comprehensive testing and validation of the seat booking system's functionality, performance, and scalability.
