#새로운 파티션 추가
alter table cjk_mart_usr_hdfs add partition (etl_ym='201512') location '/user/b10144880/hdfs_user/201512'