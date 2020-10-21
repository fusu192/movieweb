



import os
import sqlite3
import json
import time

json_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),"static","json_file")

#当前目录
cdir=os.path.dirname((os.path.abspath(__file__)))
sql_dir=os.path.join(cdir,"db.sqlite3")

#连接数据库
conn=sqlite3.connect(sql_dir)
cursor=conn.cursor()

#表名
t_name="play_page_Barrage_list"
#查询语句
sql='''select id,movie_id,time_tmp,author_tmp,text_tmp,color_tmp,type_tmp from {}'''.format(t_name)
#返回结果
results=cursor.execute(sql)
all_result=results.fetchall()

if(all_result):
    for w in all_result:
        id=w[0]
        movie_id=w[1]
        time_tmp=w[2]
        author_tmp=w[3]
        text_tmp=w[4]
        color_tmp=w[5]
        type_tmp=w[6]

        #读取json文件
        tmp_json=os.path.join(json_path,"{}.json".format(movie_id))

        if(os.path.exists(tmp_json)):
            with open(tmp_json,'r',encoding="utf-8") as f:
                content = json.load(f)
                print(content)
        else:
            #不存在
            content={"code": 0, "data": []}

            
        #[230.523,0,16777215,"618c713c","键盘妹子挺好看？"]
        tmp_item=[time_tmp, type_tmp, color_tmp, author_tmp, text_tmp]
        content["data"].append(tmp_item)

        #排序
        tmp_content=sorted(content["data"], key=lambda item: float(item[0]))

        content["data"]=tmp_content

        #写入json文件
        with open(tmp_json, "w", encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False)


        #删除数据
        sql_delete_ip='''delete from {} where id={}'''.format(t_name,id)
        #返回结果
        delete_result=cursor.execute(sql_delete_ip)
        conn.commit()