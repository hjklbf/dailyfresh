#coding=utf-8
from django.shortcuts import render
from django.http import JsonResponse
from models import *
from django.core.paginator import Paginator
from df_cart.models import *
# Create your views here.
def index(request):
    typelist=TypeInfo.objects.all()
    list=[]
    for type in typelist:
        list.append({
            'type':type,
            'click_list':type.goodsinfo_set.order_by('-gclick')[0:3],
            'new_list':type.goodsinfo_set.order_by('-id')[0:4]
        })
    context={'title':'首页','list':list,'cart_count':cart_count(request)}
    return render(request,'df_goods/index.html',context)

def index2(request,tid):
    #查询点击最高、最新的商品
    t1_click= GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gclick')[0:3]
    t1_new=GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-id')[0:4]
    #构造点击量最高的商品列表
    click_list=[]
    for click in t1_click:
        click_list.append({'id':click.id,'title':click.gtitle})
    #构造最新的商品列表
    new_list=[]
    for new in t1_new:
        new_list.append({'id':new.id,'title':new.gtitle,'price':new.gprice,'pic':new.gpic.name})
    #返回json
    context={'click_list':click_list,'new_list':new_list}
    return JsonResponse(context)

def list(request,tid,pindex,orderby):
    gtype=TypeInfo.objects.get(id=int(tid))
    #查询两条最新的数据
    new_list=gtype.goodsinfo_set.order_by('-id')[0:2]
    #查询指定分类tid的商品
    goods_list=GoodsInfo.objects.filter(gtype_id=int(tid))
    #根据指定规则排序
    if orderby=='1':
        goods_list=goods_list.order_by('-id')
    elif orderby=='2':
        goods_list=goods_list.order_by('-gprice')
    elif orderby=='3':
        goods_list=goods_list.order_by('-gclick')
    #进行分页
    paginator=Paginator(goods_list,10)
    pindex2=int(pindex)
    if pindex2<=0:
        pindex2=1
    elif pindex2>paginator.num_pages:
        pindex2=paginator.num_pages
    page=paginator.page(pindex2)
    context={'title':'列表页','page':page,
             'tid':tid,'gtype':gtype,'orderby':orderby,
             'new_list':new_list
            , 'cart_count':cart_count(request)}
    return render(request,'df_goods/list.html',context)

def detail(request,gid):
    goods=GoodsInfo.objects.get(pk=gid)
    goods.gclick=goods.gclick+1
    goods.save()
    #当前商品goods对应的分类，最新的两个商品
    new_list=goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    context={'title':'商品详细','goods':goods,'new_list':new_list,'cart_count':cart_count(request)}
    response=render(request,'df_goods/detail.html',context)
    # 最近浏览
    liulan=request.COOKIES.get('liulan','')
    if liulan=="":
        response.set_cookie('liulan',gid)
    else:
        liulan_list=liulan.split(',')#['6','4','1','2','3','5']
        if gid in liulan_list:#如果当前商品已经被浏览则删除
            liulan_list.remove(gid)
        #加到第一个
        liulan_list.insert(0,gid)
        #保证只有5个元素
        if len(liulan_list)>5:
            liulan_list.pop()
        liulan2=','.join(liulan_list)
        response.set_cookie('liulan',liulan2)

    return response

from haystack.views import SearchView
class MySearchView(SearchView):
    def extra_context(self):
        extra = super(MySearchView, self).extra_context()
        extra['title']=self.request.GET.get('q')
        extra['cart_count']=cart_count(self.request)
        return extra

def cart_count(request):
    if request.session.has_key('user_id'):
        return CartInfo.objects.filter(user_id=request.session['user_id']).count()
    else:
        return 0
