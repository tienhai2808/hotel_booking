const formRoom = document.querySelector('[form-room]')
const inputFiles = formRoom.querySelectorAll('input[type="file"]')
inputFiles.forEach((input) => {
  input.classList.add('form-control')
})


const btnAdd = document.querySelector(".btn-add");
const divTienNghi = document.querySelector('#div-tiennghi')

btnAdd.addEventListener('click', () => {
  const newTienNghi = document.createElement('div')
  newTienNghi.classList.add('new-tiennghi', 'd-flex', 'align-items-center', 'mt-2');

  const inputTienNghi = document.createElement('input');
  inputTienNghi.type = 'text';
  inputTienNghi.name = 'tien_nghi_moi';
  inputTienNghi.classList.add('form-control');
  inputTienNghi.placeholder = 'Nhập tiện nghi mới';

  const btnClose = document.createElement('div');
  btnClose.classList.add('div-close')
  btnClose.innerHTML = `<i class="fa-regular fa-circle-xmark close-button"></i>`;
  btnClose.addEventListener('click', () => {
    newTienNghi.remove(); 
  });
  newTienNghi.appendChild(inputTienNghi);
  newTienNghi.appendChild(btnClose);

  divTienNghi.appendChild(newTienNghi);
})