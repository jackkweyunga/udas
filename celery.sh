#!/bin/sh

set FORKED_BY_MULTIPROCESSING=1 

cd src && celery -A auth worker -l info

