# loadtest
loadtest/benchmark students sites over a 2 week period.

## Method
We will use two methods for this.  We will use siege to create load on the servers of about 100 request/sec, this will measure response time, failures, and total successful requests in a given amount of time.  We will also run a python script that will be checking the returned results from the students site.  So probably 99% of the traffic they'll receive will not be checking the result, and 1% will be checking the result.  Either way, hopefully they won't be able to tell the difference in the requests and should always return the correct result.
