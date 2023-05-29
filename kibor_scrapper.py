import argparse
from datetime import datetime
import pandas as pd
import calendar
import requests
import tabula
from tabula.io import read_pdf


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True, help="date in DD/MM/YYYY format")
    args = vars(ap.parse_args())
    scrapper_kibor(args)

def scrapper_kibor(args):

    date_time_str = args['date']
    scrape_date = datetime.strptime(date_time_str, '%d/%m/%Y')
    get_pdf_from_spb(scrape_date)

def get_pdf_from_spb(scrape_date):

    day=scrape_date.strftime('%d')
    month=scrape_date.strftime('%b')
    year_YYYY=scrape_date.strftime('%Y')
    year_YY=scrape_date.strftime('%y')
    
    scrape_url = f'''https://www.sbp.org.pk/ecodata/kibor/{year_YYYY}/{month}/Kibor-{day}-{month}-{year_YY}.pdf'''
    scrapped_pdf = requests.get(scrape_url)
    with open('Kibor-{}-{}-{}.pdf'.format(day,month,year_YYYY), 'wb') as f:
        f.write(scrapped_pdf.content)
    print('Kibor-{}-{}-{}.pdf'.format(day,month,year_YYYY)," saved")
    convert_to_csv(day,month,year_YYYY)

def convert_to_csv(day,month,year_YYYY):
    file_path='Kibor-{}-{}-{}.pdf'.format(day,month,year_YYYY)
    scrapped_pdf= read_pdf(file_path,pages="all")
    df=scrapped_pdf[0]
    df.to_csv('Kibor-{}-{}-{}.csv'.format(day,month,year_YYYY))
    print('Kibor-{}-{}-{}.csv'.format(day,month,year_YYYY)," saved")


if __name__ == "__main__":
    main()
