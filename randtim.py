from random import randint
from time import sleep
import time

# random.seed()

for i in xrange(60):

    s = sleep(randint(1,5))
    agents = ['Mozilla/5.0', 'Safari/533.1', 'Chrome/33.0.1750.117']	
    s = sleep(randint(agents))
    print str(i) + ": sleep for seconds: " + str(s)
    time.sleep(2)
