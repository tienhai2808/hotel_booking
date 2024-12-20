const formAction = document.querySelector('[form-action]')

const btnStops = document.querySelectorAll('.btn-stop')
if (btnStops.length > 0) {
  btnStops.forEach((btn) => {
    btn.addEventListener('click', () => {
      const confirmStop = confirm('Xác nhận ngừng hoạt động phòng này?')
      if (confirmStop) {
        formAction.querySelector('.id-hidden').value = btn.getAttribute('id')
        formAction.querySelector('.action-hidden').value = 'stop'
        formAction.submit()
      }
    })
  })
}

const btnActives = document.querySelectorAll('.btn-active')
if (btnActives.length > 0) {
  btnActives.forEach((btn) => {
    btn.addEventListener('click', () => {
      const confirmActive = confirm('Xác nhận hoạt động lại phòng này?')
      if (confirmActive) {
        formAction.querySelector('.id-hidden').value = btn.getAttribute('id')
        formAction.querySelector('.action-hidden').value = 'active'
        formAction.submit()
      }
    })
  })
}

const btnDeletes = document.querySelectorAll('.btn-delete')
if (btnDeletes.length > 0) {
  btnDeletes.forEach((btn) => {
    btn.addEventListener('click', () => {
      const confirmDelete = confirm('Xác nhận xóa phòng này?')
      if (confirmDelete) {
        formAction.querySelector('.id-hidden').value = btn.getAttribute('id')
        formAction.querySelector('.action-hidden').value = 'delete'
        formAction.submit()
      }
    })
  })
}