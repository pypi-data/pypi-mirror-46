#!/usr/bin/env python
# coding=utf-8
#-*- encoding:utf-8 -*-
# from __future__ import print_function

__version__ = '0.1.7.6'

class Config:
    def get(self,project):
        print(project)
        # pass
    def get_version(self):
        return __version__
        
