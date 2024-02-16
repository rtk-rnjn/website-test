@echo off
gunicorn -w 4 -k gevent 'main:app'