from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from .models import Vulnerability
from datetime import datetime as dt
from bs4 import BeautifulSoup
import requests
from collections import Counter
from django.core.mail import BadHeaderError, send_mail




### Tüm güvenlik açıklarını gösteriyoruz
### Güvenlik açıkları istenilen sıralamada gösteriliyor
def index(request,order=""):
    
    if order == "":
        vuls = Vulnerability.objects.all()
        return render(request,"sec_app/index.html",{"vuls":vuls})
    elif order == "name":
        vuls = Vulnerability.objects.order_by("name")
        return render(request,"sec_app/index.html",{"vuls":vuls})
    elif order == "severity":
        vuls = Vulnerability.objects.order_by("-severity")
        return render(request,"sec_app/index.html",{"vuls":vuls})
    elif order == "date":
        vuls = Vulnerability.objects.order_by("-date")
        return render(request,"sec_app/index.html",{"vuls":vuls})
    elif order == "base_score":
        vuls = Vulnerability.objects.order_by("-cvs_tempscore")
        return render(request,"sec_app/index.html",{"vuls":vuls})
    else:
        vuls = Vulnerability.objects.all()
        return render(request,"sec_app/index.html",{"vuls":vuls})
        


### Tıklanan  güvenlik açıklarının detaylarını gösteriyoruz
def vuln_detail(request,id):
    vul = Vulnerability.objects.get(tenable_id=id)
    return render(request,"sec_app/vuln_detail.html",{"vul":vul})



### Microsoft ile ilgili tüm güvenlik açıklarını çekiyoruz anahtar kelime ile arama yapıyoruz
### Çıkan sonuçlara göre ilk 15 sayfadaki her bir zaafiyetin sayfasına girip bilgilerini çekiyoruz
### Çektiğimiz bilgileri veritabanına kaydediyoruz

words = ["microsoft","windows"]
def get_vulns(request):
    ### Kaç sayfada arama yapılacak
    baslangic_sayfasi = 1
    aranacak_sayfa_sayisi = 10
    while baslangic_sayfasi < aranacak_sayfa_sayisi:
        print(f"------------Sayfa: {baslangic_sayfasi}-------------")
        ### urldeki microsoft kelimesi yerine ne yazarsak o keyword ile arama yapar
        url = f"https://www.tenable.com/plugins/search?q={words[0]}+{words[1]}&sort=&page={baslangic_sayfasi}"

        r = requests.get(url)

        ### html kodlarını çekiyoruz
        soup = BeautifulSoup(r.text, 'lxml')

        ### Zaafiyetlerin linklerini çekiyoruz
        links = soup.find_all("a", {"class": "no-break"})
        for link in links:
            url2 = link.get('href')
            r2 = requests.get(url2)
            soup2 = BeautifulSoup(r2.text, 'lxml')

            id = 0
            name = ""
            desc = ""
            sol = ""
            base_score = 0.0
            date = ""
            
            ### Zaafların id bilgisini çekiyoruz
            try:
                id = soup2.find(text="ID").parent.nextSibling.text
            except Exception as e:
                id = 0

            ### Zaafların isim bilgisini çekiyoruz
            try:
                name = soup2.find("h1",{"class":"h2"}).text
            except Exception as e:
                name = "None"
            
            ### Zaafların açıklamasını çekiyoruz
            try:
                
                syn = soup2.find(text="Description").parent.find_next_siblings("span")
                for i in range(len(syn)):
                    desc += syn[i].text
            except Exception as e:
                desc = "None"
            
            ### Zaafların çözümünü çekiyoruz
            try:
                
                solut = soup2.find(text="Solution").parent.find_next_siblings("span")
                for i in range(len(solut)):
                    sol += solut[i].text
            except Exception as e:
                sol = "None"

            ### Zaafların base score bilgisini çekiyoruz
            try:
                base_score = float(soup2.find(text="Base Score").parent.nextSibling.text)
            except Exception as e:
                base_score = 0.0

            ### Zaafların yayınlanma tarihini çekiyoruz
            try:
                date = soup2.find(text="Published").parent.nextSibling.text
            except:
                date = "1/12/1900"
            

            ### Zaafların risk seviyesini belirliyoruz
            ### Bu belirleme CVS3 e göre yapılmıştır
            if base_score >= 0.1 and base_score <= 3.9:
                severity = 1
            elif base_score > 3.9 and base_score <= 6.9:
                severity = 2
            elif base_score > 6.9 and base_score <= 8.9:
                severity = 3
            elif base_score > 8.9 and base_score <= 10:
                ### Zaaf kritikse mail gönderiyoruz
                ### Bu işlem veri çekme hızını önemli ölçüde azaltabiliyor
                # send_mail("Kritik Zaaf",f"ID:{id}\nName: {name}\nDescription: {desc}","noreply@gmail.com",["coworkers@gmail.com"])
                severity = 4
            else:
                severity = 0
            
            print("Satır Kaydedildi")
            vul = Vulnerability(tenable_id=id,name=name,description=desc,solution=sol,cvs_tempscore=base_score,severity=severity,date=dt.strptime(date, "%m/%d/%Y"))
            vul.save()
        baslangic_sayfasi += 1
    return redirect("index")

### Databasedeki tüm verileri sıfırlıyoruz
def delete_vulns(request):
    Vulnerability.objects.all().delete()
    return redirect("index")

### Grafikler için verileri çekiyoruz
def vulnerabilites_years(request):
    vuls = Vulnerability.objects.all()
    years = []
    for vul in vuls:
        years.append(vul.date.year)
    years = list(years)
    c = Counter(years)
    graph1_data = dict(c)

    ### Tüm yıllar için
    vuls_all = Vulnerability.objects.all()
    risks2 = []
    for vul in vuls_all:
        risks2.append(vul.severity)
    risks2 = list(risks2)
    c2 = Counter(risks2)
    graph2_data = dict(c2)
    

    ### 2022 yılı için
    vuls_2022 = Vulnerability.objects.filter(date__year=2022)
    risks = []
    for vul in vuls_2022:
        risks.append(vul.severity)
    risks = list(risks)
    c3= Counter(risks)
    graph3_data = dict(c3)

    dict1 = {"graph1_data":graph1_data,"graph2_data":graph2_data,"graph3_data":graph3_data}
   
    return JsonResponse(dict1)


