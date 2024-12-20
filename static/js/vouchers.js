const btnDelete = document.querySelectorAll('.btn-delete')
const formDelete = document.querySelector('[form-delete]')

if (btnDelete) {
  btnDelete.forEach((btn) => {
    btn.addEventListener('click', () => {
      const confirmDelete = confirm('Xác nhận xóa khuyến mãi này?')
      if (confirmDelete) {
        const deleteID = btn.getAttribute('id')
        const inputHidden = formDelete.querySelector('[hidden]')
        inputHidden.value = deleteID
        formDelete.submit()
      }
    })
  })
}
