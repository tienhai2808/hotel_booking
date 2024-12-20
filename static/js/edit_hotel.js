const formHotel = document.querySelector('[form-hotel]')
const inputFiles = formHotel.querySelectorAll('input[type="file"]')
inputFiles.forEach((input) => {
  input.classList.add('form-control')
})