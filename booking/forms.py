from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import *
from django.core.exceptions import ValidationError

class ReviewForm(forms.ModelForm):
  sao = forms.IntegerField(label='Số sao', widget=forms.NumberInput(attrs={'class': 'form-control', 'max': 5, 'min': 1}), initial=5)
  class Meta:
    model = DanhGia
    exclude = ('thoi_gian', 'nguoi_dung', 'phong')
    widgets = {'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Đánh giá'})}
    labels = {'content': ''}


class OrderForm(forms.ModelForm):
  class Meta:
    model = DatPhong
    exclude = ('khach_hang', 'phong', 'trang_thai', 'tong_tien')
    widgets = {'ngay_nhan': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
              'ngay_tra': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
              'so_khach': forms.NumberInput(attrs={'class': 'form-control'}),
              'yeu_cau': forms.Textarea(attrs={'class': 'form-control'}),
              'phuong_thuc': forms.Select(attrs={'class': 'form-select'}),
              'so_tai_khoan': forms.TextInput(attrs={'class':'form-control'}),
              'ngan_hang': forms.TextInput(attrs={'class': 'form-control'}),}
    labels = {'ngay_nhan': 'Ngày nhận phòng',
              'ngay_tra': 'Ngày trả phòng',
              'so_khach': 'Số khách',
              'phuong_thuc': 'Phương thức thanh toán',
              'yeu_cau': 'Yêu cầu tới khách sạn',
              'so_tai_khoan': 'Số tài khoản',
              'ngan_hang': 'Ngân hàng'}


class VoucherForm(forms.ModelForm):
  class Meta:
    model = KhuyenMai
    fields = '__all__'
    widgets = {'phong': forms.CheckboxSelectMultiple(),
              'kieu': forms.Select(attrs={'class': 'form-control'}),
              'giam_gia': forms.NumberInput(attrs={'class': 'form-control'}),
              'ngay_bat_dau': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
              'ngay_ket_thuc': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})}
    labels = {'phong': 'Phòng áp dụng khuyến mãi',
              'kieu': 'Kiểu khuyến mãi',
              'giam_gia': 'Giảm giá',
              'ngay_bat_dau': 'Ngày bắt đầu',
              'ngay_ket_thuc': 'Ngày kết thúc',}
    
  def __init__(self, *args, **kwargs):
    user = kwargs.pop('user', None) 
    super().__init__(*args, **kwargs)
    if user and hasattr(user, 'khachsan'):
      self.fields['phong'].queryset = Phong.objects.filter(khach_san=user.khachsan)
  
  def clean_giam_gia(self):
    giam_gia = self.cleaned_data.get('giam_gia')
    kieu = self.cleaned_data.get('kieu')
    phong_selected = self.cleaned_data.get('phong')
    if kieu == 'Phần trăm':
      if not (0 <= giam_gia <= 1):
        raise ValidationError('Kiểu phần trăm thì nhập số thập phân trong khoảng từ 0 tới 1') 
    elif kieu == 'Số tiền':
      for phong in phong_selected:
        if giam_gia > phong.gia:
          raise ValidationError('Không được giảm quá số tiền của phòng')
    return giam_gia


class RoomForm(forms.ModelForm):
  class Meta:
    model = Phong
    exclude = ('khach_san', 'slug', 'trang_thai')
    widgets = {'ten': forms.TextInput(attrs={'class': 'form-control'}),
               'mo_ta': forms.Textarea(attrs={'class': 'form-control'}),
               'gia': forms.NumberInput(attrs={'class': 'form-control'}),
               'suc_chua': forms.NumberInput(attrs={'class': 'form-control'}),
               'tien_nghi': forms.CheckboxSelectMultiple(attrs={'required':False})}
    labels = {'hinh_anh1': 'Hình ảnh 1',
               'hinh_anh2': 'Hình ảnh 2',
               'hinh_anh3': 'Hình ảnh 3',
               'gia': 'Giá',
               'suc_chua': 'Sức chứa',
               'ten': 'Tên phòng',
               'mo_ta': 'Mô tả',
               'tien_nghi': 'Tiện nghi'}
    
  def __init__(self, *args, **kwargs):
    khach_san = kwargs.pop('khach_san', None)
    super().__init__(*args, **kwargs)
    self.fields['tien_nghi'].required = False
    if khach_san:
      self.fields['tien_nghi'].queryset = TienNghi.objects.filter(khach_san=khach_san)


class HotelForm(forms.ModelForm):
  class Meta:
    model = KhachSan
    exclude = ('trang_thai', 'chu_khach_san', 'slug', 'ngay_tao')
    widgets = {'dia_chi': forms.TextInput(attrs={'class': 'form-control'}),
               'dien_thoai': forms.TextInput(attrs={'class': 'form-control'}),
               'ten': forms.TextInput(attrs={'class': 'form-control'}),
               'email': forms.EmailInput(attrs={'class': 'form-control'}),
               'mo_ta': forms.Textarea(attrs={'class': 'form-control'}),
               'website': forms.URLInput(attrs={'class': 'form-control'}),}
    labels = {'hinh_anh1': 'Hình ảnh 1',
               'hinh_anh2': 'Hình ảnh 2',
               'hinh_anh3': 'Hình ảnh 3',
               'dia_chi': 'Địa chỉ khách sạn',
               'dien_thoai': 'Số điện thoai',
               'ten': 'Tên khách sạn',
               'email': 'Địa chỉ Email',
               'mo_ta': 'Mô tả',
               'website': 'Đường dẫn Website'}


class PCForm(PasswordChangeForm):
  old_password = forms.CharField(label="Mật khẩu hiện tại", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
  new_password1 = forms.CharField(label="Mật khẩu mới", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
  new_password2 = forms.CharField(label="Xác nhận mật khẩu mới", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

  class Meta:
      model = User
      fields = ['old_password', 'new_password1', 'new_password2']

  def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields['old_password'].help_text = ""
      self.fields['new_password1'].help_text = ""
      self.fields['new_password2'].help_text = ""

  
class UserForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ('email', 'first_name', 'last_name')
    widgets = {'email': forms.EmailInput(attrs={'class':'form-control'}),
               'first_name': forms.TextInput(attrs={'class':'form-control'}),
               'last_name': forms.TextInput(attrs={'class': 'form-control'})}
    labels = {'email': 'Email',
              'last_name': 'Tên', 
              'first_name': 'Họ',}


class ProfileForm(forms.ModelForm):
  class Meta:
    model = HoSo
    exclude = ('vai_tro', 'nguoi_dung')
    widgets = {'dien_thoai': forms.TextInput(attrs={'class': 'form-control', 'required': False}),
               'dia_chi': forms.TextInput(attrs={'class': 'form-control', 'required': False}),
               'ngay_sinh': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
               'gioi_tinh': forms.Select(attrs={'class': 'form-select'}),
               'cccd': forms.TextInput(attrs={'class': 'form-control'})}


class LoginForm(AuthenticationForm):
  username = forms.CharField(min_length=6, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Tài khoản')
  password = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Mật khẩu')
  error_messages = {'invalid_login': "Tên đăng nhập hoặc mật khẩu không đúng."}
  

class RegisterForm(UserCreationForm):
  class Meta:
    model = User 
    fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    widgets = {'username': forms.TextInput(attrs={'minlength': 6, 'class': 'form-control'}),
               'email': forms.EmailInput(attrs={'class':'form-control'}),
               'first_name': forms.TextInput(attrs={'class':'form-control'}),
               'last_name': forms.TextInput(attrs={'class': 'form-control'})}
    labels = {'email': 'Email', 
              'username': 'Tên đăng nhập',
              'last_name': 'Tên', 
              'first_name': 'Họ',}
    help_texts = {'username': ''}

  def __init__(self, *args, **kwargs):
    super(RegisterForm, self).__init__(*args, **kwargs)
    self.fields['password1'].widget.attrs['minlength'] = 8
    self.fields['password1'].widget.attrs['class'] = 'form-control'
    self.fields['password1'].label = 'Mật khẩu'
    self.fields['password1'].help_text = ''
    self.fields['password2'].widget.attrs['minlength'] = 8
    self.fields['password2'].widget.attrs['class'] = 'form-control'
    self.fields['password2'].label = 'Xác nhận mật khẩu'
    self.fields['password2'].help_text = ''   