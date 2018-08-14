# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from __future__ import absolute_import
from __future__ import division     
from __future__ import print_function

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pymysql
from pymysql import connections
from baidu_baike import settings

class BaiduBaikePipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(
            host=settings.HOST_IP,
#            port=settings.PORT,
            user=settings.USER,
            passwd=settings.PASSWD,
            db=settings.DB_NAME,
            charset='utf8mb4',
            use_unicode=True
            )   
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # process info for actor
        actor_chName = str(item['actor_chName']).decode('utf-8')
        actor_foreName = str(item['actor_foreName']).decode('utf-8')
        movie_chName = str(item['movie_chName']).decode('utf-8')
        movie_foreName = str(item['movie_foreName']).decode('utf-8')

	if (item['actor_chName'] != None or item['actor_foreName'] != None) and item['movie_chName'] == None:
            actor_bio = str(item['actor_bio']).decode('utf-8')
            actor_nationality = str(item['actor_nationality']).decode('utf-8')
            actor_constellation = str(item['actor_constellation']).decode('utf-8')
            actor_birthPlace = str(item['actor_birthPlace']).decode('utf-8')
            actor_birthDay = str(item['actor_birthDay']).decode('utf-8')
            actor_repWorks = str(item['actor_repWorks']).decode('utf-8')
            actor_achiem = str(item['actor_achiem']).decode('utf-8')
            actor_brokerage = str(item['actor_brokerage']).decode('utf-8')

            self.cursor.execute("SELECT actor_chName FROM actor;")
            actorList = self.cursor.fetchall()
            if (actor_chName,) not in actorList :
                # get the nums of actor_id in table actor
                self.cursor.execute("SELECT MAX(actor_id) FROM actor")
                if None in self.cursor.fetchall()[0]:
                    actor_id = 1
                else:
                    actor_id = self.cursor.fetchall()[0] + 1
                sql = """
                INSERT INTO actor(actor_id, actor_bio, actor_chName, actor_foreName, actor_nationality, actor_constellation, actor_birthPlace, actor_birthDay, actor_repWorks, actor_achiem, actor_brokerage ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                self.cursor.execute(sql, (actor_id, actor_bio, actor_chName, actor_foreName, actor_nationality, actor_constellation, actor_birthPlace, actor_birthDay, actor_repWorks, actor_achiem, actor_brokerage ))
                self.conn.commit()
            else:
                print("#" * 20, "Got a duplict actor!!", actor_chName)
        elif (item['movie_chName'] != None or item['movie_foreName'] != None) and item['actor_chName'] == None:
            movie_bio = str(item['movie_bio']).decode('utf-8')
            movie_prodTime = str(item['movie_prodTime']).decode('utf-8')
            movie_prodCompany = str(item['movie_prodCompany']).decode('utf-8')
            movie_director = str(item['movie_director']).decode('utf-8')
            movie_screenwriter = str(item['movie_screenwriter']).decode('utf-8')
            movie_genre = str(item['movie_genre']).decode('utf-8')
            movie_star = str(item['movie_star']).decode('utf-8')
            movie_length = str(item['movie_length']).decode('utf-8')
            movie_rekeaseTime = str(item['movie_rekeaseTime']).decode('utf-8')
            movie_language = str(item['movie_language']).decode('utf-8')
            movie_achiem = str(item['movie_achiem']).decode('utf-8')

            self.cursor.execute("SELECT movie_chName FROM movie;")
            movieList = self.cursor.fetchall()
            if (movie_chName,) not in movieList :
                self.cursor.execute("SELECT MAX(movie_id) FROM movie")
                result = self.cursor.fetchall()[0]
                if None in result:
                    movie_id = 1
                else:
                    movie_id = result[0] + 1
                sql = """
                INSERT INTO movie(  movie_id, movie_bio, movie_chName, movie_foreName, movie_prodTime, movie_prodCompany, movie_director, movie_screenwriter, movie_genre, movie_star, movie_length, movie_rekeaseTime, movie_language, movie_achiem ) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                self.cursor.execute(sql, ( movie_id, movie_bio, movie_chName, movie_foreName, movie_prodTime, movie_prodCompany, movie_director, movie_screenwriter, movie_genre, movie_star, movie_length, movie_rekeaseTime, movie_language, movie_achiem ))
                self.conn.commit()
            else:
                print("Got a duplict movie!!", movie_chName)
        else:
            print("Skip this page because wrong category!! ")
        return item
    def close_spider(self, spider):
        self.conn.close()
