from cam import IPCam, IPFeed

#example usage
def main():
    f = IPFeed()
    c = IPCam()

    while True:
        center = f.get_face_center()
        rel_pos = f.get_relative_pos(center)
        x_diff = 0.5 - rel_pos[0]
        y_diff = 0.5 - rel_pos[1]
        pan = 0
        tilt = 0
        if x_diff < -0.1:
            pan = 0.005
        elif x_diff > 0.1:
            pan = -0.005
        if y_diff < -0.1:
            tilt = -0.005
        elif y_diff > 0.1:
            tilt = 0.005
        c.relative_move(pan, tilt, 0)


if __name__ == '__main__':
    main()
