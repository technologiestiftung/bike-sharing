select *
from (
    select  "bikeId", "providerId", "timestamp", latitude, longitude,
			lag("bikeId") over (order by "bikeId" ASC, "timestamp" ASC) as prev_id,
            lead("bikeId") over (order by "bikeId" ASC, "timestamp" ASC) as next_id,
            lag("latitude") over (order by "bikeId" ASC, "timestamp" ASC) as prev_lat,
            lead("latitude") over (order by "bikeId" ASC, "timestamp" ASC) as next_lat,
			lag("longitude") over (order by "bikeId" ASC, "timestamp" ASC) as prev_lon,
            lead("longitude") over (order by "bikeId" ASC, "timestamp" ASC) as next_lon
    from public."bikeLocations"
    )x
	where ("bikeId" <> next_id) or
		   ("bikeId" <> prev_id) or
		   (latitude <> next_lat or longitude <> next_lon or latitude <> prev_lat or longitude <> prev_lon)
	order by "bikeId" ASC
	
	--keep first and last instance of bike (bikeId <> prev_id or bikeId <> next_id)
	--keep all changes inbetween, where bike_Id is equal to next_id but lat or lon changed to prev or next