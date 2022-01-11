CREATE TABLE IF NOT EXISTS add_reaction
(
    trigger       varchar,
    reaction_list text[],
    id            serial
        constraint add_reaction_pk
            primary key
);
