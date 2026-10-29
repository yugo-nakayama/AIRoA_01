from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))
F="HeiseiKakuGo-W5"
ss=getSampleStyleSheet()
T=ParagraphStyle("t",fontName=F,fontSize=16,leading=22,spaceAfter=6)
H=ParagraphStyle("h",fontName=F,fontSize=12,leading=17,spaceBefore=8,spaceAfter=3,textColor=colors.HexColor("#1F4E79"))
B=ParagraphStyle("b",fontName=F,fontSize=9.5,leading=15)
doc=SimpleDocTemplate("outputs/説明資料_PAI最終課題_ACCOUNT.pdf",pagesize=A4,leftMargin=40,rightMargin=40,topMargin=36,bottomMargin=36)
s=[]
P=lambda t,st=B:s.append(Paragraph(t,st))
P("AI形状認識による仕分けロボットアーム",T)
P("Physical AI応用1講座 最終課題 ／ 動画：約76秒（等倍）")
P("1. 概要・目的",H)
P("天面カメラ画像からAI（多層パーセプトロン）で物体の形状（circle / square / triangle）を推論し、2リンクのロボットアームが対応するビンへ自動で仕分けるピック&amp;プレースタスクを実装した。"
  "物流・リサイクル現場での「見て判断して動かす」仕分け作業を最小構成で再現することが目的である。")
P("2. システム構成",H)
P("① 知覚：ノイズ付きカメラ画像 → 2値化・輪郭抽出で物体候補を検出<br/>"
  "② 認識（AI推論）：候補ごとに切り出したシルエット(32×32)をMLP(128-64)で3クラス分類、確信度も出力<br/>"
  "③ 判断：現在の手先位置に最も近い物体から処理（移動距離の削減）<br/>"
  "④ 計画：解析的逆運動学(IK)で目標関節角を算出、3次補間で滑らかな軌道を生成<br/>"
  "⑤ 制御：慣性・減衰を持つ関節モデルに対するPD制御（120Hz）で追従し、到達誤差を確認してから把持")
s.append(Image("data/screenshot.png",width=500,height=211))
P("図：左＝ロボット（シミュレーション）、右＝カメラ画像とAI推論結果。仕分け済み物体はビン内に蓄積。")
P("3. 工夫した点",H)
P("・<b>色に頼らない認識</b>：物体の色・大きさ・回転を毎回ランダムにし、色では判別できない設定にした。当初は濃淡画像入力で精度86%（circle/square混同）だったが、"
  "2値シルエット特徴に変更して色・明るさ不変とし、テスト精度100%に改善した。<br/>"
  "・<b>学習データの自動生成</b>：シミュレータと同じ描画関数で4,500枚の合成データを生成し、ラベル付け工数ゼロで学習（sim-to-sim）。<br/>"
  "・<b>閉ループ動作</b>：1個仕分けるごとにカメラで再認識し、仕分け済みのビン領域は認識対象から除外。到達誤差が30mmを超えた場合は把持失敗として扱う。<br/>"
  "・<b>可視化</b>：検出枠・クラス・確信度・動作フェーズを動画内に表示し、AIの判断過程を説明可能にした。")
P("4. 結果",H)
t=Table([["項目","結果"],["分類器テスト精度（900枚）","100%"],["仕分け成功（3エピソード）","15 / 15 個（正答率100%）"],["平均到達誤差","約2.2 mm"],["学習時間（CPUのみ）","約15秒"]],colWidths=[220,220])
t.setStyle(TableStyle([("FONT",(0,0),(-1,-1),F,9.5),("BACKGROUND",(0,0),(-1,0),colors.HexColor("#DDEBF7")),("GRID",(0,0),(-1,-1),0.5,colors.grey)]))
s.append(t)
P("5. 考察・今後の展開",H)
P("・本実装は2D・合成画像のため認識が容易であり、実カメラでは照明・影・重なりへの対応（CNN化、データ拡張、ドメインランダム化）が必要。<br/>"
  "・把持は位置一致で簡略化しており、物理エンジン（Gazebo / Genesis）での把持力・接触の再現が次の課題。<br/>"
  "・発展案：ROS 2 + Gazeboへの移植、SO-101等の実機アームでの検証、自然言語指示（例：「三角だけ集めて」）によるタスク指定。")
P("6. 実行方法",H)
P("pip install -r requirements.txt → python vision.py（学習）→ python main.py（実行・動画出力）。依存：numpy, OpenCV, scikit-learn。")
doc.build(s)
