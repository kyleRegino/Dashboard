import datetime
import random

CDR_TYPES = ["com", "vou", "cm", "adj", "first", "mon", "data", "voice", "sms", "clr"];
random.randint(0,10000000)

START_DATE = datetime.datetime(2010, 12, 1)
END_DATE = datetime.datetime(2010, 12, 30)
STEP = datetime.timedelta(days=1)


with open("dummy.csv","w") as f:
    while START_DATE <= END_DATE:
        file_date = START_DATE.strftime('%Y-%m-%d')
        for c in CDR_TYPES:
            for i in range(24):
                ocs_manifest = random.randint(0,10000000)
                t1 = random.randint(0,10000000)
                variance  = ocs_manifest - t1
                write_string = "{},{},{},{},{},{}\n".format(file_date,i,c,ocs_manifest,t1,variance)
                f.write(write_string)
        START_DATE += STEP
