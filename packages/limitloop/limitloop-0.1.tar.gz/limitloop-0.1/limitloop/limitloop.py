from time import perf_counter, sleep
import math, threading

class Loop(object):
    def __init__(self, func, freq=30, saveArgs=False):
        self._running = False
        self._function = func
        self._frequency = freq
        self._saveArgs = saveArgs
        self._args = []
        self._kwargs = {}
        self._lastReturn = None
        self._lastFrameTime = 0
        self._currentFrameStartTime = 0
    
    @property
    def running(self):
        return self._running
    
    @property
    def frequency(self):
        return self._frequency
        
    @frequency.setter
    def frequency(self, newValue):
        if self._running: raise RuntimeError('Loop.frequency cannot be set while the loop is running')
        self._frequency = newValue
    
    @property
    def saveArgs(self):
        return self._saveArgs
    
    @saveArgs.setter
    def saveArgs(self, newValue):
        if self._running: raise RuntimeError('Loop.saveArgs cannot be set while the loop is running')
        self._saveArgs = newValue
    
    def run(self, maxIterations=-1):
        if self._running: raise RuntimeError('Loop.run cannot be called while the loop is already running')
        self._running = True
        frameTargetTime = self.targetTime()
        iteration=0
        while self._running:
            self._currentFrameStartTime = perf_counter()
            self._lastReturn = self._function(self, *self._args, **self._kwargs)
            iteration += 1
            if iteration >= maxIterations and maxIterations > 0:
                self.end()
            self._lastFrameTime = perf_counter() - self._currentFrameStartTime
            if(self._lastFrameTime < frameTargetTime):
                sleep(frameTargetTime - self._lastFrameTime)
    
    def end(self):
        if not self._running: raise RuntimeError('Loop.end can only be called while the loop is running')
        self._running = False
        self._lastFrameTime = 0
        self._currentFrameStartTime = 0
    
    def frameTime(self):
        if not self._running: raise RuntimeError('Loop.frameTime can only be called while the loop is running')
        return self._currentFrameStartTime - perf_counter()
    
    def targetTime(self):
        return 1/self._frequency
    
    def framesPerSecond(self):
        return 1/self._lastFrameTime if self._lastFrameTime != 0 else 0
    
    def setArgs(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
    
    def lastReturn(self):
        return self._lastReturn
