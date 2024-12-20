from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from .forms import *
from .models import *
from django.contrib import messages
from django.utils import timezone

# Create your views here.
def home(request):
  khachsans = KhachSan.objects.all()
  return render(request, 'home.html', {'khachsans': khachsans})

def login(request):
  form = LoginForm(data=request.POST or None)
  if request.POST:
    if form.is_valid():
      auth.login(request, form.get_user())
      return redirect('/')
  return render(request, 'login.html', {'form': form})

def register(request):
  form = RegisterForm(request.POST or None)
  profile_form = ProfileForm(request.POST or None)
  if request.POST:
    if form.is_valid():
      user = form.save()
      profile = profile_form.save(commit=False)
      profile.nguoi_dung = user
      profile.vai_tro = request.POST.get('vai_tro')
      profile.save()
      auth.login(request, user)
      return redirect('/')
  return render(request, 'register.html', {'form': form, 'profile_form': profile_form})

def logout(request):
  auth.logout(request)
  return redirect('/')

def my(request):
  if request.user.is_authenticated:
    return render(request, 'my.html')
  else:
    return redirect('login')
  
def edit(request):
  if request.user.is_authenticated:
    u_form = UserForm(request.POST or None, instance=request.user)
    p_form = ProfileForm(request.POST or None, instance=request.user.hoso)
    if request.POST:
      if u_form.is_valid() and p_form.is_valid():
        u_form.save()
        p_form.save()
        messages.success(request, 'Cập nhật thông tin thành công')
        return redirect('my')
    return render(request, 'edit.html', {'u_form': u_form, 'p_form': p_form})
  else:
    return redirect('login')
  
def change_password(request):
  form = PCForm(user=request.user, data=request.POST or None)
  if request.POST:
    if form.is_valid():
      user = form.save()
      auth.update_session_auth_hash(request, user)
      messages.success(request, 'Cập nhật mật khẩu thành công')
      return redirect('my')
  return render(request, 'change_password.html', {'form': form})

def create_hotel(request):
  if request.user.is_authenticated and request.user.hoso.vai_tro == 'Khách sạn' and not hasattr(request.user, 'khachsan'):
    form = HotelForm(request.POST or None, request.FILES or None)
    if request.POST:
      if form.is_valid():
        hotel = form.save(False)
        hotel.chu_khach_san = request.user
        hotel.save()
        messages.success(request, 'Bạn đã mở khách sạn thành công')
        return redirect('my')
    return render(request, 'create_hotel.html', {'form': form})
  else:
    return redirect('my')

def edit_hotel(request):
  if request.user.is_authenticated and request.user.hoso.vai_tro == 'Khách sạn' and hasattr(request.user, 'khachsan'):
    form = HotelForm(request.POST or None, request.FILES or None, instance=request.user.khachsan)
    if request.POST:
      if form.is_valid():
        form.save()
        messages.success(request, 'Sửa thông tin thành công')
        return redirect('my')
    return render(request, 'edit_hotel.html', {'form': form})
  else:
    return redirect('my')
  
def hotel_detail(request, hotel_slug):
  hotel = get_object_or_404(KhachSan, slug=hotel_slug)
  return render(request, 'hotel_detail.html', {'hotel': hotel})

def create_room(request):
  if request.user.is_authenticated and hasattr(request.user, 'khachsan'):
    form = RoomForm(request.POST or None, request.FILES or None, khach_san=request.user.khachsan)
    if request.POST:
      if form.is_valid():
        new_room = form.save(False)
        new_room.khach_san = request.user.khachsan
        new_room.save()
        form.save_m2m()
        list_tien_nghi_new = [tn.capitalize() for tn in request.POST.getlist('tien_nghi_moi')]
        exist_tien_nghi = TienNghi.objects.filter(khach_san=request.user.khachsan).values_list('ten', flat=True)
        new_tien_nghi_instances = []
        for tn in list_tien_nghi_new:
          if tn not in exist_tien_nghi:
            new_tien_nghi = TienNghi.objects.create(khach_san=request.user.khachsan, ten=tn)
            new_tien_nghi_instances.append(new_tien_nghi)
        new_room.tien_nghi.add(*new_tien_nghi_instances)   
        messages.success(request, "Tạo phòng thành công")
        return redirect('hotel_detail', request.user.khachsan.slug)  
      else:
        print(form.errors)   
    return render(request, 'create_room.html', {'form': form})
  else:
    return redirect('/')
  
def room_detail(request, hotel_slug, room_slug):
  room = get_object_or_404(Phong, khach_san__slug=hotel_slug, slug=room_slug, trang_thai=True)
  voucher = room.khuyenmais.filter(ngay_ket_thuc__gte=timezone.now().date()).last()
  if voucher:
    if voucher.kieu == 'Phần trăm':
      room.gia_uu_dai = room.gia - room.gia*voucher.giam_gia
      km = f'{round(voucher.giam_gia * 100, 0)}%'
    else:
      room.gia_uu_dai = room.gia - voucher.giam_gia
      km = f'{round(voucher.giam_gia, 0)}VND'
  else:
    km = None
  if request.user.is_authenticated:
    for order in request.user.phongdats.all():
      if order.phong == room and order.ngay_tra >= timezone.now().date() and (order.trang_thai == 'Chờ xác nhận' or order.trang_thai == 'Đã xác nhận'):
        room.ordered = True
      if order.phong == room and order.ngay_tra + timezone.timedelta(days=7) >= timezone.now().date() and order.trang_thai == 'Đã hoàn thành' and request.user.phanhois.filter(phong=room).count() < request.user.phongdats.filter(phong=room, trang_thai='Đã hoàn thành').count():
        room.allow_review = True
    room.is_enjoyed = request.user.yeuthichs.filter(phong=room).exists()
    if request.POST:
      action = request.POST.get('action', '')
      if action:
        enjoy, created = YeuThich.objects.get_or_create(nguoi_dung=request.user, phong=room)
        if not created:
          enjoy.delete()
          messages.success(request, 'Đã bỏ yêu thích phòng này')
        else:
          messages.success(request, 'Đã thêm phòng vào danh sách yêu thích')
        return redirect('room_detail', room.khach_san.slug, room.slug)
  form = OrderForm(request.POST or None)
  if request.POST:
    if form.is_valid():
      order = form.save(False)
      order.khach_hang = request.user
      order.phong = room
      order.tong_tien = request.POST.get('tong_tien')
      order.save()
      messages.success(request, 'Đặt phòng thành công')
      return redirect('/')
  form_rv = ReviewForm(request.POST or None)
  if request.POST:
    if form_rv.is_valid():
      review = form_rv.save(False)
      review.nguoi_dung = request.user
      review.phong = room
      review.save()
      messages.success(request, 'Đã gửi đánh giá')
      return redirect('/')
  return render(request, 'room_detail.html', {'room': room, 'form': form, 'form_rv': form_rv, 'km':km})
  
def edit_room(request, room_slug):
  room = get_object_or_404(Phong, slug=room_slug)
  if request.user.is_authenticated and hasattr(request.user, 'khachsan') and request.user.khachsan == room.khach_san:
    form = RoomForm(request.POST or None, request.FILES or None, instance=room, khach_san=request.user.khachsan)
    if request.POST:
      if form.is_valid():
        room_update = form.save()
        list_tien_nghi_new = [tn.capitalize() for tn in request.POST.getlist('tien_nghi_moi')]
        exist_tien_nghi = TienNghi.objects.filter(khach_san=request.user.khachsan).values_list('ten', flat=True)
        new_tien_nghi_instances = []
        for tn in list_tien_nghi_new:
          if tn not in exist_tien_nghi:
            new_tien_nghi = TienNghi.objects.create(khach_san=request.user.khachsan, ten=tn)
            new_tien_nghi_instances.append(new_tien_nghi)
        room_update.tien_nghi.add(*new_tien_nghi_instances)  
        messages.success(request, 'Chỉnh sửa thành công')
        return redirect('room_detail', request.user.khachsan.slug, room_update.slug)
    return render(request, 'edit_room.html', {'form':form})
  else:
    return redirect('/')
  
def rooms(request):
  if request.user.is_authenticated and hasattr(request.user, 'khachsan'):
    phongs = request.user.khachsan.phongs.all()
    if request.POST:
      room_id = request.POST.get('room_id')
      action = request.POST.get('action')
      room = get_object_or_404(Phong, id=room_id)
      if action == 'stop':
        room.trang_thai = False
        room.save()
        messages.success(request, 'Đã ngừng hoạt động')
      if action == 'active':
        room.trang_thai = True
        room.save()
        messages.success(request, 'Đã hoạt động lại')
      if action == 'delete':
        room.delete()
        messages.success(request, 'Đã xóa phòng')
      return redirect('rooms')
    return render(request, 'rooms.html', {'phongs': phongs})
  else:
    return redirect('my')
  
def create_voucher(request):
  if request.user.is_authenticated and hasattr(request.user, 'khachsan'):
    form = VoucherForm(request.POST or None, user=request.user)
    if request.POST:
      if form.is_valid():
        form.save()
        messages.success(request, 'Tạo khuyến mãi thành công')
        return redirect('vouchers')
    return render(request, 'create_voucher.html', {'form': form})
  else:
    return redirect('/')
  
def vouchers(request):
  if request.user.is_authenticated and hasattr(request.user, 'khachsan'):
    phongs = request.user.khachsan.phongs.all()
    khuyenmais = KhuyenMai.objects.filter(phong__in=phongs).distinct()
    for km in khuyenmais:
      if km.kieu == 'Phần trăm':
        km.giam_gia = km.giam_gia * 100
      km.trang_thai = 'Hết hạn' if km.ngay_ket_thuc < timezone.now().date() else 'Đang áp dụng'
    if request.POST:
      id_delete = request.POST.get('id_delete', '')
      if id_delete:
        KhuyenMai.objects.get(id=id_delete).delete()
        messages.success(request, 'Đã xóa voucher')
        return redirect('vouchers')
    return render(request, 'vouchers.html', {'vouchers': khuyenmais})
  else:
    return redirect('/')
  
def edit_voucher(request, id_km):
  km = get_object_or_404(KhuyenMai, id=id_km)
  if request.user.is_authenticated and hasattr(request.user, 'khachsan') and request.user.khachsan == km.phong.first().khach_san:
    form = VoucherForm(request.POST or None, instance=km, user=request.user)
    if request.POST:
      if form.is_valid():
        form.save()
        messages.success(request, 'Chỉnh sửa khuyến mãi thành công')
        return redirect('vouchers')
    return render(request, 'edit_voucher.html', {'form': form})
  else:
    return redirect('/')
  
def my_order(request):
  if request.user.is_authenticated and request.user.hoso.vai_tro == 'Khách thuê':
    orders = request.user.phongdats.all()
    if request.POST:
      id_order = request.POST.get('order_id')
      cancel_order = get_object_or_404(DatPhong, id=id_order)
      cancel_order.trang_thai = 'Đã hủy'
      cancel_order.save()
      messages.success(request, 'Hủy phòng thành công')
      return redirect('my')
    return render(request, 'my_order.html', {'orders': orders})
  else:
    return redirect('my')
  
def orders(request):
  if request.user.is_authenticated and hasattr(request.user, 'khachsan'):
    donhangs = DatPhong.objects.filter(phong__khach_san=request.user.khachsan)
    status = request.GET.get('status', '')
    if status:
      if status == 'Tất cả':
        donhangs = donhangs.order_by('-thoi_gian')
      elif status == 'Đã hủy':
        donhangs = donhangs.filter(trang_thai='Đã hủy')
      elif status == 'Chờ xác nhận':
        donhangs = donhangs.filter(trang_thai='Chờ xác nhận')
      elif status == 'Đã xác nhận':
        donhangs = donhangs.filter(trang_thai='Đã xác nhận')
      else:
        donhangs = donhangs.filter(trang_thai='Đã hoàn thành')
    if request.POST:
      action = request.POST.get('action')
      id_order = request.POST.get('order_id')
      order = get_object_or_404(DatPhong, id=id_order)
      if action == 'confirm':
        order.trang_thai = 'Đã xác nhận'
        order.save()
        messages.success(request, 'Đã xác nhận đặt phòng')
      if action == 'complete':
        order.trang_thai = 'Đã hoàn thành'
        order.save()
        messages.success(request, 'Đã xác nhận hoàn thành dịch vụ')
      return redirect('orders')
    return render(request, 'orders.html', {'orders': donhangs, 'status': status})
  else:
    return redirect('/')
  
def order_detail(request, id_order):
  if request.user.is_authenticated and hasattr(request.user, 'khachsan'):
    order = get_object_or_404(DatPhong, id=id_order, phong__khach_san = request.user.khachsan)
    if request.POST:
      action = request.POST.get('action')
      if action == 'confirm':
        order.trang_thai = 'Đã xác nhận'
        order.save()
        messages.success(request, 'Đã xác nhận đặt phòng')
      if action == 'complete':
        order.trang_thai = 'Đã hoàn thành'
        order.save()
        messages.success(request, 'Đã xác nhận hoàn thành dịch vụ')
      return redirect('orders')
    return render(request, 'order_detail.html', {'order': order})
  else:
    return redirect('/')
  
def my_hotel(request):
  if request.user.is_authenticated and request.user.hoso.vai_tro == 'Khách sạn':
    if hasattr(request.user, 'khachsan'):
      hotel = request.user.khachsan
      return render(request, 'my_hotel.html', {'hotel': hotel})
    else:
      return render(request, 'my_hotel.html')
  else:
    return redirect('my')
  
def search(request):
  q = request.GET.get('q', '')
  if q:
    hotels = KhachSan.objects.filter(ten__icontains=q)
    rooms = Phong.objects.filter(ten__icontains=q)
    return render(request, 'search.html', {'hotels': hotels, 'rooms':rooms, 'q': q})
  else:
    return render(request, 'search.html')
  
def my_enjoy(request):
  if request.user.is_authenticated and request.user.hoso.vai_tro=='Khách thuê':
    enjoys = request.user.yeuthichs.all()
    return render(request, 'my_enjoy.html', {'enjoys': enjoys})
  else:
    return redirect('my')