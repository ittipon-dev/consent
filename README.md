# Install Hive with docker-compose

## Push source code
git clone https://github.com/big-data-europe/docker-hive.git

## Start docker-compose
sudo docker-compose up -d

## SSH to container
sudo docker exec -it docker-hive_hive-server_1 /bin/bash

# Hive with docker-compose

## Use hive2

/opt/hive/bin/beeline -u jdbc:hive2://localhost:10000

## Show DB

show databases;

## Create DB

create databases ksdev_semX_mcd;

## Create TB with ksdev_semX_mcd

CREATE TABLE ksdev_semX_mcd.KOL_MST_CUSTOMER
     (
      CUST_ID STRING ,
      CIFID STRING ,
      CUST_NICK_NAME STRING ,
      GENDER STRING ,
      DATE_OF_BIRTH TIMESTAMP,
      EMAIL STRING ,
      ADDRESS  STRING,
      ZIP_CODE STRING ,
      PROVINCE_CODE STRING ,
      COUNTRY_CODE STRING ,
      PHONE_NO STRING ,
      FAX_NO STRING ,
      APPLY_NEWSLETTER BIGINT,
      NEWSLETTER_LANG STRING ,
      PREFER_LANG STRING ,
      ADDRESS_TYPE BIGINT,
      USER_TYPE STRING ,
      BIZ_ADDRESS  STRING,
      BIZ_ZIP_CODE STRING ,
      BIZ_PROVINCE_CODE STRING ,
      BIZ_COUNTRY_CODE STRING ,
      BIZ_ADDRESS_TYPE BIGINT,
      BIZ_PHONE_NO STRING ,
      BIZ_FAX_NO STRING ,
      JOB_POSITION STRING ,
      DEPARTMENT STRING ,
      PROFILE_IMAGE STRING ,
      COMPANY_CODE STRING ,
      RETRY_COUNT_OTP BIGINT,
      REGISTER_CHANNEL STRING ,
      REGISTER_TYPE BIGINT,
      IS_FIRST_SIGNIN STRING ,
      STATUS BIGINT,
      LAST_LOGIN_DATE TIMESTAMP,
      LAST_LOGIN_DATE_KOL TIMESTAMP,
      CANCEL_DATE TIMESTAMP,
      IS_TEMP_CUST STRING ,
      TEMP_CUST_ID STRING ,
      TEMP_PWD_EXP_DATE TIMESTAMP,
      IS_ALERT_LOGIN STRING ,
      OTP_STATUS BIGINT,
      OTP_CHANNEL BIGINT,
      CREATED_DATE TIMESTAMP,
      CREATED_BY STRING ,
      UPDATED_DATE TIMESTAMP,
      UPDATED_BY STRING ,
      ISBLOCK_POPUP_CRM STRING ,
      ISOTP_24H STRING ,
      MOBILE_COUNTRY_ID BIGINT,
      PROMOTE_CUST_ID STRING ,
      CUSTOMER_TYPE BIGINT,
      FIRST_SIGNIN_DATE TIMESTAMP,
      IS_TEMPPASS_EXP STRING ,
      IS_TEMPUSER_EXP STRING ,
      NAME_OF_ORGANIZATION STRING ,
      CUST_MD5 STRING ,
      VERIFICATION_EMAIL STRING 
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '|'
STORED AS TEXTFILE;

## Show detial of table
describe kol_mst_customer;