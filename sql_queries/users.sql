CREATE TABLE IF NOT EXISTS users
(
    discord_id bigint                                             not null,
    user_name  varchar(100),
    birth_date date,
    id         integer default nextval('users_int_seq'::regclass) not null
        constraint users_pk
            primary key
);