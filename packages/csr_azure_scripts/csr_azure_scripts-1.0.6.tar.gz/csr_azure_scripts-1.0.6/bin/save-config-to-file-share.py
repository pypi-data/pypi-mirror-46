#!/usr/bin/env python
import sys
import cli
from csr_azure_scripts import cas
import argparse

parser = argparse.ArgumentParser(description="Upload config file")
parser.add_argument('storage', help='The name of the storage to upload to')
parser.add_argument('filename', help='Filename to upload to container')
parser.add_argument("--storage_key", help='Storage key to upload to container', default="")

args = parser.parse_args()
storage = args.storage
filename = args.filename
storage_key = args.storage_key

print storage
print filename

# first, save the config to bootflash
get_config = "copy running-config bootflash:%s" % filename
result = cli.execute(get_config)
if 'copied' not in result:
    print result
    sys.exit(1)

result = result.splitlines()

# print output of ios cli output showing the config copy
for line in result:
    if 'copied' in line:
        print line

local_filepath = "/bootflash/"+filename
cas().upload_file_to_file_share(local_filepath, filename, storage, storage_key)
