# coding=utf-8
import cv2


def video_feed(cam, drone):
    running = True
    while running:
        # get current frame of video
        running, frame = cam.read()
        status = "No Targets"
        if running:

            if cv2.waitKey(1) & 0xFF == ord('q'):
                # when 'q' key pressed
                print("Landing and turning video off..")
                running = False
                drone.land()
                cam.release()
                cv2.destroyAllWindows()
        else:
            # error reading frame
            print 'Error reading video feed'

        if not running:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        edged = cv2.Canny(blurred, 50, 150)

        (_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # loop over the contours
        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.01 * peri, True)

            # ensure that the approximated contour is "roughly" rectangular
            if 4 <= len(approx) <= 6:
                # compute the bounding box of the approximated contour and
                # use the bounding box to compute the aspect ratio
                (x, y, w, h) = cv2.boundingRect(approx)
                aspect_ratio = w / float(h)

                # compute the solidity of the original contour
                area = cv2.contourArea(c)
                hull_area = cv2.contourArea(cv2.convexHull(c))
                solidity = area / float(hull_area)

                # compute whether or not the width and height, solidity, and
                # aspect ratio of the contour falls within appropriate bounds
                keep_dims = w > 15 and h > 15
                keep_solidity = solidity > 0.9
                keep_aspect_ratio = 0.8 >= aspect_ratio >= 0.5

                # ensure that the contour passes all our tests
                if keep_dims and keep_solidity and keep_aspect_ratio:
                    # draw an outline around the target and update the status
                    # text
                    cv2.drawContours(frame, [approx], -1, (0, 0, 255), 4)
                    status = "Found square(s)"

                    # compute the center of the contour region and draw the crossbars
                    M = cv2.moments(approx)
                    (cX, cY) = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    (startX, endX) = (int(cX - (w * 0.15)), int(cX + (w * 0.15)))
                    (startY, endY) = (int(cY - (h * 0.15)), int(cY + (h * 0.15)))
                    cv2.line(frame, (startX, cY), (endX, cY), (0, 0, 255), 3)
                    cv2.line(frame, (cX, startY), (cX, endY), (0, 0, 255), 3)

        # draw the status text on the frame
        cv2.putText(frame, status, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 0, 255), 2)

        # show the frame
        cv2.imshow("Frame", frame)

    cam.release()
    cv2.destroyAllWindows()


class capture(object):
    def __init__(self):
        print("Video capture: Class loaded")
