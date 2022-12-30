from django.db import models


### Güvenlik açıklarının bilgilerini tutacağımız Database modeli
### Güvenlik açıklarının bilgilerini çektiğimiz sayfadan çektiğimiz bilgileri bu modelde tutuyoruz
class Vulnerability(models.Model):
    name = models.CharField(max_length=150)
    tenable_id = models.IntegerField(default=0)
    severity = models.IntegerField(default=0)
    description = models.CharField(max_length=5000)
    solution = models.CharField(max_length=1000)
    cvs_tempscore = models.DecimalField(max_digits=3, decimal_places=1)
    date = models.DateField()



