CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL, cash NUMERIC NOT NULL DEFAULT 10000.00);

CREATE UNIQUE INDEX username ON users (username);

CREATE TABLE stocks (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL);

CREATE TABLE portfolios (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    stock_id INTEGER NOT NULL,
    shares INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (stock_id) REFERENCES stocks(id)
    );

CREATE TABLE history (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    stock_id INTEGER NOT NULL,
    transaction_type TEXT NOT NULL,
    shares INTEGER NOT NULL,
    share_price REAL NOT NULL,
    date DATETIME NOT NULL,
    total REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (stock_id) REFERENCES stocks(id)
    );

SELECT cash FROM users
 WHERE id = ?

SELECT * FROM portfolios
 WHERE user_id = ? AND stock_id = ?

SELECT name FROM stocks
 WHERE name = ?

INSERT INTO stocks (name)
     VALUES (?)

UPDATE users SET cash = cash - ?, WHERE id = ?

INSERT INTO portfolios (user_id, stock_id, shares)
     VALUES (?, ?, ?)

UPDATE portfolios SET shares = ?
 WHERE user_id = ? AND stock_id = ?

SELECT * FROM stocks
  JOIN portfolios on stocks.id = portfolios.stock_id
 WHERE portfolios.user_id = ?

SELECT cash FROM users WHERE user_id = ?

SELECT name FROM stocks
  JOIN portfolios on stocks.id = portfolios.stock_id
 WHERE portfolios.user_id = ?

SELECT stocks.name, portfolios.shares FROM stocks
  JOIN portfolios on stocks.id = portfolios.stock_id
 WHERE portfolios.user_id = ? AND stocks.name = ?

SELECT id FROM stocks
 WHERE name = ?

UPDATE users
   SET cash = cash + ?
 WHERE id = ?

UPDATE portfolios
  JOIN stocks ON portfolios.stock_id = stocks.id
   SET shares = shares - ?
 WHERE stocks.id = ? AND portfolios.user_id = ?

DELETE FROM portfolios
  JOIN stocks ON portfolios.stock_id = stocks.id
 WHERE stocks.name = ? AND portfolios.user_id = ?

SELECT stocks.name, history.transaction_type, history.shares, history.date, history.share_price, history.total
  FROM stocks
  JOIN history ON stocks.id = history.stock_id
  JOIN users ON history.user_id = users.id
 WHERE users.id = ?
