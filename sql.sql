-- table creation
create table top_films (
	title varchar(255),
	year int4
)

create table films_data (
    Title varchar(255),
	year int4,
	Rated varchar(10),
	Runtime varchar(40),
	Genre text,
	Director text,
	Actors text,
	Plot text,
	Country text,
	Awards text,
	Poster text,
	imdbRating varchar(40),
	imdbVotes varchar(40),
	BoxOffice varchar(60),
	imdbID varchar(60)

    CHECK (year BETWEEN 1888 AND 2200)
)


-- replace N/A by nulls (dynamic query)
do
$$
declare
	col_name text;
begin
	for col_name in
		SELECT column_name from information_schema.columns
		where table_name = 'films_data'
		and table_schema = 'public'
		and data_type != 'jsonb'
		and data_type != 'integer'
	loop
		execute format(
					'update films_data set %I = null where %I = %L',
					col_name,
					col_name,
					'N/A'
				);
	end loop;
end
$$;

-- clear select
select
	Title,
	Year,
	Rated,
	split_part(Runtime,' ',1)::integer runtime,
	Genre,
	Director,
	Actors,
	Plot,
	Country,
	Awards,
	Poster,
	imdbRating::float,
	replace(imdbVotes, ',','')::integer imdbvotes,
	replace(right(boxoffice,-1), ',', '')::integer boxoffice,
	imdbID
from films_data