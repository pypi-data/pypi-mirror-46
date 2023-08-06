#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# pi_security_cam/runtime.py
# v.0.1.0
# Developed in 2019 by Travis Kessler <travis.j.kessler@gmail.com>
#
# Contains object for starting multiprocessed image capture/upload runtime
#

# stdlib. imports
import time
import multiprocessing

# pi_security_cam imports
from pi_security_cam.security_camera import SecurityCamera
from pi_security_cam.dropbox_uploader import DropboxUploader
from pi_security_cam.logger import LOGGER, add_file_handler


class Runtime:

    def __init__(self, log_level: int=20, log_dir: str=None):
        ''' Runtime object: for running camera/uploader in parallel

        Args:
            log_level (int): log level for text logs
            log_dir (str): if not none, saves logs in this directory
        '''

        self._jobs = []
        LOGGER.setLevel(log_level)
        if log_dir is not None:
            add_file_handler(LOGGER, log_dir)
        return

    def run(self, img_dir: str='./to_upload', cam_num: int=0,
            dbx_folder: str='/Security Camera',
            dbx_access_token: str='./access_token.json'):
        ''' run: runs camera/uploader in parallel

        Args:
            img_dir (str): path to where images are saved/uploaded from
            cam_num (int): address of camera (e.g. "video0")
            dbx_folder (str): Dropbox folder where uploaded images are placed
            dbx_access_token (str): JSON file containing account access token
                ({"access_token": "my_token"})
        '''

        cam = SecurityCamera()
        uploader = DropboxUploader()
        self._jobs.append(multiprocessing.Process(
            target=self._start_security_camera, args=(cam,)
        ))
        self._jobs.append(multiprocessing.Process(
            target=self._start_dropbox_uploader, args=(uploader,)
        ))
        for job in self._jobs:
            job.start()
        return

    @staticmethod
    def _start_security_camera(cam: SecurityCamera):
        '''Called via multiprocessing.Process.start'''

        while True:
            cam.run(50)
        return

    @staticmethod
    def _start_dropbox_uploader(uploader: DropboxUploader):
        '''Called via multiprocessing.Process.start'''

        while True:
            time.sleep(60)
            uploader.upload()
        return
