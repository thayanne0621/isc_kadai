from __future__ import print_function
import sys
import numpy as np
from scipy import signal
import cv2

mask = np.ones((3, 3), dtype=int)

def init_state(width, height, init_alive_prob=0.5):
    N = width*height
    v = np.array(np.random.rand(N) + init_alive_prob, dtype=int)
    return v.reshape(height, width)

def count_neighbor(F):
    return signal.correlate2d(F, mask, mode="same", boundary="wrap")

def next_generation(F):
    N = count_neighbor(F)
    G = (N == 3) + F * (N == 4)
    return G

def to_image(F, scale=3.0):
    img = np.array(F, dtype=np.uint8)*255
    W = int(F.shape[1]*scale)
    H = int(F.shape[0]*scale)
    img = cv2.resize(img, (W, H), interpolation=cv2.INTER_NEAREST)
    return img

def main():
    p = 0.08
    F = init_state(100, 100, init_alive_prob=p)
    ret = 0
    wait = 10
    while True:
        img = to_image(F, scale=5.0)
        cv2.imshow("lifeGame", img)
        ret = cv2.waitKey(wait)
        F = next_generation(F)
        if ret == ord('r'):
            F = init_state(100, 100, init_alive_prob=p)
        if ret == ord('s'):
            wait = min(wait*2, 1000)
        if ret == ord('f'):
            wait = max(wait//2, 10)
        if ret == ord('q') or ret == 27:
            break
        if ret == ord('w'):
            np.savetxt("save.txt", F, "%d")
        if ret == ord('l'):
            if os.path.exists("save.txt"):
                F = np.loadtxt("save.txt")

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()