from smartdashboard import db



class Job_Monitoring(db.Model):
    __tablename__ = "job_monitoring"
    starttime = db.Column(db.String(100) ) #palitan ng datetime
    duration_mins = db.Column(db.String(100))
    tasklabel = db.Column(db.String(50))  
    id = db.Column(db.String(200), primary_key=True)
    status = db.Column(db.String(10))

    def __repr__(self):
        self.starttime = starttime
        self.duration_mins = duration_mins
        self.tasklabel = tasklabel
        self.id = id
        self.status = status

class Job_BCA(db.Model):
    __tablename__ = "job_bca_monitoring"
    RunDate = db.Column(db.String(10), primary_key=True )
    Dly_Prp_Acct = db.Column(db.String(10))
    Dly_PCODES = db.Column(db.String(10))  
    UsageType_Total = db.Column(db.String(10))
    UsageType_DataDeducts = db.Column(db.String(10))
    UsageType_SMSDeducts = db.Column(db.String(10))
    UsageType_VoiceDeducts = db.Column(db.String(10))
    UsageType_VasDeducts = db.Column(db.String(10))
    UsageType_Topup = db.Column(db.String(10))
    UsageType_Expiration = db.Column(db.String(10))


    def __repr__(self):
        self.RunDate =  RunDate
        self.Dly_Prp_Acct =  Dly_Prp_Acct
        self.Dly_PCODES =  Dly_PCODES
        self.UsageType_Total = UsageType_Total
        self.UsageType_DataDeducts =  UsageType_DataDeducts
        self.UsageType_SMSDeducts =  UsageType_SMSDeducts
        self.UsageType_VoiceDeducts =  UsageType_VoiceDeducts
        self.UsageType_VasDeducts =  UsageType_VasDeducts
        self.UsageType_Topup =  UsageType_Topup
        self.UsageType_Expiration =  UsageType_Expiration

class Dly_Usagetype(db.Model):
    __tablename__ = "dly_usagetype_stats"
    txn_dt = db.Column(db.String(10),)
    usage_type_class = db.Column(db.String(50), primary_key=True)
    total_count = db.Column(db.String(10))  
    TOTAL_DEDUCT = db.Column(db.String(10))
    USAGE_TYPE_DESC = db.Column(db.String(10))
    DEDUCTED_WALLET_DESC = db.Column(db.String(10))
    UOM_OF_WALLET = db.Column(db.String(10))
    INTERNATIONAL_TAG = db.Column(db.String(10))
    ROAMING_TAG = db.Column(db.String(10))

    def __repr__(self):
        self.RunDate =  RunDate
        self.usage_type_class =  usage_type_class
        self.total_count =  total_count
        self.TOTAL_DEDUCT = TOTAL_DEDUCT
        self.USAGE_TYPE_DESC =  USAGE_TYPE_DESC
        self.DEDUCTED_WALLET_DESC =  DEDUCTED_WALLET_DESC
        self.UOM_OF_WALLET =  UOM_OF_WALLET
        self.INTERNATIONAL_TAG =  INTERNATIONAL_TAG
        self.ROAMING_TAG =  ROAMING_TAG

class Dly_Prp_Acct(db.Model):
    __tablename__ = "dly_prp_acct_stats"
    cre_dt = db.Column(db.String(10),)
    brand = db.Column(db.String(50), primary_key=True)
    total_bal = db.Column(db.String(10))  
    total_count = db.Column(db.String(10))

    def __repr__(self):
        self.cre_dt =  cre_dt
        self.brand =  brand
        self.total_bal =  total_bal
        self.total_count = total_count

class Dly_Pcodes(db.Model):
    __tablename__ = "dly_pcodes_prp_stats"
    txn_dt = db.Column(db.String(10),)
    brand = db.Column(db.String(50), primary_key=True)
    total_topup = db.Column(db.String(20))  
    count_topup = db.Column(db.String(20))  
    total_count = db.Column(db.String(20))

    def __repr__(self):
        self.txn_dt =  txn_dt
        self.brand =  brand
        self.total_topup =  total_topup
        self.count_topup =  count_topup
        self.total_count = total_count

class topsku_prod(db.Model):
    __tablename__ = "top_sku_prod"
    txn_date = db.Column(db.String(10),)
    processing_dttm = db.Column(db.String(10))
    brand = db.Column(db.String(20), primary_key=True)  
    txn_amount = db.Column(db.String(20))  
    topup_cnt = db.Column(db.String(20))

    def __repr__(self):
        self.txn_date =  txn_date
        self.processing_dttm =  processing_dttm
        self.brand =  brand
        self.txn_amount =  txn_amount
        self.topup_cnt = topup_cnt

class topsku_talend(db.Model):
    __tablename__ = "top_sku_talendfc"
    txn_date = db.Column(db.String(10),)
    processing_dttm = db.Column(db.String(50))
    brand = db.Column(db.String(20))  
    txn_amount = db.Column(db.String(20))  
    topup_cnt = db.Column(db.String(20), primary_key=True)

    def __repr__(self):
        self.txn_date =  txn_date
        self.processing_dttm =  processing_dttm
        self.brand =  brand
        self.txn_amount =  txn_amount
        self.topup_cnt = topup_cnt