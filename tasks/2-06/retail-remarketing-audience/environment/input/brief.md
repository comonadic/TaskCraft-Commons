# 合成企业政策 v1
固定 as_of=2025-03-31。合格受众要求 transaction_count_90d>=8 且 spend_90d>=3000 且 email_opens_30d恰为0，缺失邮件互动不当作0。active_support为true剔除。渠道都不合格者仍保留在人群中。
sms_eligible:明确sms_opt_in=true、sms_opt_out=false且phone_present=true；push同理。
名单列严格为 customer_id,transaction_count_90d,spend_90d,email_opens_30d,sms_eligible,push_eligible,any_channel_eligible。布尔写true/false。
segment_definition.json字段：as_of、audience_count、sms_count、push_count、any_channel_count。
overlap_report.tsv列：segment_id,overlap_count,overlap_pct；overlap_pct=交集人数/全部合格受众人数*100，保留6位小数，包含所有S0..S5。
