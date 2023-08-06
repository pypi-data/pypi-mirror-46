#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# pi_security_cam/security_camera.py
# v.0.1.0
# Developed in 2019 by Travis Kessler <travis.j.kessler@gmail.com>
#
# Contains object for taking photos with USB webcam
#

# stdlib. imports
import cv2
import time
import datetime
import os

# pi_security_cam imports
from pi_security_cam.logger import LOGGER


class SecurityCamera:

    def __init__(self, img_dir: str='./to_upload', cam_num: int=0):
        ''' SecurityCamera: uses camera to take pictures, detects if movement
        occurs, and saves images with movement

        Args:
            img_dir (str): local location where images with motion are stored
            cam_num (int): location of camera on linux system (e.g. "video0")
        '''

        # create folder to store images with detected motion
        if not os.path.isdir(img_dir):
            os.mkdir(img_dir)
        self._img_dir = img_dir

        # setup OpenCV camera
        self._cam = cv2.VideoCapture(cam_num)
        self._cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self._cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # log SecurityCamera initialization
        LOGGER.log(10, 'SecurityCamera initialized with arguments:'
                   '\n\t| img_dir: {}\n\t| cam_num: {}'.format(
                       img_dir, cam_num
                   ))
        return

    def run(self, num_iter: int):
        ''' run: runs SecurityCamera for a specified number of iterations

        Args:
            num_iter (int): number of iterations to run the camera (number of
                pictures taken this cycle)
        '''

        # initialize variables
        img_static = None

        # for specified number of iterations
        for _ in range(num_iter):

            t_start = time.time()

            # take a picture
            _, img = self._cam.read()
            # camera is upside-down
            img = cv2.flip(img, -1)

            # convert to gray, apply gaussian blur
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            # first image is assumed to have no movement
            if img_static is None:
                img_static = gray
                continue

            # determine if motion occurred (20% change in pixels)
            img_diff = cv2.absdiff(img_static, gray)
            img_diff = cv2.threshold(
                img_diff, 20, 255,
                cv2.THRESH_BINARY
            )[1]
            img_diff = cv2.dilate(img_diff, None, iterations=2)
            (_, cnts, _) = cv2.findContours(
                img_diff.copy(),
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )
            motion = False
            for contour in cnts:
                if cv2.contourArea(contour) < 10000:
                    continue
                motion = True
                break

            # if motion occurred, save the image
            if motion:
                curr_time = datetime.datetime.now().strftime(
                    '%Y%m%d%H%M%S%f'
                )[:-3]
                LOGGER.log(20, 'Motion detected at {}'.format(curr_time))
                img_path = os.path.join(
                    self._img_dir,
                    curr_time + '.jpg')
                cv2.imwrite(img_path, img)
                LOGGER.log(10, 'Image saved to {}'.format(img_path))
            img_static = gray
            LOGGER.log(10, 'Camera processing time: {} seconds'.format(
                time.time() - t_start
            ))

        return
