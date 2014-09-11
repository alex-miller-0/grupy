__author__ = 'asmiller'
import os




def ReadInput():
    dir = []
    # sg = ""
    bz_path = []
    temps = []
    pathRead = False

    cwd = os.getcwd()

    for file in os.listdir(cwd):
        if file.lower() == "grupy.in":
            f = open(file, 'r')

            for line in f:

                # Don't read comments
                if line.startswith("//") or line.startswith("#"):
                    if pathRead == True:
                        pathRead = False
                    continue

                # Directories
                if "dir" in line.lower():
                    s = line.split()
                    for i in xrange(len(s)):
                        if i > 0 and s[i] != "=":
                            dir.append(s[i])

                # Path (in Cartesian coordinates!)
                if "path" in line.lower():
                    pathRead = True
                    s = line.split()
                    if (len(s) - 1) % 4 != 0:
                        print "Error: check your BZ path and make sure all points are labelled"
                        return 0
                    n = ((len(s) - 1) / 4)

                    for i in xrange(0, n):
                        label = s[1 + i * 4]
                        one = float(s[2 + i * 4])
                        two = float(s[3 + i * 4])
                        three = float(s[4 + i * 4])

                        c = [label, one, two, three]

                        bz_path.append(c)

                # Continuation of path
                elif pathRead == True:
                    s = line.split()
                    if len(s) % 4 != 0:
                        print "Error: check your BZ path and make sure all points are labelled"
                        return 0
                    n = (len(s) / 4)

                    for i in xrange(0, n):
                        label = s[i * 4]
                        one = float(s[1 + i * 4])
                        two = float(s[2 + i * 4])
                        three = float(s[3 + i * 4])

                        c = [label, one, two, three]

                        bz_path.append(c)


                # Temperatures (for average Gruneisen)
                if "temps" in line.lower():
                    s = line.split()
                    for i in range(len(s)):
                        try:
                            t = float(s[i])
                            temps.append(t)
                        except:
                            pass





            f.close()

    return dir, bz_path, temps