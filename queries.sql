CREATE TABLE stocks (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL)
CREATE TABLE portfolios (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    stock_id INTEGER NOT NULL,
    shares INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (stock_id) REFERENCES stocks(id)
    );

-- SELECT cash FROM users WHERE id = ?

-- SELECT * FROM portfolios WHERE user_id = ? AND stock_id = ?

-- SELECT name FROM stocks WHERE name = ?

-- INSERT INTO stocks (name) VALUES (?)

-- UPDATE users SET cash = cash - ?, WHERE id = ?

-- INSERT INTO portfolios (user_id, stock_id, shares) VALUES (?, ?, ?)

-- UPDATE portfolios SET shares = ? WHERE user_id = ? AND stock_id = ?

-- SELECT * FROM stocks
-- JOIN portfolios on stocks.id = portfolios.stock_id
-- WHERE portfolios.user_id = ?

-- SELECT cash FROM users WHERE user_id = ?

-- SELECT name FROM stocks
-- JOIN portfolios on stocks.id = portfolios.stock_id
-- WHERE portfolios.user_id = ?

-- SELECT stocks.name, portfolios.shares FROM stocks
-- JOIN portfolios on stocks.id = portfolios.stock_id
-- WHERE portfolios.user_id = ? AND stocks.name = ?

-- SELECT id FROM stocks WHERE name = ?

-- UPDATE users SET cash = cash + ? WHERE id = ?

-- UPDATE portfolios JOIN stocks ON portfolios.stock_id = stocks.id SET shares = shares - ? WHERE stocks.id = ? AND portfolios.user_id = ?

-- DELETE FROM portfolios JOIN stocks ON portfolios.stock_id = stocks.id WHERE stocks.name = ? AND portfolios.user_id = ?
