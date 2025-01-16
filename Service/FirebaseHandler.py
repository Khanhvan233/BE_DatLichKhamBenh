import firebase_admin
from firebase_admin import credentials, storage
import os

rootDirectory = os.path.dirname(os.path.abspath(__file__))
while not os.path.exists(os.path.join(rootDirectory, 'Service')):
    rootDirectory = os.path.dirname(rootDirectory)

class FirebaseHandler:
    def __init__(self):
        self.databaseURL = "banrem-efaac.appspot.com"
        self.cred = credentials.Certificate(rootDirectory + "/Resource/serviceAccountKey.json")

        # Kiểm tra nếu ứng dụng Firebase đã được khởi tạo
        if not firebase_admin._apps:
            # Nếu chưa khởi tạo, khởi tạo Firebase App với tên ứng dụng tùy chọn
            self.app = firebase_admin.initialize_app(self.cred, {'storageBucket': self.databaseURL})
        else:
            # Nếu đã khởi tạo, lấy ứng dụng hiện tại
            self.app = firebase_admin.get_app()

        self.bucket = storage.bucket(app=self.app)

    def updateImagePublic(self, pathBlog, imageByte, contentType):
        blob = self.bucket.blob(pathBlog)
        blob.upload_from_string(imageByte, content_type=contentType)
        blob.make_public()
        return blob.public_url

    def updateVideoPublic(self, pathBlog, videoByte, contentType):
        blob = self.bucket.blob(pathBlog)
        blob.upload_from_string(videoByte, content_type=contentType)
        blob.make_public()
        return blob.public_url

    def updateImagePrivate(self, pathBlog, imageByte, contentType):
        blob = self.bucket.blob(pathBlog)
        blob.upload_from_string(imageByte, content_type=contentType)

    def updateVideoPrivate(self, pathBlog, videoByte, contentType):
        blob = self.bucket.blob(pathBlog)
        blob.upload_from_string(videoByte, content_type=contentType)

    def deleteBlog(self, pathBlog):
        try:
            blob = self.bucket.blob(pathBlog)
            blob.delete()
            return True
        except Exception as e:
            return False

    def makeBlobPrivate(self, pathBlog):
        blob = self.bucket.blob(pathBlog)
        blob.acl.all().revoke_read()
        blob.acl.save(client=blob.client)

    def makeBlobPublic(self, pathBlog):
        blob = self.bucket.blob(pathBlog)
        blob.make_public()
        return blob.public_url

    def generateSignedUrl(self, blobName, time=2):
        expiration = timedelta(minutes=time)
        bucket = storage.bucket()
        blob = bucket.blob(blobName)
        signed_url = blob.generate_signed_url(expiration=expiration, version='v4')
        return signed_url
