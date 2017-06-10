drop table if exists entries;
create table students (
    id integer primary key autoincrement,
    username text not null,
	bio text,
	score integer
);
