const selectRole = document.querySelector('#role')
const profileForm = document.querySelector('#profile-form')
selectRole.addEventListener('change', () => {
  const isHotel = selectRole.value === 'Khách sạn';
  profileForm.classList.toggle('d-none', !isHotel);
  profileForm.querySelectorAll('input').forEach(input => input.required = isHotel);
  const selectForm = profileForm.querySelector('select');
  if (selectForm) selectForm.required = isHotel;
})