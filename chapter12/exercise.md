# 第12章 演習問題

# Exercise 12.1

収益が、式(3.9) $G_t = R_t + \gamma G_{t+1}$ のように最初の報酬とそれ以降の収益の再帰的な指揮としてかけるのと同様に、 $\lambda$-収益 $G_t^{\lambda}$ も同様に書けることを示せ。

## 解答

$\lambda$-収益 $G_t^{\lambda}$ は以下で定義される。

$$
\begin{align*}
G_t^{\lambda} &\doteq (1 - \lambda) \sum_{n=1}^{\infty} \lambda^{n-1} G_{t:t+n} \\
\end{align*}
$$

$n$-step 収益 $G_{t:t+n}$ を再帰的に展開すると以下のようになる。

$$
\begin{align*}
G_{t:t+n} &\doteq R_{t+1} + \gamma R_{t+2} + \cdots + \gamma^{n-1} R_{t+n} + \gamma^{n} \hat{v}(S_{t+n}, \mathbf{w}_{t+n-1}) \\
&= R_{t+1} + \gamma \left( R_{t+2} + \gamma R_{t+3} + \cdots + \gamma^{n-2} R_{t+n} + \gamma^{n-1} \hat{v}(S_{t+n}, \mathbf{w}_{t+n-1}) \right) \\
&= R_{t+1} + \gamma G_{t+1:t+n}
\end{align*}
$$

これを $\lambda$-収益 $G_t^{\lambda}$ の定義に代入すると以下のようになる。

$$
\begin{align*}
G_t^{\lambda} &\doteq (1 - \lambda) \sum_{n=1}^{\infty} \lambda^{n-1} G_{t:t+n} \\
&= (1 - \lambda) \sum_{n=1}^{\infty} \lambda^{n-1} \left( R_{t+1} + \gamma G_{t+1:t+n} \right) \\
&= (1 - \lambda) R_{t+1} \sum_{n=1}^{\infty} \lambda^{n-1} + \gamma (1 - \lambda) \sum_{n=1}^{\infty} \lambda^{n-1} G_{t+1:t+n}
\end{align*}
$$

ここで、等比数列の和の公式を使うと、

$$
\sum_{n=1}^{\infty} \lambda^{n-1} = \frac{1}{1 - \lambda}
$$

となる。
また、第2項の和の部分を展開すると、

$$
\begin{align*}
\sum_{n=1}^{\infty} \lambda^{n-1} G_{t+1:t+n} &= G_{t+1:t+1} + \lambda G_{t+1:t+2} + \lambda^2 G_{t+1:t+3} + \cdots \\
&= \hat{v}(S_{t+1}, \mathbf{w}_t) + \lambda \left( G_{t+1:t+2} + \lambda G_{t+1:t+3} + \cdots \right) \\
&= \hat{v}(S_{t+1}, \mathbf{w}_t) + \lambda \sum_{k=1}^{\infty} \lambda^{k-1} G_{t+1:t+1+k}
\end{align*}
$$

となる。したがって、

$$
\begin{align*}
G_t^{\lambda} &= R_{t+1} + \gamma (1 - \lambda) \left( \hat{v}(S_{t+1}, \mathbf{w}_t) + \lambda \sum_{k=1}^{\infty} \lambda^{k-1} G_{t+1:t+1+k} \right) \\
&= R_{t+1} + \gamma (1 - \lambda) \hat{v}(S_{t+1}, \mathbf{w}_t) + \gamma \lambda (1 - \lambda) \sum_{k=1}^{\infty} \lambda^{k-1} G_{t+1:t+1+k} \\
&= R_{t+1} + \gamma (1 - \lambda) \hat{v}(S_{t+1}, \mathbf{w}_t) + \gamma \lambda G_{t+1}^{\lambda}
\end{align*}
$$

# Exercise 12.2

パラメータ $\lambda$ は図12.2の指数的重み付けがどれほど速く減衰するかを特徴づけ、したがって $\lambda$-収益アルゴリズムが更新を決定する際にどれだけ未来を見るかを決める。しかし、 $\lambda$ のような率係数は、減衰の速度を特徴づける方法として時に扱いにくいことがある。目的によっては、時定数または半減期を指定する方が良い場合がある。 $\lambda$ と半減期 $\tau_\lambda$（重み付けシーケンスが初期値の半分まで減衰する時間）を関連づける方程式は何か？

## 解答

半減期 $\tau_\lambda$ は重み付けシーケンスが初期値の半分まで減衰する時間である。したがって、以下の方程式が成り立つ。

$$
\begin{align*}
\lambda^{\tau_\lambda} &= \frac{1}{2} \\
\end{align*}
$$

これを $\lambda$ について解くと以下のようになる。

$$
\begin{align*}
\ln \left( \lambda^{\tau_\lambda} \right) &= \ln\left(\frac{1}{2}\right) \\
\tau_\lambda \ln(\lambda) &= \ln\left(\frac{1}{2}\right) \\
\tau_\lambda \ln(\lambda) &= - \ln(2) \\
\ln(\lambda) &= - \frac{\ln(2)}{\tau_\lambda} \\
\lambda &= e^{- \frac{\ln(2)}{\tau_\lambda}}
\end{align*}
$$

ここで、 $\exp(A \cdot B) = (e^A)^B$, $\exp(- \ln(2)) = \frac{1}{\exp(\ln(2))} = \frac{1}{2}$ を使うと、以下のように書ける。

$$
\begin{align*}
\lambda &= \left( e^{- \ln(2)} \right)^{\frac{1}{\tau_\lambda}} \\
&= \left( \frac{1}{2} \right)^{\frac{1}{\tau_\lambda}} \\
\end{align*}
$$

この式は、半減期 $\tau_\lambda$ が大きいほど、 $\lambda$ が1に近づく（減衰が遅い）ことを示している。


# Exercise 12.3

TD( $\lambda$ ) 法がどのようにオフライン $\lambda$-収益法を厳密に近似するかについては、オフライン $\lambda$-収益法の式におけるエラー項 $G_t^{\lambda} - \hat{v}(S_t, \mathbf{w}_{t})$ が単一の固定した $\mathbf{w}$ に対するTD誤差の和としてかけることから、いくつかの洞察が得られる。このことを、式6.6のやり方に沿って、exercise 12.1で得た $\lambda$-収益の再帰的な定義を使って示せ。

## 解答

$\lambda$-収益 $G_t^{\lambda}$ の更新誤差 $G_t^{\lambda} - \hat{v}(S_t, \mathbf{w}_{t})$ を、定数重みベクトル $\mathbf{w}$ を使ってTD誤差 $\delta_k$ の和として表すことを示す。

$\hat{v}(S_t, \mathbf{w})$ を $V_t$ とすると、式12.6のTD誤差は以下で定義される。

$$
\begin{align*}
\delta_t &\doteq R_{t+1} + \gamma v̂(S_{t+1}, w) - v̂(S_t, w) \\
&= R_{t+1} + \gamma V_{t+1} - V_t
\end{align*}
$$

Exercise 12.1で得た $\lambda$-収益の再帰的な関係式の両辺から $V_t$ を引くと、

$$
\begin{align*}
G_t^{\lambda} - V_t &= R_{t+1} + \gamma (1 - \lambda) V_{t+1} + \gamma \lambda G_{t+1}^{\lambda} - V_t \\
&= R_{t+1} + \gamma V_{t+1} - \gamma \lambda V_{t+1} + \gamma \lambda G_{t+1}^{\lambda} - V_t \\
&= \delta_t + \gamma \lambda (G_{t+1}^{\lambda} - V_{t+1}) \\
&= \delta_t + \gamma \lambda \left( \delta_{t+1} + \gamma \lambda (G_{t+2}^{\lambda} - V_{t+2}) \right) \\
&= \delta_t + \gamma \lambda \delta_{t+1} + (\gamma \lambda)^2 (G_{t+2}^{\lambda} - V_{t+2}) \\
&\ \ \vdots \\
&= \sum_{k=t}^{T-1} (\gamma \lambda)^{k-t} \delta_k
\end{align*}
$$

ここで、エピソードの終了時刻を $T$ とし、 $G_{T}^{\lambda} = V_{T}$ と仮定した。

したがって、 $\lambda$-収益の更新誤差は、TD誤差の割引和として表されることが示された。


# Exercise 12.4

Exercise 12.3の結果を用いて、あるエピソードの重みの更新が各ステップごとに計算されていても、実際には重みの変更には使われていない場合（つまり、 $\mathbf{w}$ が固定されている場合）、TD( $\lambda$ ) 法の重みの更新の総和はオフライン $\lambda$-収益法の更新の和に等しいことを示せ。

## 解答

オフライン $\lambda$-収益法の重みの更新の総和は以下で与えられる。

$$
\begin{align*}
\Delta \mathbf{w}_{\text{offline}} &\doteq \alpha \sum_{t=0}^{T-1} \left( G_t^{\lambda} - \hat{v}(S_t, \mathbf{w}) \right) \nabla_{\mathbf{w}} \hat{v}(S_t, \mathbf{w})
\end{align*}
$$

TD( $\lambda$ ) 法の重みの更新の総和は以下で与えられる。

$$
\begin{align*}
\Delta \mathbf{w}_{\text{TD}} &\doteq \alpha \sum_{t=0}^{T-1} \delta_t \mathbf{z}_t
\end{align*}
$$

ここで、 $\mathbf{z}_t$ は時刻 $t$ の累積的なエリジビリティトレースであり、以下で定義される。

$$
\begin{align*}
\mathbf{z}_t &\doteq \gamma \lambda \mathbf{z}_{t-1} + \nabla_{\mathbf{w}} \hat{v}(S_t, \mathbf{w}) \\
&= \sum_{k=0}^{t} (\gamma \lambda)^{t-k} \nabla_{\mathbf{w}} \hat{v}(S_k, \mathbf{w}), \quad \text{with } \mathbf{z}_{-1} = 0
\end{align*}
$$

Exercise 12.3の結果を用いると、オフライン $\lambda$-収益法の更新誤差はTD誤差の割引和として表される。これをオフライン $\lambda$-収益法の重みの更新に代入すると、

$$
\begin{align*}
\Delta \mathbf{w}_{\text{offline}} &= \alpha \sum_{t=0}^{T-1} \left( \sum_{k=t}^{T-1} (\gamma \lambda)^{k-t} \delta_k \right) \nabla_{\mathbf{w}} \hat{v}(S_t, \mathbf{w}) \\
&= \alpha \sum_{k=0}^{T-1} \delta_k \left( \sum_{t=0}^{k} (\gamma \lambda)^{k-t} \nabla_{\mathbf{w}} \hat{v}(S_t, \mathbf{w}) \right) \\
&= \alpha \sum_{k=0}^{T-1} \delta_k \mathbf{z}_k \\
&= \Delta \mathbf{w}_{\text{TD}}
\end{align*}
$$

したがって、TD( $\lambda$ ) 法の重みの更新の総和はオフライン $\lambda$-収益法の更新の和に等しいことが示された。


# Exercise 12.5

本書では何度も（しばしば演習問題で）、価値関数が一定に保たれている場合、収益はTD誤差の和として書けることを確認してきた。なぜ式(12.10)もこの一例なのか？式(12.10)を証明せよ。

## 解答

式(12.10)は以下である。

$$
\begin{align*}
G_{t:t+k}^{\lambda} = \hat{v}(S_t, \mathbf{w}_{t-1}) + \sum_{i=t}^{t+k-1} (\gamma \lambda)^{i-t} \delta_i'
\end{align*}
$$

ここで、

$$
\begin{align*}
\delta_i' &\doteq R_{i+1} + \gamma \hat{v}(S_{i+1}, \mathbf{w}_{t}) - \hat{v}(S_i, \mathbf{w}_{t-1})
\end{align*}
$$

価値関数が一定に保たれている場合、すなわち $\mathbf{w}_{t} = \mathbf{w}$ の場合、 $\delta_i'$ は通常のTD誤差 $\delta_i$ と等しくなる。

$$
\begin{align*}
\delta_i' &= R_{i+1} + \gamma \hat{v}(S_{i+1}, \mathbf{w}) - \hat{v}(S_i, \mathbf{w}) \\
&= \delta_i
\end{align*}
$$

したがって、証明すべき式は以下のようになる。

$$
\begin{align*}
G_{t:t+k}^{\lambda} &= \hat{v}(S_t, \mathbf{w}) + \sum_{i=t}^{t+k-1} (\gamma \lambda)^{i-t} \delta_i \\
G_{t:t+k}^{\lambda} - \hat{v}(S_t, \mathbf{w}) &= \sum_{i=t}^{t+k-1} (\gamma \lambda)^{i-t} \delta_i
\end{align*}
$$

まず、 exercise 12.1で得た $\lambda$-収益の再帰的な関係を用いると、

$$
\begin{align*}
G_{t:t+k}^{\lambda} &= R_{t+1} + \gamma (1 - \lambda) \hat{v}(S_{t+1}, \mathbf{w}) + \gamma \lambda G_{t+1:t+k}^{\lambda} \\
G_{t:t+k}^{\lambda} - \hat{v}(S_t, \mathbf{w}) &= R_{t+1} + \gamma (1 - \lambda) \hat{v}(S_{t+1}, \mathbf{w}) + \gamma \lambda G_{t+1:t+k}^{\lambda} - \hat{v}(S_t, \mathbf{w}) \\
&= \delta_t + \gamma \lambda (G_{t+1:t+k}^{\lambda} - \hat{v}(S_{t+1}, \mathbf{w}))
\end{align*}
$$

これを繰り返し展開すると、

$$
\begin{align*}
G_{t:t+k}^{\lambda} - \hat{v}(S_t, \mathbf{w}) &= \delta_t + \gamma \lambda \left( \delta_{t+1} + \gamma \lambda (G_{t+2:t+k}^{\lambda} - \hat{v}(S_{t+2}, \mathbf{w})) \right) \\
&= \delta_t + \gamma \lambda \delta_{t+1} + (\gamma \lambda)^2 (G_{t+2:t+k}^{\lambda} - \hat{v}(S_{t+2}, \mathbf{w})) \\
&\ \ \vdots \\
&= \sum_{i=t}^{t+k-1} (\gamma \lambda)^{i-t} \delta_i
\end{align*}
$$

したがって、式(12.10)は価値関数が一定に保たれている場合の一例であることが示された。


# Exercise 12.6

真のオンラインアルゴリズムのダッチとレース以外の特徴的な要素を使わずに、ダッチトレース(12.11)を使用するようにSarsa( $\lambda$ )の疑似コードを修正せよ。線形関数近似とバイナリ特徴を仮定する。

## 解答

式12.11は

$$
\begin{align*}
z_i &\doteq \gamma \lambda z_{i-1} + \left( 1 - \alpha \gamma \lambda z_{i-1}^\top x_i \right) x_i
\end{align*}
$$

Sarsa( $\lambda$ )の疑似コードを以下のように修正する。


- 入力: $s, a$ に対するアクティブな特徴量のインデックス集合を返す関数 $\mathcal{F}(s, a)$
- 入力: 方策 $\pi(a|s)$ ( $q_\pi$ を推定する場合)
- アルゴリズムパラメータ: ステップサイズ $\alpha > 0$, トレース減衰率 $\lambda \in [0, 1]$, 割引率 $\gamma \in [0, 1]$
- 初期化: $\mathbf{w} = (w_1, w_2, \ldots, w_d)^T \in \mathbb{R}^d$ , $\mathbf{z} = (z_1, z_2, \ldots, z_d)^T \in \mathbb{R}^d$ (例えば、 $\mathbf{0}$ に設定)
- 各エピソードについて繰り返し:
  - $S$ を初期化
  - $A \sim \pi(\cdot|S)$ または $\hat{q}(S, \cdot, \mathbf{w})$ に基づいて $\epsilon$-グリーディに選択
  - $\mathbf{z} \leftarrow \mathbf{0}$
  - 各ステップについて繰り返し:
    - 行動 $A$ を実行し、報酬 $R$ と次の状態 $S'$ を観測
    - $\delta \leftarrow R$
    - $S'$ が終端状態の場合:
      - $\delta \leftarrow \delta - \hat{q}(S, A, \mathbf{w})$
      - $\mathbf{w} \leftarrow \mathbf{w} + \alpha \delta \mathbf{z}$
      - 次のエピソードへ移行
    - $A' \sim \pi(\cdot|S')$ または $\hat{q}(S', \cdot, \mathbf{w})$ に基づいて $\epsilon$-グリーディに選択
    - $\delta \leftarrow \delta + \gamma \hat{q}(S', A', \mathbf{w}) - \hat{q}(S, A, \mathbf{w})$
    - $M \leftarrow 0$
    - $\mathcal{F}(S, A)$ において $i$ について繰り返し:
      - $M \leftarrow M + z_i x_i(S, A)$
    - $i = 0, 1, \ldots, d-1$ について繰り返し:
      - $i \in \mathcal{F}(S, A)$ の場合:
        - $z_i \leftarrow \gamma \lambda z_i + (1 - \alpha \gamma \lambda M) x_i(S, A)$
      - それ以外の場合:
        - $z_i \leftarrow \gamma \lambda z_i$
    - $\mathbf{w} \leftarrow \mathbf{w} + \alpha \delta \mathbf{z}$
    - $S \leftarrow S'$
    - $A \leftarrow A'$


# Exercise 12.7

3つの再帰的方程式（12.18、12.19、12.20）を打ち切り型に一般化し、 $G_{t:h}^{\lambda_{s}}$ と $G^{\lambda_{a}}_{t:h}$ を定義せよ。

## 解答

打ち切り型 $\lambda$-収益 $G_{t:h}^{\lambda}$ は、非打ち切り型 $G^{\lambda}_{t}$ の漸化式を $t < h$ の間適用し、最終ステップ（ $t = h−1$ ）でブートストラップ項（ $\hat{v}$ または $\hat{q}$ の推定値）を用いて終了するように定義される。

$t < h$ および $0 \leq t < T$（ $T$ はエピソードの終了時間）を仮定し、可変パラメータ $\gamma_{t+1} = \gamma(S_{t+1})$ および $\lambda_{t+1} = \lambda(S_{t+1}, A_{t+1})$ を使用する。

#### 打ち切り型 $\lambda$-収益 $G^{\lambda}_{t:h}$

$$
\begin{align*}
G^{\lambda_s}_{t:h} &\doteq R_{t+1} + \gamma_{t+1} \left( (1 - \lambda_{t+1}) \hat{v}(S_{t+1}, \mathbf{w}_{t}) + \lambda_{t+1} G^{\lambda_s}_{t+1:h} \right), \qquad t < h
\end{align*}
$$

ここで

$$
G^{\lambda_s}_{h:h} \doteq \hat{v}(S_h, \mathbf{w}_{h-1})
$$

#### 打ち切り型 $\lambda$-収益 $G^{\lambda_a}_{t:h}$

$$
\begin{align*}
G^{\lambda_a}_{t:h} &\doteq R_{t+1} + \gamma_{t+1} \left( (1 - \lambda_{t+1}) \hat{q}(S_{t+1}, A_{t+1}, \mathbf{w}_{t}) + \lambda_{t+1} G^{\lambda_a}_{t+1:h} \right), \qquad t < h
\end{align*}
$$

ここで

$$
G^{\lambda_a}_{h:h} \doteq \hat{q}(S_h, A_h, \mathbf{w}_{h-1})
$$

また、期待Sarsa形式の打ち切り型 $\lambda$-収益 $G^{\lambda_e}_{t:h}$ も同様に定義できる。

$$
\begin{align*}
G^{\lambda_a}_{t:h} &\doteq R_{t+1} + \gamma_{t+1} \left( (1 - \lambda_{t+1}) \sum_{a} \pi(a|S_{t+1}) \hat{q}(S_{t+1}, a, \mathbf{w}_{t}) + \lambda_{t+1} G^{\lambda_e}_{t+1:h} \right) \\
&= R_{t+1} + \gamma_{t+1} \left( (1 - \lambda_{t+1}) \overline{V}_{t}(S_{t+1}) + \lambda_{t+1} G^{\lambda_e}_{t+1:h} \right), \qquad t < h
\end{align*}
$$

ここで

$$
G^{\lambda_e}_{h:h} \doteq \sum_{a} \pi(a|S_h) \hat{q}(S_h, a, \mathbf{w}_{h-1}) = \overline{V}_{h-1}(S_h)
$$


# Exercise 12.8

価値関数が変化しない場合、式(12.24)が厳密になることを証明せよ。
記述を簡潔にするため、 $t = 0$ の場合を考え、 $V_k \doteq \hat{v}(S_k, \mathbf{w})$ という記法を用いよ。

## 解答

式(12.24)は以下である。

$$
\begin{align*}
\delta_{t}^{s} &\doteq R_{t+1} + \gamma_{t+1} \hat{v}(S_{t+1}, \mathbf{w}_t) - \hat{v}(S_t, \mathbf{w}_t) \\
G^{\lambda_s}_{t} &\approx \hat{v}(S_t, \mathbf{w}_t) + \rho_t \sum_{k=t}^{\infty} \delta_{k}^{s} \prod_{i=t+1}^{k} \gamma_i \lambda_i \rho_i
\end{align*}
$$

$t = 0$ の場合、式(12.24)が厳密に成り立つことを証明する。すなわち、

$$
\begin{align*}
G^{\lambda_s}_{0} &= V_0 + \rho_0 \sum_{k=0}^{\infty} \delta^s_k \prod_{i=1}^{k} \gamma_i \lambda_i \rho_i
\end{align*}
$$

価値関数が変化しない場合、すなわち

$$\mathbf{w}_t = \mathbf{w}$$

の場合、
$\delta^{s}\_{t}$ と $G^{\lambda_s}_{t}$ (式12.22) は以下のようになる。

$$
\begin{align*}
\delta^s_t &\doteq R_{t+1} + \gamma_{t+1} V_{t+1} - V_t \\
G^{\lambda_s}_{t} &\doteq \rho_t \left( R_{t+1} + \gamma_{t+1} \left( (1-\lambda_{t+1}) V_{t+1} + \lambda_{t+1} G^{\lambda_s}_{t+1} \right) \right) + (1-\rho_t)V_t
\end{align*}
$$

まず、 $G^{\lambda_s}_{0}$ を展開する。

$$
\begin{align*}
G^{\lambda_s}_{0} &= \rho_0 \left( R_{1} + \gamma_{1} \left( (1-\lambda_{1}) V_{1} + \lambda_{1} G^{\lambda_s}_{1} \right) \right) + (1-\rho_0)V_0 \\
&= \rho_0 R_{1} + \rho_0 \gamma_{1} (1-\lambda_{1}) V_{1} + \rho_0 \gamma_{1} \lambda_{1} G^{\lambda_s}_{1} + (1-\rho_0)V_0 \\
&= \rho_0 \left( R_{1} + \gamma_{1} V_{1} - \gamma_{1} \lambda_{1} V_{1} \right) + \rho_0 \gamma_{1} \lambda_{1} G^{\lambda_s}_{1} + (1-\rho_0)V_0 \\
&= \rho_0 R_{1} + \rho_0 \gamma_{1} V_{1} - \rho_0 \gamma_{1} \lambda_{1} V_{1} + \rho_0 \gamma_{1} \lambda_{1} G^{\lambda_s}_{1} + V_0 - \rho_0 V_0 \\
&= V_0 + \rho_0 \left( R_{1} + \gamma_{1} V_{1} - V_0 \right) + \rho_0 \gamma_{1} \lambda_{1} \left( G^{\lambda_s}_{1} - V_{1} \right) \\
&= V_0 + \rho_0 \delta^s_0 + \rho_0 \gamma_{1} \lambda_{1} \left( G^{\lambda_s}_{1} - V_{1} \right)
\end{align*}
$$

次に、 $G^{\lambda_s}_{1}$ を同様に展開する。

$$
\begin{align*}
G^{\lambda_s}_{1} &= V_1 + \rho_1 \delta^s_1 + \rho_1 \gamma_{2} \lambda_{2} \left( G^{\lambda_s}_{2} - V_{2} \right)
\end{align*}
$$

これを $G^{\lambda_s}_{0}$ の式に代入すると、

$$
\begin{align*}
G^{\lambda_s}_{0} &= V_0 + \rho_0 \delta^s_0 + \rho_0 \gamma_{1} \lambda_{1} \left( V_1 + \rho_1 \delta^s_1 + \rho_1 \gamma_{2} \lambda_{2} \left( G^{\lambda_s}_{2} - V_{2} \right) - V_{1} \right) \\
&= V_0 + \rho_0 \delta^s_0 + \rho_0 \gamma_{1} \lambda_{1} \rho_1 \delta^s_1 + \rho_0 \gamma_{1} \lambda_{1} \rho_1 \gamma_{2} \lambda_{2} \left( G^{\lambda_s}_{2} - V_{2} \right)
\end{align*}
$$

この過程を繰り返すと、一般項が得られる。

$$
\begin{align*}
G^{\lambda_s}_{0} &= V_0 + \rho_0 \delta^s_0 + \rho_0 \gamma_{1} \lambda_{1} \rho_1 \delta^s_1 + \rho_0 \gamma_{1} \lambda_{1} \rho_1 \gamma_{2} \lambda_{2} \delta^s_2 + \cdots \\
&= V_0 + \rho_0 \sum_{k=0}^{\infty} \delta^s_k \prod_{i=1}^{k} \gamma_i \lambda_i \rho_i
\end{align*}
$$

したがって、式(12.24)が厳密に成り立つことが示された。


# Exercise 12.9

一般的なオフ方策収益の打ち切り版は $G^{\lambda_s}_{t:h}$ で表される。式(12.24)に基づいて、正しい方程式を推測せよ。

## 解答

式(12.24)は以下である。

$$
\begin{align*}
G^{\lambda_s}_{t} &\approx \hat{v}(S_t, \mathbf{w}_t) + \rho_t \sum_{k=t}^{\infty} \delta_{k}^{s} \prod_{i=t+1}^{k} \gamma_i \lambda_i \rho_i
\end{align*}
$$

打ち切り版 $G^{\lambda_s}_{t:h}$ に対して、同様の形式で表現できると推測される。

$$
\begin{align*}
G^{\lambda_s}_{t:h} &\approx \hat{v}(S_t, \mathbf{w}_{h-1}) + \rho_t \sum_{k=t}^{h-1} \delta_{k}^{s} \prod_{i=t+1}^{k} \gamma_i \lambda_i \rho_i \\
\delta_{k}^{s} &\doteq R_{k+1} + \gamma_{k+1} \hat{v}(S_{k+1}, \mathbf{w}_{h-1}) - \hat{v}(S_k, \mathbf{w}_{h-1})
\end{align*}
$$


# Exercise 12.10

価値関数が変化しない場合、式(12.27)が厳密になることを証明せよ。
記述を簡潔にするため、 $t = 0$ の場合を考え、 $Q_k = \hat{q}(S_k , A_k , \mathbf{w})$ という記法を用いよ。

ヒント:

まず $\delta_{0}^{a}$ と $G_{0}^{\lambda_a}$ を書き出し、次に $G^{\lambda_a}_{0} - Q_0$ を求めよ。

## 解答

式(12.27)は以下である。

$$
\begin{align*}
\delta_{t}^{a} &\doteq R_{t+1} + \gamma_{t+1} \overline{V}_{t}(S_{t+1}) - \hat{q}(S_t, A_t, \mathbf{w}_t) \\
G^{\lambda_a}_{t} &\approx \hat{q}(S_t, A_t, \mathbf{w}_t) + \sum_{k=t}^{\infty} \delta_{k}^{a} \prod_{i=t+1}^{k} \gamma_i \lambda_i \rho_i
\end{align*}
$$

$t = 0$ の場合、式(12.27)が厳密に成り立つことを証明する。すなわち、

$$
\begin{align*}
G^{\lambda_a}_{0} = Q_0 + \sum_{k=0}^{\infty} \delta^a_k \prod_{i=1}^{k} \gamma_i \lambda_i \rho_i
\end{align*}
$$

価値関数が変化しない場合、すなわち $\mathbf{w_t} = \mathbf{w}$ の場合、 $\delta_{t}^{a}, G^{\lambda_a}_{t}$ (式12.26) は以下のようになる。

$$
\begin{align*}
\delta^a_t &\doteq R_{t+1} + \gamma_{t+1} \overline{V}(S_{t+1}) - Q_t \\
G^{\lambda_a}_{t} &\doteq R_{t+1} + \gamma_{t+1} \left( \overline{V}(S_{t+1}) + \lambda_{t+1} \rho_{t+1} \left[ G^{\lambda_a}_{t+1} - Q_{t+1} \right] \right)
\end{align*}
$$

まず、 $G^{\lambda_a}_{0}$ を展開する。

$$
\begin{align*}
G^{\lambda_a}_{0} &= R_{1} + \gamma_{1} \left( \overline{V}(S_{1}) + \lambda_{1} \rho_{1} \left[ G^{\lambda_a}_{1} - Q_{1} \right] \right) \\
&= R_{1} + \gamma_{1} \overline{V}(S_{1}) + \gamma_{1} \lambda_{1} \rho_{1} \left( G^{\lambda_a}_{1} - Q_{1} \right) \\
&= Q_0 + \left( R_{1} + \gamma_{1} \overline{V}(S_{1}) - Q_0 \right) + \gamma_{1} \lambda_{1} \rho_{1} \left( G^{\lambda_a}_{1} - Q_{1} \right) \\
&= Q_0 + \delta^a_0 + \gamma_{1} \lambda_{1} \rho_{1} \left( G^{\lambda_a}_{1} - Q_{1} \right)
\end{align*}
$$

次に、 $G^{\lambda_a}_{0} - Q_0$ を求める。

$$
\begin{align*}
G^{\lambda_a}_{0} - Q_0 &= \delta^a_0 + \gamma_{1} \lambda_{1} \rho_{1} \left( G^{\lambda_a}_{1} - Q_{1} \right)
\end{align*}
$$

これを繰り返し展開すると、

$$
\begin{align*}
G^{\lambda_a}_{0} - Q_0 &= \delta^a_0 + \gamma_{1} \lambda_{1} \rho_{1} \left( \delta^a_1 + \gamma_{2} \lambda_{2} \rho_{2} \left( G^{\lambda_a}_{2} - Q_{2} \right) \right) \\
&= \delta^a_0 + \gamma_{1} \lambda_{1} \rho_{1} \delta^a_1 + \gamma_{1} \lambda_{1} \rho_{1} \gamma_{2} \lambda_{2} \rho_{2} \left( G^{\lambda_a}_{2} - Q_{2} \right) \\
&= \delta^a_0 + \gamma_{1} \lambda_{1} \rho_{1} \delta^a_1 + \gamma_{1} \lambda_{1} \rho_{1} \gamma_{2} \lambda_{2} \rho_{2} \delta^a_2 + \cdots \\
&= \sum_{k=0}^{\infty} \delta^a_k \prod_{i=1}^{k} \gamma_i \lambda_i \rho_i
\end{align*}
$$

したがって、式(12.27)が厳密に成り立つことが示された。


# Exercise 12.11

一般的なオフ方策収益の打ち切り版は $G^{\lambda_a}_{t:h}$ で表される。式(12.27)に基づいて、正しい方程式を推測せよ。

## 解答

式(12.27)は以下である。

$$
\begin{align*}
G^{\lambda_a}_{t} &\approx \hat{q}(S_t, A_t, \mathbf{w}_t) + \sum_{k=t}^{\infty} \delta_{k}^{a} \prod_{i=t+1}^{k} \gamma_i \lambda_i \rho_i
\end{align*}
$$

打ち切り版 $G^{\lambda_a}_{t:h}$ に対して、同様の形式で表現できると推測される。

$$
\begin{align*}
G^{\lambda_a}_{t:h} &\approx \hat{q}(S_t, A_t, \mathbf{w}_{h-1}) + \sum_{k=t}^{h-1} \delta_{k}^{a} \prod_{i=t+1}^{k} \gamma_i \lambda_i \rho_i \\
\delta_{k}^{a} &\doteq R_{k+1} + \gamma_{k+1} \overline{V}_{h-1}(S_{k+1}) - \hat{q}(S_k, A_k, \mathbf{w}_{h-1})
\end{align*}
$$


# Exercise 12.12

式(12.27)から式(12.29)を導出する上記の手順を詳細に示せ。
更新式(12.15)から始め、 $G_{t}^{\lambda}$ を式(12.26)の $G^{\lambda_a}_{t}$ で置き換え、式(12.25)に至ったのと同様の手順に従え。

## 解答
行動価値ベースの $\lambda$ リターンの近似形である式(12.27)

$$
G^{\lambda_a}_t \approx q̂(S_t, A_t, w_t) + \sum_{k=t}^{\infty} \delta^a_k \prod_{i=t+1}^{k} \gamma_i \lambda_i \rho_i
$$

ここで、 $\delta^a_k$ は行動価値ベースのTD誤差（式(12.28)で定義される期待値形式）、 $\rho_i = \pi(A_i|S_i) / b(A_i|S_i)$ は単ステップの重要度サンプリング比である。

から、行動価値に対する適格度トレースである式(12.29)

$$
\begin{align*}
z_t &\doteq \gamma_t \lambda_t \rho_t \mathbf{z}_{t-1} + \nabla_{w} q̂(S_t, A_t, \mathbf{w}_t)
\end{align*}
$$

を導出する手順を詳細に示す。

まず、更新式(12.15)を考える。

$$
\begin{align*}
\mathbf{w}_{t+1} &\doteq \mathbf{w}_t + \alpha \left( G^{\lambda}_{t} - \hat{q}(S_t, A_t, \mathbf{w}_t) \right) \nabla_{w} \hat{q}(S_t, A_t, \mathbf{w}_t)
\end{align*}
$$

ここで、 $G_{t}^{\lambda}$ を式(12.27)の $G^{\lambda_a}_{t}$ で置き換える。

$$
\begin{align*}
\mathbf{w}_{t+1} &\approx \mathbf{w}_t + \alpha \left( \hat{q}(S_t, A_t, \mathbf{w}_t) + \sum_{k=t}^{\infty} \delta^a_k \prod_{i=t+1}^{k} \gamma_i \lambda_i \rho_i - \hat{q}(S_t, A_t, \mathbf{w}_t) \right) \nabla_{w} \hat{q}(S_t, A_t, \mathbf{w}_t) \\
&= \mathbf{w}_t + \alpha \left( \sum_{k=t}^{\infty} \delta^a_k \prod_{i=t+1}^{k} \gamma_i \lambda_i \rho_i \right) \nabla_{w} \hat{q}(S_t, A_t, \mathbf{w}_t)
\end{align*}
$$

次に、式(12.25)に至るために、更新式を適格度トレースの形式に変換する。

$$
\begin{align*}
\mathbf{w}_{t+1} &\approx \mathbf{w}_t + \alpha \sum_{k=t}^{\infty} \delta^a_k \left( \prod_{i=t+1}^{k} \gamma_i \lambda_i \rho_i \right) \nabla_{w} \hat{q}(S_t, A_t, \mathbf{w}_t) \\
&= \mathbf{w}_t + \alpha \sum_{k=t}^{\infty} \delta^a_k \left( \gamma_{t+1} \lambda_{t+1} \rho_{t+1} \prod_{i=t+2}^{k} \gamma_i \lambda_i \rho_i \right) \nabla_{w} \hat{q}(S_t, A_t, \mathbf{w}_t)
\end{align*}
$$

ここで、エピソード全体（または継続的なタスクの無限の時間）にわたる更新の合計

$$
\sum_{t=0}^{\infty} \mathbf{w}_{t+1} - \mathbf{w}_{t} = \sum_{t=0}^{\infty} \Delta \mathbf{w}_{t}
$$

を考える。

総和の順序を入れ替えると、( $\sum_{t=0}^{\infty} \sum_{k=t}^{\infty} = \sum_{k=0}^{\infty} \sum_{t=0}^{k}$ )

$$
\begin{align*}
\sum_{t=0}^{\infty} \Delta \mathbf{w}_t &\approx \alpha \sum_{k=0}^{\infty} \delta^a_k \left( \sum_{t=0}^{k} \left( \prod_{i=t+1}^{k} \gamma_i \lambda_i \rho_i \right) \nabla_{w} \hat{q}(S_t, A_t, \mathbf{w}_t) \right)
\end{align*}
$$

ここで、内側の和を適格度トレース $\mathbf{z}_k$ と定義する。

$$
\begin{align*}
\mathbf{z}_k &\doteq \sum_{t=0}^{k} \left( \prod_{i=t+1}^{k} \gamma_i \lambda_i \rho_i \right) \nabla_{w} \hat{q}(S_t, A_t, \mathbf{w}_t)
\end{align*}
$$

この適格度トレース $\mathbf{z_k}$ を時間ステップ $k$ に関して再帰的に表現するために、 $\mathbf{z}_{k-1}$ を用いて書き直す。 総和の部分を $t = 0$ から $t = k-1$ と $t = k$ に分割する。

$$
\begin{align*}
\mathbf{z}_k &= \sum_{t=0}^{k-1} \left( \prod_{i=t+1}^{k} \gamma_i \lambda_i \rho_i \right) \nabla_{w} \hat{q}(S_t, A_t, \mathbf{w}_t) + \left( \prod_{i=k+1}^{k} \gamma_i \lambda_i \rho_i \right) \nabla_{w} \hat{q}(S_k, A_k, \mathbf{w}_k) \\
&= \sum_{t=0}^{k-1} \left( \prod_{i=t+1}^{k-1} \gamma_i \lambda_i \rho_i \right) \gamma_k \lambda_k \rho_k \nabla_{w} \hat{q}(S_t, A_t, \mathbf{w}_t) + \nabla_{w} \hat{q}(S_k, A_k, \mathbf{w}_k) \\
&= \gamma_k \lambda_k \rho_k \sum_{t=0}^{k-1} \left( \prod_{i=t+1}^{k-1} \gamma_i \lambda_i \rho_i \right) \nabla_{w} \hat{q}(S_t, A_t, \mathbf{w}_t) + \nabla_{w} \hat{q}(S_k, A_k, \mathbf{w}_k) \\
&= \gamma_k \lambda_k \rho_k \mathbf{z}_{k-1} + \nabla_{w} \hat{q}(S_k, A_k, \mathbf{w}_k)
\end{align*}
$$

したがって、式(12.29)が導出された。


# Exercise 12.13

状態価値法と行動価値法におけるオフ方策適格度トレースのダッチトレース版と置換トレース版は何か?

## 解答

#### 状態価値法

オフ方策学習における状態価値法（TD( $\lambda$ )）の累積トレースは、式(12.25) である。

$$
\begin{align*}
\mathbf{z}_t = \rho_t (\gamma_t \lambda_t \mathbf{z}_{t-1} + \nabla \hat{v}(S_t, \mathbf{w}_t))
\end{align*}
$$

#### ダッチトレース版

真のオンラインTD( $\lambda$ )の式(12.11)に重要度サンプリング比 $\rho_t$ を組み込んだものである。

$$
\begin{align*}
\mathbf{z}_t &\doteq \gamma_t \lambda_t \rho_t \mathbf{z}_{t-1} + \left( 1 - \alpha \gamma_t \lambda_t \rho_t \mathbf{z}_{t-1}^\top \mathbf{x}_t(S_t) \right) \mathbf{x}_t(S_t)
\end{align*}
$$

#### 置換トレース版

置換トレースは式(12.12)で示され、現在のタイムステップで特徴がアクティブになった場合そのトレース要素を 1 に置換し、そうでなければ減衰させる。
オフ方策の文脈では、この置換のプロセスが重要度サンプリング比 $\rho_t$ によって変調される。具体的には、特徴がアクティブな場合、そのトレース要素は $\rho_t$ を用いて更新されるが、累積ではなく過去の値を上書きする形になる。

$$
\begin{align*}
z_{i,t} &\doteq \begin{cases}
\rho_t & \text{if } x_i(S_t) = 1 \\
\gamma_t \lambda_t z_{i,t-1} & \text{if } x_i(S_t) = 0
\end{cases}
\end{align*}
$$

### 行動価値法

オフ方策学習における行動価値法の累積トレースは、式(12.29) である。

$$
\begin{align*}
\mathbf{z}_t = \gamma_t \lambda_t \rho_t \mathbf{z}_{t-1} + \nabla \hat{q}(S_t, A_t, \mathbf{w}_t)
\end{align*}
$$

#### ダッチトレース版

$$
\begin{align*}
\mathbf{z}_t &\doteq \gamma_t \lambda_t \rho_t \mathbf{z}_{t-1} + \left( 1 - \alpha \gamma_t \lambda_t \rho_t \mathbf{z}_{t-1}^\top \mathbf{x}_t(S_t, A_t) \right) \mathbf{x}_t(S_t, A_t)
\end{align*}
$$

#### 置換トレース版

$$
\begin{align*}
z_{i,t} &\doteq \begin{cases}
\rho_t & \text{if } x_i(S_t, A_t) = 1 \\
\gamma_t \lambda_t z_{i,t-1} & \text{if } x_i(S_t, A_t) = 0
\end{cases}
\end{align*}
$$


# Exercise 12.14

二重期待Sarsa法は、どのようにして適格度トレースに拡張できるだろうか。

## 解答

まず、適格度トレースを用いない**二重期待Sarsa（Double Expected Sarsa）**を導出し、それを適格度トレースに拡張する。

#### 二重期待Sarsa

二重学習（Double Learning）は、最大化バイアスを避けるために2つの独立した価値関数推定器 $Q_1$ と $Q_2$ を使用する。更新対象の推定器（例えば $Q_1$）を決定した後、ターゲット値の計算にはもう一方の推定器（ $Q_2$ ）を使用する。

期待Sarsa（Expected Sarsa）は、ターゲット値の計算において、次の行動の価値の代わりに、現在の方策 $\pi$ に基づく期待値を使用する。

これらを組み合わせると、 $Q_1$ を更新する場合のTD誤差 $\delta_t$ は以下のようになる。

$$
\delta_t = R_{t+1} + \gamma \sum_a \pi(a|S_{t+1}) Q_2(S_{t+1}, a) - Q_1(S_t, A_t)
$$

ここで、 $\pi(a|S_{t+1})$ はターゲット方策（通常は $Q_1$ と $Q_2$ の平均や和に基づく $\epsilon$-greedy 方策など）である。この式は、二重学習の「評価と選択の分離」と、期待Sarsaの「期待値による分散低減」を兼ね備えている。

#### 適格度トレースへの拡張（二重期待Sarsa($\lambda$)）

このアルゴリズムを適格度トレースに拡張するには、各推定器 $Q_1, Q_2$ に対応する適格度トレースベクトル $\mathbf{z}_1, \mathbf{z}_2$ を導入する。

各ステップでの更新手順は以下のようになる。

#### 1. 更新する推定器の選択:

確率（例えば0.5）で $Q_1$ または $Q_2$ のどちらを更新するかを選択する。ここでは $Q_1$ が選ばれたとする。

#### 2. TD誤差の計算:
前述の二重期待SarsaのTD誤差を計算する。

$$
\delta_t = R_{t+1} + \gamma \sum_a \pi(a|S_{t+1}) Q_2(S_{t+1}, a) - Q_1(S_t, A_t)
$$

#### 3. 適格度トレースの更新:
選ばれた推定器に対応するトレース $\mathbf{z}_1$ を更新する。

$$
\mathbf{z}_1 \leftarrow \gamma \lambda \mathbf{z}_1 + \nabla Q_1(S_t, A_t)
$$

（他方のトレース $\mathbf{z}_2$ は更新しない、あるいは減衰のみ行う）

#### 4. 重みの更新:

TD誤差とトレースを用いて、選ばれた推定器の重み $\mathbf{w}_1$ を更新する。

$$
\mathbf{w}_1 \leftarrow \mathbf{w}_1 + \alpha \delta_t \mathbf{z}_1
$$

このようにして、二重期待Sarsaの安定性とバイアス除去の特性を維持しつつ、適格度トレースによる学習効率の向上を図ることができる。
