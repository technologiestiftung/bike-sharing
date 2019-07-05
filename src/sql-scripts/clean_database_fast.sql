DROP TABLE IF EXISTS  tmp ;
CREATE TEMP TABLE tmp AS
select *
from (
    select  id, "bikeId", "providerId", "timestamp", latitude, longitude,
			lag("bikeId") over (order by "bikeId" ASC, "timestamp" ASC) as prev_id,
            lead("bikeId") over (order by "bikeId" ASC, "timestamp" ASC) as next_id,
            lag("latitude") over (order by "bikeId" ASC, "timestamp" ASC) as prev_lat,
			lag("longitude") over (order by "bikeId" ASC, "timestamp" ASC) as prev_lon,
            lead("latitude") over (order by "bikeId" ASC, "timestamp" ASC) as next_lat,
            lead("longitude") over (order by "bikeId" ASC, "timestamp" ASC) as next_lon
    from public."bikeLocations"
    )x
	where ("bikeId" <> next_id) or
		   ("bikeId" <> prev_id) or
		   (latitude <> next_lat or longitude <> next_lon or latitude <> prev_lat or longitude <> prev_lon);
			
TRUNCATE public."bikeLocations";             -- empty table - truncate is very fast for big tables

INSERT INTO public."bikeLocations"
SELECT id, "bikeId", "providerId", "timestamp", latitude, longitude FROM tmp;        -- insert back surviving rows.