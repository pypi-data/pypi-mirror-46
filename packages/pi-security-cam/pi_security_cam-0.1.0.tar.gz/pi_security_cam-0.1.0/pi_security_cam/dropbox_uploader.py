#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# pi_security_cam/dropbox_uploader.py
# v.0.1.0
# Developed in 2019 by Travis Kessler <travis.j.kessler@gmail.com>
#
# Contains object for uploading images to Dropbox
#

# stdlib. imports
import datetime
import os
import json
import dropbox
import time

# pi_security_cam imports
from pi_security_cam.logger import LOGGER


class DropboxUploader:

    def __init__(self, img_dir: str='./to_upload',
                 dbx_folder: str='/Security Camera',
                 dbx_access_token: str='./access_token.json'):
        ''' DropboxUploader: uploads images in specified directory to a Dropbox
        folder

        Args:
            img_dir (str): directory to upload files from
            dbx_folder (str): Dropbox folder to upload to
            dbx_access_token (str): JSON file containing Dropbox access token
                ({"access_token": "my_token"})
        '''

        # obtain Dropbox access token, initialize connection
        if not os.path.isdir(img_dir):
            os.mkdir(img_dir)
        self._img_dir = img_dir
        self._dbx_folder = dbx_folder
        with open(dbx_access_token, 'r') as access_file:
            access_token = json.load(access_file)['access_token']
        access_file.close()
        self._dbx_connection = dropbox.Dropbox(access_token)

        # log DropboxUploader initialization
        LOGGER.log(10, 'DropboxUploader initialized with arguments:'
                   '\n\t| img_dir: {}\n\t| dbx_folder: {}'
                   '\n\t| dbx_access_token: {}'.format(
                       img_dir, dbx_folder, dbx_access_token
                   ))
        return

    def upload(self):
        '''Uploads images in specified directory to Dropbox'''

        # create folder for date on Dropbox if it doesn't exist
        curr_date = datetime.datetime.now().strftime('%Y%m%d')
        upload_folder = self._dbx_folder + '/' + curr_date
        try:
            self._dbx_connection.files_create_folder(upload_folder)
            LOGGER.log(10, 'Created Dropbox folder for current date: {}'
                       .format(curr_date))
        except:
            LOGGER.log(10, 'Dropbox folder already exists: {}'.format(
                curr_date
            ))

        # scan image directory, upload each file, remove local files
        for file in os.listdir(self._img_dir):
            t_start = time.time()
            try:
                with open(os.path.join(
                    self._img_dir, file
                ), 'rb') as to_upload:
                    self._dbx_connection.files_upload(
                        to_upload.read(),
                        os.path.join(upload_folder, file),
                        mode=dropbox.files.WriteMode('overwrite')
                    )
                os.remove(os.path.join(self._img_dir, file))
                LOGGER.log(10, 'Uploaded {} in {} seconds'.format(
                    file, time.time() - t_start
                ))
            except Exception as ex:
                LOGGER.log(40, 'Failed upload: {}, {}'.format(file, ex))

        return
