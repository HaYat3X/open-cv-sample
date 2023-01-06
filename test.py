import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from glob import glob

# 比較もと画像、比較さき画像
moto_gazo, saki_gazos = 'base_gazo.png', sorted(glob('./PNG/*.png'))

# 正規化時の一辺のサイズ
size = 8

# 画像の正規化
def normalize(file):
    img = Image.open(file)
    img = img.convert('L').resize((size, size), Image.LANCZOS)  # 圧縮とグレースケール化
    px = np.array(img)  # 画像を配列化
    avg = px.mean()  # 画素値の平均値
    px = 1 * (px < avg) # 平均より小さい要素を１にする
    return px

# 比較もと画像、比較さき画像の正規化後の配列（ピクセル値
moto_gazo_px = normalize(moto_gazo)
saki_gazos_px = [normalize(saki_gazo) for saki_gazo in saki_gazos]

# 比較もと画像と一致したピクセルの個数合計
match_cnt = [(moto_gazo_px == saki_gazo_px).sum() for saki_gazo_px in saki_gazos_px]

# /////類似判定と可視化/////
datas = {
    '比較さき画像名': saki_gazos,
    '一致px数': match_cnt,
    '不一致px数': [(size*size)-m for m in match_cnt],
    '類似度': [(m/(size*size))*100 for m in match_cnt]
}

df = pd.DataFrame(datas)
similar = 80 # 合格ライン
df['判定'] = ['OK' if x >= similar else 'NG' for x in df['類似度']]

# 比較もと画像
img = Image.open(moto_gazo)
display(img)
print('比較もと画像名:', moto_gazo)
print('-'*50)
print('')

# 比較さき画像群
for saki_gazo in saki_gazos:
    img = Image.open(saki_gazo)
    display(img)
    display(df[df.比較さき画像名==saki_gazo])
    print('')