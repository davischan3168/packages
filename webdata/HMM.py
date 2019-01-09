#!/usr/bin/env python3
# -*-coding:utf-8-*-

import numpy as np
class HMM():

    def __init__(self, A, B, pi):
        self.A = A
        self.B = B
        self.pi = pi
        
    def simulate(self, T):
        # draw_from接受一个概率分布，然后生成该分布下的一个样本。    
        def draw_from(probs):
            return np.where(np.random.multinomial(1, probs) == 1)[0][0]
        observations = np.zeros(T, dtype=int)
        states = np.zeros(T, dtype=int)    
        states[0] = draw_from(self.pi)
        observations[0] = draw_from(self.B[states[0], :])
        for t in range(1, T):
            states[t] = draw_from(self.A[states[t-1], :])
            observations[t] = draw_from(self.B[states[t], :])
        return states, observations

    def forward(self, obs_seq):
        """前向算法"""
        N = self.A.shape[0]
        T = len(obs_seq)
        
        F = np.zeros((N, T))
        F[:, 0] = self.pi * self.B[:, obs_seq[0]]
        
        for t in range(1, T):
            for n in range(N):
                F[n, t] = np.dot(F[:, t-1], (self.A[:, n])) * self.B[n, obs_seq[t]]
        return F

    def backward(self, obs_seq):
        """后向算法"""
        N = self.A.shape[0]
        T = len(obs_seq)
        
        M = np.zeros((N, T))
        M[:, T-1] = 1
        # 或者M[:, -1:] = 1，列上表示最后一行
        
        for t in reversed(range(T-1)):
            for n in range(N):
                #M[n, t] = np.dot(self.A[n, :], M[:, t+1]) * self.B[n, obs_seq[t+1]]
                M[n, t] = np.sum(self.A[n, :], M[:, t+1]) * self.B[n, obs_seq[t+1]]
        return M


    def EM(self, observation, criterion=0.05):
        """EM算法进行参数学习"""
        n_state = self.A.shape[0]
        n_sample = len(observation)
        done = 1
        while done:
            Alpha = self.forward(observation)
            Beta = self.backward(observation)
            xi = np.zeros((n_state, n_state, n_sample-1))
            gamma = np.zeros((n_state, n_sample))
            for t in range(n_sample-1):
                denom = np.sum(np.dot(Alpha[:, t].T, self.A) * self.B[:, observation[t+1]].T * Beta[:, t+1].T)
                sum_gamma1 = np.sum(Alpha[:, t] * Beta[:, t])
                for i in range(n_state):
                    numer = Alpha[i, t] * self.A[i, :] * self.B[:, observation[t+1]].T * Beta[:, t+1].T
                    xi[i, :, t] = numer/denom
                gamma[i, t] = Alpha[i, t] * Beta[i, t] / sum_gamma1
            last_col = Alpha[:, n_sample-1].T * Beta[:, n_sample-1]
            gamma[:, n_sample-1] = last_col / np.sum(last_col)
            # 更新参数
            n_pi = gamma[:, 0]
            n_A = np.sum(xi, 2) / np.sum(gamma[:, :-1], 1)
            n_B = np.copy(self.B)
            num_level = self.B.shape[1]
            sum_gamma = 0
            a = 0
            for lev in range(num_level):
                for h in range(n_state):
                    for t in range(n_sample):
                        sum_gamma = sum_gamma + gamma[h, t]
                        if observation[t] == lev:
                            a = a + gamma[h, t]
                    n_B[h, lev] = a / sum_gamma
                    a = 0
            # 检查阈值
            if np.max(np.abs(self.pi-n_pi)) < criterion and np.max(np.abs(self.B-n_B)) < criterion and np.max(np.abs(self.A-n_A)) < criterion:
                done = 0
            self.A, self.B, self.pi = n_A, n_B, n_pi
        return self.A, self.B, self.pi

    def viterbi(self, obs_seq):
        """viterbi算法预测状态序列"""
        N = self.A.shape[0]
        T = len(obs_seq)
        P = np.zeros((N, T))
        prev_point = np.zeros((N, T))
        prev_point[:, 0] = 0
        P[:, 0] = self.pi * self.B[:, obs_seq[0]]
        for t in range(1, T):
            for n in range(N):
                P[n, t] = np.max(P[:, t - 1] * self.A[:, n]) * self.B[n, obs_seq[t]]
                prev_point[n, t] = np.argmax(P[:, t - 1] * self.A[:, n] * self.B[n, obs_seq[t]])
        return P, prev_point

    def build_path(self, obs_seq):
        """return the optimal path"""
        P, prev_point = self.viterbi(obs_seq)
        T = len(obs_seq)
        opt_path = np.zeros(T)
        last_state = np.argmax(P[:, T-1])
        opt_path[T-1] = last_state
        for t in reversed(range(T-1)):
            opt_path[t] = prev_point[int(opt_path[t+1]), t+1]
        last_path = reversed(opt_path)
        return last_path

if __name__ == '__main__':
    # 用《统计学习方法》中的案例进行测试
    A = np.array([[0.5, 0.2, 0.3], [0.3, 0.5, 0.2], [0.2, 0.3, 0.5]])
    B = np.array([[0.5, 0.5], [0.4, 0.6], [0.7, 0.3]])
    pi = np.array([0.2, 0.4, 0.4])
    test1 = HMM(A, B, pi)
    obs_seq = [0, 1, 0]
    print(test1.forward(obs_seq))
    print(test1.backward(obs_seq))
    print(test1.viterbi(obs_seq))
    print(test1.build_path(obs_seq))
    print(test1.EM(obs_seq))
