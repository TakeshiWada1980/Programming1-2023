%reset -f
class MyVector2 :

  # コンストラクタの定義
  def __init__(self,init_x,init_y):
    assert type(init_x) == int or type(init_x) == float
    assert type(init_y) == int or type(init_y) == float
    self.x = float(init_x)
    self.y = float(init_y)
  
  # メソッド length の定義
  def length(self):
    return (self.x**2 + self.y**2)**0.5
  
  # メソッド normalize の定義
  def normalize(self):
    t = self.length()
    assert t != 0  # 大きさゼロの単位ベクトルはNG
    return [self.x/t,self.y/t]
  
  # メソッド scale_by の定義
  def scale_by(self,factor):
    assert type(factor) == int or type(factor) == float
    self.x *= factor
    self.y *= factor

# ここから MyVector をテストするコード
vec = MyVector2(2,3)
print(type(vec))
print(vec.x)
print(vec.length())
print(vec.normalize())

vec.scale_by(3)
print(f'[{vec.x},{vec.y}]')