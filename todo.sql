DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS todos;

--Table users
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);
INSERT INTO users VALUES (1,'admin','admin');

--Table todo list
CREATE TABLE todos(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  taskname VARCHAR(255) NOT NULL,
  status char(30) NOT NULL
);
