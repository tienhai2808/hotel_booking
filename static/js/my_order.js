const btnCancels = document.querySelectorAll('.btn-cancel')
const formCancel = document.querySelector('[form-cancel]')

if (btnCancels.length > 0) {
  btnCancels.forEach((btn) => {
    btn.addEventListener('click', () => {
      const paymentMethod = btn.getAttribute('method')
      if (paymentMethod == 'Thanh toán chuyển khoản') {
        const confirmCancel = confirm('Bạn đã thanh toán tiền phòng rồi, bạn vẫn muốn hủy chứ?')
        if (confirmCancel) {
          formCancel.querySelector('[hidden]').value = btn.getAttribute('id')
          formCancel.submit()
        }
      } else {
        const confirmCancel = confirm('Bạn chắc chắn hủy phòng chứ?')
        if (confirmCancel) {
          formCancel.querySelector('[hidden]').value = btn.getAttribute('id')
          formCancel.submit()
        }
      }
    })
  })
}