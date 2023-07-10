import json
import random
from hashlib import sha256

from django.db import models

# Create your models here.


class System(models.Model):
    """
    A System is a single computer running the boop-boop client.
    """
    properties = models.JSONField()
    secret = models.CharField(max_length=10)

    def get_auth_code(self, properties):
        """
        Get the auth code for a given set of properties.
        """
        return self.secret + sha256(json.dumps(sorted(properties['system'].items())).encode('utf-8')).hexdigest()

    def verify_auth_code(self, code, properties):
        """
        Verify that the given auth code is valid.
        """
        print(sorted(properties['system'].items()))
        print(sorted(self.properties['system'].items()))
        print(code, self.get_auth_code(self.properties))
        return properties == self.properties and code == self.get_auth_code(self.properties)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        """
        Override the save method to generate a secret if one does not exist.
        """
        if self.secret == '':
            self.secret = str(random.randint(1000000000, 9999999999))
        super().save(force_insert, force_update, using, update_fields)


class Report(models.Model):
    """
    A Report is a single report from a single system.

    It will contain the coordinates of their clicking action and a base64-encoded image from their webcam.
    """
    time_created = models.DateTimeField(auto_now_add=True)
    system = models.ForeignKey(System, on_delete=models.DO_NOTHING, related_name='reports')
    click_data = models.JSONField()
    image = models.FileField()
