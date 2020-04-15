from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import csv
import datetime

def home(request):
    context = {}
    # Requests for a website document from worldometer
    src_file = requests.get("https://www.worldometers.info/coronavirus/").text

    # Initialize Soup object
    soup = BeautifulSoup(src_file, "lxml")

    # CSV file
    csv_file = open("worldometer_scraper.csv", "w")
    csv_writer = csv.writer(csv_file) # Write to csv file
    csv_writer.writerow(["total_cases","total_deaths","total_recovered"]) # Rows to hold respective data

    # Total Cases
    total_counter = []
    for main_counter in soup.find_all("div", class_="maincounter-number"):
        total_counter.append(main_counter.text)
    
    context["total_cases"] = total_counter[0]
    context["total_deaths"] = total_counter[1]
    context["total_recovered"] = total_counter[2]

    # Save data to csv file
    for data in total_counter:
        csv_writer.writerow([total_counter[total_counter.index(data)]])
    
    # Close file
    csv_file.close()

    infected_patients = soup.find("div", class_="number-table-main").text
    context["infected_patients"] = infected_patients

    mild_patients = soup.find("span", class_="number-table").text

    # Calculate percentage
    x = infected_patients
    y = x.split(',')
    infected_total = []
    for value in y:
        infected_total.append(value)
    infected_total = ''.join(infected_total)

    r = mild_patients
    s = r.split(',')
    mild_total = []
    for value in s:
        mild_total.append(value)
    mild_total = ''.join(mild_total)

    mild_percent = ((int(mild_total)/int(infected_total))*100)

    context["mild_patients"] = mild_patients
    context["mild_percent"] = round(mild_percent,2)

    critical_patient = int(infected_total) - int(mild_total)
    context["critical_patient"] = critical_patient
    context["critical_percent"] = round(100-mild_percent,2)

    t = total_counter[1]
    t = t.split(',')
    total_deaths = []
    for value in t:
        total_deaths.append(value)
    total_deaths = ''.join(total_deaths)

    u = total_counter[2]
    u = u.split(',')
    total_recover = []
    for value in u:
        total_recover.append(value)
    total_recover = ''.join(total_recover)

    total_cases_closed = int(total_recover) + int(total_deaths)

    context["total_cases_closed"] = total_cases_closed
    death_percent_on_active_cases = total_cases_closed - int(total_deaths)
    # print(death_percent_on_active_cases, total_cases_closed)
    death_percent_on_active_cases = round((int(total_deaths)/total_cases_closed)*100,2)
    context["death_percent_on_active_cases"] = death_percent_on_active_cases

    #Recovered/ Discharged Percent
    context["recovered_or_discharged_percent"] = round(100-death_percent_on_active_cases,2)

    # Time
    time = datetime.datetime.now()
    context["time"] = time

    # Cases in Tanzania
    src_file_tz = requests.get("https://www.worldometers.info/coronavirus/country/tanzania/").text
    soup_tz = BeautifulSoup(src_file_tz,"lxml")

    total_cases_tz = []
    for cases_tz in soup_tz.findAll("div", class_="maincounter-number"):
        total_cases_tz.append(cases_tz.span.text)


    context["total_cases_tz"]=total_cases_tz[0]
    context["total_recovered_tz"]=total_cases_tz[2]
    context["total_deaths_tz"]=total_cases_tz[1]

    return render(request, "index/home.html",context)