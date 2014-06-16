def GetGroupVelocity( bands ):

    velocity = []

    # bands has 3 dimensions
    # bands[i] has dimensionality = # q points
    # bands[i][j] has dimensionality = 3N +1  (the first column is q)
    for i in xrange( len(bands) ):
        velocity.append([])
        for j in xrange( len(bands[i])):
            velocity[i].append([])
            for k in xrange( len(bands[i][j])):
                if k==0:
                    velocity[i][j].append( bands[i][j][k])

                elif j==0:
                    velocity[i][j].append(None)
                # Not sure how else to treat the initial value
                # For now I'll just stick with ignoring it

                else:
                # v = domega/dk
                    v = (bands[i][j][k] - bands[i][j-1][k]) / (bands[i][j][0] - bands[i][j-1][k])
                    velocity[i][j].append(v)


    return velocity
