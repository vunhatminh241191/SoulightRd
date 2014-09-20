from soulightrd.apps.app_helper import setup_constant_countries_alpha2, setup_constant_countries_alpha3

VALID_FILE_SIZE = 5242880

PUBLIC = "1"
PRIVATE = "0"

UNLIMITED = -1

NEW = "1"
OLD = "0"

HIDE = "0"
SHOW = "1"

YES_VALUE = "1"
NO_VALUE = "0"

SECONDS_PER_DAY = 86400
SECONDS_PER_HOUR = 3600
SECONDS_PER_MINUTE = 60

MONTH_SHORT_MAP = {
    1: "Jan",
    2: "Feb", 
    3: "Mar", 
    4: "Apr", 
    5: "May", 
    6: "Jun", 
    7: "Jul", 
    8: "Aug", 
    9: "Sep", 
    10: "Oct", 
    11: "Nov", 
    12: "Dec"
}

MONTH_FULL_MAP = {
    1: "January", 
    2: "February", 
    3: "March", 
    4: "April", 
    5: "May", 
    6: "June", 
    7: "July", 
    8: "August", 
    9: "September", 
    10: "October", 
    11: "November", 
    12: "December"
}

DAY_IN_MONTH_MAP = {
    1:31, 
    2:28, 
    3:31, 
    4:30, 
    5:31, 
    6:30, 
    7:31, 
    8:31, 
    9:30, 
    10:31, 
    11:30, 
    12:31
}

WEEK_DAY_TEXT_MAP = {
    "Mon": "Monday", 
    "Tue": "Tuesday", 
    "Wed": "Wednesday", 
    "Thu": "Thursday", 
    "Fri": "Friday", 
    "Sat": "Saturday", 
    "Sun": "Sunday"
}

WEEK_DAY_NUM_MAP = {
    0: "Monday", 
    1: "Tuesday", 
    2: "Wednesday", 
    3: "Thursday", 
    4: "Friday", 
    5: "Saturday", 
    6: "Sunday"
}

WEEK_DAY = (
  ('0',"Monday"), 
  ('1',"Tuesday"), 
  ('2',"Wednesday"), 
  ('3',"Thursday"), 
  ('4',"Friday"), 
  ('5',"Saturday"), 
  ('6',"Sunday")
)

DAY_SUFFIX = {
    1: "st", 
    2: "nd", 
    3: "rd"
}

USA_STATES = (
   ("AL","Alabama"),("AK","Alaska"),("AZ","Arizona"),("AR","Arkansas"),("CA","California"),
   ("CO","Colorado"),("CT","Connecticut"),("DE","Delaware"),("FL","Florida"),("GA","Georgia"),
   ("HI","Hawaii"),("ID","Idaho"),("IL","Illinois"),("IN","Indiana"),("IA","Iowa"),
   ("KS","Kansas"),("KY","Kentucky"),("LA","Louisana"),("ME","Maine"),("MD","Maryland"),
   ("MA","Massachusetts"),("MI","Michigan"),("MN","Minnesota"),("MS","Mississippi"),("MO","Missouri"),
   ("MT","Montana"),("NE","Nebraska"),("NV","Nevada"),("NH","New Hampshire"),("NJ","New Jersey"),
   ("NM","New Mexico"),("NY","New York"),("NC","North Carolina"),("ND","North Dakota"),("OH","Ohio"),
   ("OK","Oklahoma"),("OR","Oregon"),("PA","Pennsylvania"),("RI","Rhode Island"),("SC","South Carolina"),
   ("SD","South Dakota"),("TN","Tennessee"),("TX","Texas"),("UT","Utah"),("VT","Vermont"),
   ("VA","Virginia"),("WA","Washington"),("WV","West Virginia"),("WI","Wisconsin"),("WY","Wyoming"),
)

COUNTRIES_ALPHA2 = setup_constant_countries_alpha2()
COUNTRIES_ALPHA3 = setup_constant_countries_alpha3()

DEFAULT_COUNTRIES_FORMAT = COUNTRIES_ALPHA2

YES_NO = (
  ("1","Yes"),
  ("0","No"),
)

NOTIFICATION_STATUS = (
  (OLD, "old"),
  (NEW, "new"),
) 

MESSAGE_STATUS = NOTIFICATION_STATUS

APPEARANCE_STATUS = (
  (HIDE, "hide"),
  (SHOW, "show"),
) 

NOTIFICATION_TYPE = (
  
) 

PRIVACY_STATUS = (
    (PUBLIC,'Public'),
    (PRIVATE,"Private")
)

PRIVACY_STATUS_MAP = {
  "1": "Public",
  "0": "Private"
}

GENDER = (
    ("m", "Male"),
    ("f", "Female"),
)

GENDER_MAP_BY_NAME = {
  "male":"1",
  "female":"0"
}

GENDER_MAP_BY_CODE = {
  "1":"male",
  "0":"female"
}

COMMENT_TYPE = (
)

REPORT_TYPE = (
    ('comment','comment'),
    ("user","user")
)

PHOTO_TYPE = (
    ('user_profile','user_profile'),
    ("default_image","default_image")
)

PROJECT_TYPE = (
    
)

PHOTO_TYPE = (

)



