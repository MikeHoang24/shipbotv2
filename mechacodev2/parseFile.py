def parseFile(fileName):
    f = open(fileName, 'r')
    fData = f.read()
    f.close()

    # Split the text at commas
    stationList = fData.split(',')

    # Ignore Target Time
    stationList = stationList[:-1]
    instrList = []
    
    # Split station string into station, device and endVal strings
    for i,station in enumerate(stationList) :
        # Extract Station Letter
        station = station.strip();
        instrList +=  [[station[0], '', '']];

        # Split Device and end position
        station = station[1:]
        [instrList[i][1], instrList[i][2]] = station.split(' ');

        # Remove remaining Spaces
        instrList[i][1] = instrList[i][1].strip();
        instrList[i][2] = instrList[i][2].strip();

        
    return instrList

lol = parseFile("mission_file.txt")