create table if not exists students (
    id integer primary key autoincrement,
    username text not null,
	bio text,
	score integer,
	isactive integer,
    unique(username)
);
