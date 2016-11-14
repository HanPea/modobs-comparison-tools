"""
This script contains several functions for spatio- (or spatio-temporally) interpolating 2D, 3D or 4D (with time dimension) model output onto selected sites, altitudes and times
Author: Hana Pearce
Last edited: 12.10.2016
"""

def interpolate_array2d_surfaceobs(array2d,glon,glat,lon_obs,lat_obs):

    import math
    import numpy as np
    if np.array(lon_obs).shape == ():
        nstat = 1
	lon_obs = np.hstack((lon_obs,np.nan))
        lat_obs = np.hstack((lat_obs,np.nan))
    else:
        nstat = len(lon_obs)

    nstat=len(lon_obs)
    nlon=len(glon)
    nlat=len(glat)
    array_interp=[0]*nstat

    for i in range(nstat):
        if lon_obs[i] < 0.0:
           lon_obs[i] = lon_obs[i]+360.0

    iglon = 0
    for i in range(nlon):
        if glon[i] < 0.0:
            glon[i] = glon[i] + 360.0
	    iglon = iglon + 1

    for i in range(len(lon_obs)):
        if math.isnan(lon_obs[i]) == False:
            # which tomcat square is point to interpolate to
            ii, = np.where(glon > lon_obs[i]) #comma is required here to unpack the result from numpy.where and assign ii to be the first element of that tuple
            # ii contains the indexes of all model latitudes greater than lat_obs
            if (len(ii) < 1):     #i.e. if longitude is between 358.125deg and 0deg (360)
                print 'No longitude grid-points greater than lon_obs[i]=',lon_obs[i]
                print 'Set ii just to include grid-point with max longitude (up to 360)'
                maxlon=np.max(glon)
                imaxlon = np.where(glon==maxlon)
                ii = imaxlon

            # pick lowest longitude value of array that's larger than obs lon
            minlongtobslon = np.min(glon[ii]) # first longitude larger than lat_obs
            iminlongtobslon, = np.where(glon==minlongtobslon) # glat index ref. of first latitude larger than lat_obs

            jj, = np.where(glat > lat_obs[i]) # jj = index of all model latitudes greater than lat_obs
            minlatitobslat = np.min(glat[jj]) # first latitude larger than lat_obs
            iminlatitobslat, = np.where(glat==minlatitobslat) # glat index ref. of first latitude larger than lat_obs
	    # calculate latitude ordering: UM (S->N) or TOMCAT (N->S)
	    if glat[1] > glat[2]: ilatincreasing = 0
            if glat[1] < glat[2]: ilatincreasing = 1

            if ilatincreasing == 0: # follow TOMCAT lat ordering (+ve to -ve)
		print 'ilatincreasing = 0'
                lat0 = int(iminlatitobslat)
                lat1 = int(iminlatitobslat) +1
		if lat0 == nlat-1: # fix it for South Pole
                    lat0=nlat-2
                    lat1=nlat-1
                lon0 = int(iminlongtobslon) -1
                lon1 = int(iminlongtobslon)
		
            if ilatincreasing == 1: #follow UM lat ordering (-ve to +ve)
                print 'ilatincreasing = 1'
                lat0 = int(iminlatitobslat)
                lat1 = int(iminlatitobslat) -1
		if lat0 == 0: # fix it for South Pole
                    lat0=1
                    lat1=0
                lon0 = int(iminlongtobslon) -1
                lon1 = int(iminlongtobslon)
                if lon0 == -1: lon0 = nlon-1
                print 'site lat ', lat_obs[i], 'is between model lats ', glat[lat0],' and ', glat[lat1]
                print 'site lon ', lon_obs[i], 'is between model lons ', glon[lon0],' and ', glon[lon1]
                print 'lat0 %d, lat1 %d, lon0 %d, lon1 %d' % (lat0, lat1, lon0, lon1)
		
            array_pres=[0,0,0,0]
            array_lon=[0,0]

            array_pres[0]=array2d[lat0,lon0]
            array_pres[1]=array2d[lat0,lon1]
            array_pres[2]=array2d[lat1,lon0]
            array_pres[3]=array2d[lat1,lon1]
	    print 'array_press[0:4] is ', array_pres
            factor_lon =(lon_obs[i]-glon[lon0])/(glon[lon1]-glon[lon0])

            array_lon[0] = array_pres[0] + factor_lon*(array_pres[1] - array_pres[0])
            array_lon[1] = array_pres[2] + factor_lon*(array_pres[3] - array_pres[2])

            factor_lat = (lat_obs[i]-glat[lat0])/(glat[lat1] - glat[lat0])

            array_interp[i] = array_lon[0] + factor_lat*(array_lon[1] - array_lon[0])

    #convert lon_obs back to original format i.e. -180 to +180

    for i in range(nstat):
        if lon_obs[i] >= 180.0:
            lon_obs[i] = lon_obs[i]-360.0

    if iglon > 0:
    	for i in range(nlon):
        	if glon[i] >= 180.0:
            		glon[i] = glon[i]-360.0

    return array_interp


def interpolate_array3d_surfaceobs(array3d,glon,glat,lon_obs,lat_obs):

    import math
    import numpy as np
    if np.array(lon_obs).shape == (): 
	nstat = 1
    else:
	nstat = len(lon_obs)
    print 'nstat is ', nstat
    lon_obs = np.hstack((lon_obs,np.nan))
    lat_obs = np.hstack((lat_obs,np.nan))
    nlon=len(glon)
    nlat=len(glat)
    array_interp=[0]*nstat

    for i in range(nstat):
        if lon_obs[i] < 0.0:
           lon_obs[i] = lon_obs[i]+360.0

    iglon = 0
    for i in range(nlon):
	if glon[i] < 0.0:
	    glon[i] = glon[i] + 360.0
	    iglon = iglon + 1
    for i in range(nstat):
        if math.isnan(lon_obs[i]) == False:
            # which tomcat square is point to interpolate to
            ii, = np.where(glon > lon_obs[i]) #comma is required here to unpack the result from numpy.where and assign ii to be the first element of that tuple
            # ii contains the indexes of all model latitudes greater than lat_obs
	   # print 'ii is ', ii
            if (len(ii) < 1):     #i.e. if longitude is between 358.125deg and 0deg (360)
                print 'No longitude grid-points greater than lon_obs[i]=',lon_obs[i]
                print 'Set ii just to include grid-point with max longitude (up to 360)'
                maxlon=np.max(glon)
                imaxlon = np.where(glon==maxlon)
                ii = imaxlon
               # nlongstobslon=1

            # pick lowest longitude value of array that's larger than obs lon
            minlongtobslon = np.min(glon[ii]) # first longitude larger than lat_obs
            iminlongtobslon, = np.where(glon==minlongtobslon) # glat index ref. of first latitude larger than lat_obs

            jj, = np.where(glat > lat_obs[i]) # jj = index of all model latitudes greater than lat_obs
	    #print 'jj is', jj
            minlatitobslat = np.min(glat[jj]) # first latitude larger than lat_obs
            iminlatitobslat, = np.where(glat==minlatitobslat) # glat index ref. of first latitude larger than lat_obs

            # calculate latitude ordering: UM (S->N) or TOMCAT (N->S)
            if glat[1] > glat[2]: ilatincreasing = 0
            if glat[1] < glat[2]: ilatincreasing = 1

            if ilatincreasing == 0: # follow TOMCAT lat ordering (+ve to -ve)
                lat0 = int(iminlatitobslat)
                lat1 = int(iminlatitobslat) +1
                if lat0 == nlat-1: # fix it for South Pole
                    lat0=nlat-2
                    lat1=nlat-1
                lon0 = int(iminlongtobslon) -1
                lon1 = int(iminlongtobslon)

            if ilatincreasing == 1: #follow UM lat ordering (-ve to +ve)
                lat0 = int(iminlatitobslat)
                lat1 = int(iminlatitobslat) -1
                if lat0 == 0: # fix it for South Pole
                    lat0=1
                    lat1=0
                lon0 = int(iminlongtobslon) -1
                lon1 = int(iminlongtobslon)
                if lon0 == -1: lon0 = nlon-1
                #print 'site lat ', lat_obs[i], 'is between model lats ', glat[lat0],' and ', glat[lat1]
                #print 'site lon ', lon_obs[i], 'is between model lons ', glon[lon0],' and ', glon[lon1]
                #print 'lat0 %d, lat1 %d, lon0 %d, lon1 %d' % (lat0, lat1, lon0, lon1)
	
	    print 'ilatincreasing is ', ilatincreasing

            array_pres=[0,0,0,0]
            array_lon=[0,0]

            array_pres[0]=array3d[:,lat0,lon0]
            array_pres[1]=array3d[:,lat0,lon1]
            array_pres[2]=array3d[:,lat1,lon0]
            array_pres[3]=array3d[:,lat1,lon1]
	    print array_pres[0].shape
            print type(array_pres[0])
            factor_lon =(lon_obs[i]-glon[lon0])/(glon[lon1]-glon[lon0])
            #print 'factor_lon is ', factor_lon
	    print 'lon_obs[i] is ', lon_obs[i]
	    print 'glon[lon0] is ', glon[lon0]
	    print 'glon[lon1] is ', glon[lon1]
            array_lon[0] = array_pres[0] + factor_lon*(array_pres[1] - array_pres[0])
            array_lon[1] = array_pres[2] + factor_lon*(array_pres[3] - array_pres[2])
	    print 'array lon type is ', type(array_lon[1])
            factor_lat = (lat_obs[i]-glat[lat0])/(glat[lat1] - glat[lat0])
            #print 'factor lat is ', factor_lat
	    print 'lat_obs[i] is ', lat_obs[i]
            print 'glat[lat0] is ', glat[lat0]
            print 'glat[lat1] is ', glat[lat1]
            array_interp[i] = array_lon[0] + factor_lat*(array_lon[1] - array_lon[0])
#	    if glon[lon0] < lon_obs[i] < glon[lon1]: print '-----------------------TRUE LON'
#	    if glat[lat1] < lat_obs[i] < glat[lat0]: print '-----------------------TRUE LAT'

    #convert lon_obs back to original format i.e. -180 to +180
	    
    for i in range(nstat):
        if lon_obs[i] >= 180.0:
            lon_obs[i] = lon_obs[i]-360.0

    if iglon > 0:
	for i in range(nlon):
            if glon[i] >= 180.0:
                glon[i] = glon[i]-360.0


    # convert array_interp to numpy array
    array_interp = np.array(array_interp)

    print '+++++++++++++++++++++++++++++++++++++++++++++++'
    return array_interp


def interp_array2d_altitude(array2d,gpress,obs_press):
#       assert(len(array2d[0]) == len(obs_alt)
        # press = mid point
	import numpy as np

        if np.array(obs_press).shape == ():
                nstat = 1
        else:
                nstat = len(obs_press)
        print nstat
        press_interp=[0]*nstat
        #array_interp = [0]*nstat
        obs_press = np.hstack((obs_press,np.nan))
        print 'starting vertical interpolation'
        print 'gpress shape is ', gpress.shape
        print 'obs press shape is ', obs_press.shape
        for i in range(nstat):
             print 'i is ', i
             ii, = np.where(gpress < obs_press[i])
             minpresstobspress = np.min(gpress[ii])# first pressure level lower than obs_press
             iminpresstobspress, = np.where(gpress == minpresstobspress)
             #iminpresstobspress = np.min(ii)

             # calculate latitude ordering: UM (S->N) or TOMCAT (N->S)
             if gpress[1] > gpress[2]: ipressincreasing = 0
             if gpress[1] < gpress[2]: ipressincreasing = 1

             if ipressincreasing == 0: # pressures ordered +ve to -ve (sfc to upper)
                press0 = int(iminpresstobspress) - 1
                press1 = int(iminpresstobspress) 

             if ipressincreasing == 1: # pressures ordered -ve to +ve (upper to sfc)
                press0 = int(iminpresstobspress) + 1
                press1 = int(iminpresstobspress) 

             diffpress = gpress[press0]-gpress[press1]
             diffpress2 =   gpress[press0] - obs_press[i]
             factor_press = diffpress2 / diffpress
            # print 'factor press ', factor_press
            # print 'diffpress ', diffpress
            # print 'diffpress2 ', diffpress2
             press_interp[i] = gpress[press0] - (factor_press * diffpress)

             array_press=[0,0]
            # print 'press0 is ', press0
            # print 'press1 is ', press1
             array_press[0] = array2d[i,press0]
             array_press[1] = array2d[i,press1]
             #print 'arraypress[0] is ',array_press[0]
             #print 'arraypress[1] is ', array_press[1]

#            array_interp[i] = array_press[0] + factor_press *(array_press[1] - array_press[0])
             array_interp = array_press[0] + factor_press *(array_press[1] - array_press[0])

            # print 'array_interp[i] ', array_interp[i]
             print 'array_interp[i] ', array_interp

             if (array_press[0] < array_interp) and (array_interp < array_press[1]):
                print 'TRUE'
             elif (array_press[0] > array_interp) and (array_interp > array_press[1]):
                print 'TRUE'



             # print len(array_interp[i])

        # convert array_interp to numpy array
        #array_interp = np.array(array_interp)

        return press_interp, array_interp

def interp_array1d_altitude(array2d,gpress,obs_press):

        import numpy as np

	full_array_interp = []
	full_press_interp = []
        if np.array(obs_press).shape == ():
                nstat = 1
        else:
                nstat = len(obs_press)
        print nstat
        press_interp=[0]*nstat
        obs_press = np.hstack((obs_press,np.nan))
        print 'starting vertical interpolation'
        print 'gpress shape is ', gpress.shape
        print 'obs press shape is ', obs_press.shape

        # calculate latitude ordering: UM (S->N) or TOMCAT (N->S)
        if gpress[1] > gpress[2]: ipressincreasing = 0
        if gpress[1] < gpress[2]: ipressincreasing = 1

        for i in range(nstat):
             print 'i is ', i
             ii, = np.where(gpress < obs_press[i])
	     print 'ii is ', ii
	     print 'ipressincreasing is ', ipressincreasing

             if ipressincreasing == 0: # pressures ordered +ve to -ve (sfc to upper)
		if 1 <= len(ii) < len(gpress):
			minpresstobspress = np.max(gpress[ii]) # first pressure level lower than obs_press
             		iminpresstobspress, = np.where(gpress == minpresstobspress)

			press0 = int(iminpresstobspress) - 1
               		press1 = int(iminpresstobspress)

               		diffpress = gpress[press0]-gpress[press1]
               		diffpress2 =   gpress[press0] - obs_press[i]
                	factor_press = diffpress2 / diffpress
                	# print 'factor press ', factor_press
                	# print 'diffpress ', diffpress
                	# print 'diffpress2 ', diffpress2
               		press_interp = gpress[press0] - (factor_press * diffpress)
               		print 'gpress[press0] is ',gpress[press0]
               		print 'obs_press[i] is ',obs_press[i]
                	print 'g[ress[press1] is ', gpress[press1]
                	array_press=[0,0]
                	array_press[0] = array2d[press0]
                	array_press[1] = array2d[press1]

                	array_interp = array_press[0] + factor_press *(array_press[1] - array_press[0])
			print 'TEST 1'

	     	elif (len(ii) < 1):     #i.e. if longitude is between 358.125deg and 0deg (360)
                	print 'No obs/aerocom pressure levels less than GLOMAP level ', obs_press[i]
			print ' all obs/aerocom pressure levels are greater than GLOMAP level', obs_press[i]
                        maxpress=np.max(gpress)
                        imaxpress, = np.where(gpress==maxpress)
                        press0 = int(imaxpress)

                        press_interp = gpress[press0]
                        array_interp = array2d[press0]
                        print 'gpress[press0] is ',gpress[press0]
                        print 'obs_press[i] is ',obs_press[i]
                        

                        print 'ipressincreasing is ', ipressincreasing
			print 'TEST 2'

		elif (len(ii) == len(gpress)):
			print 'All obs/aerocom pressure levels less than GLOMAP level ', obs_press[i]
			minpress=np.min(gpress)
                        iminpress, = np.where(gpress==minpress)
                        press_interp = gpress[int(iminpress)]
                        array_interp = array2d[int(iminpress)]
                        print 'obs_press[i] is ', obs_press[i]
                        print 'press_interp is ', press_interp

			print 'TEST 6'

             elif ipressincreasing == 1: # pressures ordered -ve to +ve (upper to sfc)

                if 1 <= len(ii) < len(gpress):
                        minpresstobspress = np.max(gpress[ii]) # first pressure level lower than obs_press
                        iminpresstobspress, = np.where(gpress == minpresstobspress)
			
			press0 = int(iminpresstobspress)
	                press1 = int(iminpresstobspress) + 1

		        diffpress = gpress[press0]-gpress[press1]
	                diffpress2 =   gpress[press0] - obs_press[i]
	                factor_press = diffpress2 / diffpress
          		# print 'factor press ', factor_press
           		# print 'diffpress ', diffpress
            		# print 'diffpress2 ', diffpress2
            		press_interp = gpress[press0] - (factor_press * diffpress)
            		print 'gpress[press0] is ',gpress[press0]
            		print 'obs_press[i] is ',obs_press[i]
            		print 'g[ress[press1] is ', gpress[press1]
             		array_press=[0,0]
             		array_press[0] = array2d[press0]
           		array_press[1] = array2d[press1]

             		array_interp = array_press[0] + factor_press *(array_press[1] - array_press[0])
			print 'TEST 3'
                elif (len(ii) == len(gpress)):     #i.e. if longitude is between 358.125deg and 0deg (360)
                        print 'All obs/aerocom pressure levels are less than GLOMAP level ', obs_press[i]
                        print 'Set ii just to include grid-point with min pressure'
                        maxpress=np.max(gpress)
                        imaxpress, = np.where(gpress==maxpress)
                        press0 = int(imaxpress)
			
			press_interp = gpress[press0]
			array_interp = array2d[press0]
			print 'gpress[press0] is ',gpress[press0]
             		print 'obs_press[i] is ',obs_press[i]
            		             		
             		print 'ipressincreasing is ', ipressincreasing
             		print 'TEST 4'
		elif len(ii) < 1:
			print ' No obs/aerocom pressure levels are less than GLOMAP level ', obs_press[i]
			print ' all obs/aerocom pressure levels are greater than GLOMAP level', obs_press[i]
			minpress=np.min(gpress)
			iminpress, = np.where(gpress==minpress)
			press_interp = gpress[int(iminpress)]
			array_interp = array2d[int(iminpress)]
			print 'obs_press[i] is ', obs_press[i]
			print 'minpress is ', minpress
                        print  'TEST 5'

             print 'array_interp ', array_interp

	     full_array_interp.append(array_interp)
	     full_press_interp.append(press_interp)
        print '+++++++++++++++++++++++++++++++++++++++++'
        return full_press_interp, full_array_interp

