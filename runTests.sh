#!/bin/sh

coverage run $(which nosetests)
coverage report -m --omit='lib/*','tests/*'
