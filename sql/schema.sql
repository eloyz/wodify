drop table if exists athlete;
create table athlete(
    id text not null,
    name text not null,
    unique (id) on conflict replace
);

drop table if exists weight;
create table weight(
    id text not null,
    name text not null,
    unique (id) on conflict replace
);

drop table if exists record;
create table record(
    athlete_id text not null,
    weight_id text not null,
    sets integer not null,
    reps integer not null,
    weight integer not null,
    max_weight integer not null,
    accomplished_on text not null,
    unique (athlete_id, weight_id, sets, reps, weight, accomplished_on) on conflict replace,
    foreign key(athlete_id) references athlete(id),
    foreign key(weight_id) references weight(id)
);
