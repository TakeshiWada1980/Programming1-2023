import pygame as pg

# 初期化処理・グローバル変数
scale_factor = 3
chip_s = int(24*scale_factor) # マップチップ基本サイズ
map_s  = pg.Vector2(16,9)     # マップの横・縦の配置数 

# PlayerCharacterクラスの定義
class PlayerCharacter:

  # コンストラクタ
  def __init__(self,init_pos,img_path):
    self.pos  = pg.Vector2(init_pos)
    self.size = pg.Vector2(24,32)*scale_factor
    self.dir  = 2
    img_raw = pg.image.load(img_path)
    self.__img_arr = []
    for i in range(4):
      self.__img_arr.append([])
      for j in range(3):
        p = pg.Vector2(24*j,32*i)
        tmp = img_raw.subsurface(pg.Rect(p,(24,32)))
        tmp = pg.transform.scale(tmp, self.size)
        self.__img_arr[i].append(tmp)
      self.__img_arr[i].append(self.__img_arr[i][1])

    # 移動アニメーション関連
    self.is_moving = False  # 移動処理中は True になるフラグ
    self.__moving_vec = pg.Vector2(0,0) # 移動方向ベクトル
    self.__moving_acc = pg.Vector2(0,0) # 移動微量の累積

  def turn_to(self,dir):
    self.dir = dir

  def move_to(self,vec):
    self.is_moving = True
    self.__moving_vec = vec.copy()
    self.__moving_acc = pg.Vector2(0,0)
    self.update_move_process()
  
  def update_move_process(self):
    assert self.is_moving
    self.__moving_acc += self.__moving_vec * 3
    if self.__moving_acc.length() >= chip_s:
      self.pos += self.__moving_vec
      self.is_moving = False

  def get_dp(self):
    dp = self.pos*chip_s - pg.Vector2(0,12)*scale_factor
    if self.is_moving :  # キャラ状態が「移動中」なら
      dp += self.__moving_acc # 移動微量の累積値を加算
    return dp
  
  def get_img(self,frame):
    return self.__img_arr[self.dir][frame//6%4]

# ゲームループを含むメイン処理
def main():

  # 初期化処理
  pg.init() 
  pg.display.set_caption('ぼくのかんがえたさいきょうのげーむ II')
  map_s  = pg.Vector2(16,9)     # マップの横・縦の配置数 
  disp_w = int(chip_s*map_s.x)
  disp_h = int(chip_s*map_s.y)
  screen = pg.display.set_mode((disp_w,disp_h))
  clock  = pg.time.Clock()
  font   = pg.font.Font(None,15)
  frame  = 0
  exit_flag = False
  exit_code = '000'

  # グリッド設定
  grid_c = '#bbbbbb'

  # 自キャラ移動関連
  cmd_move = -1 # 移動コマンドの管理変数
  cmd_move_km = [pg.K_w, pg.K_d, pg.K_s, pg.K_a]
  m_vec = [
    pg.Vector2(0,-1),  # 0: 上移動 
    pg.Vector2(1,0),   # 1: 右移動
    pg.Vector2(0,1),   # 2: 下移動
    pg.Vector2(-1,0)   # 3: 左移動
  ] 

  # 自キャラの生成・初期化
  reimu = PlayerCharacter((2,3),'./data/img/reimu.png')

  # ゲームループ
  while not exit_flag:

    # システムイベントの検出
    for event in pg.event.get():
      if event.type == pg.QUIT: # ウィンドウ[X]の押下
        exit_flag = True
        exit_code = '001'

    # キー状態の取得
    key = pg.key.get_pressed()
    cmd_move = -1
    for i, k in enumerate(cmd_move_km):
      cmd_move = i if key[k] else cmd_move
  
    # 背景描画
    screen.fill(pg.Color('WHITE'))

    # グリッド
    for x in range(0, disp_w, chip_s): # 縦線
      pg.draw.line(screen,grid_c,(x,0),(x,disp_h))
    for y in range(0, disp_h, chip_s): # 横線
      pg.draw.line(screen,grid_c,(0,y),(disp_w,y))

    # 移動コマンドの処理
    if not reimu.is_moving :
      if cmd_move != -1:
        reimu.turn_to(cmd_move)
        af_pos = reimu.pos + m_vec[cmd_move] # 移動(仮)した座標
        if (0 <= af_pos.x <= map_s.x-1) and (0 <= af_pos.y <= map_s.y-1) :
          reimu.move_to(m_vec[cmd_move]) # 画面範囲内なら移動指示

    # キャラが移動中ならば、移動アニメ処理の更新
    if reimu.is_moving:
      reimu.update_move_process()

    # 自キャラの描画
    screen.blit(reimu.get_img(frame),reimu.get_dp())

    # フレームカウンタの描画
    frame += 1
    frm_str = f'{frame:05}'
    screen.blit(font.render(frm_str,True,'BLACK'),(10,10))
    screen.blit(font.render(f'{reimu.pos}',True,'BLACK'),(10,20))
    
    # 画面の更新と同期
    pg.display.update()
    clock.tick(30)

  # ゲームループ [ここまで]
  pg.quit()
  return exit_code

if __name__ == "__main__":
  code = main()
  print(f'プログラムを「コード{code}」で終了しました。')