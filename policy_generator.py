import datetime
async def generate_system_time():
    from datetime import datetime
    import pytz

    UTC = pytz.utc
    IST = pytz.timezone('Asia/Kolkata')

    datetime_ist = datetime.now(IST)
    Time = datetime_ist.strftime('%H:%M:%S')
    return Time

async def generate_permission_policy(Date,Time,UserId,UserType, CreatePermission,EditPermission,DeletePermission):
    policy = {
      "Version": "V5",
      "Date": Date,
      "Time": Time,
      "Statement": [{
      "UserId": UserId,
      "UserType": UserType,
        "Permission": [{
            "CREATE": CreatePermission,
            "EDIT": EditPermission,
            "DELETE": DeletePermission}],}]}
    return policy


# from datetime import datetime
# from datetime import timedelta
# import pytz

# UTC = pytz.utc
# IST = pytz.timezone('Asia/Kolkata')

# datetime_ist = datetime.now(IST)
# current_date = datetime_ist.strftime('%Y:%m:%d')
# print("current_date ",current_date)
# time_datetime_ist = datetime_ist + timedelta(days=365 * 5)
# Delay_date = time_datetime_ist.strftime('%Y:%m:%d')
# print("Delay_date ",Delay_date)