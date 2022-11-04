def filter_by_origin(data_pickup,data_regions):
    """
    This function filter out the trips that are not originated from any of our selected region, and add a region tag
    data_pickup  # here the pic_Up is the end station for am peak, and the start station for pm peak ## or this is not differntiable, ......
    data_region  # here region is the subway station 
    """
    #print(data_pickup.columns.tolist())
    #data_pickup.columns = data_pickup.columns.str.strip()
    data_pickup = data_pickup.reset_index()
    #print (data_pickup.head())
    # Create a copy
    data_pickup_filtered = data_pickup.copy()
    # Initialize the list to record which region the origin is located
    in_which_region_list = []

    print(f"len(data_pickup) = {len(data_pickup)}, len(data_regions) = {len(data_regions)}")
    for i in range(0, len(data_pickup)):
        pickup_latitude =  data_pickup['Lat'][i]
        pickup_longitude = data_pickup['Long'][i]
        in_which_region = -1 # Initialize with -1
        for j in range(0,len(data_regions)):
            # lyon = (45.7597, 4.8422) # (lat, lon)
            # paris = (48.8567, 2.3508)
            # haversine(lyon, paris)
            # distance = measure_geo_distance(pickup_longitude,pickup_latitude,data_regions['Long'][j],data_regions['Lat'][j])
            distance = hs.haversine((pickup_latitude,pickup_longitude),(data_regions['Lat'][j],data_regions['Long'][j]))  # uint in km
            if distance <= data_regions['raidus'][j]:
                in_which_region = j
        in_which_region_list.append(in_which_region)
    data_pickup_filtered['Region'] = in_which_region_list
    # Keep only those have real region indice
    data_pickup_filtered = data_pickup_filtered[data_pickup_filtered.Region != -1]
    # Reset the indice
    data_pickup_filtered = data_pickup_filtered.dropna(how='any').reset_index(drop=True)
    #print (data_pickup_filtered.describe())
    return data_pickup_filtered



def filter_by_origin_vectorized(data_pickup,data_regions):
    data_pickup = data_pickup.reset_index()
    # Create a copy
    data_pickup_filtered = data_pickup.copy()
    #print(data_pickup.head())


    pickup_latitudes = data_pickup['Lat']
    pickup_longitudes = data_pickup['Long']
    pickup_coords = [(x,y) for x,y in zip(pickup_latitudes, pickup_longitudes)]
    
    in_which_region_list = np.full(len(data_pickup), -1) # init array with -1
    for j in range(0,len(data_regions)):
        region_center = (data_regions['Lat'][j], data_regions['Long'][j])
        distances = hs.haversine_vector(pickup_coords, [region_center], hs.Unit.KILOMETERS, comb=True)
        region_radius = data_regions['raidus'][j]
        in_which_region_list[distances[0] < region_radius] = j # distances is a 2d matrix

    data_pickup_filtered['Region'] = in_which_region_list
    # Keep only those have real region indice
    data_pickup_filtered = data_pickup_filtered[data_pickup_filtered.Region != -1]
    # Reset the indice
    data_pickup_filtered = data_pickup_filtered.dropna(how='any').reset_index(drop=True)

    return data_pickup_filtered



