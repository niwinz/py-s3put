Usage guide.
============

To upload files to amazon s3 need these keys: AWS_ACCESS_KEY and AWS_SECRET_KEY.

Which we can defend as parameters of the environment or passed as arguments to the script. See examples below.

For those who are already familiar with Amazon S3, I would be very easy to use script.

Environment Variables.
^^^^^^^^^^^^^^^^^^^^^^

.. program:: s3put.py file1 file2 file3

.. envvar:: AWS_ACCESS_KEY
   
   You specify the amazon access key.

.. envvar:: AWS_SECRET_KEY
   
   You specify the amazon secret key.



Parameters.
^^^^^^^^^^^

.. option:: --prefix <string>
    
   You specify the remote directory.

.. option:: --overwrite

   Tells the script if you want to overwrite the files if these exist.

.. option:: --bucket <string>

   You specify the name of the bucket you want to use.

.. option:: -diferential

   Makes just upload modified files.

.. option:: --access-key <string>

   Set amazon access key. Only if you not have environ vars.

.. option:: --secret-key <string>
   
   Set amazon secret key. Only if you not have environ vars.


Usage example.
^^^^^^^^^^^^^^

This is an simple example of use::
    
    s3put.py --prefix=foodirbackup \
        --access-key=ACCESSKEY \
        --secret-key=SECRETKEY \
        --bucket="bucket-name" \
        --overwirte /home/user/foo.tar.bz2


