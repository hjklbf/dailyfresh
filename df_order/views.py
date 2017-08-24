#coding=utf-8
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db import transaction
from datetime import datetime
from df_goods.models import GoodsInfo
from df_cart.models import CartInfo
from models import *
# Create your views here.
'''
1、判断库存
2、减少库存
3、创建订单对象
4、创建详单对象
5、删除购物车
对于以上操作，应该使用事务
问题是：在django的模型类中如何使用事务？

未实现功能：
    真实支付
    物流跟踪
'''
@transaction.atomic
def order(request):
    post=request.POST
    address=post.get('address')
    cart_id=post.getlist('cart_id')

    sid = transaction.savepoint()

    try:
        # 1、新建订单对象
        order = OrderInfo()
        now = datetime.now()
        uid = request.session['user_id']
        order.oid = '%s%d' % (now.strftime('%Y%m%d%H%M%S'), uid)
        order.user_id = uid
        order.odate = now
        order.oaddress = address
        order.ototal = 0
        order.save()
        #计算总金额
        total=0
        #逐个判断购物车中的商品是可否足够库存
        for cid in cart_id:
            cart=CartInfo.objects.get(pk=cid)
            if cart.goods.gkucun>=cart.count:
                #库存足够，可以购买
                #减少库存量
                cart.goods.gkucun-=cart.count
                cart.goods.save()
                #将信息加入详单
                detail=OrderDetailInfo()
                detail.order=order
                detail.goods=cart.goods
                detail.price=cart.goods.gprice
                detail.count=cart.count
                detail.save()
                total+=cart.goods.gprice*cart.count
                #删除购物车数据
                cart.delete()
            else:
                #库存中够，中止此次下单
                transaction.savepoint_rollback(sid)
                return redirect('/cart/')
        #保存总价
        order.ototal=total
        order.save()
        transaction.savepoint_commit(sid)
        return redirect('/user/order/')
    except:
        transaction.savepoint_rollback(sid)
        return redirect('/cart/')

def pay(request,oid):
    order=OrderInfo.objects.get(pk=oid)
    order.oIsPay=True
    order.save()
    return redirect('/user/order/')
