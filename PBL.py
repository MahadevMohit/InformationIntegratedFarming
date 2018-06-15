from flask import *
from pymongo import MongoClient
import json
import pyproj
import shapely
import shapely.ops as ops
from shapely.geometry.polygon import Polygon
from functools import partial

'''Flask '''
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


'''Mongo DB Connection'''
client = MongoClient('mongodb://main:rcb#123@ds257627.mlab.com:57627/pbl_farming')
db = client.pbl_farming
farmer_details = db.farmer_details
survey_details = db.survey_details


'''Index page route'''
@app.route("/",methods=["GET","POST"])
def index():
    #variables
    survey_no_list = []
    for survey_number in survey_details.find():
        survey_no_list.append(survey_number["surveyno"])
    survey_no_list.sort()


    crop_list=[]
    for farrmer_entry in farmer_details.find():
        crop_list.append(farrmer_entry["ccrop"])
    crop_list=list(set(crop_list))
    crop_list.sort()

    soil_list=[]
    for farmer_entry in farmer_details.find():
        soil_list.append(farmer_entry["soil_type"])
    soil_list=list(set(soil_list))
    soil_list.sort()

    irrigation_list=[]
    for farmer_entry in farmer_details.find():
        irrigation_list.append(farmer_entry["irrigation"])
    irrigation_list=list(set(irrigation_list))
    irrigation_list.sort()

    farmer_list=[]
    for farmer_entry in farmer_details.find():
        farmer_list.append(farmer_entry["name"])
    farmer_list=list(set(farmer_list))
    farmer_list.sort()

    #get method
    if request.method=="GET":
        #get the drop down list
       return render_template("index.html", survey_no_list=survey_no_list,crop_list=crop_list,soil_list=soil_list,irrigation_list=irrigation_list,farmer_list=farmer_list)

    #post method
    if request.method=="POST":

        #check what submit btn is clicked
        if request.form['btnSubmit']=="btnSurvey":
            #Survey submit is clicked
            print("Survey is clicked")
            # get the survey no.and query the db accordingly
            survey_no_selected = request.form.get("survey_dropdown")
            land_details = survey_details.find_one({"surveyno": survey_no_selected})
            print(survey_no_selected + " is selected  and land details \n" + str(land_details))
            land_details.pop('_id')
            print(land_details)
            print(land_details["area"],"area of land")
            #get the sidebar details from farmer_details
            try:
                land_side_details=farmer_details.find_one({"surveyno":survey_no_selected},{"_id":0,"coordinates":0,"area":0})
                land_side_details["area"]=round(land_details["area"],2)
                #land_side_details=str(json.dumps(land_side_details))
                print("Land Side Details : ",land_side_details)
            except TypeError:
                print("Farmer doesnt exist")
            return render_template("landresult.html", land_details=land_details["coordinates"],land_side_details=land_side_details)
        elif request.form['btnSubmit']=="btnCrop":
            #crop submit btn implementation
            print("crop is clicked")
            crop_land_list=[]
            #get the crop name and query the db accordingly
            crop_selected=request.form.get("crop_dropdown")
            crop_land_details=farmer_details.find({"ccrop":crop_selected},{"coordinates":1,"_id":0})
            for crop_land in crop_land_details:
                crop_land_list.append(crop_land["coordinates"])
                print(crop_selected + " is selected  and land details \n" + str(crop_land));
            print("Crop Land List passed to html ",crop_land_list)
            #crop side bar details
            try:
                crop_side_list=[]
                crop_side_details=farmer_details.find({"ccrop":crop_selected},{"_id":0,"coordinates":0})
                for crop_side in crop_side_details:
                    crop_side_list.append(crop_side)
                print("Crop Side Details : ",crop_side_list)
            except TypeError:
                print("Crop doesnt exist")
            return render_template("cropresult.html",crop_details_list=crop_land_list,crop_side_list=crop_side_list)
        elif request.form['btnSubmit']=="btnSoil":
            #soil submit is clicked
            print("Soil is clicked")
            soil_details_list=[]
            # get the soil type and query the db accordingly
            soil_selected = request.form.get("soil_dropdown")
            soil_details = farmer_details.find({"soil_type": soil_selected}, {"coordinates": 1, "_id": 0})
            for soil_land in soil_details:
                soil_details_list.append(soil_land["coordinates"])
                print(soil_selected + " is selected  and land details \n" + str(soil_land))
            print("Crop Land List passed to html ", soil_details_list)
            #soil side bar details
            try:
                soil_side_list=[]
                soil_side_details=farmer_details.find({"soil_type":soil_selected},{"_id":0,"coordinates":0})
                for soil_side in soil_side_details:
                    soil_side_list.append(soil_side)
                print("Crop Side Details : ",soil_side_list)
            except TypeError:
                print("Soil doesnt exist")
            return render_template("soilresult.html", soil_details_list=soil_details_list,soil_side_list=soil_side_list)
        elif request.form['btnSubmit']=="btnIrrigation":
            #irrigation submit is clicked
            print("Irrigation is clicked")
            irrigation_details_list = []
            # get the soil type and query the db accordingly
            irrigation_selected = request.form.get("irrigation_dropdown")
            irrigation_details = farmer_details.find({"irrigation": irrigation_selected}, {"coordinates": 1, "_id": 0})
            for irrigation_land in irrigation_details:
                irrigation_details_list.append(irrigation_land["coordinates"])
                print(irrigation_selected + " is selected  and land details \n" + str(irrigation_land));
            print("Iriigation Land List passed to html ", irrigation_details_list)
            #irrigation side details
            try:
                irrigation_side_list=[]
                irrigation_side_details=farmer_details.find({"irrigation":irrigation_selected},{"_id":0,"coordinates":0})
                for irrigation_side in irrigation_side_details:
                    irrigation_side_list.append(irrigation_side)
                print("Irrigation Side Details : ",irrigation_side_list)
            except TypeError:
                print("Irrigation doesnt exist")
            return render_template("irrigationresult.html", irrigation_details_list=irrigation_details_list,irrigation_side_list=irrigation_side_list)
        elif request.form["btnSubmit"]=="btnFarmer":
            #farmer submit is clicked
            print("Farmer is clicked")
            farmer_details_list = []
            # get the soil type and query the db accordingly
            farmer_selected = request.form.get("farmer_dropdown")
            farmer_land_details = farmer_details.find({"name": farmer_selected}, {"coordinates": 1, "_id": 0})
            for farmer_land in farmer_land_details:
                farmer_details_list.append(farmer_land["coordinates"])
                print(farmer_selected + " is selected  and land details \n" + str(farmer_land))
            print("Iriigation Land List passed to html ", farmer_details_list)
            #farmer side details
            try:
                farmer_side_list=[]
                farmer_side_details=farmer_details.find({"name":farmer_selected},{"_id":0,"coordinates":0})
                for farmer_side in farmer_side_details:
                    farmer_side_list.append(farmer_side)
                print("Farmer Side Details : ",farmer_side_list)
            except TypeError:
                print("Farmer doesnt exist")
            return render_template("farmerresult.html", farmer_details_list=farmer_details_list,farmer_side_list=farmer_side_list)
        elif request.form["btnSubmit"] == "btnMulti":
            # multi option query
            print("multi option query is selected")
            # main query dict and query result list
            query_dict={}
            multi_side_list = []
            multi_detail_list=[]
            # get all the parameters choosen
            if request.form.get("survey_dropdown") != " ":
                sel_land=request.form.get("survey_dropdown")
                query_dict["surveyno"]=sel_land
            if request.form.get("crop_dropdown") != " ":
                sel_crop=request.form.get("crop_dropdown")
                query_dict["ccrop"]=sel_crop
            if request.form.get("soil_dropdown") != " ":
                sel_soil=request.form.get("soil_dropdown")
                query_dict["soil_type"]=sel_soil
            if request.form.get("irrigation_dropdown") != " ":
                sel_irrigation=request.form.get("irrigation_dropdown")
                query_dict["irrigation"]=sel_irrigation
            if request.form.get("farmer_dropdown") != " ":
                sel_farmer=request.form.get("farmer_dropdown")
                query_dict["name"] = sel_farmer
            # check the details
            print("Details collected : dict : ",query_dict)
            # query the db accordingly
            multi_side_details = farmer_details.find(query_dict, {"_id": 0})
            for multi_side in multi_side_details:
                multi_side_list.append(multi_side)
                multi_detail_list.append(multi_side["coordinates"])
            print("Farmer Side Details : ", multi_side_list)
            if not multi_detail_list :
                return  render_template("noresult.html")
            else:
                return render_template("multiresult.html", multi_details_list=multi_detail_list,multi_side_list=multi_side_list)



    return render_template("index.html",crop_details_list='" "',land_details='" "',survey_no_list=survey_no_list,crop_list=crop_list)


'''Farmer Registeration : pushing data to mlab mongo database'''
@app.route('/farmerRegistration', methods=["GET","POST"])
def farmer_registration():
    if request.method=="GET":
        return render_template("farmer_reg.html")
    if request.method=="POST":
        survey_no=request.form["survey_no"].upper()
        farmer_name=request.form["name"].upper()
        farmer_age=request.form["age"].upper()
        farmer_phno=request.form["phone"].upper()
        #agri_area=request.form["area"].upper()
        agri_soil=request.form["soil_type"].upper()
        agri_irrigation=request.form["irrigation_type"].upper()
        agri_ccrop=request.form["current_crop"].upper()
        agri_prev_crop=request.form["prev_crop"].upper()
        agri_cattles=request.form["cattle"].upper()

        #spliting the agri_prev_crop with , as del
        agri_pcrop=agri_prev_crop.split(",")
        print(agri_pcrop)
        print(".........................................................")
        print(survey_no+farmer_age+farmer_name+farmer_phno+agri_soil+agri_irrigation+agri_ccrop+agri_prev_crop+agri_cattles)
        print(".........................................................")




        #get the geojson data

        geo_data=survey_details.find_one({"surveyno":survey_no})
        agri_geodata=geo_data["coordinates"]
        agri_area=geo_data["area"]
        print(geo_data)


        #create the document for collection
        farmer_details_data={
            "surveyno":survey_no,
            "name":farmer_name,
            "age":farmer_age,
            "phone_no":farmer_phno,
            "area":agri_area,
            "soil_type":agri_soil,
            "irrigation":agri_irrigation,
            "ccrop":agri_ccrop,
            "pcrop":agri_pcrop,
            "coordinates":agri_geodata,
            "no_of_cattles":agri_cattles
        }
        obj_id=farmer_details.insert_one(farmer_details_data).inserted_id;
        print(obj_id)
        return render_template("farmer_reg.html")

'''Survey Addition Route: Pushing Survey no, coordinates and area'''
@app.route("/surveyadd",methods=["POST","GET"])
def survey_add():
    if request.method=="GET":
        return render_template("surveyadd.html")
    if request.method=="POST":
        survey_number = request.form["survey_no"].upper()
        geo_coordinates = request.form["co_ordinates"].upper()
        print("------------------------------------------------------------------------------------------------")
        print(survey_number + " " + geo_coordinates)
        print("------------------------------------------------------------------------------------------------")
        geo_coordinates_list = eval(geo_coordinates)
        print(geo_coordinates_list)
        print(geo_coordinates_list)
        geom = Polygon(geo_coordinates_list)
        geom_area = ops.transform(
            partial(
                pyproj.transform,
                pyproj.Proj(init='EPSG:4326'),
                pyproj.Proj(
                    proj='aea',
                    lat1=geom.bounds[1],
                    lat2=geom.bounds[3])),
            geom)
        print(geom_area.area)  # area in square metres
        land_area = (geom_area.area) * 0.000247105
        print(land_area)  # area in acres

        # area attributed is to be added to the database (not added currently)
        '''land_details_data={
            "surveyno":survey_number,
            "coordinates":geo_coordinates_list,
            "area":land_area
        }
        obj_id=survey_details.insert_one(land_details_data).inserted_id;
        print(obj_id)'''
        return render_template("surveyadd.html")

if __name__ == '__main__':
    app.run()
