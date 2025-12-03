-- Insert seed data
INSERT INTO example (id, name, title, entry_date, description, is_active)
VALUES 
    (1, 'First Example', 'Introduction', '2025-12-02 12:00:00', 'This is the first example entry', true),
    (2, 'Second Example', 'Advanced Topics', '2025-12-01 12:00:00', 'This is the second example entry', true);

-- Update sequence to continue from the seed data
SELECT setval(pg_get_serial_sequence('example', 'id'), (SELECT MAX(id) FROM example));
