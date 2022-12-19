import pathlib
import os
import time
import requests
from database import record_product, create_table, create_photos_dir
import shutil
import json


languages = ["de", "fr", "it"]
categories_url = {
    "Computer & Gaming": {"Notebooks": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F500%3AcategoryPath%3A%2F1%2F500%2F5100&lang={language}",
                          "Peripherie": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F500%3AcategoryPath%3A%2F1%2F500%2F5500&lang{language}",
                          "Druckerpatronen & Toner": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F500%3AcategoryPath%3A%2F1%2F500%2F5400&lang{language}",
                          "Kabel": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F500%3AcategoryPath%3A%2F1%2F500%2F5200&lang{language}",
                          "Smart Home & Netzwerk": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F500%3AcategoryPath%3A%2F1%2F500%2F5700&lang{language}",
                          "Gaming": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F500%3AcategoryPath%3A%2F1%2F500%2F2100&lang{language}",
                          "PC Komponenten": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F500%3AcategoryPath%3A%2F1%2F500%2F5800&lang{language}",
                          "Drucker & Scanner": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F500%3AcategoryPath%3A%2F1%2F500%2F5300&lang{language}",
                          "PCs & Monitore": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F500%3AcategoryPath%3A%2F1%2F500%2F5900&lang{language}",
                          "Speicher & Laufwerke": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F500%3AcategoryPath%3A%2F1%2F500%2F5600&lang{language}",
                          "Software": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F500%3AcategoryPath%3A%2F1%2F500%2F5110&lang{language}"},
    "Mobiltelefon, Tablet & Smartwatch": {"Mobiltelefon": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F400%3AcategoryPath%3A%2F1%2F400%2F4100&lang={language}",
                                          "Smartwatch": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F400%3AcategoryPath%3A%2F1%2F400%2F4300&lang={language}",
                                          "Tablet & Ebook": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F400%3AcategoryPath%3A%2F1%2F400%2F4110&lang={language}",
                                          "Navigation": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F400%3AcategoryPath%3A%2F1%2F400%2F4400&lang={language}",
                                          "Telefongeräte": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F400%3AcategoryPath%3A%2F1%2F400%2F4200&lang={language}",
                                          "Funktechnik": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F400%3AcategoryPath%3A%2F1%2F400%2F4210&lang={language}",
                                          "Geschenk- & Wertkarten": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F400%3AcategoryPath%3A%2F1%2F400%2F1000&lang={language}"},
    "TV & Audio": {"Filme": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F100%3AcategoryPath%3A%2F1%2F100%2F1400&lang={language}",
                   "Kopfhörer": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F100%3AcategoryPath%3A%2F1%2F100%2F1800&lang={language}",
                   "Kabel & Adapter": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F100%3AcategoryPath%3A%2F1%2F100%2F1910&lang={language}",
                   "Fernseher": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F100%3AcategoryPath%3A%2F1%2F100%2F1100&lang={language}",
                   "HiFi": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F100%3AcategoryPath%3A%2F1%2F100%2F1600&lang={language}",
                   "DJ & Studio Equipment": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F100%3AcategoryPath%3A%2F1%2F100%2F1620&lang={language}",
                   "Beamer & Leinwände": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F100%3AcategoryPath%3A%2F1%2F100%2F1200&lang={language}",
                   "Multiroom & Bluetooth": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F100%3AcategoryPath%3A%2F1%2F100%2F1900&lang={language}",
                   "Heimkino & Video": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F100%3AcategoryPath%3A%2F1%2F100%2F1500&lang={language}",
                   "Empfangstechnik": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F100%3AcategoryPath%3A%2F1%2F100%2F1300&lang={language}",
                   "Car HiFi": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F100%3AcategoryPath%3A%2F1%2F100%2F1700&lang={language}",
                   "MP3 & Audiorecording": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F100%3AcategoryPath%3A%2F1%2F100%2F1610&lang={language}"},
    "Beauty, Gesundheit & Baby": {"Rasieren & Haarentfernung": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F910%3AcategoryPath%3A%2F1%2F910%2F6400&lang={language}",
                                  "Therapie & Massage": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F910%3AcategoryPath%3A%2F1%2F910%2F5190&lang={language}",
                                  "Zahnpflege": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F910%3AcategoryPath%3A%2F1%2F910%2F6900&lang={language}",
                                  "Haarpflege & Styling": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F910%3AcategoryPath%3A%2F1%2F910%2F6410&lang={language}",
                                  "Gesundheits Messgeräte": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F910%3AcategoryPath%3A%2F1%2F910%2F5210&lang={language}",
                                  "Baby": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F910%3AcategoryPath%3A%2F1%2F910%2F3580&lang={language}",
                                  "Körper & Gesichtspflege": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F910%3AcategoryPath%3A%2F1%2F910%2F9100&lang={language}",
                                  "Maniküre & Pediküre": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F910%3AcategoryPath%3A%2F1%2F910%2F9600&lang={language}",
                                  "Hausapotheke": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F910%3AcategoryPath%3A%2F1%2F910%2F5820&lang={language}"},
    "Foto & Video": {"Foto- & Videokamera Zubehör": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F300%3AcategoryPath%3A%2F1%2F300%2F3300&lang={language}",
                     "Objektive": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F300%3AcategoryPath%3A%2F1%2F300%2F3200&lang={language}",
                     "Stative & Beleuchtung": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F300%3AcategoryPath%3A%2F1%2F300%2F3260&lang={language}",
                     "Ferngläser & Teleskope": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F300%3AcategoryPath%3A%2F1%2F300%2F3400&lang={language}",
                     "Fotokamera": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F300%3AcategoryPath%3A%2F1%2F300%2F3100&lang={language}",
                     "Video & Actionkamera": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F300%3AcategoryPath%3A%2F1%2F300%2F3130&lang={language}"},
    "Haushalt & Küche": {"Haustechnik & Stromversorgung": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F600%3AcategoryPath%3A%2F1%2F600%2F6800&lang={language}",
                         "Küchengeräte": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F600%3AcategoryPath%3A%2F1%2F600%2F6200&lang={language}",
                         "Reinigen & Saugen": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F600%3AcategoryPath%3A%2F1%2F600%2F6100&lang={language}",
                         "Kaffee & Tee": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F600%3AcategoryPath%3A%2F1%2F600%2F6300&lang={language}",
                         "Raumklima": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F600%3AcategoryPath%3A%2F1%2F600%2F6500&lang={language}",
                         "Küchen-Grossgeräte": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F600%3AcategoryPath%3A%2F1%2F600%2F6600&lang={language}",
                         "Waschen & Bügeln": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F600%3AcategoryPath%3A%2F1%2F600%2F6700&lang={language}",
                         "Küchenmessgeräte": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F600%3AcategoryPath%3A%2F1%2F600%2F4740&lang={language}",
                         "Wasseraufbereitung": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F600%3AcategoryPath%3A%2F1%2F600%2F4711&lang={language}",
                         "Küchenpressen": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F600%3AcategoryPath%3A%2F1%2F600%2F4780&lang={language}",
                         "Verschlussöffner": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F600%3AcategoryPath%3A%2F1%2F600%2F4790&lang={language}",
                         "Schneidutensilien": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F600%3AcategoryPath%3A%2F1%2F600%2F4720&lang={language}"},
    "Wohnen & Licht": {"Innen- & Aussenleuchten": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F610%3AcategoryPath%3A%2F1%2F610%2F6110&lang={language}",
                       "Leuchtmittel": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F610%3AcategoryPath%3A%2F1%2F610%2F6140&lang={language}",
                       "Weihnachten": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F610%3AcategoryPath%3A%2F1%2F610%2F8190&lang={language}",
                       "Dekorationsbeleuchtung": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F610%3AcategoryPath%3A%2F1%2F610%2F6150&lang={language}",
                       "Wohnen": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F610%3AcategoryPath%3A%2F1%2F610%2F8230&lang={language}"},
    "Garten & Grill": {"Grillieren": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F720%3AcategoryPath%3A%2F1%2F720%2F7400&lang={language}",
                       "Pools & Planschbecken": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F720%3AcategoryPath%3A%2F1%2F720%2F7310&lang={language}",
                       "Gartenmöbel": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F720%3AcategoryPath%3A%2F1%2F720%2F1210&lang={language}"},
    "Büro & Papeterie": {"Schreiben & Korrigieren": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F800%3AcategoryPath%3A%2F1%2F800%2F4520&lang={language}",
                         "Ordnen & Registrieren": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F800%3AcategoryPath%3A%2F1%2F800%2F4540&lang={language}",
                         "Notieren": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F800%3AcategoryPath%3A%2F1%2F800%2F4550&lang={language}",
                         "Bürogeräte & Zubehör": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F800%3AcategoryPath%3A%2F1%2F800%2F4500&lang={language}",
                         "Verpackung & Versand": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F800%3AcategoryPath%3A%2F1%2F800%2F4580&lang={language}",
                         "Präsentationsmaterial": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F800%3AcategoryPath%3A%2F1%2F800%2F4600&lang={language}",
                         "Büromöbel": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F800%3AcategoryPath%3A%2F1%2F800%2F4590&lang={language}",
                         "Schulmaterial": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F800%3AcategoryPath%3A%2F1%2F800%2F9800&lang={language}",
                         "Schneiden & Kleben": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F800%3AcategoryPath%3A%2F1%2F800%2F4530&lang={language}",
                         "Heften & Lochen": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F800%3AcategoryPath%3A%2F1%2F800%2F4510&lang={language}",
                         "Technisches Zeichnen": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F800%3AcategoryPath%3A%2F1%2F800%2F4570&lang={language}"},
    "Freizeit & Sport": {"Outdoor": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F710%3AcategoryPath%3A%2F1%2F710%2F7910&lang={language}",
                         "Uhren": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F710%3AcategoryPath%3A%2F1%2F710%2F9300&lang={language}",
                         "Mobility": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F710%3AcategoryPath%3A%2F1%2F710%2F7500&lang={language}",
                         "Velo Zubehör": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F710%3AcategoryPath%3A%2F1%2F710%2F4810&lang={language}",
                         "Sport": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F710%3AcategoryPath%3A%2F1%2F710%2F1122&lang={language}",
                         "Stand Up Paddle": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F710%3AcategoryPath%3A%2F1%2F710%2F4738&lang={language}",
                         "Schwimmen": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F710%3AcategoryPath%3A%2F1%2F710%2F4731&lang={language}",
                         "Boote": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F710%3AcategoryPath%3A%2F1%2F710%2F4736&lang={language}"},
    "Spielwaren & Drohnen": {"Drohnen & RC Modellbau": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F222%3AcategoryPath%3A%2F1%2F222%2F8100&lang={language}",
                             "Spiele & Puzzle": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F222%3AcategoryPath%3A%2F1%2F222%2F8700&lang={language}",
                             "Outdoor, Spielwaren & Kinderfahrzeuge": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F222%3AcategoryPath%3A%2F1%2F222%2F8600&lang={language}",
                             "Figuren, Puppen & Plüschtiere": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F222%3AcategoryPath%3A%2F1%2F222%2F8400&lang={language}",
                             "Bauspielzeug & Spielzeugsets": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F222%3AcategoryPath%3A%2F1%2F222%2F8200&lang={language}",
                             "Fahrzeuge & Bahnen": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F222%3AcategoryPath%3A%2F1%2F222%2F8300&lang={language}",
                             "LEGO": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F222%3AcategoryPath%3A%2F1%2F222%2F2222&lang={language}",
                             "Kindermultimedia": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F222%3AcategoryPath%3A%2F1%2F222%2F8900&lang={language}",
                             "Experimentieren, Sammeln & Gestalten": "https://www.interdiscount.ch/idocc/occ/id/products/search?currentPage={page}&pageSize=100&query=%3Arelevance%3AcategoryPath%3A%2F1%2F222%3AcategoryPath%3A%2F1%2F222%2F8500&lang={language}"}
}


ua_iphone = " ".join(["Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X)",
                      "AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A356 Safari/604.1"])
headers = {"user-agent": ua_iphone}
domain = "https://www.interdiscount.ch"


def get_max_page(url):
    response = requests.get(url=url, headers=headers)
    json_object = response.json()
    max_page = json_object["pagination"]["numberOfPages"]
    return max_page


def get_characteristics(characteristic_objects):
    characteristics = list()
    for characteristic_object in characteristic_objects:
        sub_characteristics = list()
        characteristic_name = characteristic_object["name"]
        sub_characteristic_objects = characteristic_object["features"]
        for sub_characteristic_object in sub_characteristic_objects:
            sub_characteristic_name = sub_characteristic_object["name"]
            sub_characteristic_values = sub_characteristic_object["featureValues"]
            sub_characteristic_values = [element["value"] for element in sub_characteristic_values]
            sub_characteristic = {sub_characteristic_name: sub_characteristic_values}
            sub_characteristics.append(sub_characteristic)
        characteristic = {characteristic_name: sub_characteristics}
        characteristics.append(characteristic)
    characteristics = {"characteristics": characteristics}
    characteristics_json = json.dumps(characteristics)
    return characteristics_json


def create_photo_dir(product_id):
    path = pathlib.Path("photos", product_id)
    if os.path.isdir(path):
        shutil.rmtree(path)
        os.mkdir(path)
    else:
        os.mkdir(path)
    print(f"[INFO] Папка для фотографий товара с id = {product_id} успешно создана")
    return path


def download_photo(path, index, image_url):
    image_url = domain + image_url
    response = requests.get(url=image_url, headers=headers)
    path = pathlib.Path(path, f"{index}.jpg")
    with open(path, "wb") as file:
        file.write(response.content)


def download_product_photos(image_objects, product_id):
    index = 0
    path = create_photo_dir(product_id=product_id)
    for image_object in image_objects:
        index += 1
        image_url = image_object["sizes"][-1]["url"]
        download_photo(path=path, index=index, image_url=image_url)
    print(f"[INFO] Все изображения ({len(image_objects)}) товара с id = {product_id} успешно загружены")


def get_product_data(category, product_id, language):
    try:
        url = f"https://www.interdiscount.ch/idocc/occ/id/products/{product_id}?fieldSet=FULL&lang={language}"
        response = requests.get(url=url, headers=headers, timeout=30)
        json_object = response.json()
        title = json_object["name"]
        description = json_object["markupDescription"]
        price = json_object["productPriceData"]["prices"][0]["finalPrice"]["value"]
        characteristic_objects = json_object["classifications"]
        image_objects = json_object["customImageData"]
        characteristics = get_characteristics(characteristic_objects=characteristic_objects)
        record_product(product_id=product_id, language=language, title=title, price=price,
                       category=category, description=description, characteristics=characteristics)
        return image_objects
    except TimeoutError:
        return get_product_data(category, product_id, language)


def parsing():
    for main_key in categories_url.keys():
        for key in categories_url[main_key].keys():
            category = f"{main_key}-{key}"
            url = categories_url[main_key][key].replace("{page}", "0").replace("{language}", "de")
            max_page = get_max_page(url=url)
            for page in range(0, max_page):
                url = categories_url[main_key][key].replace("{page}", str(page)).replace("{language}", "de")
                response = requests.get(url=url, headers=headers)
                json_object = response.json()
                product_objects = json_object["products"]
                for product_object in product_objects:
                    product_id = product_object["code"]
                    images = str()
                    for language in languages:
                        images = get_product_data(category=category, product_id=product_id, language=language)
                    download_product_photos(image_objects=images, product_id=product_id)
                    print(f"[INFO] Товар с id = {product_id} успешно обработан\n")


def main():
    print("[INFO] Программа запущена. Она все сделает в автоматическом режиме, но потребует некоторого времени")
    print("[INFO] Из-за объемов трафика, который необходимо обработать, программа может занять не один час")
    print("[INFO] Наберитесь терпения и приятного использования!)")
    start_time = time.time()
    create_table()
    create_photos_dir()
    parsing()
    stop_time = time.time()
    print("[INFO] Программа успешно завершена")
    print(f"[INFO] На работу программы потребовалось {(stop_time - start_time) / 60} минут")


if __name__ == "__main__":
    main()
