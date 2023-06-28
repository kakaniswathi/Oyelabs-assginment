const mysql = require('mysql');

const customers = [
  {
    email: 'anurag11@yopmail.com',
    name: 'anurag',
  },
  {
    email: 'sameer11@yopmail.com',
    name: 'sameer',
  },
  {
    email: 'ravi11@yopmail.com',
    name: 'ravi',
  },
  {
    email: 'akash11@yopmail.com',
    name: 'akash',
  },
  {
    email: 'anjali11@yopmail.com',
    name: 'anjai',
  },
  {
    email: 'santosh11@yopmail.com',
    name: 'santosh',
  },
];

// MySQL connection configuration
const dbConfig = {
  host: 'localhost',
  user: 'your_username',
  password: 'your_password',
  database: 'your_database',
};

// Create a MySQL connection
const connection = mysql.createConnection(dbConfig);

connection.connect((err) => {
  if (err) {
    console.error('Error connecting to MySQL:', err);
    return;
  }

  console.log('Connected to MySQL.');

  insertCustomers(customers);
});

function insertCustomers(customers) {
  customers.forEach((customer) => {
    const { email, name } = customer;

    const selectQuery = 'SELECT customerId FROM customers WHERE email = ?';
    connection.query(selectQuery, [email], (selectErr, selectResults) => {
      if (selectErr) {
        console.error('Error executing SELECT query:', selectErr);
        return;
      }

      if (selectResults.length > 0) {
        // Email already exists, update the customer's name
        const updateQuery = 'UPDATE customers SET name = ? WHERE email = ?';
        connection.query(updateQuery, [name, email], (updateErr, updateResults) => {
          if (updateErr) {
            console.error('Error executing UPDATE query:', updateErr);
          } else {
            console.log(`Customer updated: ${email}`);
          }
        });
      } else {
        // Email doesn't exist, insert a new customer
        const insertQuery = 'INSERT INTO customers (name, email) VALUES (?, ?)';
        connection.query(insertQuery, [name, email], (insertErr, insertResults) => {
          if (insertErr) {
            console.error('Error executing INSERT query:', insertErr);
          } else {
            console.log(`Customer inserted: ${email}`);
          }
        });
      }
    });
  });

  connection.end((endErr) => {
    if (endErr) {
      console.error('Error closing MySQL connection:', endErr);
    } else {
      console.log('MySQL connection closed.');
    }
  });
}
