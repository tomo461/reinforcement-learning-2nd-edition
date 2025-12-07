# 第13章 演習問題

# Exercise 13.1

例13.1において、右へ進む行動を選択する最適な確率について、グリッドワールドとその動力学に関する知識を用いて、厳密な記号的表現を求めよ。

## 解答

非終端状態は区別できないと定義されているため、ポリシーは以下のように表せる。

$$
\begin{align*}
\pi(right \mid s) &= p \\
\pi(left \mid s) &= 1 - p \\
p &\in [0, 1]
\end{align*}
$$

状態遷移のダイナミクスは以下の通りである。

$$
\begin{align*}
P(S'= S_2 \mid S=S_1, A=right) &= p \\
P(S'= S_1 \mid S=S_1, A=left) &= 1 - p \\
P(S'= S_1 \mid S=S_2, A=right) &= p \\
P(S'= S_3 \mid S=S_2, A=left) &= 1 - p \\
P(S'= S_4 \mid S=S_3, A=right) &= p \\
P(S'= S_2 \mid S=S_3, A=left) &= 1 - p
\end{align*}
$$

ポリシー $\pi$ のもとでの状態価値関数 $v_\pi(S)$ は以下のように表せる。ただし、報酬はすべての遷移で $r = -1$ とし、割引率を $\gamma = 1$ とする。

$$
\begin{align*}
v_\pi(S_1) &= p [r + \gamma v_\pi(S_2)] + (1 - p)[r + \gamma v_\pi(S_1)] \\
&= r + p \gamma v_\pi(S_2) + (1 - p) \gamma v_\pi(S_1) \\
&= -1 + p v_\pi(S_2) + (1 - p) v_\pi(S_1) \\
v_\pi(S_2) &= p [r + \gamma v_\pi(S_1)] + (1 - p)[r + \gamma v_\pi(S_3)] \\
&= r + p \gamma v_\pi(S_1) + (1 - p) \gamma v_\pi(S_3) \\
&= -1 + p v_\pi(S_1) + (1 - p) v_\pi(S_3) \\
v_\pi(S_3) &= p [r + \gamma v_\pi(S_4)] + (1 - p)[r + \gamma v_\pi(S_2)] \\
&= r + p \gamma v_\pi(S_4) + (1 - p) \gamma v_\pi(S_2) \\
&= -1 + p v_\pi(S_4) + (1 - p) v_\pi(S_2) \\
v_\pi(S_4) &= 0
\end{align*}
$$

これらの方程式を解いて $v_\pi(S_1)$ を求める。

$$
\begin{align*}
v_\pi(S_1) - (1 - p) v_\pi(S_1) &= -1 + p v_\pi(S_2) \\
p v_\pi(S_1) &= -1 + p v_\pi(S_2) \\
v_\pi(S_1) &= v_\pi(S_2) - \frac{1}{p} \quad \cdots (1)
\end{align*}
$$

$v_\pi(S_4)=0$ なので、

$$
v_\pi(S_3) = -1 + (1 - p) v_\pi(S_2) \quad \cdots (2)
$$

式(1)と(2)を $v_\pi(S_2)$ の式に代入する。

$$
\begin{align*}
v_\pi(S_2) &= -1 + p \left( v_\pi(S_2) - \frac{1}{p} \right) + (1 - p) \left( -1 + (1 - p) v_\pi(S_2) \right) \\
&= -1 + p v_\pi(S_2) - 1 - (1 - p) + (1 - p)^2 v_\pi(S_2) \\
&= p - 3 + (p + (1 - p)^2) v_\pi(S_2) \\
&= p - 3 + (p + 1 - 2p + p^2) v_\pi(S_2) \\
&= p - 3 + (1 - p + p^2) v_\pi(S_2)
\end{align*}
$$

整理すると、

$$
\begin{align*}
v_\pi(S_2) - (1 - p + p^2) v_\pi(S_2) &= p - 3 \\
v_\pi(S_2) (1 - 1 + p - p^2) &= p - 3 \\
v_\pi(S_2) (p - p^2) &= p - 3 \\
v_\pi(S_2) &= \frac{p - 3}{p(1 - p)}
\end{align*}
$$

これを式(1)に代入して $v_\pi(S_1)$ を求める。

$$
\begin{align*}
v_\pi(S_1) &= \frac{p - 3}{p(1 - p)} - \frac{1}{p} \\
&= \frac{p - 3 - (1 - p)}{p(1 - p)} \\
&= \frac{2p - 4}{p(1 - p)}
\end{align*}
$$

最適な確率 $p$ を求めるために、 $v_\pi(S_1)$ を $p$ で微分して $0$ になる点を求める。

$$
\frac{d v_\pi(S_1)}{dp} = \frac{2(p - p^2) - (2p - 4)(1 - 2p)}{(p - p^2)^2}
$$

分子が $0$ になる条件を求める。

$$
\begin{align*}
2(p - p^2) - (2p - 4)(1 - 2p) &= 0 \\
2p - 2p^2 - (2p - 4p^2 - 4 + 8p) &= 0 \\
2p - 2p^2 - (10p - 4p^2 - 4) &= 0 \\
2p - 2p^2 - 10p + 4p^2 + 4 &= 0 \\
2p^2 - 8p + 4 &= 0 \\
p^2 - 4p + 2 &= 0
\end{align*}
$$

解の公式より、

$$
p = \frac{4 \pm \sqrt{16 - 8}}{2} = 2 \pm \sqrt{2}
$$

$p \in [0, 1]$ であるため、最適な確率は

$$
p = 2 - \sqrt{2} \approx 0.586 \approx 0.59
$$

となる。


# Exercise 13.2

177ページの枠内、方策勾配定理(13.5)、方策勾配定理の証明（289ページ）、そしてREINFORCEアルゴリズムの更新式(13.8)に至るまでの流れを一般化せよ。
このとき、式(13.8)に係数 $\gamma^t$ が加わる形とし、疑似コードで与えられた一般的なアルゴリズムと一致するようにせよ。

## 解答

### 1. オンポリシー分布（177ページの枠内）の一般化

割引率 $\gamma$ を考慮に入れると、これは状態訪問の期待回数を重み付けする役割を果たす。エピソード的タスクにおいて、 $\gamma < 1$ の場合、 $\gamma$ は各ステップでの非終端確率として機能していると解釈できる。

状態 $s$ でエピソードが開始される確率を $h(s)$ とし、ポリシー $\pi$ に従って状態 $s$ が訪問される「割引された」期待回数を $\eta(s)$ とすると、その再帰関係は以下のように一般化される（式(9.2)に $\gamma$ を導入）。

$$
\eta(s) = h(s) + \sum_{\bar{s}} \eta(\bar{s}) \gamma \sum_{a} \pi(a|\bar{s}) p(s|\bar{s}, a)
$$

ここで、 $\gamma$ が次の状態 $\bar{s}$ から $s$ への遷移確率を重み付けているため、早く訪問される状態ほど、その後の学習に与える影響が大きくなる。

この割引された訪問回数の合計を正規化することで、割引されたオンポリシー分布 $\mu(s)$ が得られる（ソースの式(9.3)に対応）。

$$
\mu(s) = \frac{\eta(s)}{\sum_{s'} \eta(s')}
$$

### 2. 方策勾配定理の一般化（式 13.5）

割引率 $\gamma$ を含むエピソード的な設定では、性能尺度 $J(\boldsymbol{\theta}) = v_{\pi}(S_0)$ の勾配 $\nabla J(\boldsymbol{\theta})$ は、各時点 $t$ での行動の対数勾配 $\nabla \ln \pi(A_t|S_t, \boldsymbol{\theta})$ が、その時点からの割引収益 $G_t$ と、さらに $\boldsymbol{\theta}$ の探索開始時点からの割引率 $\gamma^t$ によってスケーリングされたものの期待値に比例する（291ページ）。

$\nabla J(\boldsymbol{\theta})$ の厳密な勾配表現は、行動の対数勾配 $\nabla \ln \pi(a|s, \boldsymbol{\theta})$ と行動価値関数 $q_{\pi}(s, a)$ を用いて、状態 $s$ の割引された訪問頻度 $\eta(s)$ の重み付き和として表現できる（式(13.5)に相当する勾配の期待値形式を保持）。

$$
\nabla J(\boldsymbol{\theta}) \propto \sum_{s} \eta(s) \sum_{a} q_{\pi}(s, a) \nabla \pi(a|s, \boldsymbol{\theta})
$$

### 3. 方策勾配定理の証明の一般化（289ページ）

状態価値関数の勾配 $\nabla v_{\pi}(s)$ は、行動価値関数 $q_{\pi}(s, a)$ を用いて以下のように再帰的に展開される（証明の最初のステップ）。

$$
\nabla v_{\pi}(s) = \sum_{a} \left[ \nabla \pi(a|s) q_{\pi}(s, a) + \pi(a|s) \nabla q_{\pi}(s, a) \right]
$$

ここで、 $\nabla q_{\pi}(s, a)$ の展開には $\gamma$ が含まれる（式(3.19)と(3.2)の勾配をとる）。

$$
\nabla q_{\pi}(s, a) = \nabla \sum_{s', r} p(s', r | s, a) \left[ r + \gamma v_{\pi}(s') \right] = \sum_{s'} p(s'|s, a) \gamma \nabla v_{\pi}(s')
$$

これを $\nabla v_{\pi}(s)$ の式に代入し、展開を繰り返すと、 $\nabla v_{\pi}(s)$ は、状態 $s$ から到達可能な全ての状態 $x$ における $\gamma^t$ で割引された期待勾配の和として表される（証明の最後のステップに相当）。

$$
\nabla v_{\pi}(s) = \sum_{x} \sum_{t=0}^{\infty} \text{Pr}(s \to x, t, \pi) \gamma^t \sum_{a} \nabla \pi(a|x) q_{\pi}(x, a)
$$

ここで、 $s=S_0$ とすると $\nabla J(\boldsymbol{\theta}) = \nabla v_{\pi}(S_0)$ が得られる。
この式を方策勾配定理に比例する形式に書き直すことができる。

$$
\nabla J(\boldsymbol{\theta}) \propto \sum_{s} \eta(s) \sum_{a} q_{\pi}(s, a) \nabla \pi(a|s, \boldsymbol{\theta})
$$

### 4. REINFORCE更新則（式 13.8）の一般化

勾配 $\nabla J(\boldsymbol{\theta})$ のサンプリング表現を導出するにあたり、上記で得られた勾配表現の期待値を取る。

勾配の期待値は、ポリシー $\pi$ に従う状態-行動のサンプリングによって表現される（式(13.8)の導出過程を一般化）。

$$
\nabla J(\boldsymbol{\theta}) = \mathbb{E}_{\pi} \left[ \sum_{t=0}^{T} \gamma^t G_t \frac{\nabla \pi(A_t|S_t, \boldsymbol{\theta})}{\pi(A_t|S_t, \boldsymbol{\theta})} \right]
$$

一般化されたREINFORCE更新式は、以下のようになる。

$$
\boldsymbol{\theta}_{t+1} = \boldsymbol{\theta}_t + \alpha \gamma^t G_t \frac{\nabla \pi(A_t|S_t, \boldsymbol{\theta}_t)}{\pi(A_t|S_t, \boldsymbol{\theta}_t)}
$$

この形式は、擬似コードにおいて $G$ が $\sum_{k=t+1}^T \gamma^{k-t-1} R_k$ であり、更新に $\gamma^t$ が乗算される形と一致する。

以上により、割引率 $\gamma$ を考慮に入れた方策勾配定理とREINFORCEアルゴリズムの一般化が完成した。


# Exercise 13.3

13.1節では、戦型の行動優先度(13.3)を用いた行動優先度のソフトマックスによる方策のパラメータ化について検討した。このパラメータ化に対して、適格度ベクトルが

$$
\nabla \ln \pi(a|s, \boldsymbol{\theta}) = \mathbf{x}(s, a) - \sum_{b} \pi(b|s, \boldsymbol{\theta}) \mathbf{x}(s, b)
$$

となることを、定義と基本的な微分法を用いて示せ。

## 解答

方策 $\pi(a|s, \boldsymbol{\theta})$ は、行動優先度

$$h(s, a, \boldsymbol{\theta}) = \boldsymbol{\theta}^T \mathbf{x}(s, a)
$$

のソフトマックス関数として定義される。

$$
\pi(a|s, \boldsymbol{\theta}) = \frac{e^{h(s, a, \boldsymbol{\theta})}}{\sum_{b} e^{h(s, b, \boldsymbol{\theta})}}
$$

これを用いると、

$$
\begin{align*}
\nabla \ln \pi(a|s, \boldsymbol{\theta}) &= \nabla \ln \left( \frac{e^{h(s, a, \boldsymbol{\theta})}}{\sum_{b} e^{h(s, b, \boldsymbol{\theta})}} \right) \\
&= \nabla \left( h(s, a, \boldsymbol{\theta}) - \ln \left( \sum_{b} e^{h(s, b, \bold{\theta})} \right) \right) \\
&= \nabla h(s, a, \boldsymbol{\theta}) - \nabla \ln \left( \sum_{b} e^{h(s, b, \boldsymbol{\theta})} \right)
\end{align*}
$$

ここで、 $h(s, a, \boldsymbol{\theta}) = \boldsymbol{\theta}^T \mathbf{x}(s, a)$ であるため、

$$
\nabla h(s, a, \boldsymbol{\theta}) = \mathbf{x}(s, a)
$$

次に、 $\nabla \ln \left( \sum_{b} e^{h(s, b, \boldsymbol{\theta})} \right)$ を計算する。
連鎖率 $\nabla \ln u = \frac{1}{u} \nabla u$ を用いると、

$$
\begin{align*}
\nabla \ln \left( \sum_{b} e^{h(s, b, \boldsymbol{\theta})} \right) &= \frac{1}{\sum_{b} e^{h(s, b, \boldsymbol{\theta})}} \nabla \left( \sum_{b} e^{h(s, b, \boldsymbol{\theta})} \right)
\end{align*}
$$

さらに、 $\nabla e^{h(s, b, \boldsymbol{\theta})} = e^{h(s, b, \boldsymbol{\theta})} \nabla h(s, b, \boldsymbol{\theta})$ を用いると、

$$
\begin{align*}
\nabla \left( \sum_{b} e^{h(s, b, \boldsymbol{\theta})} \right) &= \sum_{b} e^{h(s, b, \boldsymbol{\theta})} \nabla h(s, b, \boldsymbol{\theta}) \\
&= \sum_{b} e^{h(s, b, \boldsymbol{\theta})} \mathbf{x}(s, b)
\end{align*}
$$

したがって、

$$
\begin{align*}
\nabla \ln \left( \sum_{b} e^{h(s, b, \boldsymbol{\theta})} \right) &= \frac{1}{\sum_{b} e^{h(s, b, \boldsymbol{\theta})}} \sum_{b} e^{h(s, b, \boldsymbol{\theta})} \mathbf{x}(s, b) \\
&= \sum_{b} \frac{e^{h(s, b, \boldsymbol{\theta})}}{\sum_{c} e^{h(s, c, \boldsymbol{\theta})}} \mathbf{x}(s, b) \\
&= \sum_{b} \pi(b|s, \boldsymbol{\theta}) \mathbf{x}(s, b)
\end{align*}
$$

これを元の式に代入すると、

$$
\begin{align*}
\nabla \ln \pi(a|s, \boldsymbol{\theta}) &= \mathbf{x}(s, a) - \sum_{b} \pi(b|s, \boldsymbol{\theta}) \mathbf{x}(s, b)
\end{align*}
$$

これにより、求める適格度ベクトルの表現が示された。


# Exercise 13.4

正規分布による方策のパラメータ化(13.19)では、敵角度ベクトルは次の2つになることを示せ。

$$
\begin{align*}
\nabla \ln \pi(a \mid s, \boldsymbol{\theta}_\mu) &= \frac{ \nabla \pi(a \mid s, \boldsymbol{\theta}_\mu) }{ \pi(a \mid s, \boldsymbol{\theta}) } \\
&= \frac{1}{\sigma(s, \boldsymbol{\theta})^2} \left( a - \mu(s, \boldsymbol{\theta}) \right) \mathbf{x}_\mu(s) \\
\\
\nabla \ln \pi(a \mid s, \boldsymbol{\theta}_\sigma) &= \frac{ \nabla \pi(a \mid s, \boldsymbol{\theta}_\sigma) }{ \pi(a \mid s, \boldsymbol{\theta}) } \\
&= \left[ \frac{(a - \mu(s, \boldsymbol{\theta}))^2}{\sigma(s, \boldsymbol{\theta})^2} - 1 \right] \mathbf{x}_\sigma(s)
\end{align*}
$$

## 解答

方策 $\pi(a|s, \boldsymbol{\theta})$ は、平均 $\mu(s, \boldsymbol{\theta_\mu})$ と標準偏差 $\sigma(s, \boldsymbol{\theta_\sigma})$ を持つ正規分布として定義される。

$$
\begin{align*}
\pi(a|s, \boldsymbol{\theta}) &= \frac{1}{\sqrt{2 \pi} \sigma(s, \boldsymbol{\theta})} \exp \left( -\frac{(a - \mu(s, \boldsymbol{\theta}))^2}{2 \sigma(s, \boldsymbol{\theta})^2} \right) \\
\boldsymbol{\theta} &= \left[ \boldsymbol{\theta}_\mu, \boldsymbol{\theta}_\sigma \right]^T
\end{align*}
$$

まず、平均 $\mu(s, \boldsymbol{\theta})$ に関する勾配を計算する。

$$
\begin{align*}
\nabla \pi(a|s, \boldsymbol{\theta}_\mu) &= \nabla \left( \frac{1}{\sqrt{2 \pi} \sigma(s, \boldsymbol{\theta})} \exp \left( -\frac{(a - \mu(s, \boldsymbol{\theta}))^2}{2 \sigma(s, \boldsymbol{\theta})^2} \right) \right) \\
&= \frac{1}{\sqrt{2 \pi} \sigma(s, \boldsymbol{\theta})} \cdot \nabla \exp \left( -\frac{(a - \mu(s, \boldsymbol{\theta}))^2}{2 \sigma(s, \boldsymbol{\theta})^2} \right) \\
&= \frac{1}{\sqrt{2 \pi} \sigma(s, \boldsymbol{\theta})} \cdot \exp \left( -\frac{(a - \mu(s, \boldsymbol{\theta}))^2}{2 \sigma(s, \boldsymbol{\theta})^2} \right) \cdot \nabla \left( -\frac{(a - \mu(s, \boldsymbol{\theta}))^2}{2 \sigma(s, \boldsymbol{\theta})^2} \right) \\
&= \pi(a|s, \boldsymbol{\theta}) \cdot \left( - \frac{1}{2 \sigma(s, \boldsymbol{\theta})^2} \cdot \nabla (a - \mu(s, \boldsymbol{\theta}))^2 \right) \\
&= \pi(a|s, \boldsymbol{\theta}) \cdot \left( - \frac{1}{2 \sigma(s, \boldsymbol{\theta})^2} \cdot 2 (a - \mu(s, \boldsymbol{\theta})) \cdot (-\nabla \mu(s, \boldsymbol{\theta})) \right) \\
&= \pi(a|s, \boldsymbol{\theta}) \cdot \frac{(a - \mu(s, \boldsymbol{\theta}))}{\sigma(s, \boldsymbol{\theta})^2} \cdot \nabla \mu(s, \boldsymbol{\theta})
\end{align*}
$$

ここで、平均は

$$
\mu(s, \boldsymbol{\theta}) = \boldsymbol{\theta_\mu}^T \mathbf{x}_\mu(s)
$$

とパラメータ化されているため、その勾配は

$$
\nabla \mu(s, \boldsymbol{\theta}) = \mathbf{x}_\mu(s)
$$

となる。これを代入すると、

$$
\nabla \pi(a|s, \boldsymbol{\theta}_\mu) = \pi(a|s, \boldsymbol{\theta}) \cdot \frac{(a - \mu(s, \boldsymbol{\theta}))}{\sigma(s, \boldsymbol{\theta})^2} \cdot \mathbf{x}_\mu(s)
$$


したがって、

$$
\begin{align*}
\nabla \ln \pi(a|s, \boldsymbol{\theta}_\mu) &= \frac{\nabla \pi(a|s, \boldsymbol{\theta}_\mu)}{\pi(a|s, \boldsymbol{\theta})} \\
&= \frac{1}{\sigma(s, \boldsymbol{\theta})^2} (a - \mu(s, \boldsymbol{\theta})) \mathbf{x}_\mu(s)
\end{align*}
$$

次に、標準偏差 $\sigma(s, \boldsymbol{\theta})$ に関する勾配を計算する。

$$
\begin{align*}
\nabla \pi(a|s, \boldsymbol{\theta}_\sigma) &= \nabla \left( \frac{1}{\sqrt{2 \pi} \sigma(s, \boldsymbol{\theta})} \exp \left( -\frac{(a - \mu(s, \boldsymbol{\theta}))^2}{2 \sigma(s, \boldsymbol{\theta})^2} \right) \right) \\
&= \nabla \left( \frac{1}{\sqrt{2 \pi} \sigma(s, \boldsymbol{\theta})} \right) \cdot \exp \left( -\frac{(a - \mu(s, \boldsymbol{\theta}))^2}{2 \sigma(s, \boldsymbol{\theta})^2} \right) + \frac{1}{\sqrt{2 \pi} \sigma(s, \boldsymbol{\theta})} \cdot \nabla \exp \left( -\frac{(a - \mu(s, \boldsymbol{\theta}))^2}{2 \sigma(s, \boldsymbol{\theta})^2} \right) \\
\end{align*}
$$

$$
\begin{align*}
\quad &= \frac{1}{\sqrt{2 \pi}} \cdot \nabla \left( \frac{1}{\sigma(s, \boldsymbol{\theta})} \right) \cdot \exp \left( -\frac{(a - \mu(s, \boldsymbol{\theta}))^2}{2 \sigma(s, \boldsymbol{\theta})^2} \right) \\
&\quad + \frac{1}{\sqrt{2 \pi} \sigma(s, \boldsymbol{\theta})} \cdot \exp \left( -\frac{(a - \mu(s, \boldsymbol{\theta}))^2}{2 \sigma(s, \boldsymbol{\theta})^2} \right) \cdot \nabla \left( -\frac{(a - \mu(s, \boldsymbol{\theta}))^2}{2 \sigma(s, \boldsymbol{\theta})^2} \right) \\
&= \frac{1}{\sqrt{2 \pi}} \cdot \left( -\frac{1}{\sigma(s, \boldsymbol{\theta})^2} \right) \cdot \nabla \sigma(s, \boldsymbol{\theta}) \cdot \exp \left( -\frac{(a - \mu(s, \boldsymbol{\theta}))^2}{2 \sigma(s, \boldsymbol{\theta})^2} \right) \\
&\quad + \frac{1}{\sqrt{2 \pi} \sigma(s, \boldsymbol{\theta})} \cdot \exp \left( -\frac{(a - \mu(s, \boldsymbol{\theta}))^2}{2 \sigma(s, \boldsymbol{\theta})^2} \right) \cdot \left( -\frac{(a - \mu(s, \boldsymbol{\theta}))^2}{2} \right) \cdot \nabla \left( \frac{1}{\sigma(s, \boldsymbol{\theta})^2} \right) \\
\end{align*}
$$

$$
\begin{align*}
\quad &= \pi(a|s, \boldsymbol{\theta}) \cdot \left( -\frac{1}{\sigma(s, \boldsymbol{\theta})} \right) \cdot \nabla \sigma(s, \boldsymbol{\theta}) \\
&\quad + \pi(a|s, \boldsymbol{\theta}) \cdot \left( -\frac{(a - \mu(s, \boldsymbol{\theta}))^2}{2} \right) \cdot \left( -\frac{2}{\sigma(s, \boldsymbol{\theta})^3} \right) \cdot \nabla \sigma(s, \boldsymbol{\theta}) \\
&= \pi(a|s, \boldsymbol{\theta}) \cdot \left( -\frac{1}{\sigma(s, \boldsymbol{\theta})} \cdot \nabla \sigma(s, \boldsymbol{\theta}) \right) + \pi(a|s, \boldsymbol{\theta}) \cdot \left( \frac{(a - \mu(s, \boldsymbol{\theta}))^2}{\sigma(s, \boldsymbol{\theta})^3} \cdot \nabla \sigma(s, \boldsymbol{\theta}) \right) \\
&= \pi(a|s, \boldsymbol{\theta}) \cdot \left( -\frac{1}{\sigma(s, \boldsymbol{\theta})} + \frac{(a - \mu(s, \boldsymbol{\theta}))^2}{\sigma(s, \boldsymbol{\theta})^3} \right) \cdot \nabla \sigma(s, \boldsymbol{\theta}) \\
&= \pi(a|s, \boldsymbol{\theta}) \cdot \left( \frac{(a - \mu(s, \boldsymbol{\theta}))^2 - \sigma(s, \boldsymbol{\theta})^2}{\sigma(s, \boldsymbol{\theta})^3} \right) \cdot \nabla \sigma(s, \boldsymbol{\theta})
\end{align*}
$$

ここで、標準偏差は

$$
\sigma(s, \boldsymbol{\theta}) = \exp(\boldsymbol{\theta_\sigma}^T \mathbf{x}_\sigma(s))
$$

とパラメータ化されているため、その勾配は

$$
\nabla \sigma(s, \boldsymbol{\theta}) = \sigma(s, \boldsymbol{\theta}) \mathbf{x}_\sigma(s)
$$

となる。これを代入すると、

$$
\begin{align*}
\nabla \pi(a|s, \boldsymbol{\theta}_\sigma) &= \pi(a|s, \boldsymbol{\theta}) \cdot \left( \frac{(a - \mu(s, \boldsymbol{\theta}))^2 - \sigma(s, \boldsymbol{\theta})^2}{\sigma(s, \boldsymbol{\theta})^3} \right) \cdot \sigma(s, \boldsymbol{\theta}) \mathbf{x}_\sigma(s) \\
&= \pi(a|s, \boldsymbol{\theta}) \cdot \left( \frac{(a - \mu(s, \boldsymbol{\theta}))^2 - \sigma(s, \boldsymbol{\theta})^2}{\sigma(s, \boldsymbol{\theta})^2} \right) \cdot \mathbf{x}_\sigma(s)
\end{align*}
$$

したがって、

$$
\begin{align*}
\nabla \ln \pi(a|s, \boldsymbol{\theta}_\sigma) &= \frac{\nabla \pi(a|s, \boldsymbol{\theta}_\sigma)}{\pi(a|s, \boldsymbol{\theta})} \\
&= \left[ \frac{(a - \mu(s, \boldsymbol{\theta}))^2}{\sigma(s, \boldsymbol{\theta})^2} - 1 \right] \mathbf{x}_\sigma(s)
\end{align*}
$$

これにより、求める適格度ベクトルの表現が示された。


# Exercise 13.5

ベルヌーイ・ロジスティック・ユニットは、一部の人工ニューラルネットワーク（ANN）で用いられる確率的ニューロン様ユニットである（9.7節を参照）。
時刻 $t$ におけるユニットの入力は特徴ベクトル $\mathbf{x}(S_t)$ であり、その出力 $A_t$ は2つの値、0と1をとる確率変数である。
ここで、 $Pr\{A_t = 1\} = P_t$ かつ $Pr\{A_t = 0\} = 1 - P_t$ （ベルヌーイ分布）とする。

状態 $s$ におけるユニットの2つの行動に対する優先度を、方策パラメータ $\boldsymbol{\theta}$ を与えて $h(s, 0, \boldsymbol{\theta})$ および $h(s, 1, \boldsymbol{\theta})$ とする。
行動優先度の差がユニットの入力ベクトルの重み付き和によって与えられると仮定する。
つまり、

$$
h(s, 1, \boldsymbol{\theta}) - h(s, 0, \boldsymbol{\theta}) = \boldsymbol{\theta}^\top \mathbf{x}(s)
$$

であると仮定する。ただし、 $\boldsymbol{\theta}$ はユニットの重みベクトルである。

  (a) 行動優先度を方策に変換するためにソフトマックス分布 (13.2) が使用される場合、

$$
\begin{align*}
P_t &= \pi(1 \mid S_t, \boldsymbol{\theta}_t)  \\
&= 1 / (1 + \exp(-\boldsymbol{\theta}_t^\top \mathbf{x}(S_t))), \quad （ロジスティック関数）
\end{align*}
$$

  であることを示せ。

  (b) 収益 $G_t$ を受け取った際の $\boldsymbol{\theta_t}$ から $\boldsymbol{\theta_{t+1}}$ へのモンテカルロREINFORCE更新はどのようになるか？

  (c) ベルヌーイ・ロジスティック・ユニットの適格度ベクトル $r \ln \pi(a|s, \boldsymbol{\theta})$ を、勾配を計算することによって、 $a$、 $\mathbf{x}(s)$ 、および $\pi(a|s, \boldsymbol{\theta})$ を用いて表せ。

ヒント:

それぞれの行動について、最初に $P = \pi(1|s, \boldsymbol{\theta})$ に関して対数の導関数を計算し、2つの結果を $a$ と $P_t$ に依存する1つの式にまとめよ。
そして、ロジスティック関数 $f(x)$ の微分が $f(x)(1 - f(x))$ であることに注意しつつ、連鎖律を適用せよ。

## 解答

### (a)

行動優先度の差がユニットの入力ベクトルの重み付き和によって与えられると仮定すると、

$$
\begin{align*}
h(s, 1, \boldsymbol{\theta}) - h(s, 0, \boldsymbol{\theta}) &= \boldsymbol{\theta}^\top \mathbf{x}(s) \\
h(s, 1, \boldsymbol{\theta}) &= h(s, 0, \boldsymbol{\theta}) + \boldsymbol{\theta}^\top \mathbf{x}(s)
\end{align*}
$$

方策はソフトマックス分布として定義されるため、

$$
\begin{align*}
\pi(1|s, \boldsymbol{\theta}) &= \frac{e^{h(s, 1, \boldsymbol{\theta})}}{e^{h(s, 0, \boldsymbol{\theta})} + e^{h(s, 1, \boldsymbol{\theta})}} \\
&= \frac{e^{h(s, 0, \boldsymbol{\theta}) + \boldsymbol{\theta}^\top \mathbf{x}(s)}}{e^{h(s, 0, \boldsymbol{\theta})} + e^{h(s, 0, \boldsymbol{\theta}) + \boldsymbol{\theta}^\top \mathbf{x}(s)}} \\
&= \frac{e^{\boldsymbol{\theta}^\top \mathbf{x}(s)}}{1 + e^{\boldsymbol{\theta}^\top \mathbf{x}(s)}} \\
&= \frac{1}{1 + e^{-\boldsymbol{\theta}^\top \mathbf{x}(s)}}
\end{align*}
$$

### (c)

(c)の結果を使って(b)を解くために、先に(c)を解く。

最初に $P = \pi(1|s, \boldsymbol{\theta})$ に関して対数の導関数を計算する。

$$
\begin{align*}
\nabla \ln \pi(1|s, \boldsymbol{\theta}) &= \frac{1}{P} \nabla P \\
\nabla \ln \pi(0|s, \boldsymbol{\theta}) &= \frac{1}{1 - P} \nabla (1 - P) = -\frac{1}{1 - P} \nabla P
\end{align*}
$$

2つの結果を $a$ と $P_t$ に依存する1つの式にまとめると、

$$
\begin{align*}
\nabla \ln \pi(a|s, \boldsymbol{\theta}) &= a \frac{1}{P} \nabla P + (1 - a) \left( -\frac{1}{1 - P} \nabla P \right) \\
&= \left( \frac{a - P}{P(1 - P)} \right) \nabla P
\end{align*}
$$

そして、ロジスティック関数 $f(x)$ の微分が $f(x)(1 - f(x))$ であることに注意しつつ、連鎖律を適用すると、

$$
\begin{align*}
\nabla P &= \nabla \left( \frac{1}{1 + e^{-\boldsymbol{\theta}^\top \mathbf{x}(s)}} \right) \\
&= P(1 - P) \mathbf{x}(s)
\end{align*}
$$

これを代入すると、ベルヌーイ・ロジスティック・ユニットの適格度ベクトルは次のように表される。

$$
\begin{align*}
\nabla \ln \pi(a|s, \boldsymbol{\theta}) &= \left( \frac{a - P}{P(1 - P)} \right) P(1 - P) \mathbf{x}(s) \\
&= (a - P) \mathbf{x}(s) \\
&= (a - \pi(1|s, \boldsymbol{\theta})) \mathbf{x}(s)
\end{align*}
$$

### (b)

REINFORCEアルゴリズムの更新式は、

$$
\boldsymbol{\theta}_{t+1} = \boldsymbol{\theta}_t + \alpha G_t \nabla \ln \pi(A_t|S_t, \boldsymbol{\theta}_t)
$$

である。
(c)で導出するように、ベルヌーイ・ロジスティック・ユニットの適格度ベクトルは

$$
\nabla \ln \pi(A_t|S_t, \boldsymbol{\theta}_t) = (A_t - \pi(1|S_t, \boldsymbol{\theta}_t)) \mathbf{x}(S_t)
$$

となる。
したがって、更新式は以下のようになる。

$$
\boldsymbol{\theta}_{t+1} = \boldsymbol{\theta}_t + \alpha G_t (A_t - \pi(1|S_t, \boldsymbol{\theta}_t)) \mathbf{x}(S_t)
$$
