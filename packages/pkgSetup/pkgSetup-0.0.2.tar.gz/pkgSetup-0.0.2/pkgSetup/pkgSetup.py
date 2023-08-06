#!/bin/python3
import os
import subprocess as sp
import re
from codecs import decode
from pprint import pprint
from pathlib import Path
import shutil
import sys


class pyPkg:
    def __init__(self, pkgName):
        self.masterPath = os.path.realpath(__file__).split('/')
        self.masterPath = '/'.join(self.masterPath[:(len(self.masterPath)-1)])+'/src'
        self.pkgName = pkgName
        self.pySitePath=self.getPySitePath()
        self.pyDistPaths=self.getPyDistPath()
        self.pkgPath = self.pySitePath +'/'+self.pkgName
        self.pkgScriptPath= self.pySitePath+'/'+self.pkgName+'/'+self.pkgName
    def getPySitePath(self):
        out=sp.check_output('python3 -m site | grep "^USER_SITE"', shell=True)
        out=decode(out, 'utf-8')
        out=re.search('\'(.*)\'', out)
        return out.group(1)

    def getPyDistPath(self):
        out=sp.check_output('python3 -m site | grep "dist-packages"', shell=True)
        out=decode(out,'utf-8')
        out=out.splitlines()
        distPaths=[]
        for each in out:
            distPath = re.search('\'(.*)\'', each)
            distPaths.append(distPath.group(1))
        return distPaths

    def setupNewPkg(self):
        try:
            if self.pkgPath not in os.listdir():
                os.makedirs(self.pkgPath, exist_ok=True)
            if self.pkgName not in os.listdir(self.pkgPath):
                os.makedirs(self.pkgScriptPath, exist_ok=True)
            
            for root, dirs, files in os.walk(self.masterPath):
                for eachFile in files:
                    if dirs == []:
                        filepath= self.pkgScriptPath + os.sep + eachFile
                        Path(filepath).touch()
                    elif 'src' in dirs:
                        filepath=(self.pkgPath + os.sep + eachFile)
                        Path(filepath).touch()
        except Exception as e:
            print(str(e), 'setupNewPkg failed.')

    def rmPkg(self):
        shutil.rmtree(self.pkgPath)
        return os.listdir(self.pySitePath)

    def rmPkgBuild(self):
        shutil.rmtree(self.pkgPath+'/build', self.pkgPath+'/dist', self.pkgPath+'/'+self.pkgName+'.egg-info')
        return os.listdir(self.pkgPath)
        
    def debug(self): 
        pkgName='testPkgName'
        testPkg=pkgSetup(pkgName)
        print(testPkg.pySitePath)
        print(testPkg.pyDistPaths)
        print(testPkg.masterPath)
        print(testPkg.setupNewPkg())
        print(os.chdir(testPkg.pySitePath))
        print(os.listdir())
        if pkgName in os.listdir():
            print('rm')
            print(testPkg.rmPkg())
    
