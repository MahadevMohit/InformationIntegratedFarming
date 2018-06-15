from pymongo import MongoClient

client = MongoClient('mongodb://main:rcb#123@ds257627.mlab.com:57627/pbl_farming')
db=client.pbl_farming

survey_details=db.survey_details
# geoLocation={
#     "coordinates":[
# 	[13.097464,77.566962],
# [13.097851,77.569859],
# [13.093773,77.569412],
# [13.092211,77.569977],
# [13.093993,77.571555],
# [13.093251,77.573932],
# [13.086603,77.57302],
# [13.087084,77.570358],
# [13.085462,77.570047],
# [13.085881,77.568469],
# [13.091691,77.56406],
# [13.091827,77.563824],
# [13.096336,77.566782],
# [13.09752,77.566986],
# ],
#     "surveyno": "GK015"
# }
# obj_id=survey_details.insert_one(geoLocation).inserted_id;
# print(obj_id)
survey_details=db.survey_details

geo_data = survey_details.find_one({"surveyno": "GK002"})
print(geo_data["coordinates"])