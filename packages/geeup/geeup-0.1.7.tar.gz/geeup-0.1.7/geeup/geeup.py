__copyright__ = """

    Copyright 2019 Samapriya Roy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""
__license__ = "Apache 2.0"

#! /usr/bin/env python

import argparse,os,ee,sys,platform
os.chdir(os.path.dirname(os.path.realpath(__file__)))
from batch_uploader import upload
from batch_remover import delete
from sel_tuploader import seltabup
from metadata_ingest import selupload
from zipfiles import zipshape
from os.path import expanduser
lpath=os.path.dirname(os.path.realpath(__file__))
sys.path.append(lpath)

def update():
    if str(platform.system()) =="Windows":
        os.system("python sel-latest-win.py")
        print("Updated selenium driver for Windows64")
    elif str(platform.system()) =="Linux":
        os.system("python sel-latest-linux.py")
        print("Updated selenium driver for Linux64")
    else:
        print("Architecture not recognized")
def update_from_parser(args):
    update()

suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
def humansize(nbytes):
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])

def quota():
    quota=ee.data.getAssetRootQuota(ee.data.getAssetRoots()[0]['id'])
    print('')
    print("Total Quota: "+str(humansize(quota['asset_size']['limit'])))
    print("Used Quota: "+str(humansize(quota['asset_size']['usage'])))

def quota_from_parser(args):
    quota()

def zipshape_from_parser(args):
    zipshape(directory=args.input,export=args.output)

def _comma_separated_strings(string):
  """Parses an input consisting of comma-separated strings.
     Slightly modified version of: https://pypkg.com/pypi/earthengine-api/f/ee/cli/commands.py
  """
  error_msg = 'Argument should be a comma-separated list of alphanumeric strings (no spaces or other' \
              'special characters): {}'
  values = string.split(',')
  for name in values:
      if not name.isalnum():
          raise argparse.ArgumentTypeError(error_msg.format(string))
  return values

def upload_from_parser(args):
    upload(user=args.user,
           source_path=args.source,
           destination_path=args.dest,
           metadata_path=args.metadata,
           nodata_value=args.nodata,
           bucket_name=args.bucket,
           band_names=args.bands)

def selupload_from_parser(args):
    selupload(user=args.user,
           source_path=args.source,
           destination_path=args.dest,
           metadata_path=args.metadata,
           nodata_value=args.nodata,
           bucket_name=args.bucket,
           manifest=args.manifest)

def seltabup_from_parser(args):
    seltabup(uname=args.user,
           dirc=args.source,
           destination=args.dest)
def tasks():
    statuses=ee.data.getTaskList()
    st=[]
    for status in statuses:
        st.append(status['state'])
    print("Tasks Running: "+str(st.count('RUNNING')))
    print("Tasks Ready: "+str(st.count('READY')))
    print("Tasks Completed: "+str(st.count('COMPLETED')))
    print("Tasks Failed: "+str(st.count('FAILED')))
    print("Tasks Cancelled: "+str(st.count('CANCELLED')))

def tasks_from_parser(args):
    tasks()

def delete_collection_from_parser(args):
    delete(args.id)

spacing="                               "
def main(args=None):
    parser = argparse.ArgumentParser(description='Simple Client for Earth Engine Uploads with Selenium Support')

    subparsers = parser.add_subparsers()

    parser_update=subparsers.add_parser('update',help='Updates Selenium drivers for firefox [windows or linux systems]')
    parser_update.set_defaults(func=update_from_parser)

    parser_quota = subparsers.add_parser('quota', help='Print Earth Engine total quota and used quota')
    parser_quota.set_defaults(func=quota_from_parser)

    parser_zipshape = subparsers.add_parser('zipshape', help='Zips all shapefiles and subsidary files into individual zip files')
    required_named = parser_zipshape.add_argument_group('Required named arguments.')
    required_named.add_argument('--input', help='Path to the input directory with all shape files', required=True)
    required_named.add_argument('--output', help='Destination folder Full path where shp, shx, prj and dbf files if present in input will be zipped and stored', required=True)
    parser_zipshape.set_defaults(func=zipshape_from_parser)

    parser_upload = subparsers.add_parser('upload', help='Batch Asset Uploader using Selenium')
    required_named = parser_upload.add_argument_group('Required named arguments.')
    required_named.add_argument('--source', help='Path to the directory with images for upload.', required=True)
    required_named.add_argument('--dest', help='Destination. Full path for upload to Google Earth Engine, e.g. users/pinkiepie/myponycollection', required=True)
    optional_named = parser_upload.add_argument_group('Optional named arguments')
    optional_named.add_argument('-m', '--metadata', help='Path to CSV with metadata.')
    optional_named.add_argument('--nodata', type=int, help='The value to burn into the raster as NoData (missing data)')
    optional_named.add_argument('--bands', type=_comma_separated_strings, help='Comma-separated list of names to use for the image bands. Spaces'
                                                                               'or other special characters are not allowed.')

    required_named.add_argument('-u', '--user', help='Google account name (gmail address).')
    optional_named.add_argument('-b', '--bucket', help='Google Cloud Storage bucket name.')

    parser_upload.set_defaults(func=upload_from_parser)

    parser_selupload = subparsers.add_parser('selupload', help='Batch Asset Uploader for Planet Items & Assets using Selenium')
    required_named = parser_selupload.add_argument_group('Required named arguments.')
    required_named.add_argument('--source', help='Path to the directory with images for upload.', required=True)
    required_named.add_argument('--dest', help='Destination. Full path for upload to Google Earth Engine, e.g. users/pinkiepie/myponycollection', required=True)
    required_named.add_argument('-m', '--metadata', help='Path to CSV with metadata.')
    required_named.add_argument('-mf','--manifest',help='Manifest type to be used,Choose PS OrthoTile(PSO)|PS OrthoTile DN(PSO_DN)|PS OrthoTile Visual(PSO_V)|PS4Band Analytic(PS4B)|PS4Band DN(PS4B_DN)|PS4Band SR(PS4B_SR)|PS3Band Analytic(PS3B)|PS3Band DN(PS3B_DN)|PS3Band Visual(PS3B_V)|RE OrthoTile (REO)|RE OrthoTile Visual(REO_V)')
    optional_named = parser_selupload.add_argument_group('Optional named arguments')
    optional_named.add_argument('--nodata', type=int, help='The value to burn into the raster as NoData (missing data)')
    required_named.add_argument('-u', '--user', help='Google account name (gmail address).')
    optional_named.add_argument('-b', '--bucket', help='Google Cloud Storage bucket name.')

    parser_selupload.set_defaults(func=selupload_from_parser)

    parser_seltabup = subparsers.add_parser('seltabup', help='Batch Table Uploader using Selenium.')
    required_named = parser_seltabup.add_argument_group('Required named arguments.')
    required_named.add_argument('--source', help='Path to the directory with zipped folder for upload.', required=True)
    required_named.add_argument('--dest', help='Destination. Full path for upload to Google Earth Engine, e.g. users/pinkiepie/myponycollection', required=True)
    required_named.add_argument('-u', '--user', help='Google account name (gmail address).')
    parser_seltabup.set_defaults(func=seltabup_from_parser)

    parser_tasks=subparsers.add_parser('tasks',help='Queries current task status [completed,running,ready,failed,cancelled]')
    parser_tasks.set_defaults(func=tasks_from_parser)

    parser_delete = subparsers.add_parser('delete', help='Deletes collection and all items inside. Supports Unix-like wildcards.')
    parser_delete.add_argument('id', help='Full path to asset for deletion. Recursively removes all folders, collections and images.')
    parser_delete.set_defaults(func=delete_collection_from_parser)

    args = parser.parse_args()

    #ee.Initialize()
    args.func(args)

if __name__ == '__main__':
    main()
