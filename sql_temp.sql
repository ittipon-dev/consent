SELECT a.cust_id, a.cifid, a.status, a.last_login_date from ksdev_semX_mcd.KOL_MST_CUSTOMER a


CREATE TABLE ksdev_semX_mcd.OB_KMA_CUST_SURVEY
(
	cust_id    string,   
	cifid	   string,   
	survey_dt  string
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '|'
STORED AS TEXTFILE;

insert into ksdev_semX_mcd.OB_KMA_CUST_SURVEY
SELECT a.cust_id, a.cifid, CURRENT_TIMESTAMP() || '.00000000' as survey_dt  
from   ksdev_semX_mcd.KOL_MST_CUSTOMER a
WHERE  STATUS = 1

select status, count(*) 
from  ksdev_semX_mcd.KOL_MST_CUSTOMER
group by rollup(status);
