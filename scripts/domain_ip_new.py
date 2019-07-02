# -*- coding: utf-8 -*-
__author__ = "MoR03r"

import dns.resolver
import argparse
import sqlite3
import time
from multiprocessing import Pool, Manager

def readfile(inputfile):
    with open(inputfile, 'rt', encoding='utf-8') as file:
        domains = file.read().split()
    return domains

usage = '''DnsSolver To Get Real IP'''
parser = argparse.ArgumentParser(description=usage)
parser.add_argument('-t', dest='threads', action='store', default=10, help='set multiprocessing number')
parser.add_argument('-f', dest='inputfile', action='store', help='input file')
parser.add_argument('-i', dest='domain', action='store', help='domain you want analyze')
parser.add_argument('-c', dest='check', action='store_true', help='check if domain exists or resolved')
args = parser.parse_args()

# DNS Settings
resolver = dns.resolver.Resolver()
resolver.nameservers = ['8.8.8.8', '8.8.4.4', '114.114.114.114', '223.5.5.5']
resolver.timeout = 2
resolver.lefetime = 2

# Connect to sqlite
db = sqlite3.connect("domains.db")
# Database Table name
sql_sheet = "domain_analysis"
cursor = db.cursor()

class Dboprate:
    domain_lists = []

    def __init__(self, domain_lists):
        self.domain_lists = domain_lists

    def drop_table(self):
        sql = 'DROP TABLE IF EXISTS {0}'.format(sql_sheet)
        cursor.execute(sql)
        db.commit()

    def create_table(self):
        sql = '''CREATE TABLE {sql_sheet}(
                    `domain` text,
                    `A` text,
                    `MX` text,
                    `NS` text,
                    `CNAME` text,
                    `TXT` text,
                    `ERROR_A` text,
                    `ERROR_MX` text,
                    `ERROR_NS` text,
                    `ERROR_CNAME` text,
                    `ERROR_TXT` text,
                    `ERROR` text,
                    `REMARK` text)'''.format(sql_sheet=sql_sheet)
        cursor.execute(sql)
        db.commit()

    def init_db(self):
        self.drop_table()
        self.create_table()
        for domain in self.domain_lists:
            self.insert(domain)
        print('\033[1;32m[*]\033[0m Database init finished.')

    def insert(self, li):
        sql = 'INSERT INTO {sql_sheet}(domain) VALUES ("{value}")'.format(sql_sheet=sql_sheet, value=li)
        cursor.execute(sql)
        db.commit()

    def update(self, name, value, domain):
        sql = 'UPDATE {sql_sheet} SET {set_name}=\'{set_value}\' where domain=\'{domain}\''.format(
                    sql_sheet=sql_sheet, set_name=name, set_value=value, domain=domain)
        cursor.execute(sql)
        db.commit()

    def select(self, records, domain):
        sql = 'SELECT {records} from {sql_sheet} where domain="{domain}"'.format(
            records=records, sql_sheet=sql_sheet, domain=domain)
        cursor.execute(sql)
        return cursor.fetchone()


class nslookup:
    domains = []

    def __init__(self, domains):
        self.domains = domains

    def check(self):
        tp = ['A', 'TXT', 'CNAME', 'NS', 'MX']
        length = len(tp)
        output = '\033[1;32m[+]\033[0m Domain Check: {0} {1} finished.'
        pa = ''
        for i in self.domains:
            res = dboprator.select('A,TXT,CNAME,NS,MX', i)
            NULL_tuple = (None, None, None, None, None)
            if res == NULL_tuple:
                dboprator.update('ERROR', 'Domain didnt analyze or didnt exists.', i)
            for n in range(length):
                if not res[n] == None:
                    pa += tp[n]+' '
            if pa == '':
                pa = 'Nothing for'
                output = output.replace('32m[+]', '31m[-]')
            print(output.format(pa, i))
            pa = ''
            output = '\033[1;32m[+]\033[0m Domain Check: {0} {1} finished.'


    def record(self, domain, typer):
        res = self.log(domain, typer)

    def log(self, domain, qm):
        for q in qm:
            try:
                res = resolver.query(domain, q)
                self.write(domain, q, res)
                print('\033[1;32m[+]\033[0m {0} record: {1} finished.'.format(q, domain))
            except Exception as e:
                self.error(e, domain, q)
                continue
        return '\033[1;32m[+]\033[0m Done.'

    def write(self, domain, q, ress):
        for res in ress:
            data = dboprator.select(q, domain)
            if data[0] == None:
                dboprator.update(q, str(res), domain)
            else:
                if data[1].find(str(res)) != -1:
                    continue
                else:
                    dboprator.update(q, 'CONCAT({0},"\r\n{1}'.format(q, res), domain)

    def error(self, err, open_element, class_element):
        data = dboprator.select(class_element, open_element)
        if data[0] == None:
            dboprator.update('ERROR_{0}'.format(class_element), str(err), open_element)
        else:
            dboprator.update('ERROR_{0}'.format(class_element),
                             'CONCAT(ERROR_{0},\"\r\n{1}\")'.format(class_element, open_element),
                             open_element)
        print('\033[1;31m[-]\033[0m {0}:ERROR_{1} has recorded.'.format(open_element, class_element))


def main():
    nsl = nslookup(files)
    if args.check:
        nsl.check()
    else:
        pool = Pool(int(args.threads))
        typr = ['A', 'MX', 'NS', 'TXT', 'CNAME']
        for i in files:
            pool.apply_async(nsl.record, args=(i, typr,))

        num = 0
        allnum = len(typr)
        while True:
            pool.close()
            pool.join()
            num += 1
            if num >= allnum:
                break


def one_domain(domain):
    nsl = nslookup([domain])
    typr = ['A', 'MX', 'NS', 'TXT', 'CNAME']
    if args.check:
        nsl.check()
    else:
        nsl.record(domain, typr)


if args.domain:
    files = [args.domain]
else:
    files = readfile(args.inputfile)
dboprator = Dboprate(files)
if not args.check:
    dboprator.init_db()

if __name__ == '__main__':
    start = time.time()
    if args.domain:
        one_domain(args.domain)
    else:
        main()
    end = time.time()
    print('\033[1;32m[+]\033[0m Time used: {0:.3f}s'.format(end - start))
    print('\033[1;32m[+]\033[0m Done.')
