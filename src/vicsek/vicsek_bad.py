import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import math

class VicsekModel:

    n = 200
    d = 0.01
    v = 0.01
    dt = 1
    eta = 0.1
    r = np.random.random((n, 2))
    theta = np.random.random(n)
    counter = 0

    x = r[:, 0]
    y = r[:, 1]
    u = np.cos(2 * np.pi * theta)
    vv = np.sin(2 * np.pi * theta)

    plt.rcParams['animation.embed_limit'] = 300

    fig, ax = plt.subplots(figsize=(6, 6))

    q = ax.quiver(x, y, u, vv, angles='xy')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("Vicsek Model")

    def update_model(self):

        for i in range(self.n):
            sum_sin = 0
            sum_cos = 0
            neighbours = 0

            for j in range(self.n):
                if i != j:
                    if self.distance(self.r[i], self.r[j]) < self.d:
                        theta_j = 2 * np.pi * self.theta[j]
                        sum_sin = sum_sin + np.sin(theta_j)
                        sum_cos = sum_cos + np.cos(theta_j)
                        neighbours = neighbours + 1

            if neighbours > 0:
                avg_theta = np.arctan2(sum_sin / neighbours, sum_cos / neighbours)
                self.theta[i] = (avg_theta / (2 * np.pi)) + self.eta * (np.random.rand() - 0.5)

            dx = self.v * self.dt * np.cos(2 * np.pi * self.theta[i])
            dy = self.v * self.dt * np.sin(2 * np.pi * self.theta[i])

            self.r[i, 0] = self.r[i, 0] + dx
            self.r[i, 1] = self.r[i, 1] + dy

            if self.r[i, 0] > 1:
                self.r[i, 0] = 0
            if self.r[i, 1] > 1:
                self.r[i, 1] = 0
            if self.r[i, 0] < 0:
                self.r[i, 0] = 1
            if self.r[i, 1] < 0:
                self.r[i, 1] = 1

            self.counter = self.counter + 1

    def distance(self, p1, p2):
        return np.sqrt(((p1 - p2) ** 2).sum())

    def animate(self, frame):

        self.update_model()

        x = []
        y = []
        u = []
        vv = []

        for i in range(self.n):
            x.append(self.r[i, 0])
            y.append(self.r[i, 1])
            u.append(np.cos(2 * np.pi * self.theta[i]))
            vv.append(np.sin(2 * np.pi * self.theta[i]))

        self.q.set_offsets(np.c_[x, y])
        self.q.set_UVC(u, vv)

        print("frame", frame, "counter", self.counter)

        return self.q,

if __name__ == "__main__":

    vicsek_model = VicsekModel()
    ani = FuncAnimation(vicsek_model.fig, vicsek_model.animate, frames=200, interval=50, blit=True)
    plt.show()
