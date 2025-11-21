# 第6章 演習問題

# Exercise 6.1

エピソード中に価値関数 $V$ が変化する場合、式 (6.6) は厳密には成り立たない。
TD 誤差 (6.5) と TD 更新 (6.2) で用いる価値関数を、時刻 $t$ における値の配列 $V_t$ とする。
(6.6) の導出をやり直し、**モンテカルロ誤差と一致させるために TD 誤差の和に加えるべき追加項**を求めよ。

## 回答

#### ● 前提

一般のリターン：

$$
G_t = R_{t+1} + \gamma G_{t+1}
$$

Monte Carlo 誤差：

$$
G_t - V_t(S_t)
$$

TD 誤差（価値が時刻ごとに変化する場合）：

$$
\delta_k = R_{k+1} + \gamma V_k(S_{k+1}) - V_k(S_k)
$$

ここで $V_k$ は「時刻 $k$ での価値関数」。

#### ● Step 1： $R_{k+1}$ の分解

まず、TD 誤差になる形を作るために、
次を足して引く：

$$
+\gamma V_k(S_{k+1}) - \gamma V_k(S_{k+1})
$$

すると：

$$
\begin{aligned}
R_{k+1}
&= \bigl(R_{k+1} + \gamma V_k(S_{k+1}) - V_k(S_k)\bigr)
\
&\qquad + \bigl(V_t(S_k) - V_k(S_k)\bigr)
\
&\qquad - \gamma\bigl(V_t(S_{k+1}) - V_k(S_{k+1})\bigr)
\end{aligned}
$$

第1項は TD 誤差 $\delta_k$：

$$
R_{k+1}
= \delta_k + (V_t(S_k)-V_k(S_k)) - \gamma(V_t(S_{k+1})-V_k(S_{k+1}))
$$

#### ● Step 2：これを $G_t - V_t(S_t)$ に代入

$$
\begin{aligned}
G_t - V_t(S_t)
&= \sum_{k=t}^{T-1} \gamma^{k-t} R_{k+1} - V_t(S_t) \\
&= \sum_{k=t}^{T-1} \gamma^{k-t} \Big[
\delta_k + (V_t(S_k)-V_k(S_k)) - \gamma(V_t(S_{k+1})-V_k(S_{k+1}))
\Big] - V_t(S_t)
\end{aligned}
$$

#### ● Step 3：整理して補正項を明確化

$$
\begin{aligned}
G_t - V_t(S_t)
&= \sum_{k=t}^{T-1} \gamma^{k-t}\delta_k
\
&\quad + \sum_{k=t}^{T-1}\gamma^{k-t}(V_t(S_k)-V_k(S_k))
\
&\quad - \sum_{k=t}^{T-1}\gamma^{k-t+1}(V_t(S_{k+1})-V_k(S_{k+1}))
\
&\quad - V_t(S_t)
\end{aligned}
$$

第2・3項・最後の項をまとめると：

$$
\sum_{k=t}^{T-1} \gamma^{k-t} \Big[
(V_t(S_k)-V_k(S_k)) - \gamma(V_t(S_{k+1})-V_k(S_{k+1}))
\Big] - V_t(S_t)
$$

添字のずれを直してまとめると以下の形に整理できる。

#### ● 結論：

$$
\boxed{
G_t - V_t(S_t) = \sum_{k=t}^{T-1} \gamma^{k-t} \delta_k + \sum_{k=t}^{T-1} \gamma^{k-t} \Big[
(V_t(S_{k+1}) - V_k(S_{k+1})) - (V_t(S_k) - V_k(S_k))
\Big]
}
$$

#### ● 検算

* **もし $V_k = V_t$（価値がエピソード中に固定）なら**
  補正項は 0 になる：

$$
(V_t - V_k) = 0
$$

よって

$$
G_t - V(S_t)
= \sum_{k=t}^{T-1} \gamma^{k-t}\delta_k
$$


# Exercise 6.2

「家に運転して帰る」例を用いて、なぜ TD 法が Monte Carlo 法より効率的になり得るか説明せよ。
特に、**過去の経験の一部を再利用できる状況**ではどのように TD が有利になるかを述べよ。

## 回答

#### ● シナリオ

* 旧ビル → 家というルートを長期間運転していた
* 高速道路入口以降の価値はよく学習されている
* 新しいビルから出発するが、高速道路入口は同じ位置

#### ● MC の弱点

Monte Carlo 法はスタート地点 $S_0$ の更新のために、
**家まで完全に走り切った後の $G_0$ が必要**。

→ 「新ビル → 家まで」1 回走り切るまで、 $V(S_0)$  を更新できない\
→ サンプル効率が低い

#### ● TD(0) の強み

TD(0) は部分的なブートストラップ：

$$
V(S_t) \leftarrow V(S_t) + \alpha (R_{t+1} + V(S_{t+1}) - V(S_t))
$$

高速入口 $S_{\text{enter}}$ に着いた瞬間、
**$V(S_{\text{enter}})$ は過去の経験からすでに良い値になっている**。

したがって、新ビル直後の状態 $S_0$ は、

$$
V(S_0) \leftarrow V(S_0) + \alpha (R_1 + V(S_1) - V(S_0))
$$

により、**家まで行かなくても良い推定が得られる**。

→ **環境の一部だけが変わった場合、TD が圧倒的に効率的**


# Exercise 6.3

Random Walk 左図（TD(0)）で、最初のエピソード後に状態  $A$  のみ値が変化している。

(1) 何が起きたことを意味するか？\
(2) なぜ  $A$  だけ更新されたのか？\
(3) どれだけ変化したか？

## 回答

#### (1) 最初のエピソード

図から、 $A$  だけが少し減少している：

$$
C \to B \to A \to 0
$$

と左端に落ちたことを示す。

#### (2) なぜ A だけか（TD(0) の性質）

TD(0) は

$$
V(S_t) \leftarrow V(S_t)+\alpha (R_{t+1}+V(S_{t+1})-V(S_t))
$$

最後の遷移は $A \to 0$（ $V(0)=0$ ）。
**この 1 ステップだけ更新されるため、A のみが変化。**

#### (3) 更新量

初期値 $0.5$、報酬 0、 $\alpha=0.1$ ：

$$
V(A) \leftarrow 0.5 + 0.1 (0 - 0.5)
= 0.45
$$

変化量は $-0.05$。


# Exercise 6.4

右図の結果はステップサイズ $\alpha$ に依存する。
より広い $\alpha$ を用いた場合、結論（TD の方が良い）は変わるか？
極端に良い $\alpha$ は存在するか？

## 回答

#### ● 結論

* どの $\alpha$ を使っても **TD の方が MC より RMS 誤差が低い傾向は変わらない**
* 結論がひっくり返るような特別な $\alpha$ は存在しない

#### ● 理由

1. **MC は分散が高い**

   完全リターン $G_t$ に依存するためエピソードのノイズを大きく受ける。

2. **TD はベルマン構造を利用**

   $R + V(S_{t+1})$ を使うため少ないサンプルで滑らかな推定値が得られる。

3. **$\alpha$ を変えても本質は不変**

   大きくすれば両者揺れるが MC の方が顕著。
   小さくすれば遅いが TD の優位性は変わらない。


# Exercise 6.5

右図では TD の RMS 誤差が一度下がり、その後上がっている。
高い $\alpha$ で顕著である。この原因は何か？
常に起きるのか？
初期値の取り方で変わるか？

## 回答

#### ● 原因

* 大きい $\alpha$ では **ブートストラップ誤差が増幅**され、推定値が振動しやすい
* 初期値（0.5）と真値に大きなギャップがある
* 初期は急速に改善するが、その後に振動成分が支配し RMS が上昇

#### ● 常に起きるか？

* **いいえ**。
* 小さな $\alpha$ や良い初期値ではほとんど起こらない。

#### ● 初期値依存

* 真値から大きくズレた初期値（例：全部 0.5）だと揺れやすい
* 真値に近い初期化をすると振動はほぼ無くなる


# Exercise 6.6

Random Walk の真値

$$
1/6,2/6,3/6,4/6,5/6
$$

はどのように計算できるか？少なくとも 2 通り挙げよ。
著者が使った方法はどれか？

## 回答

#### ● 方法1：吸収確率（解析解）

Random Walk を位置  $0,1,2,3,4,5,6$  の対称ランダムウォークとみなす。
右端 6 に到達する確率は、古典的結果より

$$
\Pr(\text{右端へ到達}\mid \text{位置 } i) = \frac{i}{6}
$$

よって

* $A$（位置1）： $1/6$
* $B$（位置2）： $2/6$
* $C$（位置3）： $3/6$
* $D$（位置4）： $4/6$
* $E$（位置5）： $5/6$

#### ● 方法2：ベルマン連立方程式を解く

終端 $V(0)=0,;V(6)=1$
中間 5 状態は以下の 5 元連立方程式：

$$
\begin{aligned}
V(A) &= \tfrac{1}{2}V(0) + \tfrac{1}{2}V(B) \\
V(B) &= \tfrac{1}{2}V(A) + \tfrac{1}{2}V(C) \\
V(C) &= \tfrac{1}{2}V(B) + \tfrac{1}{2}V(D) \\
V(D) &= \tfrac{1}{2}V(C) + \tfrac{1}{2}V(E) \\
V(E) &= \tfrac{1}{2}V(D) + \tfrac{1}{2}V(6)
\end{aligned}
$$

これを解くと

$$
V(A)=\frac16,;
V(B)=\frac26,;
V(C)=\frac36,;
V(D)=\frac46,;
V(E)=\frac56
$$

#### ● 著者が実際に使ったと思われる方法

図の真値が**完全な直線でノイズがない**ため、

* サンプリングではなく
* **解析（方法1）またはベルマン連立（方法2）**

を使ったと推測される。


# Exercise 6.7

ターゲット方策 $\pi$ と、これをカバーする行動方策 $b$ がある。
1ステップ重要度サンプリング比 $\rho_{t:t}$（式 5.3）を用いるとして、
**オフポリシー版 TD(0) 更新式**を設計せよ。

## 回答

#### ● 重要度サンプリング比（1 ステップ）

式 (5.3) より、1ステップでは：

$$
\rho_t
= \frac{\pi(A_t\mid S_t)}{b(A_t\mid S_t)}
$$

#### ● 通常の TD(0)

$$
V(S_t)
\leftarrow
V(S_t)
+
\alpha \left( R_{t+1} + \gamma V(S_{t+1}) - V(S_t) \right)
$$

これは「行動方策＝ターゲット方策」のオンポリシー更新。

#### ● オフポリシー化の考え方

行動は $b$ に従っているので、
「もし $\pi$ がこの行動を選んでいたら」
という重み付けが必要。

そこで TD 誤差に $\rho_t$ を掛ける：

$$
\delta_t = R_{t+1} + \gamma V(S_{t+1}) - V(S_t)
$$

更新は：

$$
V(S_t)
\leftarrow
V(S_t)
+
\alpha \rho_t , \delta_t
$$

### ■ 結論：オフポリシー TD(0)

$$
\boxed{
V(S_t) \gets V(S_t) + \alpha \frac{\pi(A_t\mid S_t)}{b(A_t\mid S_t)} \left(
R_{t+1} * \gamma V(S_{t+1}) - V(S_t)
\right)
}
$$

これは行動方策 $b$ による経験から、
ターゲット方策 $\pi$ の価値を学習する 1-step オフポリシー TD である。


# Exercise 6.8

行動価値版の (6.6) を示せ。

## 回答

本問は、状態価値版の式 (6.6)

$$
G_t - V(S_t)
= \sum_{k=t}^{T-1} \gamma^{k-t} \delta_k
$$

と**同じ構造を、行動価値関数 $Q$ に対して示す**ことが目的である。
ただし、一般の割引率 $\gamma$ を含む場合を扱う。

#### ● Step 1：リターンの定義を使う

一般のリターン $G_t$ は

$$
G_t = R_{t+1} + \gamma G_{t+1}
$$

で定義される。
これを左辺に代入すると：

$$
G_t - Q(S_t,A_t)
= R_{t+1} + \gamma G_{t+1} - Q(S_t,A_t)
$$

#### ● Step 2：TD 誤差の形を作るために足して引く

行動価値版 TD 誤差は：

$$
\delta_t
= R_{t+1} + \gamma Q(S_{t+1},A_{t+1}) - Q(S_t,A_t)
$$

これを現れさせるために

$$
+\gamma Q(S_{t+1},A_{t+1}) - \gamma Q(S_{t+1},A_{t+1})
$$

を足して引くと：

$$
\begin{aligned}
G_t - Q(S_t,A_t)
&= \underbrace{ R_{t+1} + \gamma Q(S_{t+1},A_{t+1}) - Q(S_t,A_t) }_{\delta_t} + \gamma \left( G_{t+1} - Q(S_{t+1},A_{t+1}) \right)
\end{aligned}
$$

#### ● Step 3：同じ形を繰り返し展開

次にも同じ展開が使え：

$$
G_{t+1} - Q(S_{t+1},A_{t+1})
= \delta_{t+1} + \gamma \left( G_{t+2} - Q(S_{t+2},A_{t+2}) \right)
$$

よって：

$$
G_t - Q(S_t,A_t)
= \delta_t + \gamma\delta_{t+1} + \gamma^2\delta_{t+2} + \cdots  + \gamma^{T-t-1}\delta_{T-1} + \gamma^{T-t}(G_T - Q(S_T,A_T))
$$

終端では
** $G_T = 0$ 、 $Q(S_T,A_T)=0$ **
（終端は価値 0）
なので最後の項は 0 になる。

#### ● 結論：行動価値版の (6.6)

$$
\boxed{
G_t - Q(S_t,A_t)
= \sum_{k=t}^{T-1} \gamma^{k-t} \delta_k 
}
$$

これは、状態価値版の式 (6.6)

$$
G_t - V(S_t)=\sum_{k=t}^{T-1} \gamma^{k-t} \delta_k
$$

に一致する。


# Exercise 6.11

なぜ Q-learning は off-policy だと言えるのか？

## 回答
「行動方策（実際に経験を生成する方策）と、学習している価値を最大化する方策（ターゲット方策）が異なる」ため。

実際には探索方策で行動しているが、Q-learning は “最良の行動を選んだと仮定した更新” をしている。

Q-learning の更新は：

$$
Q(S_t, A_t) \leftarrow Q(S_t, A_t) + \alpha \left(R_{t+1} + \gamma \max_a Q(S_{t+1}, a) - Q(S_t, A_t) \right)
$$

ここで重要なのは、次の状態 $S_{t+1}$ の価値として $\max_a Q(S_{t+1}, a)$ を使っていること。
これは 「次は常に最良行動を取る」 と仮定した学習になっている。

一方で、実際に行動を選ぶときは：
- ε-greedy
- softmax
- またはランダム探索

など、**最良行動ではない行動を選ぶ方策（行動方策）**を使う。

つまり、行動方策とターゲット方策が異なる = Off-policy であると言える。

- 行動方策（experience policy / behavior policy）
  - 例：ε-greedy、探索のためにランダムが混ざる
- ターゲット方策（target policy）
  - 常に argmax
  - 最適方策 $\pi^*(s) = \arg \max_a Q(s,a)$

#### ● SARSA（On-policy）との比較

SARSA の更新：

$$
Q(S_t, A_t)
\leftarrow Q(S_t, A_t) + \alpha \left( R_{t+1} + \gamma Q(S_{t+1}, A_{t+1}) - Q(S_t, A_t) \right)
$$

ここでは 実際に行う次の行動 $A_{t+1}$ を使う。つまり 行動方策そのものの価値を学んでいる = On-policy である。


# Exercise 6.12

行動選択が常に greedy ならば、Q-learning と SARSA は同じアルゴリズムになるか？

## 回答

No.

行動選択が常に greedy でも、Q-learning と SARSA は 完全に同じアルゴリズムにはならないし、同じ更新を行わない。

SARSA は on-policy（実際に選んだ行動で更新）\
Q-learning は off-policy（最良行動を仮定して更新）

この違いは greedy でも残る。

#### ● 理由①：SARSA は「実際に選んだ行動」を参照し、Q-learning は「max のみ」を参照する

SARSA は $Q$ の値が全く同じでも、わずかな差や決め方の癖（tie-breaking）があると：

$$
A_{t+1} = \text{one of the argmax actions}
$$

を取る。

Q-learning も argmax を取るが、
実行する行動と学習のための行動が同じとは限らない。

SARSA は `行動選択の決定 → 更新式に反映 → 次の行動選択にも影響` という“連鎖”がある。

Q-learning は `次状態の最大値だけ見る → 現在の行動選択には影響しない`

#### ● 理由 ②：ステップごとの「Q値の変化順」が異なるため、時間発展が一致しない

両者の更新式は似ていても、

- SARSA：次の行動を決めた瞬間、その行動の $Q$ 値を使う
- Q-learning：常に max の $Q$ 値を使う

という違いにより、

$Q$ の値の更新順序が異なる\
→ $Q$ の値は同じ軌道を通らず、最終的に収束値は同じでも経路は異なる。

これにより、行動選択も微妙に変わることがある。


# Exercise 6.13

$\epsilon$-greedy ターゲット方策を用いた二重期待SARSA 更新式はどのようになるか？

## 回答

#### ● SARSA 更新式
通常の期待 SARSA 更新式は：

$$
\begin{aligned}
Q(S_t, A_t)
& \leftarrow Q(S_t, A_t) + \alpha \Big[ R_{t+1} + \gamma \mathbb{E} \left[ Q(S_{t+1}, A_{t+1}) \mid S_{t+1} \right] - Q(S_t, A_t) \Big]
\\
& \leftarrow Q(S_t, A_t) + \alpha \Big[ R_{t+1} + \gamma \sum_a \pi(a \mid S_{t+1}) Q(S_{t+1}, a) - Q(S_t, A_t) \Big]
\end{aligned}
$$

#### ● 二重 SARSA の更新式
$Q_1$ の更新式は:

$$
\begin{aligned}
Q_1(S_t, A_t)
& \leftarrow Q_1(S_t, A_t) + \alpha \Bigg[ R_{t+1} + \gamma \sum_a \pi(a \mid S_{t+1}) Q_2(S_{t+1}, a) - Q_1(S_t, A_t) \Bigg]
\end{aligned}
$$

$Q_2$ の更新式は:

$$
\begin{aligned}
Q_2(S_t, A_t)
& \leftarrow Q_2(S_t, A_t) + \alpha \Bigg[ R_{t+1} + \gamma \sum_a \pi(a \mid S_{t+1}) Q_1(S_{t+1}, a) - Q_2(S_t, A_t) \Bigg]
\end{aligned}
$$

#### ● $\epsilon$-greedy 方策の場合
$\epsilon$-greedy 方策の場合、 $\pi(a \mid S_{t+1})$ は次のようになる：

$$
\pi(a \mid S_{t+1})
= \begin{cases}
1 - \epsilon + \frac{\epsilon}{|\mathcal{A}(S_{t+1})|} & \text{if } a = \arg\max_{a'} Q(S_{t+1}, a') \\
\frac{\epsilon}{|\mathcal{A}(S_{t+1})|} & \text{otherwise}
\end{cases}
$$

これを二重期待 SARSA の更新式に代入すると、 $\epsilon$-greedy ターゲット方策を用いた二重期待 SARSA 更新式が得られる。


＃ Exercise 6.14

Jack’s Car Rental（例 4.2）を afterstate で再定式化したらどうなるか？なぜ収束が速くなるか？

## 回答

afterstate 化することで問題が「貸出・返却の確率を考える必要のない状態価値学習」になる。\
→ 収束が速くなる。

#### ● 再定式化
例 4.2 における状態は、各営業所にある車の台数の組み合わせで表される。

$$
S_t = (n_1, n_2)
$$

ここで  $n_1$ は営業所 1 の車の台数、 $n_2$ は営業所 2 の車の台数。

行動 $a$ は、夜間に営業所間で移動させる車の台数であるから、状態の変化は次のように表される：

$$
S_{t} \xrightarrow{a} (n_1 - a, n_2 + a)
$$

その後、翌朝にPoisson分布に従う確率的な貸出・返却イベントが発生し、新しい状態 $S_{t+1}$ になる。

$$
(n_1 - a, n_2 + a) \xrightarrow{\text{Poisson}} S_{t+1}
$$

行動 $a$ は決定的に状態を変化させるため、afterstate $S_{t}^a$ を次のように定義できる：

$$
S_{t}^a = (n_1 - a, n_2 + a)
$$

つまり、行動 $a$ を取った直後の状態である。

価値関数 $V$ を afterstate に対して定義すると：

$$
V(S_{t}^a) = \mathbb{E} \left[ R_{t} + \gamma V(S_{t+1}) \mid S_{t}^a \right]
$$

ここで、 $R_{t}$  、 $S_{t+1}$ は Poisson 分布に従う貸出・返却イベントの結果として得られる報酬と次の状態である。

#### ● 収束が速くなる理由
- ① 行動の決定的遷移を状態表現から消すことができる。
- ② Poisson の確率遷移を afterstate に集約できる。
