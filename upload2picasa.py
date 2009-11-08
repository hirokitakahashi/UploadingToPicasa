import gdata.photos.service
import time

def Login(gmailaddr, passwd):
	gd_client = gdata.photos.service.PhotosService()
	gd_client.email = gmailaddr
	gd_client.password = passwd
	gd_client.ProgrammaticLogin()
	return gd_client

def SearchPhoto(obj, username, albumname, photoname):
	''' obj = Photo service object
		username = user name
	    albumname = album name
		photoname = photo name'''
	albums = obj.GetUserFeed()
	# Search for the album
	for album in albums.entry:
		t = album.title.text
		if t == albumname:
			print 'album title: %s, number of photos: %s, id: %s' % (t, 
			album.numphotos.text, album.gphoto_id.text)
			break
		else:
			album = None
	
	if album == None:
		return (None, None)
	
	# Search for the photo
	photos = obj.GetFeed('/data/feed/api/user/%s/albumid/%s?kind=photo' % (username, album.gphoto_id.text))
	for photo in photos.entry:
		t = photo.title.text
		if t == photoname:
			print 'photo title: %s, photo id: %s' % (photo.title.text, photo.gphoto_id.text)
			break
		else:
			photo = None
	
	return (album, photo)

def UpdatePhoto(obj, pobj, filename, comment=None):
	''' obj = Photo service object
	    pobj = photo entry object
		filename = path to the file to upload
		comment = comment for the photo'''
	# Update the photo entry
	photo = obj.UpdatePhotoBlob(pobj, filename)
	if comment:
		photo.summary.text = comment
		photo = obj.UpdatePhotoMetadata(photo)
	print 'photo %s updated' % photo.title.text
	return photo

def UploadPhoto(obj, username, albumname, photoname, filename, comment=None):
	album, photo = SearchPhoto(obj, username, albumname, photoname)
	if album == None:
		print 'album not found'
		return None
	
	if photo:
		photo = UpdatePhoto(obj, photo, filename, comment)
	else:
		photo = obj.InsertPhotoSimple(album, photoname, comment, filename)
		print 'photo %s inserted' % photo.title.text
	return photo

if __name__ == "__main__":
	username = 'itcqsussex'
	gmailaddr = 'itcqsussex@gmail.com'
	googlepasswd = '40calcium40ions'
	album_name = 'Endcap trap baking'
	#photo_name = 'Temperature log'
	photo_name = 'Test'
	figfile = 'temp2.png'
	
	gd = Login(gmailaddr, googlepasswd)
	comment = 'Uploaded on %s' % time.strftime('%d/%m/%Y %H:%M:%S')
	UploadPhoto(gd, username, album_name, photo_name, figfile, comment)
	# album, photo = SearchPhoto(gd, album_name, photo_name)
	# if photo:
		# comment = 'Uploaded on %s' % time.strftime('%d/%m/%Y %H:%M:%S')
		# UpdatePhoto(gd, photo, figfile, comment)