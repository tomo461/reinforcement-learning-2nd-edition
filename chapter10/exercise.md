# 第10章 演習問題

# Exercise 10.1

この章ではモンテカルロ法を明示的に検討したり、擬似コードを提供したりしなかった。

1. 関数近似を用いたモンテカルロ法はどのようなものになるか。
2. なぜ擬似コードを示さなくても良かったのか。
3. マウンテンカータスクではどのような性能を発揮するか。

## 回答

#### 1. 関数近似を用いたモンテカルロ法はどのようなものになるか。

関数近似を伴うオンポリシー制御の文脈（Chapter 10）において、モンテカルロ法は、nステップ・ブートストラップ法の極限として考えることができる。つまり、式(10.5)において、 $n \to T$ とした場合である。この場合、エピソードの終了まで待ってから、以下の式で重みベクトル $\mathbf{w}$ を更新する。

$$
\mathbf{w}_{t+1} = \mathbf{w}_t + \alpha \left( G_t - \hat{q}(S_t, A_t, \mathbf{w}_t) \right) \nabla \hat{q}(S_t, A_t, \mathbf{w}_t)
$$

のように重みベクトル $\mathbf{w}$ を更新する。ただし、 $G_t$ は時刻 $t$ からエピソード終了までの累積報酬:

$$
G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \ldots + \gamma^{T-t-1} R_T
$$

#### 2. なぜ擬似コードを示さなくても良かったのか。

1で示したように、関数近似を用いたモンテカルロ法はnステップ・ブートストラップ法の極限として表現できるため、より一般化されたnステップ法の擬似コードを理解していれば、モンテカルロ法の擬似コードも容易に導出できるからである。

#### 3. マウンテンカータスクではどのような性能を発揮するか。

図10.4で中間的な程度のブートストラップの性能が最も良かったことが示されている（例えば n = 16 より n = 4 の方が良い）。
モンテカルロ法は $n \to T$ に相当するため、中間的な程度のブートストラップよりも性能が劣ると予想される。


# Exercise 10.2

疑似勾配1ステップ期待SARSA法による制御の擬似コードを示せ。

## 回答

エピソード的擬似勾配1ステップSARSAに対して、次の行動 $A'$ の選択を期待値で置き換えることで、擬似勾配1ステップ期待SARSA法の擬似コードを得る。以下にその擬似コードを示す。

- 入力: 微分可能な行動価値関数パラメータ化 $\hat{q}(s, a, \mathbf{w}) : S \times A \times R^d \to R$
- 方策: $\pi$
- アルゴリズムパラメータ: ステップサイズ $\alpha \in (0, 1]$ , 小さな値 $\epsilon > 0$ , 整数 $n > 0$
- 初期化: 価値関数重み $\mathbf w \in \mathbb{R}^d$ を任意に初期化する（例: $\mathbf w = \mathbf 0$ ）
- 各エピソードについて繰り返す:
  - 初期状態 $S \neq \text{terminal}$ を初期化し保存
  - $Q(S,⋅)$ に関するポリシー $\pi$（例: $\epsilon$ -greedy）に従って行動 $A_0$ を選択し保存
  - 時刻ステップ $t = 0, 1, 2, \ldots$ について繰り返す:
    - 行動 $A_t$ を選択し、報酬 $R_{t+1}$ と次の状態 $S_{t+1}$ を観測し保存
    - $G \leftarrow \sum_{a} \pi(a \mid S_{t+1}) \hat{q}(S_{t+1}, a, \mathbf{w})$
    - もし $S_{t+1} \neq \text{terminal}$ ならば
      - $G \leftarrow R_{t+1} + \gamma G$
    - $\mathbf{w} \leftarrow \mathbf{w} + \alpha \left( G - \hat{q}(S_t, A_t, \mathbf{w}) \right) \nabla \hat{q}(S_t, A_t, \mathbf{w})$
    - もし $S_{t+1} = \text{terminal}$ ならば、次のエピソードへ進む


# Exercise 10.3

なぜ図10.4の結果の標準誤差は $n$ が大きいほど大きくなるのか。

## 回答

$n$ が大きくなると、更新ターゲットがより長い将来の報酬に依存するようになり、分散が大きくなる。分散が増加すると異なる試行間での性能のばらつきが大きくなるため、標準誤差が大きくなる。


# Exercise 10.4

擬似勾配Q学習の差分版の疑似コードを示せ。

## 回答

Q学習は off-policy の手法であるため、更新ターゲットは次の状態での最大の行動価値に基づいて計算される。以下に擬似勾配Q学習の差分版の擬似コードを示す。

- 入力: 微分可能な行動価値関数パラメータ化 $\hat{q}(s, a, \mathbf{w}) : S \times A \times R^d \to R$
- アルゴリズムパラメータ: ステップサイズ $\alpha > 0$ , $\beta > 0$
- 初期化: 価値関数重み $\mathbf w \in \mathbb{R}^d$ を任意に初期化する（例: $\mathbf w = \mathbf 0$ ）
- 初期化: 平均報酬の推定値 $\bar{R} \in \mathbb{R}$ を任意に初期化する（例: $\bar{R} = 0$ ）
- 状態 $S$ と行動 $A$ を初期化
- 各タイムステップについて繰り返す:
  - 行動 $A$ を実行し、報酬 $R$ と次の状態 $S'$ を観測
  - $S'$ における最大の行動価値をもつ行動 $A^* = \arg\max_{a} \hat{q}(S', a, \mathbf{w})$ を選択
  - $\delta \leftarrow R - \bar{R} + \hat{q}(S', A^*, \mathbf{w}) - \hat{q}(S, A, \mathbf{w})$
  - $\bar{R} \leftarrow \bar{R} + \beta \ \delta$
  - $\mathbf{w} \leftarrow \mathbf{w} + \alpha \ \delta \nabla \hat{q}(S, A, \mathbf{w})$
  - $S \leftarrow S'$
  - $\hat{q}(S, \dot, \mathbf{w})$ に関するポリシーに従って新しい行動 $A$ を選択


# Exercise 10.5

差分版のTD(0)法を定義するには、式(10.10)の他にどのような等式が必要か。

## 回答

差分版のTD(0)法を定義するためには、

1. 状態価値の重みベクトル $\mathbf{w}$ の更新式
2. 平均報酬 $\bar{R}$ の更新式

が必要であり、式(10.10)を用いてそれぞれ以下のように表される。

$$
\mathbf{w}_{t+1} = \mathbf{w}_t + \alpha \delta_t \nabla \hat{v}(S_t, \mathbf{w}_t)
$$

$$
\bar{R}_{t+1} = \bar{R}_t + \beta \delta_t
$$


# Exercise 10.6 (日本語版だと Exercise 10.7)

どのような方策（ポリシー）を用いても、報酬が +1,0,+1,0,+1,0,… の確定的な系列を永久に生成するマルコフ決定過程（MDP）を考える。
正確には、これはエルゴード性に反し、定常極限分布 $\mu_\pi$ も極限 (10.7) も存在しない。
それにもかかわらず、平均報酬 (10.6) は明確に定義されている。
しかしながら、平均報酬(10.6)は明確に定義できる。その値はどうなるだろうか。
このMDPの2つの状態について考えてみる。状態Aからの報酬系列は +1,0,+1,0,… であり、状態Bからの報酬系列は 0,+1,0,+1,… である。
この場合、差分収益(10.9)は極限が存在しないため明確に定義できない。これを直すために、代わりに状態価値を

$$
\begin{align*}
v_\pi(s) &= \lim_{\gamma \to 1} \lim_{h \to \infty} \sum_{t=0}^{h} \gamma^t \big( \mathbb{E}_\pi [R_{t+1} \mid S_0 = s] - r(\pi) \big) \\
&\quad \tag{10.13}
\end{align*}
$$

と定義できるかもしれない。この定義の下ではAとBの状態価値はどうなるだろうか。

## 回答

式(10.6)より、平均報酬 $r(\pi)$ は

$$
r(\pi) = \lim_{h \to \infty} \frac{1}{h} \mathbf{E} \left[ R_t \mid S_0 = s, A_{0:t-1} \sim \pi \right]
$$

で与えられる。報酬系列が +1,0,+1,0,… であるため、任意の初期状態 $s$ に対して

$$
r(\pi) = \frac{1+0}{2} = \frac{1}{2}
$$

この $r(\pi) = \frac{1}{2}$ を用いて、式(10.13) に基づいて各状態の価値を計算する。

#### 状態 A:
状態 A からの報酬系列は +1,0,+1,0,… であるため、差分の系列は $+ \frac{1}{2}, -\frac{1}{2}, +\frac{1}{2}, -\frac{1}{2}, \dots$ となる。したがって、状態 A の価値は

$$
\begin{align*}
v_\pi(A) &= \lim_{\gamma \to 1} \lim_{h \to \infty} \sum_{t=0}^{h} \gamma^t \left( \mathbb{E}_\pi [R_{t+1} \mid S_0 = A] - r(\pi) \right) \\
&= \lim_{\gamma \to 1} \sum_{t=0}^{\infty} \gamma^t \left( \mathbb{E}_\pi [R_{t+1} \mid S_0 = A] - \frac{1}{2} \right)
\end{align*}
$$

ここで、無限和の部分は報酬差分の系列 $+ \frac{1}{2}, -\frac{1}{2}, +\frac{1}{2}, -\frac{1}{2}, \dots$ に $\gamma^t$ を掛けたものの和であるため、

$$
\begin{align*}
v_\pi(A) &= \lim_{\gamma \to 1} \sum_{t=0}^{\infty} \gamma^t \left( \mathbb{E}_\pi [R_{t+1} \mid S_0 = A] - \frac{1}{2} \right) \\
&= \lim_{\gamma \to 1} \left( \frac{1}{2} + (-\frac{1}{2}) \gamma + \frac{1}{2} \gamma^2 + (-\frac{1}{2}) \gamma^3 + \ldots \right) \\
&= \lim_{\gamma \to 1} \left( \frac{1}{2} (1 - \gamma + \gamma^2 - \gamma^3 + \ldots ) \right)
\end{align*}
$$

ここで、無限等比級数の和の公式 $\sum_{t=0}^{\infty} ar^t = \frac{a}{1 - r}$ を用いると、

$$
\begin{align*}
v_\pi(A) &= \lim_{\gamma \to 1} \left( \frac{1}{2} (1 - \gamma + \gamma^2 - \gamma^3 + \ldots ) \right) \\
&= \lim_{\gamma \to 1} \frac{1}{2} \cdot \frac{1}{1 + \gamma} \\
&= \frac{1}{4}
\end{align*}
$$


#### 状態 B:
状態 B からの報酬系列は 0,+1,0,+1,… であるため、差分の系列は $- \frac{1}{2}, +\frac{1}{2}, -\frac{1}{2}, +\frac{1}{2}, \dots$ となる。したがって、状態 B の価値は

$$
\begin{align*}
v_\pi(B) &= \lim_{\gamma \to 1} \lim_{h \to \infty} \sum_{t=0}^{h} \gamma^t \left( \mathbb{E}_\pi [R_{t+1} \mid S_0 = B] - r(\pi) \right) \\
&= \lim_{\gamma \to 1} \left( -\frac{1}{2} + \frac{1}{2} \gamma - \frac{1}{2} \gamma^2 + \frac{1}{2} \gamma^3 + \ldots \right) \\
&= \lim_{\gamma \to 1} -\frac{1}{2} (1 - \gamma + \gamma^2 - \gamma^3 + \ldots ) \\
&= \lim_{\gamma \to 1} -\frac{1}{2} \cdot \frac{1}{1 + \gamma} \\
&= -\frac{1}{4}
\end{align*}
$$

したがって、状態 A の価値は $\frac{1}{4}$、状態 B の価値は $-\frac{1}{4}$ となる。


# Exercise 10.7 (日本語版だと Exercise 10.6)

以下の特性を持つマルコフ報酬課程(MRP)を考える。

- 3つの状態 $A$, $B$, $C$ が環状につながっている。
- 状態遷移は決定的であり、 $A \to B \to C \to A$ の順に遷移する。
- $A$ に到達した時に報酬 +1 を得る。その他の状態では報酬は0である。

3つの状態の差分価値 $v_\pi(s)$ を式(10.13)を用いて計算せよ。

## 回答

問題文より、平均報酬は $r(\pi) = \frac{1}{3}$ となる。

ここで、各状態における報酬と平均報酬の差分 $R_{t+1} - r(\pi)$ の系列を求め、無限和 $\sum_{t=0}^{\infty} \gamma^t (R_{t+1} - r(\pi))$ の極限として各状態の差分価値を計算する。

#### 状態 $A$:

差分の系列は、 $- \frac{1}{3}, -\frac{1}{3}, \frac{2}{3}, -\frac{1}{3}, -\frac{1}{3}, \frac{2}{3}, \dots$ となり、周期3で $- \frac{1}{3}, -\frac{1}{3}, \frac{2}{3}$ が繰り返される。 $v_\pi(A)$ はこの系列を用いた無限和の極限として計算される。

$$
\begin{aligned}
v_\pi(A) &= \lim_{\gamma \to 1} \sum_{t=0}^{\infty} \gamma^t \left( \mathbb{E}_\pi [R_{t+1} \mid S_0 = A] - r(\pi) \right) \\
&= \lim_{\gamma \to 1} \sum_{k=0}^{\infty} \gamma^{3k} \big( -\frac{1}{3} + \gamma (-\frac{1}{3}) + \gamma^2 \frac{2}{3} \big) \\
\end{aligned}
$$

ここで、 $\sum_{k=0}^{\infty} (\gamma^{3})^k = \frac{1}{1 - \gamma^3}$ を用いると、

$$
\begin{aligned}
v_\pi(A) &= \lim_{\gamma \to 1} \sum_{k=0}^{\infty} \gamma^{3k} \big( -\frac{1}{3} + \gamma (-\frac{1}{3}) + \gamma^2 \frac{2}{3} \big) \\
&= \lim_{\gamma \to 1} \frac{-\frac{1}{3} - \frac{1}{3} \gamma + \frac{2}{3} \gamma^2}{(1 - \gamma^3)} \\
&= \lim_{\gamma \to 1} \frac{1}{3} \cdot \frac{-1 - \gamma + 2 \gamma^2}{(1 - \gamma^3)} \\
\end{aligned}
$$

$\gamma \to 1$ で分母と分子がともに0になるため、ロピタルの定理を適用する。

- 分子の導関数: $\frac{d}{d\gamma} (-1 - \gamma + 2 \gamma^2) = -1 + 4 \gamma$
- 分母の導関数: $\frac{d}{d\gamma} (1 - \gamma^3) = -3 \gamma^2$

$$
\begin{aligned}
v_\pi(A) &= \lim_{\gamma \to 1} \frac{1}{3} \cdot \frac{-1 + 4 \gamma}{-3 \gamma^2} \\
&= \frac{1}{3} \cdot \frac{-1 + 4}{-3} \\
&= -\frac{1}{3}
\end{aligned}
$$

#### 状態 $B$:

差分の系列は、 $- \frac{1}{3}, \frac{2}{3}, -\frac{1}{3}, \ldots$ となる。 $v_\pi(A)$ と同様に $v_\pi(B)$ を計算する。

$$
\begin{aligned}
v_\pi(B) &= \lim_{\gamma \to 1} \sum_{k=0}^{\infty} \gamma^{3k} \big( -\frac{1}{3} + \gamma (\frac{2}{3}) + \gamma^2 (-\frac{1}{3}) \big) \\
&= \lim_{\gamma \to 1} \frac{-\frac{1}{3} + \frac{2}{3} \gamma - \frac{1}{3} \gamma^2}{(1 - \gamma^3)} \\
&= \lim_{\gamma \to 1} \frac{1}{3} \cdot \frac{-1 + 2 \gamma - \gamma^2}{(1 - \gamma^3)} \\
&= \lim_{\gamma \to 1} \frac{1}{3} \cdot \frac{2 - 2 \gamma}{-3 \gamma^2} \quad \text{(ロピタルの定理を適用)} \\
&= \frac{1}{3} \cdot \frac{2 - 2}{-3} \\
&= 0
\end{aligned}
$$

#### 状態 $C$:

差分の系列は、 $\frac{2}{3}, -\frac{1}{3}, -\frac{1}{3}, \ldots$ となる。 $v_\pi(A)$ と同様に $v_\pi(C)$ を計算する。

$$
\begin{aligned}
v_\pi(C) &= \lim_{\gamma \to 1} \sum_{k=0}^{\infty} \gamma^{3k} \big( \frac{2}{3} + \gamma (-\frac{1}{3}) + \gamma^2 (-\frac{1}{3}) \big) \\
&= \lim_{\gamma \to 1} \frac{\frac{2}{3} - \frac{1}{3} \gamma - \frac{1}{3} \gamma^2}{(1 - \gamma^3)} \\
&= \lim_{\gamma \to 1} \frac{1}{3} \cdot \frac{2 - \gamma - \gamma^2}{(1 - \gamma^3)} \\
&= \lim_{\gamma \to 1} \frac{1}{3} \cdot \frac{-1 - 2 \gamma}{-3 \gamma^2} \quad \text{(ロピタルの定理を適用)} \\
&= \frac{1}{3}
\end{aligned}
$$

したがって、各状態の差分価値は以下の通りである。

- $v_\pi(A) = -\frac{1}{3}$
- $v_\pi(B) = 0$
- $v_\pi(C) = \frac{1}{3}$


# Exercise 10.8

差分擬似勾配Sarsa法による $\hat q \approx q*$ の疑似コードでは、 $\bar R_{t+1}$ を更新するために $R_{t+1} - \bar R_{t}$ ではなく $\delta_t$ を誤差として使用している。
どちらの誤差も機能するが、 $\delta_t$ を使用する方が優れている。

その理由を確認するために、Exercise 10.7 (日本語版だと 10.6) で扱った3つの状態の環状MRPを考える。
平均報酬の推定値はすでに真の値 1/3 に収束しており、そこに固定されていると仮定する。このとき、

1. $R_{t+1} - \bar R_{t}$ の誤差系列はどうなるか。
2. また、 $\delta_t$ の誤差（式10.10を使用）の系列はどうなるか。
3. どちらの誤差系列が、価値関数を真の差分価値に近づけるために適切か。その理由は何か。

## 回答

#### 1. $R_{t+1} - \bar R_{t}$ の誤差系列はどうなるか。

状態Aから始めると、報酬系列は 0, 0, 1, 0, 0, 1, ... となる。平均報酬 $\bar{R}_t$ が真の値 $\frac{1}{3}$ に収束していると仮定すると、誤差系列は $- \frac{1}{3}, -\frac{1}{3}, \frac{2}{3}, -\frac{1}{3}, -\frac{1}{3}, \frac{2}{3}, ...$ となる。

#### 2. $\delta_t$ の誤差（式10.10を使用）の系列はどうなるか。

問題文の下で、 $\delta_t$ は以下のように定義される。

$$
\delta_t = R_{t+1} - \bar{R} + v(S_{t+1}) - v(S_t)
$$

状態Aから始めると、差分価値は $v_\pi(A) = -\frac{1}{3}$, $v_\pi(B) = 0$, $v_\pi(C) = \frac{1}{3}$ である。したがって、 $\delta_t$ の誤差系列は以下のようになる。

- 状態Aから状態Bへの遷移: $\delta_t = R_{t+1} - \bar R + v_\pi(B) - v_\pi(A) = 0 - \frac{1}{3} + 0 - (-\frac{1}{3}) = 0$
- 状態Bから状態Cへの遷移: $\delta_t = R_{t+1} - \bar R + v_\pi(C) - v_\pi(B) = 0 - \frac{1}{3} + \frac{1}{3} - 0 = 0$
- 状態Cから状態Aへの遷移: $\delta_t = R_{t+1} - \bar R + v_\pi(A) - v_\pi(C) = 1 - \frac{1}{3} + (-\frac{1}{3}) - \frac{1}{3} = 0$

したがって、 $\delta_t$ の誤差系列は $0, 0, 0, 0, 0, 0, ...$ となる。

#### 3. どちらの誤差系列が、価値関数を真の差分価値に近づけるために適切か。その理由は何か。

$\delta_t$ である。

$\delta_t$ は、価値関数 $v(s)$ が真の値 $v_\pi(s)$ に収束していれば、 $\bar R$ が真の平均報酬に固定されている場合に常にゼロになる。

$R_{t+1} - \bar R_{t}$ は、価値関数が真の差分価値に収束しても、報酬が周期的な場合ゼロに収束しない。


# Exercise 10.9



## 回答

ステップサイズトリックは、exercise 2.7 より、

$$
\beta_n = \frac{\beta}{\bar o_n} \\
\bar o_n = \bar o_{n-1} + \beta (1 - \bar o_{n-1}), \quad \text{for } n > 0, \text{with } \bar o_0 = 0
$$

これを疑似コードに組み込むには、 $\bar o = 0$ で初期化した上で、各タイムステップ $\tau$ で以下の更新を行う。

$$
\begin{align*}
\bar o &\leftarrow \bar o + \beta (1 - \bar o) \\
\beta_\tau &\leftarrow \frac{\beta}{\bar o}
\end{align*}
$$

ただし、 $\bar R$ の更新に使用するステップサイズ $\beta$ を $\beta_\tau$ に置き換える。
