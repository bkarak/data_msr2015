import time

DEBUG = True

start = time.time()
end = start


# logging facilities
def info(msg=""):
    global start, end

    if DEBUG:
        start = end
        end = time.time()
        print "[INFO][%.3f] %s" % (end - start, msg)


def warning(msg=""):
    global start, end

    if DEBUG:
        start = end
        end = time.time()
        print "[WARNING][%.3f] %s" % (end - start, msg)


def error(msg=""):
    global start, end

    if DEBUG:
        start = end
        end = time.time()
        print "[ERROR][%.3f] %s" % (end - start, msg)
