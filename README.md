# Employee Management System

A desktop-based Employee Management System developed using **Python, Tkinter and MySQL**. This application provides a simple graphical interface to manage employee records efficiently.

## Features

- **Add Employees:** Register new employees with their details.
- **View Employees:** Display stored employee records.
- **Search Employees:** Find employees using their Employee ID.
- **Edit Employees:** Update existing employee information.
- **Delete Employees:** Remove selected employee records.

## Technologies Used

- Python
- Tkinter (GUI)
- MySQL (Database)
- MySQL Connector
- Python-dotenv

## Project Structure

```text
Employee_Management_System/
│
├── csc project.py
├── requirements.txt
├── .gitignore
└── README.md
```

The `.env` file is created locally to store database credentials and is excluded from GitHub.

## Installation and Setup

**1. Clone the repository**

```bash
git clone YOUR_REPOSITORY_URL
```

**2. Install dependencies**

```bash
py -m pip install -r requirements.txt
```

**3. Configure MySQL**

- Make sure MySQL Server is running.
- Create a database named `employee_db`.
- Create an `employee` table with the columns expected by the application: `empid`, `name`, `department`, `salary` and `phno`.

**4. Configure environment variables**

Create a `.env` file in the project folder:

```env
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=employee_db
```

Replace the placeholder values with your own local MySQL credentials.

**5. Run the application**

```bash
py "csc project.py"
```

## Project Objective

To demonstrate the integration of Python GUI development and MySQL database connectivity through a practical employee record management application.
