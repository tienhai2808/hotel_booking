def relationship(request):
  cokhachsan = hasattr(request.user, 'khachsan')
  return {'cokhachsan': cokhachsan}