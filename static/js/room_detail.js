const divForm = document.querySelector('.div-form')
const orderForm = divForm.querySelector('.order-form')
const btnClose = document.querySelector('[btn-x]')
const btnOrder = document.querySelector('.btn-order')
const checkUser = btnOrder.getAttribute('user')

btnOrder.addEventListener('click', () => {
  if (!checkUser) {
    window.location.href = '/login/'
  } else {
    if (divForm.classList.contains('d-none')) {
      divForm.classList.remove('d-none')
    }
  }
})

btnClose.addEventListener('click', () => {
  if (!divForm.classList.contains('d-none')) {
    divForm.classList.add('d-none')
  }
})

const soKhachInput = document.querySelector('#id_so_khach');
const soLuongKhach = document.querySelector('.so-khach').textContent
soKhachInput.setAttribute('max', parseInt(soLuongKhach))

const selectMethod = orderForm.querySelector('#id_phuong_thuc')
const paymentBank = orderForm.querySelector('.tt-nh')
selectMethod.addEventListener('change', () => {
  if (selectMethod.value === 'Thanh toán chuyển khoản') {
    paymentBank.classList.remove('d-none')
    paymentBank.querySelectorAll('input').forEach((input) => {
      input.setAttribute('required', true)
    })
  } else {
    paymentBank.classList.add('d-none')
    paymentBank.querySelectorAll('input').forEach((input) => {
      input.removeAttribute('required');
    })
  }
})

const ngayNhanInput = document.querySelector('#id_ngay_nhan'); 
const ngayTraInput = document.querySelector('#id_ngay_tra');   
const soTienElement = document.querySelector('.so-tien');      
const giaPhongElement = document.querySelector('.gia-phong');  
const today = new Date();
const formattedToday = today.toISOString().split('T')[0];

ngayNhanInput.min = formattedToday;
ngayTraInput.min = formattedToday;

ngayNhanInput.addEventListener('change', () => {
  const ngayNhanValue = ngayNhanInput.value;

  if (ngayNhanValue) {
    const ngayNhanDate = new Date(ngayNhanValue);
    const ngayTraMinDate = new Date(ngayNhanDate);
    ngayTraMinDate.setDate(ngayTraMinDate.getDate() + 1);
    const formattedNgayTraMin = ngayTraMinDate.toISOString().split('T')[0];
    ngayTraInput.min = formattedNgayTraMin;
    if (new Date(ngayTraInput.value) <= new Date(ngayNhanValue)) {
      ngayTraInput.value = '';
    }
  }
});


const giaPhong = parseFloat(giaPhongElement.textContent.trim().replace(/\./g, ''));
const inputHidden = orderForm.querySelector('[hidden]')

function calculateTotal() {
  const ngayNhan = new Date(ngayNhanInput.value);
  const ngayTra = new Date(ngayTraInput.value);

  if (!isNaN(ngayNhan) && !isNaN(ngayTra) && ngayTra > ngayNhan) {
    const millisecondsPerDay = 24 * 60 * 60 * 1000;
    const soNgay = Math.ceil((ngayTra - ngayNhan) / millisecondsPerDay);

    const tongTien = soNgay * giaPhong;
    soTienElement.textContent = tongTien.toLocaleString('vi-VN');
    inputHidden.value = tongTien
  } else {
    soTienElement.textContent = '0';
    inputHidden.value = ''
  }
}

ngayNhanInput.addEventListener('change', calculateTotal);
ngayTraInput.addEventListener('change', calculateTotal);
