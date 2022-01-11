CREATE TABLE IF NOT EXISTS book_club_deadline
(
    deadline  date,
    book_name varchar(200),
    id        serial
        constraint book_club_deadline_pk
            primary key
);