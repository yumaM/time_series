#coding: utf-8
import numpy as np
#import pandas as pd
from pandas import DataFrame, Series
from matplotlib import pyplot as plt

EM_THRESHOLD = 1e-1
EM_ITERATION_MAXIMUM_COUNT = 5000

class TimeSeriesModel:
    def __init__(self, **args):
        print args

    def __str__(self):
        return ''

    def initialize(**args):
        raise ValueError("Model initialization failed.")


class EMmixin:
    def setData(self, obs):
        self.data = obs

    def ex_step(self, data):
        self.em_step_delegate(data)

    def em_step_delegate(self):
        assert 0, "Not implemented em_step_delegate method in child class"
    
    def expectation(self):
        assert 0, "Not implemented expectation method in child class"

    def maximization(self):
        assert 0, "Not implemented maximization method in child class"


class EM:
    def __init__(self, threshold = EM_THRESHOLD, max_count = EM_ITERATION_MAXIMUM_COUNT):
        self.threshold = threshold
        self.iteration_max_count = max_count

    def __call__(self, _model, _data):
        self.execute(_model, _data)

    def execute(self, _model, _data):
        """ Execute EM algorithm """
        self.model = _model
        #self.model.setData(_data)        
        count = 0
        diff = 100
        llh = []
        while diff>self.threshold and count<self.iteration_max_count:
            print count
            llh.append(self.model.em_step(_data))
            if count>0: diff = abs(self.llh[count] - self.llh[count-1])
            print "\tllh:", self.llh[count]
            count += 1
        #print "#"
        #return 1


if __name__ == "__main__":
    print "base.py: Called in main process."

    if 0:
        obs_p = 2
        sys_k = 2
        N = 20
        kl = Kalman(obs_p,sys_k)
        data = kl.ssm.gen_data(N)
        #kl.set_data(data[1])
        #kl.pfs()
        #for i in range(100): kl.pfs()
        em = EM(data[1], sys_k)
        em.execute()

        if 1:
            fig, axes = plt.subplots(np.int(np.ceil(sys_k/3.0)), 3, sharex=True)
            j = 0
            for i in range(3):
                while j<sys_k:
                    if sys_k<=3:
                        axes[j%3].plot(data[0][j], "k--", label="obs")
                        axes[j%3].plot(em.kl.xp[j], label="prd")
                        axes[j%3].legend(loc="best")
                        axes[j%3].set_title(j)
                    else:
                        axes[i, j%3].plot(data[0][j], "k--", label="obs")
                        axes[i, j%3].plot(em.kl.xp[j], label="prd")
                        axes[i, j%3].legend(loc="best")
                        axes[i, j%3].set_title(j)
                    j += 1
                    if j%3 == 2: break

            fig.show()
        
        #loss = data[0]-em.kl.xs
        #plt.plot(loss)
        #plt.plot(em.llh)
        #plt.show()
