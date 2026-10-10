# 合成云成本规则
只对以下情况建议操作：CVM utilization_pct<5且inactive_days>=30，schedule_stop，费用乘0.3；CDB utilization_pct<10，downsize，乘0.5；COS inactive_days>=30，archive，乘0.25；NAT utilization_pct=0且inactive_days>=30，delete_idle，变0；EIP attached=false，release，变0；LOG retention_days>30，shorten_retention，乘30/原保留天数。
current_cost=计费量乘单价。金额人民币元，先对current、projected各四舍五入2位，再相减。汇总只统计建议操作资源。图片中的字段名与CSV相同，所有字段齐全。不得把正常资源加入建议。
