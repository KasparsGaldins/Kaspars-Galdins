[1mdiff --git a/naked.py b/naked.py[m
[1mindex 7729c41..8d08562 100644[m
[1m--- a/naked.py[m
[1m+++ b/naked.py[m
[36m@@ -19,31 +19,42 @@[m [mdt = datetime.now()[m
 request_date = str(dt.year) + "-" + str(dt.month).zfill(2) + "-" + str(dt.day).zfill(2)  [m
 print("Generated today's date: " + str(request_date))[m
 [m
[31m-[m
[32m+[m[32m#Requesting info from NASA API[m
 print("Request url: " + str(nasa_api_url + "rest/v1/feed?start_date=" + request_date + "&end_date=" + request_date + "&api_key=" + nasa_api_key))[m
 r = requests.get(nasa_api_url + "rest/v1/feed?start_date=" + request_date + "&end_date=" + request_date + "&api_key=" + nasa_api_key)[m
 [m
[32m+[m[32m#Printing NASA request response data[m
 print("Response status code: " + str(r.status_code))[m
 print("Response headers: " + str(r.headers))[m
 print("Response content: " + str(r.text))[m
 [m
[32m+[m[32m# Check if the HTTP status code is 200 (OK)[m
 if r.status_code == 200:[m
[32m+[m[32m# If the status code is 200, parse the JSON data from the response text[m
[32m+[m	[32mjson_data = json.loads(r.text)[m[41m [m
[32m+[m[32m# Initialize empty lists to store asteroid data[m
[32m+[m	[32mast_safe = [] #List for safe asteroids[m
[32m+[m	[32mast_hazardous = [] #List for hazard asteroids[m
 [m
[31m-	json_data = json.loads(r.text)[m
[31m-[m
[31m-	ast_safe = [][m
[31m-	ast_hazardous = [][m
[31m-[m
[32m+[m[32m# Check if 'element_count' is present in the parsed JSON data[m
 	if 'element_count' in json_data:[m
[32m+[m[32m# If present, extract and convert the asteroid count to an integer[m
 		ast_count = int(json_data['element_count'])[m
[32m+[m[32m # Print the asteroid count for today[m
 		print("Asteroid count today: " + str(ast_count))[m
 [m
[32m+[m[32m# Check if there are asteroids for today[m
 		if ast_count > 0:[m
[32m+[m[32m# Iterate through each asteroid in the 'near_earth_objects' list for the requested date[m
 			for val in json_data['near_earth_objects'][request_date]:[m
[32m+[m[32m# Check if essential information is present in the asteroid data[m
 				if 'name' and 'nasa_jpl_url' and 'estimated_diameter' and 'is_potentially_hazardous_asteroid' and 'close_approach_data' in val:[m
[32m+[m[32m# Extract relevant information for each asteroid[m
 					tmp_ast_name = val['name'][m
 					tmp_ast_nasa_jpl_url = val['nasa_jpl_url'][m
[31m-					if 'kilometers' in val['estimated_diameter']:[m
[32m+[m
[32m+[m[32m# Check if diameter information is available[m[41m				[m
[32m+[m	[32mif 'kilometers' in val['estimated_diameter']:[m
 						if 'estimated_diameter_min' and 'estimated_diameter_max' in val['estimated_diameter']['kilometers']:[m
 							tmp_ast_diam_min = round(val['estimated_diameter']['kilometers']['estimated_diameter_min'], 3)[m
 							tmp_ast_diam_max = round(val['estimated_diameter']['kilometers']['estimated_diameter_max'], 3)[m
[36m@@ -56,33 +67,40 @@[m [mif r.status_code == 200:[m
 [m
 					tmp_ast_hazardous = val['is_potentially_hazardous_asteroid'][m
 [m
[32m+[m
[32m+[m[32m # Check if there is close approach data for the asteroid[m
 					if len(val['close_approach_data']) > 0:[m
 						if 'epoch_date_close_approach' and 'relative_velocity' and 'miss_distance' in val['close_approach_data'][0]:[m
[31m-							tmp_ast_close_appr_ts = int(val['close_approach_data'][0]['epoch_date_close_approach']/1000)[m
[32m+[m							[32m # Extract close approach information[m
[32m+[m[32mtmp_ast_close_appr_ts = int(val['close_approach_data'][0]['epoch_date_close_approach']/1000)[m
 							tmp_ast_close_appr_dt_utc = datetime.utcfromtimestamp(tmp_ast_close_appr_ts).strftime('%Y-%m-%d %H:%M:%S')[m
 							tmp_ast_close_appr_dt = datetime.fromtimestamp(tmp_ast_close_appr_ts).strftime('%Y-%m-%d %H:%M:%S')[m
 [m
[32m+[m[32m# Extract speed information[m
 							if 'kilometers_per_hour' in val['close_approach_data'][0]['relative_velocity']:[m
 								tmp_ast_speed = int(float(val['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']))[m
 							else:[m
 								tmp_ast_speed = -1[m
 [m
[32m+[m[32m# Extract miss distance information[m
 							if 'kilometers' in val['close_approach_data'][0]['miss_distance']:[m
 								tmp_ast_miss_dist = round(float(val['close_approach_data'][0]['miss_distance']['kilometers']), 3)[m
 							else:[m
 								tmp_ast_miss_dist = -1[m
 						else:[m
[32m+[m[32m # If close approach data is incomplete, set default values[m
 							tmp_ast_close_appr_ts = -1[m
 							tmp_ast_close_appr_dt_utc = "1969-12-31 23:59:59"[m
 							tmp_ast_close_appr_dt = "1969-12-31 23:59:59"[m
 					else:[m
[32m+[m[32m # If no close approach data is available, print a message and set default values[m
 						print("No close approach data in message")[m
 						tmp_ast_close_appr_ts = 0[m
 						tmp_ast_close_appr_dt_utc = "1970-01-01 00:00:00"[m
 						tmp_ast_close_appr_dt = "1970-01-01 00:00:00"[m
 						tmp_ast_speed = -1[m
 						tmp_ast_miss_dist = -1[m
[31m-[m
[32m+[m[32m# Print information for each asteroid[m
 					print("------------------------------------------------------- >>")[m
 					print("Asteroid name: " + str(tmp_ast_name) + " | INFO: " + str(tmp_ast_nasa_jpl_url) + " | Diameter: " + str(tmp_ast_diam_min) + " - " + str(tmp_ast_diam_max) + " km | Hazardous: " + str(tmp_ast_hazardous))[m
 					print("Close approach TS: " + str(tmp_ast_close_appr_ts) + " | Date/time UTC TZ: " + str(tmp_ast_close_appr_dt_utc) + " | Local TZ: " + str(tmp_ast_close_appr_dt))[m
[36m@@ -91,26 +109,31 @@[m [mif r.status_code == 200:[m
 					# Adding asteroid data to the corresponding array[m
 					if tmp_ast_hazardous == True:[m
 						ast_hazardous.append([tmp_ast_name, tmp_ast_nasa_jpl_url, tmp_ast_diam_min, tmp_ast_diam_max, tmp_ast_close_appr_ts, tmp_ast_close_appr_dt_utc, tmp_ast_close_appr_dt, tmp_ast_speed, tmp_ast_miss_dist])[m
[32m+[m
 					else:[m
 						ast_safe.append([tmp_ast_name, tmp_ast_nasa_jpl_url, tmp_ast_diam_min, tmp_ast_diam_max, tmp_ast_close_appr_ts, tmp_ast_close_appr_dt_utc, tmp_ast_close_appr_dt, tmp_ast_speed, tmp_ast_miss_dist])[m
[31m-[m
[32m+[m[32m # Print a message if there are no asteroids that pose a threat to Earth[m
 		else:[m
 			print("No asteroids are going to hit earth today")[m
[31m-[m
[32m+[m[32m# Print the count of hazardous and safe asteroids[m
 	print("Hazardous asteorids: " + str(len(ast_hazardous)) + " | Safe asteroids: " + str(len(ast_safe)))[m
[31m-[m
[32m+[m[32m# Check if there are hazardous asteroids[m
 	if len(ast_hazardous) > 0:[m
[31m-[m
[32m+[m[32m# Sort the hazardous asteroids based on their close approach times[m
 		ast_hazardous.sort(key = lambda x: x[4], reverse=False)[m
 [m
[32m+[m[32m# Print information about today's hazardous asteroids and their possible impact times[m
 		print("Today's possible apocalypse (asteroid impact on earth) times:")[m
 		for asteroid in ast_hazardous:[m
 			print(str(asteroid[6]) + " " + str(asteroid[0]) + " " + " | more info: " + str(asteroid[1]))[m
 [m
[32m+[m[32m# Sort the hazardous asteroids based on their closest passing distances[m
 		ast_hazardous.sort(key = lambda x: x[8], reverse=False)[m
 		print("Closest passing distance is for: " + str(ast_hazardous[0][0]) + " at: " + str(int(ast_hazardous[0][8])) + " km | more info: " + str(ast_hazardous[0][1]))[m
 	else:[m
[32m+[m[32m # Print a message if there are no hazardous asteroids close passing Earth today[m
 		print("No asteroids close passing earth today")[m
 [m
 else:[m
[32m+[m[32m# Print an error message if there is an issue with getting a response from the API[m
 	print("Unable to get response from API. Response code: " + str(r.status_code) + " | content: " + str(r.text))[m
