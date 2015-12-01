#CREATE EXTERNAL TABLE WITH PARTITION

CREATE EXTERNAL TABLE IF NOT EXISTS bdc_5.cjk_mart_usr_hdfs (
	user_name		STRING,
	type			STRING,
	table_name		STRING,
	SIZE			INT)
PARTITIONED BY (etl_ym	STRING)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
#사용자 폴더(/user/b10144880)에 새로운 폴더를 생성(hdfs_user)하여 지정
LOCATION '/user/b10144880/hdfs_user'