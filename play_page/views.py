from django.shortcuts import render
from django.http import HttpResponse
import json
import simplejson
import os
from .models import movielist
from .models import Barrage_list
import datetime
import itertools
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import render,redirect,reverse


#首页
def index(request):
	t=datetime.datetime.now()
	#当前年份
	t1 =t.strftime('%Y')
	#电影列表
	movie_list=movielist.objects.all().order_by('-year') 
	#电影名字列表
	movie_all_name_list=[i.movie_name for i in movie_list]
	print(movie_all_name_list)

	#播放量列表
	v_movie_list=movie_list.order_by('-view_num')[:8]

	#分页
	is_exist=1
	if(movie_list):
		paginator = Paginator(movie_list, 12) # Show 10 contacts per page
		urlpage = request.GET.get('a')
		if(urlpage):
			try:
				page=int(urlpage)
			except Exception as e:
				print(e)
				page=1

		else:
			page=1

		#总页数
		all_page_num=paginator.num_pages

		if(all_page_num<=5):
			#小于5页
			page_num_list=[i for i in range(1,all_page_num+1)]
		else:
			#大于5页
			avg=(all_page_num+1)/2.0
			#在中位数左侧
			if(page<avg):
				if(page-1>=2):
					page_num_list=[page-2,page-1,page,page+1,page+2]
				else:
					page_num_list=[1,2,3,4,5]
			#在中位数右侧
			else:
				if(all_page_num-page>=2):
					page_num_list=[page-2,page-1,page,page+1,page+2]
				else:
					page_num_list=[all_page_num-4,all_page_num-3,all_page_num-2,all_page_num-1,all_page_num]

		try:
			booklist = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			booklist = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			booklist = paginator.page(paginator.num_pages)

		if(not page==None):
			if(booklist.number==1):
				prepage=None
				nextpage=booklist.number+1
			elif(booklist.number<1):
				pass
			else:
				prepage=booklist.number-1
				nextpage=booklist.number+1
		else:
			prepage=None
			nextpage=booklist.number+1

		#print(booklist.previous_page_number())
		#print(booklist.number)
		#print(booklist.next_page_number())
	else:
		is_exist=0

	return render(request,'index.html',{"movie_all_name_list":movie_all_name_list,"cur_page":int(page),"movie_list":booklist,"t1":t1,"t_movie_list":v_movie_list,'prepage':prepage,'nextpage':nextpage,'is_exist':is_exist,'page_num_list':page_num_list})

#视频播放页
def play_page(request,movie_id):
	print(movie_id)
	t=datetime.datetime.now()
	#当前年份
	t1 =t.strftime('%Y')

	#所有电影列表
	movie_list=movielist.objects.all()
	#id 列表
	movie_id_list=[i.id for i in movie_list]
	#name 列表
	movie_name_list=[i.movie_name for i in movie_list]
	#播放量列表
	v_movie_list=movie_list.order_by('-view_num')[:8]


	if(movie_id in movie_name_list):
		#当前电影
		cur_movie=movielist.objects.get(movie_name=movie_id)
		cur_movie_id=cur_movie.id
		#推荐电影列表
		int_movie_id=int(cur_movie_id)
		movie_list_len=len(movie_list)
		width=movie_list_len-int_movie_id
		#推荐个数
		show_num=8
		
		tmp_movie=movie_list.order_by('-year')
		
		if(width>=show_num):
			t_movie_list=tmp_movie[int_movie_id:int_movie_id+8]
		else:
			tmp1=tmp_movie[0:(show_num-width)]
			tmp2=tmp_movie[int_movie_id:]
			t_movie_list = itertools.chain(tmp2,tmp1)

	elif(int(movie_id) in movie_id_list):
		#当前电影
		tmp_m_id=int(movie_id)
		cur_movie=movielist.objects.get(id=tmp_m_id)
		#推荐电影列表
		int_movie_id=tmp_m_id
		movie_list_len=len(movie_list)
		width=movie_list_len-int_movie_id
		#推荐个数
		show_num=8
		
		tmp_movie=movie_list.order_by('-year')
		
		if(width>=show_num):
			t_movie_list=tmp_movie[int_movie_id:int_movie_id+8]
		else:
			tmp1=tmp_movie[0:(show_num-width)]
			tmp2=tmp_movie[int_movie_id:]
			t_movie_list = itertools.chain(tmp2,tmp1)
	else:
		return redirect("index")

	#浏览次数加1
	cur_movie.view_num=cur_movie.view_num+1
	cur_movie.save()

	return render(request,'play_page.html',{"t_movie_list":t_movie_list,"v_movie_list":v_movie_list,"cur_movie":cur_movie})


#弹幕地址tmp
def add_Barrage(request):

	if(request.method == 'POST'):
		#{"id":"9E2E3368B56CDBB4","author":"DIYgod","time":24.064575,"text":"2222","color":16777215,"type":0}  
		dic= simplejson.loads(request.body)

		print(dic)
		movie_id=dic["id"]
		time_tmp=dic["time"]
		author_tmp=dic["author"]
		text_tmp=dic["text"]
		color_tmp=dic["color"]
		type_tmp=dic["type"]

		tmp_item=[time_tmp, type_tmp, color_tmp, author_tmp, text_tmp]

		#存到数据库中
		tmp_Barrage=Barrage_list()
		tmp_Barrage.time_tmp=time_tmp
		tmp_Barrage.author_tmp=author_tmp
		tmp_Barrage.text_tmp=text_tmp
		tmp_Barrage.color_tmp=color_tmp
		tmp_Barrage.type_tmp=type_tmp
		tmp_Barrage.movie_id=movie_id
		tmp_Barrage.save()

		#json返回本次添加的弹幕
		result = {"code": 0, "data":[tmp_item,]}
		return HttpResponse(json.dumps(result,ensure_ascii=False),content_type="application/json,charset=utf-8")
	else:
		a=request.GET['id']

		result = {"code": 0, "data": [ [149.92993, "top", "#e54256", "DIYgod", "有人么？"],]}
		#json返回为中文
		return HttpResponse(json.dumps(result,ensure_ascii=False),content_type="application/json,charset=utf-8")


def search(request,search_content):
	tmp_content=search_content.strip()
	if(tmp_content==""):
		return redirect("index")

	t=datetime.datetime.now()
	#当前年份
	t1 =t.strftime('%Y')

	#所有电影
	all_movie_list=movielist.objects.all().order_by('-year') 

	#电影搜索结果
	movie_list=movielist.objects.filter(movie_name__icontains=search_content)

	#电影名字列表
	movie_all_name_list=[i.movie_name for i in all_movie_list]

	#播放量列表
	v_movie_list=all_movie_list.order_by('-view_num')[:8]

	#分页
	is_exist=1
	if(movie_list):
		paginator = Paginator(movie_list, 12) # Show 10 contacts per page
		urlpage = request.GET.get('a')
		if(urlpage):
			try:
				page=int(urlpage)
			except Exception as e:
				print(e)
				page=1

		else:
			page=1

		#总页数
		all_page_num=paginator.num_pages

		if(all_page_num<=5):
			#小于5页
			page_num_list=[i for i in range(1,all_page_num+1)]
		else:
			#大于5页
			avg=(all_page_num+1)/2.0
			#在中位数左侧
			if(page<avg):
				if(page-1>=2):
					page_num_list=[page-2,page-1,page,page+1,page+2]
				else:
					page_num_list=[1,2,3,4,5]
			#在中位数右侧
			else:
				if(all_page_num-page>=2):
					page_num_list=[page-2,page-1,page,page+1,page+2]
				else:
					page_num_list=[all_page_num-4,all_page_num-3,all_page_num-2,all_page_num-1,all_page_num]

		try:
			booklist = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			booklist = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			booklist = paginator.page(paginator.num_pages)

		if(not page==None):
			if(booklist.number==1):
				prepage=None
				nextpage=booklist.number+1
			elif(booklist.number<1):
				pass
			else:
				prepage=booklist.number-1
				nextpage=booklist.number+1
		else:
			prepage=None
			nextpage=booklist.number+1

		#print(booklist.previous_page_number())
		#print(booklist.number)
		#print(booklist.next_page_number())
	else:
		is_exist=0

	return render(request,'index.html',{"movie_all_name_list":movie_all_name_list,"cur_page":int(page),"movie_list":booklist,"t1":t1,"t_movie_list":v_movie_list,'prepage':prepage,'nextpage':nextpage,'is_exist':is_exist,'page_num_list':page_num_list})



	