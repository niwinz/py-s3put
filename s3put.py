#!/usr/bin/python2
# -*- coding: utf-8 -*-
# Copyright (c) 2010, Andrei Antoukh <niwi@niwi.be>
# BSD License

import os, os.path, hashlib, sys
from optparse import OptionParser

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from boto.exception import S3CreateError
from boto.exception import S3ResponseError


def sha1_sum(filename):
    sha1 = hashlib.sha1()
    with open(filename,'rb') as f: 
        for chunk in iter(lambda: f.read(8192), ''): 
            sha1.update(chunk)

    return sha1.hexdigest()

if list(sys.version_info)[:2] < 2.6:
    print "Python 2.6+ required."
    sys.exit(-1)

if __name__ == '__main__':
    usage = "usage: %prog [options] arg1 arg2"
    parser = OptionParser(usage=usage)
    parser.add_option("--overwrite", action="store_true", dest="overwrite", default=False,
        help=u"Overwrite if file exists.")
    parser.add_option("--prefix", default="", dest="prefix",
        help=u"Prefix directory for S3 bucket. Default: ''")
    parser.add_option("--bucket", dest="bucket",
        help=u"Bucket name.")
    parser.add_option("--diferential", default=False, dest="diferential", action="store_true",
        help=u"Make operations diferential. (Upload if file is modified)")
    parser.add_option("--access-key", dest='accesskey',
        help=u"Set amazon access key.")
    parser.add_option("--secret-key", dest='secretkey',
        help=u"Set amazon secret-key.")

    opts, args = parser.parse_args()

    if not opts.accesskey or not opts.secretkey:
        if "AWS_ACCESS_KEY" in os.environ and "AWS_SECRET_KEY" in os.environ:
            secret_key, access_key = os.environ['AWS_SECRET_KEY'], os.environ['AWS_ACCESS_KEY']
        else:
            parser.error("options --access-key and --secret-key are mandatory")
    else:
        access_key, secret_key = opts.accesskey, opts.secretkey

    if not opts.bucket:
        parser.error("option --bucket is mandatory")
    
    connection = S3Connection(access_key, secret_key)
    bucket = None
    
    try:
        bucket = connection.get_bucket(opts.bucket)
    except S3ResponseError as e:
        if e.error_code == 'NoSuchBucket' and e.status == 404:
            if opts.create:
                bucket = connection.create_bucket(opts.bucket)

    if len(args) == 0:
        parser.print_help()
        sys.exit(-1)
    
    for file in args:
        file_path = os.path.join(os.path.abspath("."), file)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            current_sum = sha1_sum(file_path)
            remote_keyname = os.path.join(opts.prefix, os.path.basename(file))

            if opts.diferential:
                keyobj = bucket.get_key(remote_keyname)
                if keyobj:
                    remote_sum = keyobj.get_metadata("sha1sum")
                    if remote_sum == current_sum:
                        sys.stderr.write("DIFERENTIAL PUT %s file exists and checksum match ok, (skiping)\n" % (file_path))
                        sys.stderr.flush()
                        continue
                else:
                    keyobj = Key(bucket, name=remote_keyname)

                keyobj.set_metadata('sha1sum', current_sum)
                keyobj.set_contents_from_filename(file_path, replace=True)
                sys.stderr.write("DIFERENTIAL PUT %s\n" % (file_path))

            else:
                keyobj = Key(bucket, name=remote_keyname)
                keyobj.set_metadata('sha1sum', current_sum)
                keyobj.set_contents_from_filename(file_path, replace=opts.overwrite)
                sys.stderr.write("PUT %s\n" % (file_path))

        else:
            sys.stderr.write("ERR %s: is not a file.\n" % (file_path))

        sys.stderr.flush()

    sys.exit(0)
