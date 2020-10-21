#coding=utf-8
from django.db import models
from django.contrib import admin


#--------------------------------------------------------------------------------------------------------------------
#电影列表
class movielist(models.Model):
    #电影名
    movie_name=models.CharField(max_length=20)
    #电影地址
    movie_url=models.CharField(max_length=100)
    #电影封面图
    movie_pic=models.CharField(max_length=35)
    #年份
    year=models.IntegerField()
    #星级
    star_num=models.CharField(max_length=1)
    #观看量
    view_num=models.IntegerField()
    #描述
    desc=models.TextField()
    #json_file
    json_file=models.TextField()

    def __str__(self):
        return self.movie_name
class movielist_Admin(admin.ModelAdmin):
    list_display = ('id','movie_name','movie_url','movie_pic','year','star_num','view_num','desc','json_file')


#电影列表加入后台
admin.site.register(movielist,movielist_Admin)



#--------------------------------------------------------------------------------------------------------------------
#弹幕列表
class Barrage_list(models.Model):
    #弹幕内容
    time_tmp=models.TextField()
    author_tmp=models.TextField()
    text_tmp=models.TextField()
    color_tmp=models.TextField()
    type_tmp=models.TextField()
    #电影ID
    movie_id=models.CharField(max_length=100)

    def __str__(self):
        return self.text_tmp
class Barrage_list_Admin(admin.ModelAdmin):
    list_display = ('id','time_tmp','author_tmp','text_tmp','color_tmp','type_tmp','movie_id',)


#电影列表加入后台
admin.site.register(Barrage_list,Barrage_list_Admin)
