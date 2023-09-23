# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ThuvienluatPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        # Strip all whitespaces from strings
        field_names = ['url', 'title']
        for field_name in field_names:
            value = adapter.get(field_name)
            adapter[field_name] = value[0].strip()

        # Delete array from ArrayList
        array_lists = ['h2_title']
        for array_list in array_lists:
            value = adapter.get(array_list)
            adapter[array_list] = value[0]


        return item
    

# import mysql.connector
# class SaveToMySQLPipeline:
    
#     def __init__(self):
#         self.conn = mysql.connector.connect(
#             host = 'localhost',
#             user = 'root',
#             password = 'Duong@911',
#             database = 'datas'
#         )

#         self.cur = self.conn.cursor()

#         ## Create Database Law_Library if not exits
#         self.cur.execute("""
#         CREATE TABLE IF NOT EXISTS law_library(
#             id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
#             url VARCHAR(255),
#             title TEXT,
#             h2_title TEXT,
#             paragraph TEXT           
#         )
#         """)

#     def process_item(self, item, spider):
#         self.cur.execute("""insert into law_library (
#                 url,
#                 title,
#                 h2_title,
#                 paragraph
#             ) values (
#                 %s,
#                 %s,
#                 %s,
#                 %s    
#             )""", (
#                 item['url'],
#                 item['title'],
#                 item['h2_title'],
#                 item['paragraph']
#             ))

#         self.conn.commit()
#         return item
        

#     def close_spider(self, spider):
#         ## close cursor & connection to databse
#         self.cur.close()
#         self.conn.close()

import mysql.connector
class SaveToMySQLPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'Duong@911',
            database = 'datas'
        )

        self.cur = self.conn.cursor()
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INT PRIMARY KEY AUTO_INCREMENT,
            url VARCHAR(255),
            title VARCHAR(255)          
        )
        """)
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS sections (
            id INT PRIMARY KEY AUTO_INCREMENT,
            article_id INT,
            h2_title VARCHAR(255),
            paragraph TEXT,
            FOREIGN KEY (article_id) REFERENCES articles(id)   
        )
        """)

    def process_item(self, item, spider):
        self.cur.execute("""insert into articles (
                url,
                title
            ) values (
                %s,
                %s   
            )""", (
                item['url'],
                item['title']
            ))
        article_id = self.cur.lastrowid
        for i in range(len(item['h2_title'])):
             self.cur.execute("""insert into sections (
                article_id,
                h2_title,
                paragraph
            ) values (
                %s,
                %s,
                %s   
            )""", (
                article_id,
                str(item['h2_title'][i]),
                str(item['paragraph'][i])
            ))
        self.conn.commit()
        return item
    
    def close_spider(self, spider):
        ## close cursor & connection to databse
        self.cur.close()
        self.conn.close()