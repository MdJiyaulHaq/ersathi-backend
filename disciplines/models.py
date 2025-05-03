from django.db import models
from django.utils.translation import gettext_lazy as _


# disciplines models
# Create your models here.
class Discipline(models.Model):
    class DisciplineChoices(models.TextChoices):
        CIVIL = "CIVIL", _("Civil Engineering")
        COMPUTER = "COMP", _("Computer Engineering")
        SOFTWARE = "BSE", _("Software Engineering")
        EEE = "EEE", _("Electrical and Electronics Engineering")
        CHEMICAL = "CHEM", _("Chemical Engineering")
        ELECTRICAL = "ELEC", _("Electrical Engineering")
        ECE = "ECE", _("Electronics and Communication Engineering")
        CIVIL_RURAL = "CIVR", _("Civil and Rural Engineering")
        ARCHITECTURE = "ARCH", _("Architecture Engineering")
        AUTOMOBILE = "AUTO", _("Automobile Engineering")
        ELECTRONICS = "ELEN", _("Electronics Engineering")
        MECHANICAL = "MECH", _("Mechanical Engineering")
        AEROSPACE = "AERO", _("Aerospace Engineering")
        AGRICULTURAL = "AGRI", _("Agricultural Engineering")

    name = models.CharField(
        max_length=10,
        choices=DisciplineChoices.choices,
        unique=True
    )
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.get_name_display()
