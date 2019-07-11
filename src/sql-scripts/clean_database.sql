DELETE FROM public."bikeLocations"
WHERE id IN  (SELECT id
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
					where ("bikeId" = next_id) and
						   ("bikeId" = prev_id) and
						   (latitude = next_lat and longitude = next_lon and latitude = prev_lat and longitude = prev_lon))
