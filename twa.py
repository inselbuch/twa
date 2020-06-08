#
#
#	Compute time weighted averages
#
#		with testing using some simulated data
#
#	June 4, 2020 - Inselbuch
#		new module

import sys
from datetime import datetime
from datetime import timedelta
import time
from dateutil import *
from dateutil.tz import *
import random


# so we can reproduce the data if desired
random.seed(1234)

#
# twa2 = compute time-weighted averages
#
# start_time is the start of the time period
# end_time is the end of the time period (end_time must be after start_time)
#
# samples is an ordered list of tuples
#	(timestamp, value)
#
# frequency is a timedelta (e.g., 15 minutes)
#
def twa2(start_time,end_time,samples,frequency):
   mysamples = []
   weightedSamples = []

   span = end_time - start_time
   print("Interval from {} to {} a span of {} {}".format(start_time,end_time,span,span.total_seconds()))

   if start_time >= end_time:
      return(None)

   # in this loop we do two things
   # we figure out the value immediately preceding the time period
   # and we copy the data into a new list only through the end of the time period
   # so "mysamples" is a shorter list than samples passed in (potentially)
   vbefore=None
   ts = start_time
   for x in samples:
      if x[0]>end_time:
         break
      if x[0]<ts:
         vbefore = x
      else:
         mysamples.append(x)

   print("vbefore = {}".format(vbefore))
   # we need to add in the sample value that preceeded the data, so we add it to mysamples
   # it gets the weight from the start of the time period to the time of the first sample
   weightedSamples.insert(0,(vbefore[1],mysamples[0][0]-start_time))

   # each subsequent value gets the weight from it's own timestmp until the time of the next value
   for i in range(len(mysamples)-1):
      weightedSamples.append((mysamples[i][1],mysamples[i+1][0]-mysamples[i][0]))

   # last sample gets the weight from it's time to the end of the time period
   lastS = len(mysamples)-1
   weightedSamples.append((mysamples[lastS][1],end_time-mysamples[lastS][0]))

   average = 0
   for mys in weightedSamples:
      print('\t{}\t{}\t{}'.format(mys[0],mys[1],mys[1].total_seconds()))
      average = average + mys[0]*mys[1].total_seconds()

   average = average / span.total_seconds()

   return(average)


def twa(stime,etime,samps,freq):

   averages = []

   span = etime - stime
   if span < freq:
      print("invalid frequency {} for span {} to {}".format(freq,stime,etime))
      return(None)

   ints = stime
   while ints+freq < etime:
      inte = ints+freq
      avg=twa2(ints,inte,samples,freq)
      averages.append((ints,avg)) # i am associating the time stamp from the START of the interval with the average
      # averages.append((inte,avg)) # this is a common setting that people like to tweak... this line uses the END of the interval
      ints = ints+freq

   return(averages)


# generate a block of sample data
# can be before now or before a specified time (choice of next two lines)
# samples_start_time = datetime.now()
samples_start_time = datetime(2020,6,4,10,4,1)

# shift the start time back 24 hours
# and set the end time to be 16 hours after that
# so it's a 16 hour window of data
samples_start_time = samples_start_time - timedelta(hours=24)
samples_end_time = samples_start_time + timedelta(hours=16)

x=random.random()

# jam some random data into a list of tuples
# we want the timestamps to wander around a bit
# so the time stamp increment is a random number up to 900 seconds but then we limit it to be never more than 600 seconds
ts = samples_start_time
samples = []

while ts < samples_end_time:
   x=random.random()
   v = 175.2 * x
   t = 900*x
   while (t > 600):
      t = t-60
   dt = timedelta(seconds=t)
   ts = ts + dt
   samples.append((ts,v))

print("Generated {} samples in the time period from {} to {}".format(len(samples),samples_start_time,samples_end_time))
for x in samples:
   print("{}\t{}".format(x[0],x[1]))


# create our window for examination
# our window will have a nice even start time with seconds zeroed out, for example
# hence the end time will also have a nice end
# i spurge the end time by an extra few minutes to test how the algorithm deals with the incomplete interval
# start_time = datetime.now()
start_time = datetime(2020,6,4,10,4,1)
start_time = start_time - timedelta(hours=18)
start_time = start_time.replace(minute=0,second=0,microsecond=0)
end_time = start_time + timedelta(hours = 4)
end_time = end_time + timedelta(minutes = 6)

print("Computing time-weighted averages of the sample data from {} to {}".format(start_time,end_time))

# we are asking for N-minute averages using the variables "frequency"
frequency = timedelta(minutes=15)

averages=twa(start_time,end_time,samples,frequency)
for avg in averages:
   print("{} {}".format(avg[0],avg[1]))


