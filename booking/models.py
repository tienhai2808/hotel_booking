from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone

# Create your models here.
class HoSo(models.Model):
  nguoi_dung = models.OneToOneField(User, on_delete=models.CASCADE)
  dien_thoai = models.CharField(max_length=10, blank=True, null=True)
  dia_chi = models.CharField(max_length=200, blank=True, null=True)
  ngay_sinh = models.DateField(blank=True, null=True)
  gioi_tinh = models.CharField(max_length=6, choices=(('Nam', 'Nam'), ('Nữ', 'Nữ')), blank=True, null=True)
  cccd = models.CharField(max_length=12, blank=True, null=True)
  vai_tro = models.CharField(max_length=15, choices=(('Khách thuê', 'Khách thuê'), ('Khách sạn', 'Khách sạn')), default='Khách thuê')
  
  def __str__(self):
    return f'Hồ sơ của {self.nguoi_dung}'
  
  
class KhachSan(models.Model):
  chu_khach_san = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'hoso__vai_tro': 'Khách sạn'})
  ten = models.CharField(max_length=150)
  slug = models.SlugField(max_length=150, blank=True, null=True)
  hinh_anh1 = models.ImageField(upload_to='hotel_images/')
  hinh_anh2 = models.ImageField(upload_to='hotel_images/')
  hinh_anh3 = models.ImageField(upload_to='hotel_images/')
  dia_chi = models.CharField(max_length=250)
  dien_thoai = models.CharField(max_length=10)
  website = models.URLField(max_length=255)
  email = models.EmailField(max_length=255)
  mo_ta = models.TextField()
  trang_thai = models.CharField(max_length=30, choices=[('Đang hoạt động', 'Đang hoạt đông'), ('Ngừng hoạt đông', 'Ngừng hoạt động')], default='Đang hoạt động')
  ngay_tao = models.DateField(auto_now_add=True)
  
  def __str__(self):
    return self.ten
  
  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.ten)
    super().save(*args, **kwargs)
  

class TienNghi(models.Model):
  ten = models.CharField(max_length=100)
  khach_san = models.ForeignKey(KhachSan, on_delete=models.CASCADE)
  
  def __str__(self):
    return self.ten


class Phong(models.Model):
  ten = models.CharField(max_length=150)
  slug = models.SlugField(max_length=150, blank=True, null=True)
  khach_san = models.ForeignKey(KhachSan, on_delete=models.CASCADE, related_name='phongs')
  hinh_anh1 = models.ImageField(upload_to='room_images/')
  hinh_anh2 = models.ImageField(upload_to='room_images/')
  hinh_anh3 = models.ImageField(upload_to='room_images/')
  gia = models.DecimalField(max_digits=10, decimal_places=0)
  suc_chua = models.IntegerField()
  tien_nghi = models.ManyToManyField(TienNghi)
  mo_ta = models.TextField()
  trang_thai = models.BooleanField(default=True)
  
  def __str__(self):
    return self.ten
  
  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.ten)
    super().save(*args, **kwargs)
  

class KhuyenMai(models.Model):
  phong = models.ManyToManyField(Phong, blank=True, related_name='khuyenmais')
  kieu = models.CharField(max_length=20, choices=(('Phần trăm', 'Phần trăm'), ('Số tiền', 'Số tiền')))
  giam_gia = models.DecimalField(max_digits=10, decimal_places=2)
  ngay_bat_dau = models.DateField()
  ngay_ket_thuc = models.DateField()
  

class DatPhong(models.Model):
  thoi_gian = models.DateTimeField(auto_now_add=True)
  khach_hang = models.ForeignKey(User, on_delete=models.CASCADE, related_name='phongdats')
  phong = models.ForeignKey(Phong, on_delete=models.CASCADE, related_name='datphongs')
  ngay_nhan = models.DateField()
  ngay_tra = models.DateField()
  so_khach = models.IntegerField(default=1)
  yeu_cau = models.TextField(blank=True, null=True)
  phuong_thuc = models.CharField(max_length=50,
                                choices=[('Thanh toán tại quầy', 'Thanh toán tại quầy'), ('Thanh toán chuyển khoản', 'Thanh toán chuyển khoản')],
                                default='Thanh toán tại quầy')
  so_tai_khoan = models.CharField(max_length=20, blank=True, null=True)
  ngan_hang = models.CharField(max_length=70, blank=True, null=True)
  trang_thai = models.CharField(max_length=30,
                                choices=[('Chờ xác nhận', 'Chờ xác nhận'), ('Đã hủy', 'Đã hủy'), ('Đã xác nhận', 'Đã xác nhận'), ('Đã hoàn thành', 'Đã hoàn thành')], default='Chờ xác nhận')
  tong_tien = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
  
  def __str__(self):
    return f'Đặt phòng: {self.khach_hang} - {self.phong}'
    
  
class DanhGia(models.Model):
  phong = models.ForeignKey(Phong, on_delete=models.CASCADE, related_name='danhgias')
  nguoi_dung = models.ForeignKey(User, on_delete=models.CASCADE, related_name='phanhois')
  sao = models.IntegerField()
  content = models.TextField()
  thoi_gian = models.DateTimeField(auto_now_add=True)
  
  
class YeuThich(models.Model):
  nguoi_dung = models.ForeignKey(User, on_delete=models.CASCADE, related_name='yeuthichs')
  phong = models.ForeignKey(Phong, on_delete=models.CASCADE, related_name='quantams')
  
  class Meta:
    unique_together = ('nguoi_dung', 'phong')
    