#!/bin/sh

coverage run $(which nosetests)
coverage report -m --omit='bin/*','lib/*','tests/*'
