# General constants
DB_MAXLEN   = 255

# User constants
#https://www.rfc-editor.org/errata/eid1690 -- 320 but mariadb mandates <=255
EMAILMAXLEN     = 255
#https://www.bdm.vic.gov.au/births/naming-your-child/naming-restrictions#toolong
FNAMESMAXLEN    = 38
SNAMEMAXLEN     = 38

# Social Credits Constants
DEFAULT_SOCIAL_CREDITS = 200

# Chore Constants
NO_PRIORITY         = 0
LOW_PRIORITY        = 10
MEDIUM_PRIORITY     = 20
HIGH_PRIORITY       = 30
CHORE_PRIORITIES    = [(NO_PRIORITY,        "No Priority"),
                       (LOW_PRIORITY,       "Low Priority"),
                       (MEDIUM_PRIORITY,    "Medium Priority"),
                       (HIGH_PRIORITY,      "High Priority")]

# Notification Constants
UPCOMING_CHORE  = "You have an upcoming chore: "
EXPIRED_CHORE   = "You have an overdue chore: "
SHAME           = "Your social credit score is getting dangerously low."
NOTIF_BODIES    = [(UPCOMING_CHORE, "Upcoming Chore"),
                   (EXPIRED_CHORE,  "Expired Chore"),
                   (SHAME,          "Shame")]

# Date time Constants
DATETIME_FMT = "%H:%M:%S %d/%m/%Y"
DATE_FMT = "%d/%m/%Y"

# Randomness COnstants
LARGE_ENOUGH = 1000000

# History
HISTORY_PATH = "media/history.csv"
HISTORY_HEADER = ["completionDate", "assignedTo", "completedBy", "choreName", "weight"]
