import os


def MakePath(path):
    ret_path = []  # return path
    ret_labels = []  # return labels

    for i in xrange(len(path)):

        ret_labels.append(path[i])

        if i > 0:

            dist1 = ( float(path[i][1]) - float(path[i - 1][1]))
            dist2 = ( float(path[i][2]) - float(path[i - 1][2]))
            dist3 = ( float(path[i][3]) - float(path[i - 1][3]))

            for x in xrange(101):

                p = [(path[i - 1][1] + x * (dist1 / 100)), (path[i - 1][2] + x * (dist2 / 100)),
                     (path[i - 1][3] + x * (dist3 / 100))]
                #
                # throw out adjacent repeats (they pop up for some reason)
                #
                if len(ret_path) > 0:
                    if p[0] == ret_path[-1][0]:
                        if p[1] == ret_path[-1][1]:
                            if p[2] == ret_path[-1][2]:
                                continue

                ret_path.append([round(p[0], 4), round(p[1], 4), round(p[2], 4)])

    return ret_path, ret_labels