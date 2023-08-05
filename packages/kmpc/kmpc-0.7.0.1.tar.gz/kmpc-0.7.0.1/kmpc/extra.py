import os
import errno
import io
import pycountry
from PIL import Image as PImage

from twisted.internet.defer import Deferred, DeferredList


class KmpcHelpers(object):

    def formatsong(self, rec):
        """Method used by library browser to properly format a song row."""
        song = ''
        # check if there is more than one disc and display if so
        dd = rec['disc'].split('/')
        if len(dd) > 1:
            if int(dd[1]) > 1:
                song += '(Disc ' + '%02d' % int(dd[0]) + ') '
        # sometimes track numbers are like '01/05' (one of five), so drop that
        # second number
        tt = rec['track'].split('/')
        song += '%02d' % int(tt[0]) + ' '
        # if albumartist is different than track artist, display the track
        # artist
        if rec['artist'] != rec['albumartist']:
            song += rec['artist'] + ' - '
        # display the track title
        song += rec['title']
        return song

    def decodeFileName(self, name):
        """Method that tries to intelligently decode a filename to handle
        unicode weirdness."""
        if type(name) == str:
            try:
                name = name.decode('utf8')
            except Exception:
                name = name.decode('windows-1252')
        return name

    def removeEmptyFolders(self, path, removeRoot=True):
        """Function to remove empty folders"""
        if not os.path.isdir(path):
            return
        # remove empty subfolders
        files = os.listdir(path)
        if len(files):
            for f in files:
                fullpath = os.path.join(path, f)
                if os.path.isdir(fullpath):
                    self.removeEmptyFolders(fullpath)
        # if folder empty, delete it
        files = os.listdir(path)
        if len(files) == 0 and removeRoot:
            os.rmdir(path)

    def upath(self, uuid):
        """Function to expand uuid to full cache path."""
	p1 = uuid[0:2]
	p2 = uuid[2:4]
	p3 = uuid[4:6]
	p4 = uuid[6:8]
	return os.path.join(p1,p2,p3,p4,uuid)
    
    def expath(self, cachepath, uuid, idtype):
        return os.path.join(cachepath,idtype,self.upath(uuid))

    def jpath(self, cachepath, uuid, idtype):
        return os.path.join(self.expath(cachepath, uuid, idtype),uuid+'.json')

    def artexpath(self, uuid, cachepath, arttype):
        return os.path.join(cachepath,'artist',self.upath(uuid),arttype)

    def country(self, code):
        if code == 'XW':
            return "worldwide"
        elif code == 'XE':
            return "across Europe"
        else:
            c=pycountry.countries.get(alpha_2=code)
            if c.name:
                return "in "+c.name
            else:
                return "in "+code
                
    def mkdir_p(self, path):
        try:
            os.makedirs(path)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise
    
    def trim_image(self, filename):
        image = PImage.open(filename)
        try:
            # convert to RGBa before getting bounding box to account for
            # transparent pixels
            bbox = image.convert("RGBa").getbbox()
        except ValueError:
            # if grayscale, do some fancy compositing
            oimage = image.convert('RGBA')
            bimage = PImage.new('RGBA',image.size)
            bbox = PImage.composite(oimage,bimage,oimage).getbbox()
        # crop it and save
        image = image.crop(bbox)
        image.save(filename)
