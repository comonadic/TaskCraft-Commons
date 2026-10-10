径向树root=0，每变压器受从root到其node路径上所有线路故障影响。单段故障频次为lambda/年，有transfer_hours>0则该故障时长取转供小时，否则取repair_hours。负荷点lambda为路径频次和，故障outage_hours为sum(lambda*时长)。
原等权口径不含计划停电：SAIFI为点lambda均值，SAIDI为点outage_hours均值，CAIDI=SAIDI/SAIFI，ASAI=1-SAIDI/8760。ENS=sum(kw*0.6*outage_hours)，单位kWh。
合成企业口径：SAIFI按customers加权（计划停电不计次数）；SAIDI按customers加权且加上路径planned_hours之和；CAIDI及ASAI用此SAIDI；ENS同样加计划小时。total_customers为用户总数。原与企业口径并存，禁止混合分母。
