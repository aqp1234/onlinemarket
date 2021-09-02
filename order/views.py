from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.models import User
from cart.models import Cart
from .models import Order, OrderPrepare
import requests, json, random

# Create your views here.
def index(request):
    login_user = request.user
    try:
        cart = Cart.objects.get(user=login_user)
        cartitems = cart.cartitems.all()
    except Cart.DoesNotExist:
        return redirect('cart:index')
    now = timezone.now()
    order_id = now.strftime('%Y%m%d') + '-' + login_user.username + "" + str(int(random.random() * 100000000))
    if request.method == 'POST':
        url = 'https://kapi.kakao.com/v1/payment/ready'
        headers = {'Authorization': 'KakaoAK 7561e4c258228f56b204f8a7e48eab69', 'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'}
        params = {
            'cid': 'TC0ONETIME',
            'partner_order_id': order_id,
            'partner_user_id': login_user.id,
            'item_name': cartitems[0].product.name + '외 ' + (cartitems.count() - 1) + '개' if cartitems.count() > 1 else cartitems[0].product.name,
            'quantity': cart.get_quantity(),
            'total_amount': int(cart.get_cart_total()),
            'tax_free_amount': 0,
            'approval_url': 'http://127.0.0.1:8000/order/success/',
            'cancel_url': 'http://127.0.0.1:8000/order/cancel/',
            'fail_url': 'http://127.0.0.1:8000/order/fail/',
        }
        res = requests.post(url, headers=headers, params=params)
        tid = res.json()['tid']
        redirect_url = res.json()['next_redirect_pc_url']
        try:
            _orderprepare = OrderPrepare.objects.get(user=login_user)
            _orderprepare.tid = tid
            _orderprepare.order_id = ''
            _orderprepare.order_id = order_id
            _orderprepare.save()
        except OrderPrepare.DoesNotExist:
            OrderPrepare.objects.create(user=login_user, tid=tid, order_id=order_id)
        return redirect(redirect_url)
    else:
        return render(request, 'order/index.html')

def success(request):
    login_user = request.user
    _orderprepare = OrderPrepare.objects.get(user=login_user)
    print(_orderprepare.order_id[0])
    pg_token = request.GET.get('pg_token', None)
    if pg_token is None:
        return redirect('/')
    url = 'https://kapi.kakao.com/v1/payment/approve'
    headers = {'Authorization': 'KakaoAK 7561e4c258228f56b204f8a7e48eab69', 'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'}
    params = {
        'cid': 'TC0ONETIME',
        'tid': _orderprepare.tid,
        'partner_order_id': _orderprepare.order_id,
        'partner_user_id': login_user.id,
        'pg_token': pg_token,
    }
    res = requests.post(url, headers=headers, params=params)
    data = res.json()
    print(data)
    partner_user_id = User.objects.get(id=data['partner_user_id'])
    sid = None
    card_info = None
    if 'sid' in data:
        sid = data['sid']
    if 'card_info' in data:
        card_info = data['card_info']
    print(card_info)
    Order.objects.create(
        aid=data['aid'],
        tid=data['tid'],
        cid=data['cid'],
        sid=sid,
        partner_order_id=data['partner_order_id'],
        partner_user_id=partner_user_id,
        payment_method_type=data['payment_method_type'],
        amount=data['amount'],
        card_info=card_info,
        item_name=data['item_name'],
        quantity=data['quantity'],
        created=data['created_at'],
        approved=data['approved_at'],
    )
    return redirect('/')
        
