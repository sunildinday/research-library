from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
# from user.forms import UserRegistrationForm
# Create your models here.


# Create your models here.


# # class DocumentQuerySet(models.query.QuerySet):

#     def get_by_title_and_id(self, query, user_id):
#         return self.filter(Q(title__icontains=query) & Q(user_id__icontains=user_id))


# class DocumentManager(models.Manager):

# 	def get_queryset(self):
# 		return DocumentQuerySet(self.model, using=self._db)

#     def get_by_title_and_id(self, query, user_id):
#         return self.get_queryset().filter(Q(title__icontains=query) & Q(user_id__icontains=user_id))


class Documents(models.Model):

    def validate_file_extension(value):
        import os
        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.pdf', '.doc', '.docx']
        if not ext in valid_extensions:
            raise ValidationError(u'File not supported!')
    user_id = models.IntegerField(null=False, default=1)
    title = models.CharField(max_length=255, blank=False,)
    abstract = models.TextField(max_length=500, blank=True)
    document = models.FileField(upload_to='document')
    downloads = models.IntegerField(default=0)
    created_on = models.DateField(auto_now=True)
    publisher = models.CharField(max_length=300, blank=True)
    CSE = 'Computer Science and Engineering'
    ECE = 'Electronic and Communincation'
    EEE = 'Electrical and Electronic Engineering'
    ME = 'Mechanical Engineering'
    CE = 'Civil Engineering'
    branchs = (
        (CSE, 'Computer Science and Engineering'),
        (ECE, 'Electronic and Communincation'),
        (EEE, 'Electrical and Electronic Engineering'),
        (ME, 'Mechanical Engineering'),
        (CE, 'Civil Engineering'),
    )
    branch = models.CharField(choices=branchs, default=CSE, max_length=200)
    pr = 'PRIVATE'
    pu = 'PUBLIC'
    visible = (
        (pr, 'PRIVATE'),
        (pu, 'PUBLIC'),
    )

    visibilty = models.CharField(choices=visible, default=pu, max_length=200)
    folder_label = models.CharField(max_length=20, default='None')
    # objects = DocumentManager()


class Folder(models.Model):
    label = models.CharField(max_length=20)
    user_id = models.IntegerField(null=False)

    def __unicode__(self):
        self.label


class Authors(models.Model):
    author = models.CharField(max_length=150, blank=False, null=False)
    document = models.ForeignKey(Documents, on_delete=models.CASCADE)

    def __unicode__(self):
        self.author


class KeyWord(models.Model):
    key = models.CharField(max_length=30, null=False, blank=False, default='')
    document = models.ForeignKey(Documents, on_delete=models.CASCADE, null=True)
