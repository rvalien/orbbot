CREATE TABLE IF NOT EXISTS users
(
    discord_id bigint not null,
    user_name  varchar(100),
    birth_date date
);