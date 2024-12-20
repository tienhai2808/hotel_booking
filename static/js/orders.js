const formAction = document.querySelector('[form-action]')
const btnConfirms = document.querySelectorAll('.btn-confirm')
const btnComplete = document.querySelectorAll('.btn-complete')
if (btnConfirms.length > 0) {
  btnConfirms.forEach((btn) => {
    btn.addEventListener('click', () => {
      const confirmOrder = confirm('Xác nhận đặt đơn đặt phòng?')
      if (confirmOrder) {
        formAction.querySelector('.id-hidden').value = btn.getAttribute('id')
        formAction.querySelector('.action-hidden').value = 'confirm'
        formAction.submit()
      }
    })
  })
}
if (btnComplete.length > 0) {
  btnComplete.forEach((btn) => {
    btn.addEventListener('click', () => {
      const confirmComplete = confirm('Xác nhận đã hoàn thành dịch vụ?')
      if (confirmComplete) {
        formAction.querySelector('.id-hidden').value = btn.getAttribute('id')
        formAction.querySelector('.action-hidden').value = 'complete'
        formAction.submit()
      }
    })
  })
}

const formStatus = document.querySelector('.form-status')
const selectStatus = formStatus.querySelector('#select-status')
selectStatus.addEventListener('change', () => {
  formStatus.submit()
})