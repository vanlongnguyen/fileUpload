# upload_file
1. git clone git@github.com:vanlongnguyen/upload_file.git
2. sudo pip3 install virtualenv
3. cd /upload_file
3. source bin/activate
4. run python.main.py

#end points

1. Upload files
	http://localhost:5000/uploader
	Images are uploaded in assests folder
2. Generate thumbnails from uploaded images
	http://localhost:5000/generate-thumbnails
	Images are generated to thumbnails_generated folder