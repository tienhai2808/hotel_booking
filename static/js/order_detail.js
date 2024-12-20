const formAction = document.querySelector('[form-action]')
const btnAction = formAction.querySelector('button')
btnAction.addEventListener('click', () => {
  const typeAction = btnAction.getAttribute('action')
  if (typeAction === 'confirm') {
    const confirmOrder = confirm('Xác nhận đặt đơn đặt phòng?')
    if (confirmOrder) {
      formAction.submit()
    }
  } else {
    const confirmComplete = confirm('Xác nhận đã hoàn thành dịch vụ?')
    if (confirmComplete) {
      formAction.submit()
    }
  }
})