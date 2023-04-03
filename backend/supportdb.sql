

\c service_request
CREATE TABLE IF NOT EXISTS users(
    support_id INT PRIMARY KEY NOT NULL,
    user_name VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    typeOfUser INT NOT NULL
);
CREATE TABLE IF NOT EXISTS service_requests (
    task_Id SERIAL PRIMARY KEY NOT NULL,
    customer_id VARCHAR(100) NOT NULL,
    support_id  INT REFERENCES users(support_id),
    type_of_task INT NOT NULL,
    task_data text , --varchar(200) NOT NULL,
    description varchar(100) ,
    status VARCHAR(100) NOT NULL DEFAULT 'WAITING_FOR_APPROVAL',
    error_message VARCHAR(100),
    created_date DATE NOT NULL,
    approval_date DATE,
    completed_date DATE
);

