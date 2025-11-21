# 第7章 演習問題

# Exercise 7.1

第６章においてモンテカルロ誤差は、推定価値をエピソード内で固定した場合に、TD 誤差 (6.6) の総和として書けることを示した。
$n$ ステップ誤差 (7.2) に対しても同様に書けることを示せ。

## 回答

#### ● 式 (6.6) 、 (7.2) の再掲

式 (6.6)

$$
G_{t} - V_t(S_t) = \sum_{k=t}^{T-1} \gamma^{k-t} \delta_k
\\
\text{ただし $\delta_k$ は TD 誤差} \quad
\delta_k = R_{k+1} + \gamma V(S_{k+1}) - V(S_k)
$$

式 (7.2)

$$
\begin{aligned}
V_{t+n}(S_t) &= V_{t+n-1}(S_t) + \alpha \left[
  G_{t:t+n} - V_{t+n-1}(S_t)
\right], \quad 0 \leq t < T
\end{aligned}
$$

#### ● 証明
$n$ ステップ誤差を展開すると、

$$
\begin{aligned}
G_{t:t+n} - V_{t+n-1}(S_t)
&= R_{t+1} + \gamma R_{t+2} + \cdots + \gamma^{n-1} R_{t+n} + \gamma^n V_{t+n-1}(S_{t+n}) - V_{t+n-1}(S_t)
\\
\text{($V$ is fixed in episode)}
\\
&= R_{t+1} + \gamma R_{t+2} + \cdots + \gamma^{n-1} R_{t+n} + \gamma^n V(S_{t+n}) - V(S_t)
\\
&= \delta_t - \gamma V(S_{t+1}) + V(S_t) + \gamma R_{t+2} + \cdots + \gamma^{n-1} R_{t+n} + \gamma^n V(S_{t+n}) - V(S_t)
\\
&= \delta_t + \gamma \left(
  R_{t+2} + \gamma R_{t+3} + \cdots + \gamma^{n-2} R_{t+n} + \gamma^{n-1} V(S_{t+n}) - V(S_{t+1})
\right)
\\
&= \delta_t + \gamma \left(
  G_{t+1:t+n} - V_{t+n-1}(S_{t+1})
\right)
\\
&= \delta_t + \gamma \left(
  G_{t+1:t+n} - V_{t+n-2}(S_{t+1})
\right)
\\
&= \delta_t + \gamma \delta_{t+1} + \gamma^2 \left(
  G_{t+2:t+n} - V_{t+n-3}(S_{t+2})
\right)
\\
&\ \ \vdots
\\
&= \sum_{k=t}^{t+n-1} \gamma^{k-t} \delta_k + \gamma^n \left(
  G_{t+n:t+n} - V_{t-1}(S_{t+n})
\right)
\\
&= \sum_{k=t}^{t+n-1} \gamma^{k-t} \delta_k + \gamma^n \left(
  V(S_{t+n}) - V(S_{t+n})
\right)
\\
&= \sum_{k=t}^{t+n-1} \gamma^{k-t} \delta_k
\end{aligned}
$$

したがって、 $n$ ステップ誤差は TD 誤差の総和として次のように書ける。

$$
G_{t:t+n} - V_{t+n-1}(S_t) = \sum_{k=t}^{t+n-1} \gamma^{k-t} \delta_k
$$


# Exercise 7.2

$n$-step TD で、もし (7.2) の TD 誤差の代わりに“TD 誤差の和（前問の式）をそのまま使ったらどうなる？
それは良いアルゴリズムか？悪いアルゴリズムか？小さな実験を書いて答えよ。

## 回答

式 (7.2):

$$
\begin{aligned}
V_{t+n}(S_t) &= V_{t+n-1}(S_t) + \alpha \left[
G_{t:t+n} - V_{t+n-1}(S_t)
\right], \quad 0 \leq t < T
\end{aligned}
$$

もし $V$ がエピソード内で固定されている場合、前問の結果より、 $n$-step TD は次のように書ける。

$$
G_{t:t+n} - V_{t+n-1}(S_t) = \sum_{k=t}^{t+n-1} \gamma^{k-t} \delta_k
$$

しかし、実際には $V$ はエピソード内で更新されるため、上記の等式は成り立たない（別のアルゴリズムになる）。

#### ● TD 誤差の和を使ったアルゴリズムは良いアルゴリズムか？
TD 誤差の和を使ったアルゴリズムは、理論的には収束性や安定性に問題が生じる可能性があるため、必ずしも良いアルゴリズムとは言えない。
なぜなら、古い TD 誤差が現在の価値関数の更新に影響を与えるため、誤差が蓄積されやすくなるからである。

#### ● 小さな実験
See exercise_7_2_experiment.py


# Exercise 7.3

1. なぜ本章では 5-state ではなく 19-state の Random Walk を使ったのか？
2. 5-state のような小さな問題では、 $n$ によって有効性が変わるか？
3. 左側の報酬を 0 -> -1 に変えたことは、最良な $n$ の値に影響を与えるか？

## 回答

### ● 1. エピソード長が十分に長くなるため、n-step TD の比較がしやすい
5-state Random Walk の場合、C（中央）から始めるとエピソードの長さは 5〜10ステップ程度となる。
一方、19-state の場合、中央の state 10 から始めると平均エピソード長は 約 100 ステップに伸びる。

$n$ の違いによる性能差を観察するためには、エピソード長が十分に長いことが望ましい。

ちなみに、 $n=1$ はTD(0) に対応し、 $n$ がエピソード長に近づくほどモンテカルロ法に近づく。

### ● 2. 小さな問題では n の影響は小さい
5-state Random Walk のような小さな問題では、エピソード長が短いため、 $n$ の違いによる性能差はあまり顕著ではない。
エピソードが短いため、 $n$ を大きくしても、価値関数の更新に与える影響が限定的になるからである。

### ● 3. 左側の報酬を -1 に変えても最良な n の値には大きな影響はない
左側の報酬を 0 から -1 に変えることで、エピソード全体の報酬構造が変わるが、最良な $n$ の値には大きな影響はない。
なぜなら、 $n$ の選択は主にエピソード長と価値関数の更新頻度に依存するため、報酬の具体的な値よりもエピソードの構造が重要だからである。


# Exercise 7.4

Sarsa 法の $n$ ステップ収益 (7.4) が、以下のような新しい TD 誤差の和として書けることを示せ。

$$
G_{t:t+n} = Q_{t-1}(S_t, A_t) + \sum_{k=t}^{\min(t+n, T)-1} \gamma^{k-t} \big[
  R_{k+1} + \gamma Q_{k}(S_{k+1}, A_{k+1}) - Q_{k-1}(S_k, A_k)
\big]
$$

## 回答
#### ● 式 (7.4) の再掲
$$
G_{t:t+n} = R_{t+1} + \gamma R_{t+2} + \cdots + \gamma^{n-1} R_{t+n} + \gamma^n Q_{t+n-1}(S_{t+n}, A_{t+n})
\\
\text{ただし } n \geq 1, \quad 0 \leq t < T
$$

#### ● 証明
$n$ ステップ収益を展開すると、

$$
\begin{aligned}
G_{t:t+n}
&= R_{t+1} + \gamma R_{t+2} + \cdots + \gamma^{n-1} R_{t+n} + \gamma^n Q_{t+n-1}(S_{t+n}, A_{t+n})
\\
&= R_{t+1} + \gamma G_{t+1:t+n}
\end{aligned}
$$

TD 誤差を次のように定義する。

$$
\delta_k = R_{k+1} + \gamma Q_{k}(S_{k+1}, A_{k+1}) - Q_{k-1}(S_k, A_k)
$$

差分を考えると、

$$
\begin{aligned}
G_{t:t+n} - Q_{t-1}(S_t, A_t)
&= R_{t+1} + \gamma G_{t+1:t+n} - Q_{t-1}(S_t, A_t)
\\
&= R_{t+1} + \gamma Q_{t}(S_{t+1}, A_{t+1}) - Q_{t-1}(S_t, A_t) + \gamma G_{t+1:t+n} - Q_{t-1}(S_t, A_t) - \gamma Q_{t}(S_{t+1}, A_{t+1}) + Q_{t-1}(S_t, A_t)
\\
&= \delta_t + \gamma \left(
  G_{t+1:t+n} - Q_{t}(S_{t+1}, A_{t+1})
\right)
\\
&= \delta_t + \gamma \delta_{t+1} + \gamma^2 \left(
  G_{t+2:t+n} - Q_{t+1}(S_{t+2}, A_{t+2})
\right)
\\
&\ \ \vdots
\\
&= \sum_{k=t}^{t+n-1} \gamma^{k-t} \delta_k + \gamma^n \left(
  G_{t+n:t+n} - Q_{t+n-1}(S_{t+n}, A_{t+n})
\right)
\\
&= \sum_{k=t}^{t+n-1} \gamma^{k-t} \delta_k + \gamma^n \left(
  Q(S_{t+n}, A_{t+n}) - Q(S_{t+n}, A_{t+n})
\right)
\\
&= \sum_{k=t}^{t+n-1} \gamma^{k-t} \delta_k
\end{aligned}
$$

したがって、 $n$ ステップ収益は TD 誤差の総和として次のように書ける。

$$
G_{t:t+n} = Q_{t-1}(S_t, A_t) + \sum_{k=t}^{\min(t+n, T)-1} \gamma^{k-t} \big[
  R_{k+1} + \gamma Q_{k}(S_{k+1}, A_{k+1}) - Q_{k-1}(S_k, A_k)
\big]
$$


# Exercise 7.5

Section 7.4 “Per-decision Methods with Control Variates”
に対応する Off-policy n-step state-value prediction（per-decision importance sampling + control variate 版） の疑似コードを書け。

## 回答

$n$-step 収益 $G_{t:t+n}$ は以下のように定義される。

$$
\begin{aligned}
G_{t:h} &= \rho_t \left(R_{t+1} + \gamma G_{t+1:h}
\right) + (1 - \rho_t) V_{h-1}(S_t)
\\
\text{ただし } \rho_t &= \frac{\pi(A_t | S_t)}{b(A_t | S_t)}, \quad t \lt h \lt T
\end{aligned}
$$

終端においては、 $G_{h:h} = V_{h-1}(S_h)$ である。


```Algorithm: Off-policy n-step state-value prediction with per-decision importance sampling and control variate
Input: an arbitrary behavior policy b such that b(a|s) > 0, for all s in S, a in A
Initialize V(s) arbitrarily for all nonterminal states s
Set n (the horizon length)

Loop forever (for each episode):
    Initialize a buffer of states S, actions A, rewards R
    t ← 0
    T ← ∞
    Initialize S0

    Choose A0 ~ b(·|S0)   # behavior policy

    while True:
        if t < T:
            Take action At, observe Rt+1 and St+1

            If St+1 is terminal:
                T ← t + 1
            else:
                Choose At+1 ~ b(·|St+1)

        τ ← t − n + 1     # time whose update becomes available

        if τ ≥ 0:
            # --- Compute per-decision off-policy return G_{τ : τ+n} ---
            h ← min(τ + n, T)
            G ← V(S_h)      # base: G_{h:h} = V_{h-1}(S_h)

            for k = h−1 down to τ:
                ρ ← π(A_k | S_k) / b(A_k | S_k)
                G ← ρ * (R_{k+1} + gamma * G) + (1 − ρ) * V(S_k)

            # --- TD update ---
            V(S_τ) ← V(S_τ) + α * (G − V(S_τ))

        if τ == T − 1:
            break

        t ← t + 1
```

# Exercise 7.6

式 (7.14) における制御変量は、収益の期待値を変えないことを示せ。

## 回答
式 (7.14) :

$$
G_{t:h} = R_{t+1} + \gamma \big(
  \rho_{t+1} G_{t+1:h} + \bar{V}_{h-1}(S_{t+1}) - \rho_{t+1} Q_{h-1}(S_{t+1}, A_{t+1})
\big)
$$

示すべきことは、

$$
\mathbb{E}[G_{t:h}]
= \mathbb{E}\left[R_{t+1} + \gamma G_{t+1:h}\right]
$$

つまり、制御変量の期待値がゼロであることを示せばよい。

まず、(7.14) の期待値を計算する。

$$
\begin{aligned}
\mathbb{E}[G_{t:h}]
&= \mathbb{E}\left[R_{t+1} + \gamma \big(
  \rho_{t+1} G_{t+1:h} + \bar{V}_{h-1}(S_{t+1}) - \rho_{t+1} Q_{h-1}(S_{t+1}, A_{t+1})
\big)\right]
\end{aligned}
$$

行動は挙動方策 $b$ に従うため、 $\rho_{t+1}$ の期待値は次のようになる。

$$
\begin{aligned}
\mathbb{E}[\rho_{t+1} | S_{t+1}]
&= \sum_{a} b(a | S_{t+1}) \frac{\pi(a | S_{t+1})}{b(a | S_{t+1})}
\\
&= \sum_{a} \pi(a | S_{t+1}) = 1
\end{aligned}
$$

したがって、制御変量の期待値は次のようになる。

$$
\begin{aligned}
\mathbb{E}\left[\bar{V}_{h-1}(S_{t+1}) - \rho_{t+1} Q_{h-1}(S_{t+1}, A_{t+1})\right]
&= \mathbb{E}\left[\bar{V}_{h-1}(S_{t+1})\right] - \mathbb{E}\left[\rho_{t+1} Q_{h-1}(S_{t+1}, A_{t+1})\right]
\\
&= \mathbb{E}\left[\bar{V}_{h-1}(S_{t+1})\right] - \mathbb{E}\left[\mathbb{E}[\rho_{t+1} | S_{t+1}] Q_{h-1}(S_{t+1}, A_{t+1})\right]
\\
&= \mathbb{E}\left[\bar{V}_{h-1}(S_{t+1})\right] - \mathbb{E}\left[Q_{h-1}(S_{t+1}, A_{t+1})\right]
\end{aligned}
$$

ここで、

$$
\begin{aligned}
\bar{V}_{h-1}(S_{t+1})
&= \sum_{a} \pi(a | S_{t+1}) Q_{h-1}(S_{t+1}, a)
\\
&= \mathbb{E}\left[Q_{h-1}(S_{t+1}, A_{t+1})\right]
\end{aligned}
$$

であることから、制御変量の期待値はゼロになる。

$$
\mathbb{E}\left[\bar{V}_{h-1}(S_{t+1}) - \rho_{t+1} Q_{h-1}(S_{t+1}, A_{t+1})\right] = 0
$$

したがって、式 (7.14) における制御変量は収益の期待値を変えないことが示された。

$$
\mathbb{E}[G_{t:h}]
= \mathbb{E}\left[R_{t+1} + \gamma G_{t+1:h}\right]
$$

# Exercise 7.7

式 (7.14) を使った
Off-policy n-step Action-value Prediction (with Per-decision Control Variates)
の疑似コードを書け。

## 回答

ポイント:
- 挙動方策 $b$ に従って行動を選択する。
- ターゲット方策 $\pi$ の行動価値関数 $Q$ を学習する。
- 収益の再帰は式 (7.14) に基づく。ただし、最初の行動に対しては重点サンプリングを使用しない。
- $h < T$ の場合は、再帰は $G_{h:h} = Q_{h-1}(S_h, A_h)$ で終了する。
- $h = T$ の場合は、再帰は $G_{T-1:h} = R_T$ で終了する。

```Algorithm: Off-policy n-step Action-value Prediction (with Per-decision Control Variates)
Initialize Q(s,a) arbitrarily for all s,a
Given target policy π(a|s)
Given behavior policy b(a|s)
Set n  (the n-step horizon)
Set discount γ ∈ [0,1]

Loop forever (for each episode):
    Initialize S0
    Choose A0 ~ b(·|S0)
    t ← 0
    T ← ∞

    Create empty buffers S, A, R
    Store S0, A0

    repeat:
        if t < T:
            Take action At, observe Rt+1 and St+1
            Store Rt+1, St+1

            if St+1 is terminal:
                T ← t + 1
            else:
                Choose At+1 ~ b(·|St+1)
                Store At+1

        τ ← t − n + 1        # time whose update becomes available

        if τ ≥ 0:
            # compute horizon
            h ← min(τ + n, T)

            # --- base case of recursion ---
            if h < T:
                G ← Q(S_h, A_h)    # Gh:h = Q at horizon
            else:
                G ← R_T            # end of episode return

            # --- backward recursion (per-decision control variates) ---
            for k = h−1 down to τ+1:
                ρ ← π(A_k | S_k) / b(A_k | S_k)
                G ← R_{k} + γ * ( ρ * (G − Q(S_k, A_k)) + V̄(S_k) )

            # Special treatment for k = τ:
            #   first action is NOT importance sampled
            if τ + 1 < T:
                G ← R_{τ+1} + γ * (G − Q(S_{τ+1}, A_{τ+1})) + V̄(S_{τ+1})
            else:
                G ← R_{τ+1}

            # --- TD update ---
            Q(S_τ, A_τ) ← Q(S_τ, A_τ) + α * (G − Q(S_τ, A_τ))


        t ← t + 1

    until τ == T − 1
```


# Exercise 7.8

一般的な (off-policy) n-step 収益　(7.13) が、近侍状態価値関数が変更されない場合に、
状態ベースの TD誤差 (6.5) の 和により厳密かつ簡潔に書けることを示せ。

## 回答

式 (7.13)

$$
G_{t:h} = \rho_t \left(R_{t+1} + \gamma G_{t+1:h}
\right) + (1 - \rho_t) V_{h-1}(S_t), \quad t \lt h \lt T
$$

より、以下を示せばよい。

$$
G_{t:t+n} - V(S_t) = \sum_{k=t}^{t+n-1} \gamma^{k-t} \rho_{t:k} \delta_k
$$

ただし、 $\rho_{t:k} = \prod_{i=t}^{k} \rho_i$ 、 $\delta_k$ は (6.5) の状態ベースの TD 誤差
$\delta_k = R_{k+1} + \gamma V(S_{k+1}) - V(S_k)$
である。

(7.13) の両編から $V(S_t)$ を引くと、

$$
\begin{aligned}
G_{t:h} - V(S_t)
&= \rho_t \left(R_{t+1} + \gamma G_{t+1:h}
\right) + (1 - \rho_t) V(S_t) - V(S_t)
\\
&= \rho_t \left(R_{t+1} + \gamma G_{t+1:h} - V(S_t)
\right)
\end{aligned}
$$

TD 誤差を用いて次のように変形する。

$$
\begin{aligned}
G_{t:h} - V(S_t)
&= \rho_t \left(
  R_{t+1} + \gamma V(S_{t+1}) - V(S_t) + \gamma G_{t+1:h} - \gamma V(S_{t+1})
\right)
\\
&= \rho_t \left(
  \delta_t + \gamma (G_{t+1:h} - V(S_{t+1}))
\right)
\\
&= \rho_t \delta_t + \gamma \rho_t (G_{t+1:h} - V(S_{t+1}))
\\
&= \rho_t \delta_t + \gamma \rho_t \rho_{t+1} \left(
  R_{t+2} + \gamma G_{t+2:h} - V(S_{t+1})
\right)
\\
&= \rho_t \delta_t + \gamma \rho_{t:t+1} \delta_{t+1} + \gamma^2 \rho_{t:t+1} (G_{t+2:h} - V(S_{t+2}))
\\
&\ \ \vdots
\\
&= \sum_{k=t}^{h-1} \gamma^{k-t} \rho_{t:k} \delta_k + \gamma^{h-t} \rho_{t:h-1} (G_{h:h} - V(S_h))
\end{aligned}
$$

h に達したとき ( $h = t+n$ ) に、 $G_{h:h} = V(S_h)$ であることから、

$$
G_{t:t+n} - V(S_t) = \sum_{k=t}^{t+n-1} \gamma^{k-t} \rho_{t:k} \delta_k
$$

したがって、一般的な (off-policy) n-step 収益は、状態ベースの TD誤差の和として書けることが示された。


# Exercise 7.9

Exercise 7.8 について、以下の場合についても同様に示せ。

1. 行動ベースの off-policy n-step 収益 (7.14):

$$
G_{t:h} = R_{t+1} + \gamma \big(
  \rho_{t+1} G_{t+1:h} + \bar{V}_{h-1}(S_{t+1}) - \rho_{t+1} Q_{h-1}(S_{t+1}, A_{t+1})
\big)
$$

2. 期待 Sarsa TD 誤差 (式 (6.9) の括弧内の量):

$$
\begin{aligned}
Q(S_t, A_t)
&\leftarrow Q(S_t, A_t) + \alpha \left[ R_{t+1} + \gamma \mathbf{E}_{\pi}[Q(S_{t+1}, At+1) \mid S_{t+1}] - Q(S_t, A_t) \right]
\\
&\leftarrow Q(S_t, A_t) + \alpha \left[ R_{t+1} + \gamma \sum_{a} \pi(a | S_{t+1}) Q(S_{t+1}, a) - Q(S_t, A_t) \right]
\end{aligned}
$$

## 回答
以下を示せばよい。

$$
G_{t:h} - Q(S_t, A_t) = \sum_{k=t}^{h-1} \gamma^{k-t} \rho_{t+1:k} \delta_k
$$

ただし、 $\rho_{t+1:k} = \prod_{i=t+1}^{k} \rho_i$ 、 $\delta_k$ は期待 Sarsa TD 誤差


(7.14) の両辺から $Q(S_t, A_t)$ を引くと、

$$
\begin{aligned}
G_{t:h} - Q(S_t, A_t)
&= R_{t+1} + \gamma \big(
  \rho_{t+1} G_{t+1:h} + \bar{V}_{h-1}(S_{t+1}) - \rho_{t+1} Q_{h-1}(S_{t+1}, A_{t+1})
  \big) - Q(S_t, A_t)
\\
&= R_{t+1} + \gamma \bar{V}_{h-1}(S_{t+1}) - Q(S_t, A_t) + \gamma \rho_{t+1} G_{t+1:h} - \gamma \rho_{t+1} Q_{h-1}(S_{t+1}, A_{t+1})
\\
&= R_{t+1} + \gamma \sum_{a} \pi(a | S_{t+1}) Q(S_{t+1}, a) - Q(S_t, A_t) + \gamma \rho_{t+1} G_{t+1:h} - \gamma \rho_{t+1} Q(S_{t+1}, A_{t+1})
\\
&= \delta_t + \gamma \rho_{t+1} (G_{t+1:h} - Q(S_{t+1}, A_{t+1}))
\\
&= \delta_t + \gamma \rho_{t+1} \rho_{t+2} (G_{t+2:h} - Q(S_{t+2}, A_{t+2}))
\\
&\ \ \vdots
\\
&= \sum_{k=t}^{h-1} \gamma^{k-t} \rho_{t+1:k} \delta_k + \gamma^{h-t} \rho_{t+1:h-1} (G_{h:h} - Q(S_h, A_h))
\end{aligned}
$$

h に達したとき ( $h = t+n$ ) に、 $G_{h:h} = Q(S_h, A_h)$ であることから、

$$
G_{t:h} - Q(S_t, A_t) = \sum_{k=t}^{h-1} \gamma^{k-t} \rho_{t+1:k} \delta_k
$$



# Exercise 7.10

小規模な off-policy 予測問題を考案せよ。またその問題を通して、式 (7.13) や (7.2) を用いた off-policy 学習アルゴリズムが、より単純な式 (7.1) や (7.9) を用いたものよりも、データ効率が良いことを示せ。

## 回答

式 (7.13), (7.2) :

$$
G_{t:h} = \rho_t \left(R_{t+1} + \gamma G_{t+1:h}
\right) + (1 - \rho_t) V_{h-1}(S_t), \quad t \lt h \lt T
\\
\
\\
V_{t+n}(S_t) = V_{t+n-1}(S_t) + \alpha \left[
  G_{t:t+n} - V_{t+n-1}(S_t)
\right], \quad 0 \leq t < T
$$

式 (7.1), (7.9) :

$$
G_{t:t+n} = R_{t+1} + \gamma R_{t+2} + \cdots + \gamma^{n-1} R_{t+n} + \gamma^{n} V_{t+n-1}(S_{t+n})
\\
\
\\
V_{t+n}(S_t) = V_{t+n-1}(S_t) + \alpha \rho_{t:t+n-1} \left[
  G_{t:t+n} - V_{t+n-1}(S_t)
\right], \quad 0 \leq t < T
$$

See exercise_7-9_off_policy_prediction.py

#### ● 予測問題
小規模な off-policy 予測問題の設計
■ MDP（最小で理解しやすい構造）

状態：

$$
S = \{ A, B, C \}, \quad C \text{ は終端}
$$

行動：

$$
a_1, a_2
$$

遷移：
|State | Action | Next | Reward |
|-------|--------|------|--------|
| A | a1 | B | +1 |
| A | a2 | C | 0 |
| B | a1 | C | +1 |
| B | a2 | C | 0 |


割引率：

$$
\gamma = 1
$$


ターゲット方策 $\pi$ ：

$$
\pi(a_1 | A) = 1
\\
\pi(a_1 | B) = 1
$$

挙動方策 $b$ ：

$$
b(a_1 | S) = 0.1
\\
b(a_2 | S) = 0.9
\\
s \in {A,B}
$$

とすると、以下のの特徴を持つ。
- $\pi$ は「常に a1 を選ぶ」
- $b$ は「ほぼ a2 を選ぶ（90%）」
- importance sampling の分散が大きい ( $\rho_t$ が大きくなる可能性)


真の価値 $V^{\pi}$ は

$$
V^{\pi}(A) = 2, \quad V^{\pi}(B) = 1
$$

この値を off-policy で推定する。

#### ● 両者の違い
式 (7.13), (7.2) を用いた off-policy 学習アルゴリズムは、各ステップでの重要度サンプリング比率 $\rho_t$ を使用して収益を調整する。
一方、式 (7.1), (7.9) を用いたアルゴリズムは、全体の重要度サンプリング比率 $\rho_{t:t+n-1}$ を更新に使用する。

今回の問題において、後者は $\rho_{t:t+n-1} = \prod_{k=t}^{t+n-1} \frac{\pi(a_k|s_k)}{b(a_k|s_k)}$ が大きくなり、分散が増加する = データ効率が悪くなると考えられる。

#### ● プログラム
See exercise_7-9.py


# Exercise 7.11

行動価値の推定値を変更しない場合、ツリー・バックアップ収益 (7.16) :

$$
G_{t:t+n} = R_{t+1} + \gamma \sum_{a \neq A_{t+1}} \pi(a \mid S_{t+1}) Q_{t+n-1}(S_{t+1}, a) + \gamma \pi(A_{t+1} | S_{t+1}) G_{t+1:t+n}
$$

は、以下のように期待値ベースの TD 誤差の和として厳密に書けることを示せ。

$$
G_{t:t+n} =  Q(S_t, A_t) + \sum_{k=t}^{\min(t+n-1, T-1)} \delta_k \prod_{i = t+1}^{k} \gamma \pi(A_t \mid S_i)
$$

ここで、 $\delta_t = R_{t+1} + \gamma \bar{V}(S_{t+1}) - Q(S_t, A_t)$ であり、 $\bar{V}(S_{t+1}) = \sum_{a} \pi(a | S_{t+1}) Q(S_{t+1}, a)$ である。

## 回答
(7.16) の右辺に $Q(S_t, A_t)$ を足して引くと、

$$
\begin{aligned}
G_{t:t+n}
&= R_{t+1} + \gamma \sum_{a \neq A_{t+1}} \pi(a \mid S_{t+1}) Q_{t+n-1}(S_{t+1}, a) + \gamma \pi(A_{t+1} | S_{t+1}) G_{t+1:t+n} + Q(S_t, A_t) - Q(S_t, A_t)
\end{aligned}
$$

TD 誤差を用いて次のように変形する。

$$
\begin{aligned}
G_{t:t+n}
&= R_{t+1} + \gamma \sum_{a} \pi(a | S_{t+1}) Q(S_{t+1}, a) - Q(S_t, A_t)  + \gamma \sum_{a \neq A_{t+1}} \pi(a \mid S_{t+1}) Q(S_{t+1}, a) + \gamma \pi(A_{t+1} | S_{t+1}) G_{t+1:t+n} - \gamma \sum_{a} \pi(a | S_{t+1}) Q(S_{t+1}, a) + Q(S_t, A_t)
\\
&= \delta_t + \gamma \sum_{a \neq A_{t+1}} \pi(a \mid S_{t+1}) Q(S_{t+1}, a) + \gamma \pi(A_{t+1} | S_{t+1}) G_{t+1:t+n} - \gamma \sum_{a} \pi(a | S_{t+1}) Q(S_{t+1}, a)+ Q(S_t, A_t)
\\
&= \delta_t + \gamma \sum_{a } \pi(a \mid S_{t+1}) Q(S_{t+1}, a) - \gamma \pi(A_{t+1} \mid S_{t+1}) Q(S_{t+1}, A_{t+1}) + \gamma \pi(A_{t+1} | S_{t+1}) G_{t+1:t+n} - \gamma \sum_{a} \pi(a | S_{t+1}) Q(S_{t+1}, a)+ Q(S_t, A_t)
\\
&= \delta_t - \gamma \pi(A_{t+1} \mid S_{t+1}) Q(S_{t+1}, A_{t+1}) + \gamma \pi(A_{t+1} | S_{t+1}) G_{t+1:t+n}+ Q(S_t, A_t)
\\
&= \delta_t + \gamma \pi(A_{t+1} | S_{t+1}) (G_{t+1:t+n} - Q(S_{t+1}, A_{t+1}))+ Q(S_t, A_t)
\\
&= \delta_t + \gamma \pi(A_{t+1} | S_{t+1}) \delta_{t+1} + \gamma^2 \pi(A_{t+1} | S_{t+1}) \pi(A_{t+2} | S_{t+2}) (G_{t+2:t+n} - Q(S_{t+2}, A_{t+2}))+ Q(S_t, A_t)
\\
\vdots
\\
&= \sum_{k=t}^{t+n-1} \delta_k \prod_{i = t+1}^{k} \gamma \pi(A_i \mid S_i) + \gamma^{n} \prod_{i = t+1}^{t+n} \pi(A_i \mid S_i) (G_{t+n:t+n} - Q(S_{t+n}, A_{t+n}))+ Q(S_t, A_t)
\end{aligned}
$$

h に達したとき ($h = t+n$) に、 $G_{h:h} = Q(S_h, A_h)$ であることから、

$$
G_{t:t+n} = Q(S_t, A_t) + \sum_{k=t}^{t+n-1} \delta_k \prod_{i = t+1}^{k} \gamma \pi(A_i \mid S_i)
$$
