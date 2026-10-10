成人age>=18，ulcer/multimorbidity为0/1，bmi和weight完整且weight>0。sex=1表示男性。所有用药记录ascertained=1时，nsaid=是否存在drug_class=NSAID且current_use=1，否则nsaid缺失。hpyl非缺失且nsaid非缺失构成子集。
M1：全部成人，ulcer ~ const+multimorbidity+age+sex+bmi。M2：完整病例子集，同M1。M3：同一子集，M2加hpyl+nsaid。
用GLM Binomial logit，freq_weights=weight，标准非稳健协方差（固定算法练习，不冒充复杂抽样推断）。输出multimorbidity的exp(beta)、exp(beta±1.959963984540054*SE)、双侧正态p值。or_change_pct=(当前OR/M1_OR-1)*100，M1为0。容差1e-5。
