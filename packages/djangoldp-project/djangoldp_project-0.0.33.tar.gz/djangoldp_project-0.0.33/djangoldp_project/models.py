from django.conf import settings
from django.db import models

from djangoldp.models import Model


class Customer(Model):
    name = models.CharField(max_length=255, default='')
    address = models.CharField(max_length=255, default='')
    logo = models.URLField()
    companyRegister = models.CharField(default='', max_length=255)
    firstName = models.CharField(default='', max_length=255)
    lastName = models.CharField(default='', max_length=255)
    role = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(default='')
    phone = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class BusinessProvider(Model):
    name = models.CharField(max_length=255, default='')
    fee = models.PositiveIntegerField(default='0')

    def __str__(self):
        return self.name


class Project(Model):
    name = models.CharField(max_length=255, default='')
    description = models.CharField(max_length=255, default='')
    number = models.PositiveIntegerField(default='0', blank=True)
    creationDate = models.DateField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)  # WARN add import
    team = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Member', blank=True)
    businessProvider = models.ForeignKey(BusinessProvider, blank=True, null=True, on_delete=models.DO_NOTHING)
    jabberID = models.CharField(max_length=255, blank=True, null=True)
    jabberRoom = models.BooleanField(default=True)

    class Meta:
        nested_fields = ['team', 'customer', 'members']
        default_permissions = ('add', 'change', 'delete', 'view', 'control')
        rdf_type = 'hd:project'
        depth = 0

    def __str__(self):
        return self.name


class Member(Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


Member._meta.container_path = "project-members/"
