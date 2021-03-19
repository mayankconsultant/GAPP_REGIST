from django.db import models

from PIL import Image

from django_countries.fields import CountryField

from .utils import image_resize


# Create your models here.


def customer_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'media/cust_{0}/{1}'.format(instance.MOBILE_NUMBER, filename)


class states(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        # return str(self.name).upper()
        return self.name

    # def __unicode__(self):
    #         return str(self.name).upper()


class county(models.Model):
    name = models.CharField(max_length=100)
    states = models.ForeignKey(states, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class payam(models.Model):
    name = models.CharField(max_length=100)
    county = models.ForeignKey(county, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Gender(models.TextChoices):
    MALE = ("MALE", "MALE")
    FEMALE = ("FEMALE", "FEMALE")


class CUSTOMER(models.Model):
    ID_TYPES = (
        ("1", "Work ID"),
        ("2", "Student ID"),
        ("3", 'UN ID'),
        ("4", 'Military,Polica,SPLM'),
        ("5", 'Tribal Chiefs Cert.'),
        ("6", 'National ID'),
        ("7", 'Passport'),
        ("8", 'Voting Card'),
        ("9", 'Driving License')
    )
    """Model definition for CUSTOMER."""

    # TODO: Define fields here
    MOBILE_NUMBER = models.CharField(max_length=12)
    FIRST_NAME = models.CharField(max_length=30)
    SECOND_NAME = models.CharField(max_length=30, blank=True, null=True)
    THIRD_NAME = models.CharField(max_length=30, blank=True, null=True)
    LAST_NAME = models.CharField(max_length=30, verbose_name='Surname')
    ID_TYPE = models.CharField(max_length=30, choices=ID_TYPES)
    ID_NUMBER = models.CharField(max_length=15)
    gender = models.CharField(
        max_length=10, choices=Gender.choices, default=Gender.MALE
    )
    DOB = models.DateField(blank=True, null=True, verbose_name="Date Of Birth")
    COUNTRY = CountryField()
    ADDRESS = models.CharField(max_length=50, blank=True, null=True,
                               )
    STATE = models.ForeignKey(states, on_delete=models.DO_NOTHING)
    CITY = models.CharField(max_length=100)
    COUNTY = models.ForeignKey(county, on_delete=models.DO_NOTHING)
    PAYAM = models.ForeignKey(payam, on_delete=models.DO_NOTHING)
    BOMA = models.CharField(max_length=50, blank=True, null=True)
    ID_PROOF = models.ImageField(upload_to=customer_directory_path, verbose_name='ID PROOF FILE')
    CREATED_DATE = models.DateField(auto_now_add=True)

    class Meta:
        """Meta definition for CUSTOMER."""

        verbose_name = "CUSTOMER"
        verbose_name_plural = "CUSTOMERS"

    def __str__(self):
        """Unicode representation of CUSTOMER."""
        return self.MOBILE_NUMBER + " " + str(self.FIRST_NAME).upper() + " " + str(self.LAST_NAME).upper()

    def save(self, *args, **kwargs):
        from django.core.files.storage import DefaultStorage as storage
        image_resize(self.ID_PROOF, 512, 512)
        super(CUSTOMER, self).save(*args, **kwargs)
        # print( 'Saving Image HAhaha')
        # img = Image.open(CUSTOMER.ID_PROOF)

        # if img.height > 300 or img.width > 300:
        #     output_size = (300, 300)
        #     img.thumbnail(output_size)
        #     # img.save(CUSTOMER.ID_PROOF.path)
        #
        # fh = storage.open(CUSTOMER.ID_PROOF.name, "w")
        # picture_format = 'png'
        # img.save(fh, picture_format)
        # fh.close()
