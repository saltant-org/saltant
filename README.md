[![Build Status](https://travis-ci.com/mwiens91/saltant.svg?branch=master)](https://travis-ci.com/mwiens91/saltant)
[![Documentation Status](https://readthedocs.org/projects/saltant/badge/?version=latest)](https://saltant.readthedocs.io/en/latest/?badge=latest)

# saltant

**saltant** is a
[Celery](https://github.com/celery/celery)-powered [Django
app](https://docs.djangoproject.com/en/2.0/ref/applications/) for
running and managing asynchonous tasks. Its philosophy is that when you
update your task code, you should **never** have to restart your job
queue/workers, or migrate your backend's database. It is a great solution
for an ever-changing code base when downtime is expensive.

## Origin

>  /ˈsæl tnt/
>
> a mutant individual or strain; especially: one produced in a fungal or
> bacterial culture

saltant is a mutant strain of
[Tantalus](https://github.com/shahcompbio/tantalus), which served a dual
role as a task runner (just like saltant) and as a genomics
file/metadata database for the [Shah Lab](http://shahlab.ca/) at [BC
Cancer](http://www.bccancer.bc.ca/). The problems with Tantalus were that
tasks needed frequent updating and that changes constantly needed to be 
made in the server infrastructure. Often, these problems usually required 
bringing the backend down. When the backend was brought down, the 
file/metadata database part had to go down too. Thus, there was much to be 
gained from decoupling the job system from the file/metadata database system.
Hence, saltant.

## More!

Soon!
