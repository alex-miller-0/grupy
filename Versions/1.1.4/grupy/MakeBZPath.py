# traces a path in k-space from high symmetry points and returns its 
# cumulative distance as a set of x-coordinates
# (as well as high symmetry labels for the x-coordinates)

def MakeBZPath(hs_points, q):
    X = 0.0  # this will be updated in blocks
    c = 0  # hs_points count
    labels = []
    BZ_path = []  # should be as long as the number of q-points

    for i in xrange(len(q)):
        #
        # q-points come in as strings
        #
        q[i][0] = float(q[i][0])
        q[i][1] = float(q[i][1])
        q[i][2] = float(q[i][2])

        if i == 0:
            labels.append([hs_points[0][0], 0.0])
            BZ_path.append(0.0)
            c += 1

        if i > 0:

            if hs_points[c][1] == q[i][0] and hs_points[c][2] == q[i][1] and hs_points[c][3] == q[i][2]:


                A = hs_points[c][1] - hs_points[c - 1][1]
                B = hs_points[c][2] - hs_points[c - 1][2]
                C = hs_points[c][3] - hs_points[c - 1][3]

                dist = ( A ** 2 + B ** 2 + C ** 2 ) ** 0.5
                X += dist

                qA = q[i][0] - hs_points[c][1]
                qB = q[i][1] - hs_points[c][2]
                qC = q[i][2] - hs_points[c][3]

                q_dist = ( qA ** 2 + qB ** 2 + qC ** 2 ) ** 0.5

                BZ_path.append(X + q_dist)
                labels.append([hs_points[c][0], X + q_dist])

                c += 1


            else:
                qA = q[i][0] - hs_points[c - 1][1]
                qB = q[i][1] - hs_points[c - 1][2]
                qC = q[i][2] - hs_points[c - 1][3]

                q_dist = ( qA ** 2 + qB ** 2 + qC ** 2 ) ** 0.5

                BZ_path.append(X + q_dist)

    return BZ_path, labels