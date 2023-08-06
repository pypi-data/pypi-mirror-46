/*
Mock placeholder, so Sqlite3 tests can access the table without throwing a missing table error.
*/
CREATE VIEW database_deadlock_deadlock
AS
SELECT  'id'        AS id,
        '123'       AS blocked_pid,
        'user1'     AS blocked_user,
        'SELECT 1;' AS blocked_query,
        '456'       AS blocking_pid,
        'user2'     AS blocking_user,
        'SELECT 2;' AS blocking_query;
