from django.db import models
from user.models import User
# Create your models here.
class Post(models.Model):
    class Meta:
        db_table = 'post'
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, null=False)
    postdate = models.DateTimeField(null=False)
    auther = models.ForeignKey(User)

    def __repr__(self):
        return "<{} {} <<{}>> <{}>>".format(self.id, self.title, self.auther.name,self.content)

    __str__ = __repr__

class Content(models.Model):
    class Meta:
        db_table = 'content'

    id = models.AutoField(primary_key=True)
    post = models.OneToOneField(Post,to_field='id')
    content = models.TextField(null=False)

    def __repr__(self):
        return '<{} {}>'.format(self.id, self.content[:10])

    __str__ = __repr__