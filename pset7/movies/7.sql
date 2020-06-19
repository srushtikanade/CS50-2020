SELECT ratings.rating,movies.title FROM movies JOIN ratings ON ratings.movie_id=movies.id WHERE year=2010 ORDER BY 1 desc,2;
