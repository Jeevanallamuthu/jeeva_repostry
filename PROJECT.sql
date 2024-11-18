CREATE DATABASE BankingSystem;
USE BankingSystem;

CREATE TABLE Account_Holders (
    Account_No INT PRIMARY KEY,
    IFSC_CODE VARCHAR(10),
    MICR_CODE VARCHAR(10),
    Name VARCHAR(100),
    Address VARCHAR(255),
    PhoneNumber VARCHAR(15),
    Email VARCHAR(100)
);

CREATE TABLE Accounts (
    AccountID INT PRIMARY KEY AUTO_INCREMENT,
    Account_No INT,
    Balance DECIMAL(15, 2) DEFAULT 0,
    AccountType VARCHAR(50),
    CreatedDate DATE,
    FOREIGN KEY (Account_No) REFERENCES Account_Holders(Account_No)
);

CREATE TABLE Transaction_Types (
    TransactionTypeID INT PRIMARY KEY AUTO_INCREMENT,
    TypeName VARCHAR(50)
);

CREATE TABLE Transactions (
    TransactionID INT PRIMARY KEY AUTO_INCREMENT,
    AccountID INT,
    TransactionTypeID INT,
    Amount DECIMAL(15, 2),
    TransactionDate DATE,
    Description VARCHAR(255),
    FOREIGN KEY (AccountID) REFERENCES Accounts(AccountID),
    FOREIGN KEY (TransactionTypeID) REFERENCES Transaction_Types(TransactionTypeID)
);

INSERT INTO Account_Holders (Account_No, IFSC_CODE, MICR_CODE, Name, Address, PhoneNumber, Email) VALUES
(1001, 'IFSC001', 'MICR001', 'John Doe', '123 Main St', '555-1234', 'johndoe@example.com'),
(1002, 'IFSC002', 'MICR002', 'Jane Smith', '456 Elm St', '555-5678', 'janesmith@example.com'),
(1003, 'IFSC003', 'MICR003', 'dave jones', '1234 nor st', '888-4569', 'davejones@example.com'),
(1004, 'IFSC004', 'MICR004', 'Jack Sparrow', '12 est st', '125-7895', 'sparrow@example.com'),
(1005, 'IFSC005', 'MICR005', 'Alice Brown', '789 Oak St', '555-7890', 'alicebrown@example.com'),
(1006, 'IFSC006', 'MICR006', 'Bob Johnson', '101 Pine St', '555-2345', 'bobjohnson@example.com'),
(1007, 'IFSC007', 'MICR007', 'Carol White', '202 Maple St', '555-6789', 'carolwhite@example.com'),
(1008, 'IFSC008', 'MICR008', 'David Lee', '303 Cedar St', '555-3456', 'davidlee@example.com'),
(1009, 'IFSC009', 'MICR009', 'Eve Green', '404 Birch St', '555-9012', 'evegreen@example.com'),
(1010, 'IFSC010', 'MICR010', 'Frank Adams', '505 Cherry St', '555-1111', 'frankadams@example.com'),
(1011, 'IFSC011', 'MICR011', 'Grace King', '606 Willow St', '555-2222', 'graceking@example.com');

INSERT INTO Accounts (Account_No, Balance, AccountType, CreatedDate) VALUES
(1001, 1000.00, 'Checking', '2024-01-01'),
(1002, 2500.00, 'Savings', '2024-01-01'),
(1003, 1000.00, 'current', '2023-12-01'),
(1004, 1000.00, 'savings', '2022-01-28'),
(1005, 3000.00, 'Savings', '2024-02-01'),
(1006, 1500.00, 'Checking', '2024-03-01'),
(1007, 4000.00, 'Savings', '2024-04-01'),
(1008, 500.00, 'Checking', '2024-05-01'),
(1009, 2750.00, 'Savings', '2024-06-01'),
(1010, 1000.00, 'Checking', '2024-07-01'),
(1011, 2000.00, 'Savings', '2024-08-01');

INSERT INTO Transaction_Types (TypeName) VALUES
('Deposit'),
('Withdrawal'),
('Transfer'),
('Bill Payment'),
('Online Transfer'),
('Interest Credit');

INSERT INTO Transactions (AccountID, TransactionTypeID, Amount, TransactionDate, Description) VALUES
(1, 1, 500.00, '2024-01-15', 'Direct Deposit'),
(1, 2, 100.00, '2024-01-20', 'ATM Withdrawal'),
(2, 1, 300.00, '2024-02-01', 'Bank Deposit'),
(2, 3, 200.00, '2024-03-01', 'UPI'),
(3, 1, 600.00, '2023-12-06', 'Bank Deposit'),
(3, 3, 700.00, '2024-01-05', 'RTGS'),
(4, 1, 500.00, '2022-06-22', 'STAFF REFERAL CODE DEPOSIT'),
(5, 1, 600.00, '2024-02-15', 'Direct Deposit'),
(5, 2, 50.00, '2024-02-20', 'ATM Withdrawal'),
(6, 1, 150.00, '2024-03-10', 'Bank Deposit'),
(7, 4, 200.00, '2024-04-01', 'Bill Payment'),
(8, 5, 250.00, '2024-05-01', 'Online Transfer'),
(9, 6, 30.00, '2024-06-05', 'Interest Credit');

#drop database bankingsystem;

#1-Query to Get All Account Holders' Details
SELECT 
    Account_Holders.Account_No,
    Account_Holders.Name,
    Account_Holders.Address,
    Account_Holders.PhoneNumber,
    Account_Holders.Email,
    Account_Holders.IFSC_CODE,
    Account_Holders.MICR_CODE
FROM 
    Account_Holders;

#2-Query to Generate an Account Statement for a Specific Account Number
SELECT 
    Transactions.TransactionID,
    Transactions.TransactionDate,
    Transaction_Types.TypeName AS TransactionType,
    Transactions.Amount,
    Transactions.Description,
    Accounts.Balance
FROM 
    Transactions
JOIN 
    Accounts ON Transactions.AccountID = Accounts.AccountID
JOIN 
    Transaction_Types ON Transactions.TransactionTypeID = Transaction_Types.TransactionTypeID
WHERE 
    Accounts.Account_No = 1001
ORDER BY 
    Transactions.TransactionDate;

#3-Query to Find the Total Balance of All Accounts
SELECT 
    SUM(Accounts.Balance) AS TotalBalance
FROM 
    Accounts;

#4-Query to List All Withdrawals Over a Certain Amount
SELECT 
    Transactions.TransactionID,
    Accounts.Account_No,
    Transactions.Amount,
    Transactions.TransactionDate,
    Transactions.Description
FROM 
    Transactions
JOIN 
    Accounts ON Transactions.AccountID = Accounts.AccountID
JOIN 
    Transaction_Types ON Transactions.TransactionTypeID = Transaction_Types.TransactionTypeID
WHERE 
    Transaction_Types.TypeName = 'Withdrawal' AND Transactions.Amount < 200
ORDER BY 
    Transactions.Amount DESC;

#5-Query to Count the Number of Transactions per Transaction Type
SELECT 
    Transaction_Types.TypeName AS TransactionType,
    COUNT(Transactions.TransactionID) AS TransactionCount
FROM 
    Transactions
JOIN 
    Transaction_Types ON Transactions.TransactionTypeID = Transaction_Types.TransactionTypeID
GROUP BY 
    Transaction_Types.TypeName;
    
#6. Query to List All Accounts with Their Holder’s Name and Account Type
SELECT 
    Accounts.AccountID,
    Accounts.Account_No,
    Account_Holders.Name AS AccountHolder,
    Accounts.AccountType,
    Accounts.Balance
FROM 
    Accounts
JOIN 
    Account_Holders ON Accounts.Account_No = Account_Holders.Account_No;

#7. Query to Find the Average Transaction Amount for Each Account Type
SELECT 
    Transaction_Types.TypeName AS TransactionType,
    AVG(Transactions.Amount) AS AverageAmount
FROM 
    Transactions
JOIN 
    Transaction_Types ON Transactions.TransactionTypeID = Transaction_Types.TransactionTypeID
GROUP BY 
    Transaction_Types.TypeName;

#8.Query to Get the Highest Balance Across All Accounts
SELECT 
    Accounts.Account_No,
    Account_Holders.Name AS AccountHolder,
    Accounts.Balance
FROM 
    Accounts
JOIN 
    Account_Holders ON Accounts.Account_No = Account_Holders.Account_No
ORDER BY 
    Accounts.Balance DESC
LIMIT 1;

#9.Query to Get the Total Number of Transactions in the Past Month
SELECT 
    COUNT(Transactions.TransactionID) AS TransactionsInPastMonth
FROM 
    Transactions
WHERE 
    Transactions.TransactionDate >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH);

#10. Query to Get All Accounts Opened in a Specific Year
SELECT 
    Accounts.AccountID,
    Account_Holders.Name AS AccountHolder,
    Accounts.Account_No,
    Accounts.Balance,
    Accounts.CreatedDate
FROM 
    Accounts
JOIN 
    Account_Holders ON Accounts.Account_No = Account_Holders.Account_No
WHERE 
    YEAR(Accounts.CreatedDate) =2023;
    
#11-query to show name start with "D",end with "G"
SELECT*FROM account_holders where name like 'D%';
SELECT*FROM account_holders where name like '%G';

#12-write a query for get eve green transaction details using subqueries
SELECT * 
FROM Transactions,Transaction_types
WHERE AccountID = (
    SELECT AccountID 
    FROM Accounts 
    WHERE Account_No = (
        SELECT Account_No 
        FROM Account_Holders 
        WHERE Name = 'Eve Green'
    )
);

#13-query to retrieve a list of all deposit and withdrawal transactions from the database, including account holder names, account numbers, transaction dates, amounts, and transaction types. Use UNION and alias
SELECT 
    AH.Name AS AccountHolderName,
    A.Account_No,
    T.TransactionDate,
    T.Amount,
    'Deposit' AS TransactionType
FROM 
    Transactions T
JOIN 
    Accounts A ON T.AccountID = A.AccountID
JOIN 
    Account_Holders AH ON A.Account_No = AH.Account_No
WHERE 
    T.TransactionTypeID = (SELECT TransactionTypeID FROM Transaction_Types WHERE TypeName = 'Deposit')

UNION

SELECT 
    AH.Name AS AccountHolderName,
    A.Account_No,
    T.TransactionDate,
    T.Amount,
    'Withdrawal' AS TransactionType
FROM 
    Transactions T
JOIN 
    Accounts A ON T.AccountID = A.AccountID
JOIN 
    Account_Holders AH ON A.Account_No = AH.Account_No
WHERE 
    T.TransactionTypeID = (SELECT TransactionTypeID FROM Transaction_Types WHERE TypeName = 'Withdrawal')

ORDER BY 
    TransactionDate;

#14-create sample view for database
CREATE VIEW Account_Summary AS
SELECT 
    Account_Holders.Name,
    Account_Holders.Account_No,
    Accounts.Balance,
    COALESCE(SUM(Transactions.Amount), 0) AS Total_Transactions
FROM 
    Account_Holders
JOIN 
    Accounts ON Account_Holders.Account_No = Accounts.Account_No
LEFT JOIN 
    Transactions ON Accounts.AccountID = Transactions.AccountID
GROUP BY 
    Account_Holders.Name, Account_Holders.Account_No, Accounts.Balance;
    
#drop view account_summary;
    
    
    



