from django.db import models

# Create your models here.

class Machine(models.Model):
    machine_name = models.CharField('Hostname', max_length=200)
    machine_address = models.CharField('Adress', max_length=200)
    machine_port = models.IntegerField('Port')
    machine_http_username = models.CharField('Username', max_length=200,
            default=None, null=True, blank=True)
    machine_http_password = models.CharField('Password', max_length=200,
            default=None, null=True, blank=True)

    class Meta:
        ordering = ['machine_name', 'machine_address']

    def __str__(self):
        return self.machine_name
