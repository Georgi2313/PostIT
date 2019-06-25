from django.db import models
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

class Posts(models.Model):
    author = models.CharField(max_length=50)
    pic = models.ImageField(upload_to='images/', blank=True, null=True) 

    title = models.CharField(max_length=50)
    body = models.TextField()
    #picture
    created_date = models.DateTimeField(default=timezone.now)
    post_date = models.DateTimeField()

    def __str__(self):
        return self.title     

    def save(self, *args, **kwargs):
        if self.pic:
            if not self.id:
                self.pic = self.compressImage(self.pic)
        super(Posts, self).save(*args, **kwargs)

    def compressImage(self,uploadedImage):
        imageTemproary = Image.open(uploadedImage)
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize( (1020,573) ) 
        imageTemproary.save(outputIoStream , format='JPEG', quality=60)
        outputIoStream.seek(0)
        pic = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % uploadedImage.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return pic