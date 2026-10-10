# 合成数据限定操作协议
所有hour均为同次ICU入院后的小时，+08:00时间，无跨表时区变动。患者通过patient_id/icu_id关联。
sepsis_hour：suspected_infection=1且同一小时SOFA比baseline增加>=2的最早小时。
AKI：基线肌酐已给出，只有基线非缺失才判肌酐；1mg/dL=88.4umol/L。在本合成病例中，基线对整个住院有效，肌酐>=1.5*基线或增加>=0.3mg/dL即阳性。尿量按连续6个完整小时平均<0.5ml/kg/h判定，首次窗口末小时为起始。任一条件满足取最早小时。仅使用0<=hour<=discharge_hour的数据。
该简化协议保留本实例判定所需分支，未实现KDIGO所有临床条款（如透析、完整基线估计与时间滚动）。不应部署临床。
只有sepsis发生后0至168小时内、同次住院中首次AKI才纳入，提前AKI不纳入。无sepsis优先reason=no_sepsis；无AKI为no_aki；否则aki_before_sepsis/outside_7d/eligible。不因同人另一次住院阳性改变本次审计。
