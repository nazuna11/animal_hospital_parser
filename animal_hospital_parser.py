import requests
from bs4 import BeautifulSoup
import bs4
import re

class Hospital:
    def __init__(self, name, url, infos):
        self.name=name
        self.url=url
        self.infos=infos
        self.address=None
        self.phone_number=None
        self.lon=None
        self.lat=None
        self.parent_url="https://www.jarmec.co.jp"
        self.hospital_url=None
        self.parseInfo()
        self.setMembers()

    def parseInfo(self):
        if len(self.infos) == 2:
            self.address=self.infos[0][3:]
            self.phone_number=self.infos[1][5:]

        if len(self.infos) == 1:
            info_type_str = self.parseInfoType(self.infos[0])
            if info_type_str == "adderss":
                self.address=self.infos[0][3:]
            elif info_type_str == "phone_number":
                self.phone_number=self.infos[0][5:]
            else:
                pass

    def parseInfoType(self, info):
        if re.match(r"住所", info):
            return "adderss"
        elif re.match(r"電話番号", info):
            return "phone_number"
        else:
            return None

    def addLonlat(self, infodata):
        # hospital_detail_info = requests.get(self.parent_url+self.url)
        hospital_detail_info = infodata
        latlon_str = re.search(r"position: new google\.maps.LatLng\(\d.*\.\d.*, \d.*\.\d.*\)", hospital_detail_info.text)[0]
        latlon_list = list(map(lambda s: float(s), latlon_str.replace("position: new google.maps.LatLng(", "").replace(")", "").split(",")))
        self.lat=latlon_list[0]
        self.lon=latlon_list[1]

    def addHospitalUrl(self, infodata):
        hospital_detail_info = infodata
        reg_homepage=r'<h4>ホームページ</h4><p><a rel="nofollow" href=.*target='
        reg_url=r"https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
        result = re.search(reg_homepage, hospital_detail_info.text)
        if result:
            h_url = re.search(reg_url, result[0])
            if h_url:
                self.hospital_url=h_url[0]

    def getHospitalDetailInfo(self):
        hospital_detail_info = requests.get(self.parent_url+self.url)
        return hospital_detail_info

    def setMembers(self):
        infodata = self.getHospitalDetailInfo()
        self.addHospitalUrl(infodata)
        self.addLonlat(infodata)

    def getValue(self):
        return (self.name,self.url,self.address,self.phone_number, self.lon, self.lat, self.hospital_url)


def get_hospitals(hospital_url):
    hospitals = []
    get_url_info = requests.get(hospital_url)
    bs = BeautifulSoup(get_url_info.text, 'lxml')
    for kenindex in bs.find_all(class_="kenindex"):
        url = kenindex.find("a")["href"]
        name = kenindex.find("a").contents[0].replace("\u3000", " ")
        infos = list(filter(lambda i: isinstance(i, bs4.element.NavigableString), kenindex.find("p").contents))
        hospital = Hospital(name, url, infos)
        hospitals.append(hospital)

    return hospitals

def makeCsv(fname, data):
    with open(fname, 'w') as f:
        for row in data:
            print(*row, sep=',', file=f)



parent_url = "https://www.jarmec.co.jp"
area_url = parent_url+"/hospital/area_03.html"
hospital_url=parent_url+"/hospital/hospital_346.html"
hospital_detail_url=parent_url+"/hospital/detail_285/2026.html"
fname='animal_hospital.csv'


get_url_info = requests.get(area_url)

html_lines = get_url_info.text.split("\n")

line_reg = r'<li><a href="/hospital/hospital_\d{1,4}.html">.*</a></li>'

results = filter(lambda line: re.match(line_reg, line), html_lines)
for result in results:
    html_reg=r"/hospital/hospital_\d{1,4}.html"
    area_reg=r'">.*</a>'
    url = re.findall(html_reg, result)[0]
    hospital_url=parent_url+url
    area_name = re.findall(area_reg, result)[0]
    area = area_name[2:].replace("</a>", "")
    hospitals = get_hospitals(hospital_url)
    [print(hospital.getValue()) for hospital in hospitals]
