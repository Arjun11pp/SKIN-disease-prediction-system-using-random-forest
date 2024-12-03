from flask import Flask, render_template, request, redirect, session ,jsonify
import datetime

from sklearn.ensemble import RandomForestClassifier

from DBConnection import Db
import demjson


app = Flask(__name__)
app.secret_key="hiii"

staticpath1=r"C:\Users\LENOVO\PycharmProjects\aiskin\\"
staticpath=r"C:\Users\LENOVO\PycharmProjects\aiskin\static\pic\\"



@app.route('/login', methods=['get', 'post'])
def login():
    if request.method=="POST":
        username=request.form['textfield']
        password=request.form['textfield2']
        db=Db()
        res=db.selectOne("select * from login where username='"+username+"' and password='"+password+"'")
        if res is None:
            return "<script>alert('Incorrect details');window.location='/';</script>"
        else:
            type=res['usertype']
            if type=="admin":
                session['lg']='lin'
                return redirect("/admin_admin_home")
            elif type=="doctor":
                session['lg']='lin'
                session['lid']=res['login_id']
                return redirect("/doctor_doctor_home")
            else:
                return "<script>alert('Unauthorised user');window.location='/login';</script>"
    else:
        return render_template("Login.html")

@app.route("/")
def aa():
    return render_template("index.html")

@app.route("/admin_add_disease", methods=['get', 'post'])
def admin_add_disease():
    if session['lg']=='lin':
        if request.method == "POST":
            diseasename=request.form['textfield']
            description=request.form['textarea']
            type=request.form['select']
            hwtocure=request.form['textfield2']
            db=Db()
            db.insert("insert into disease(disease_name,description,dtype,how_to_cure) values('"+diseasename+"','"+description+"', '"+type+"', '"+hwtocure+"')")
            return "ok"
        else:
            return render_template("Admin/add_disease.html")
    else:
        return redirect('/')


@app.route("/admin_add_symptom/<did>", methods=['get', 'post'])
def admin_add_symptom(did):
    if session['lg']=='lin':
        if request.method == "POST":
            symptomname=request.form['textfield']
            db=Db()
            db.insert("insert into symptoms (disease_id,symptom_name) values('"+did+"','"+symptomname+"')")
            return "<script>alert('Symptom added');window.location='/admin_view_disease';</script>"
        else:
            return render_template("Admin/add_symptom.html")
    else:
        return redirect('/')

@app.route("/admin_admin_home")
def admin_admin_home():
    if session['lg']=='lin':
        db=Db()
        # return render_template("Admin/admin_home.html")
        return render_template("Admin/index.html")
    else:
        return redirect('/')
@app.route("/admin_approve_doctor")
def admin_approve_doctor():
    if session['lg']=='lin':
        db=Db()
        res=db.select("select * from login, doctor where login.login_id=doctor.doctor_id and login.usertype='pending'")
        return render_template("Admin/approve_doctor.html",data=res)
    else:
        return redirect('/')

@app.route("/admin_approve_btn/<up>")
def admin_approve_btn(up):
    # if session['lg']==['lin']:
        db=Db()
        db.update("update login set usertype='doctor' where login_id='"+up+"' ")
        return "<script>alert('Approved succesfully');window.location='/admin_view_approvedoctor';</script>"
    # else:
    #     return redirect('/')
@app.route("/admin_reject_btn/<up>")
def admin_reject_btn(up):
    # if session['lg']==['lin']:
        db=Db()
        db.delete("delete from  login   where login_id='"+up+"'")
        db.delete("delete from  doctor    where doctor_id='"+up+"'")
        return "<script>alert('rejected succesfully');window.location='/admin_view_approvedoctor';</script>"
    # else:
    #      return redirect('/')

@app.route("/admin_view_approvedoctor")
def admin_view_approvedoctor():
        if session['lg']=='lin':
            db=Db()
            res=db.select("select * from login, doctor where login.login_id=doctor.doctor_id and login.usertype='doctor'")
            return render_template("Admin/view_approvedoctor.html",data=res)
        else:
            return redirect('/')

@app.route("/admin_view_disease")
def admin_view_disease():
        if session['lg']=='lin':
            db=Db()
            res=db.select("select * from disease")
            return render_template("Admin/view_disease.html", data=res)
        else:
            return redirect('/')

@app.route("/delete_disease/<did>")
def delete_disease(did):
    if session['lg']=='lin':
        db=Db()
        db.delete("delete from disease where disease_id='"+did+"'")
        return redirect("/admin_view_disease")
    else:
        return redirect('/')

@app.route("/doctor_view_appointments")
def view_appointments():
    if session['lg']=='lin':
        db=Db()
        res=db.select("select * from appointment,user,schedule where appointment.sched_id = schedule.sched_id and  user.user_id=appointment.user_id and schedule.date=curdate() and schedule.doctor_id='"+str(session['lid'])+"'   ")
        return render_template('Doctor/doctor_view_appoinments.html',data=res)
    else:
        return redirect('/')

@app.route("/admin_view_doctorreview/<did>")
def admin_view_doctorreview(did):
    if session['lg']=='lin':
        db=Db()
        res=db.select("select * from review,user where review.user_id=user.user_id and review.doctor_id='"+did+"'")
        return render_template("Admin/view_doctorreview.html",data=res)
    else:
        return redirect('/')

@app.route("/admin_view_feedback")
def admin_view_feedback():
    if session['lg']=='lin':
        db = Db()
        res=db.select("select * from user,feedback where user.user_id=feedback.user_id")
        return render_template("Admin/view_feedback.html",data=res)
    else:
        return redirect('/')

@app.route("/admin_view_symptom/<did>")
def admin_view_symptom(did):
    if session['lg']=='lin':
        db = Db()
        res=db.select("select * from symptoms where disease_id='"+did+"'")
        return render_template("Admin/view_symptom.html", data=res)
    else:
        return redirect('/')

@app.route("/delete_symptom/<sid>/<did>")
def delete_symptom(sid, did):
    if session['lg']=='lin':
        db=Db()
        db.delete("delete from symptoms where symptom_id='"+sid+"'")
        return redirect("/admin_view_symptom/"+did)
    else:
        return redirect('/')


@app.route("/admin_view_user")
def admin_view_user():
    if session['lg']=='lin':
        db = Db()
        res=db.select("select * from user")
        return render_template("Admin/view_user.html",data=res)
    else:
        return redirect('/')




##############################################                      DOCTOR MODULE


@app.route("/doctor_doctor_home")
def doctor_doctor_home():
    if session['lg']=='lin':
        db=Db()
        return render_template("Doctor/doctor_index.html")
    else:
        return redirect('/')

@app.route("/doctor_add_schedule" ,methods=['get', 'post'])
def doctor_add_schedule():
    if session['lg']=='lin':
        if request.method=="POST":
            date=request.form['textfield']
            fromtime=request.form['textfield2']
            totime=request.form['textfield3']
            db=Db()
            db.insert("insert into schedule (date,time_from,time_to, doctor_id)values('"+date+"','"+fromtime+"','"+totime+"', '"+str(session['lid'])+"')")
            return "<script>alert('Schedule added');window.location='/doctor_add_schedule';</script>"
        else:
             return render_template("Doctor/add_schedule.html")
    else:
        return redirect('/')

@app.route("/doctor_change_password",methods=['get','post'])
def doctor_change_password():
    if session['lg']=='lin':
        if request.method=="POST":
            newpassword=request.form['textfield']
            conformpassword=request.form['textfield2']
            db=Db()
            res=db.selectOne("SELECT * FROM login where login_id='"+str(session['lid'])+"'")
            if res is not None:
                if newpassword==conformpassword:
                    db.update("update login set password='"+conformpassword+"' where login_id='"+str(session['lid'])+"' ")
                    return "<script>alert('password changed successfully');window.location='/';</script>"
                else :
                    return "<script>alert('password missmatched');window.location='/doctor_change_password';</script>"
            else :
                return "<script>alert('invalid data');window.location='/doctor_change_password';</script>"
        else:
            return render_template("Doctor/change_password.html")
    else:
        return redirect('/')


@app.route("/doctor_registration" ,methods=['get','post'])
def doctor_registration():
    if request.method=="POST":
        name=request.form['textfield']
        email=request.form['textfield2']
        phone=request.form['textfield3']
        qualification=request.form['textfield4']
        password=request.form['textfield5']
        spec=request.form['select']
        db=Db()
        qry=db.insert("insert into login VALUES ('','"+email+"','"+password+"','pending')")

        db.insert("insert into doctor VALUES ('"+str(qry)+"','"+name+"','"+email+"','"+phone+"','"+qualification+"', '"+spec+"')")
        return "<script>alert('Registered successfully');window.location='/';</script>"
    else:
        return render_template("Doctor/registration.html")

@app.route("/doctor_view_appointment/<sid>")
def doctor_view_appointment(sid):
    if session['lg']=='lin':
        db=Db()
        res=db.select("select * from appointment ,user where appointment.user_id=user.user_id and appointment.sched_id='"+sid+"' ")
        return render_template("Doctor/view_appointment.html",data=res)
    else:
        return redirect('/')

@app.route("/doctor_view_disease_doctor")
def doctor_view_disease_doctor():
    if session['lg']=='lin':
        db=Db()
        res=db.select("select * from disease")
        return render_template("Doctor/view_disease_doctor.html",data=res)
    else:
        return redirect('/')

@app.route("/doctor_view_previous_patients",methods=['get','post'])
def doctor_view_previous_patients():
    if session['lg']=='lin':
        if request.method=="POST":
            name=request.form['textfield']
            db=Db()
            res = db.select("select * from appointment, user, schedule where schedule.sched_id=appointment.sched_id and appointment.user_id=user.user_id and schedule.doctor_id='" + str(session['lid']) + "' and schedule.date<curdate() and user.name like '"+name+"%'")
            return render_template("Doctor/view_previous_patients.html", data=res)

        db=Db()
        res=db.select("select * from appointment, user, schedule where schedule.sched_id=appointment.sched_id and appointment.user_id=user.user_id and schedule.doctor_id='"+str(session['lid'])+"' and schedule.date<curdate()")
        return render_template("Doctor/view_previous_patients.html", data=res)
    else:
        return redirect('/')

@app.route("/doctor_view_profile", methods=['get', 'post'])
def doctor_view_profile():
    if session['lg']=='lin':
        if request.method=="POST":
            name=request.form['textfield']
            phone=request.form['textfield3']
            qualification=request.form['textfield4']
            db=Db()
            db.update("update doctor set name='"+name+"' ,phone='"+phone+"' ,qualification='"+qualification+"' where doctor_id='"+str(session['lid'])+"'")
            return redirect("/doctor_view_profile")
        else:
            db=Db()
            res=db.selectOne("select * from doctor where doctor_id='"+str(session['lid'])+"'")
            return render_template("Doctor/view_profile.html", data=res)
    else:
        return redirect('/')


@app.route("/doctor_view_reviews")
def doctor_view_reviews():
    if session['lg']=='lin':
        db=Db()
        res=db.select("select * from review, user where review.user_id=user.user_id and review.doctor_id='"+str(session['lid'])+"'")
        return render_template("Doctor/view_reviews.html",data=res)
    else:
        return redirect('/')

@app.route("/doctor_view_schedule")
def doctor_view_schedule():
    if session['lg']=='lin':
        db=Db()
        res=db.select("select * from schedule where doctor_id='"+str(session['lid'])+"'")
        return render_template("Doctor/view_schedule.html",data=res)
    else:
        return redirect('/')



@app.route("/delete_schedule/<sid>")
def delete_schedule(sid):
    if session['lg']=='lin':
        db=Db()
        db.delete("delete from schedule where sched_id='"+sid+"'")
        return redirect("/doctor_view_schedule")
    else:
        return redirect('/')
# --------------------------------------------

########################################### chat #############################################




@app.route('/ph_user_chat/<uid>')
def ph_user_chat(uid):
    if session['lg']=="lin":

        return render_template("Doctor/tech_user_chat.html",u=uid)
    else:
        return redirect('/')


# @app.route('/company_staff_chat',methods=['post'])
# def company_staff_chat():
#     if session['ln'] == "oo":
#         db=Db()
#         a=session['lid']
#         q1="SELECT `user`.* FROM `pharmacy`,`user`,`booking`,`p_medicine` WHERE `pharmacy`.`pid`=`p_medicine`.`pharmacyid` AND `p_medicine`.`p_medid`=`booking`.`p_medicineid` AND `booking`.`userid`=`user`.`userid` AND `pharmacy`.`pid`='"+str(session['lid'])+"' group by user.userid"
#         res = db.select(q1)
#         v={}
#         if len(res)>0:
#             v["status"]="ok"
#             v['data']=res
#         else:
#             v["status"]="error"
#
#         rw=demjson.encode(v)
#         print(rw)
#         return rw
#     else:
#         return login()

@app.route('/chatsnd/<u>',methods=['post'])
def chatsnd(u):
    if session['lg']=="lin":

        db=Db()
        c = session['lid']
        b=request.form['n']
        print(b)
        m=request.form['m']

        q2="insert into chat values(null,now(),curtime(),'"+str(c)+"','"+str(u)+"','"+m+"')"
        res=db.insert(q2)
        v = {}
        if int(res) > 0:
            v["status"] = "ok"

        else:
            v["status"] = "error"

        r = demjson.encode(v)

        return r
    else:
        return redirect('/')


@app.route('/chatrply',methods=['post'])
def chatrply():
    if session['lg']=="lin":

        print("...........................")
        c = session['lid']
        t = Db()
        qry2 = "select * from chat ORDER BY chat_id ASC ";
        res = t.select(qry2)
        print(res,)

        v = {}
        if len(res) > 0:
            v["status"] = "ok"
            v['data'] = res
            v['id']=c
        else:
            v["status"] = "error"

        rw = demjson.encode(v)
        return rw
    else:
        return redirect('/')








##############################################################################################



@app.route("/logout")
def logout():
    session.clear()
    session['lg']=""
    return redirect('/')



# ---------------------------------------------------MAIN SECTION----------------------------------------------------------------

# ---------------------------------------------------------------------image-------------------------------
@app.route("/doctor_prediction_image",methods=['get','post'])
def doctor_prediction_image():
    if session['lg']=='lin':
        if request.method=="POST":
            photo=request.files['fileField']
            db=Db()
            date=datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            photo.save(r"C:\Users\LENOVO\PycharmProjects\aiskin\static\pic\\"+date+'.jpg')
            import numpy as np
            from skimage import io, color, img_as_ubyte
            # from DBConnection import Db
            from skimage.feature import greycomatrix, greycoprops
            from sklearn.metrics.cluster import entropy
            #
            rgbImg = io.imread(staticpath + date + '.jpg')
            grayImg = img_as_ubyte(color.rgb2gray(rgbImg))

            distances = [1, 2, 3]
            angles = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4]
            properties = ['energy', 'homogeneity', 'dissimilarity', 'correlation', 'contrast']

            glcm = greycomatrix(grayImg,
                                distances=distances,
                                angles=angles,
                                symmetric=True,
                                normed=True)

            feats = np.hstack([greycoprops(glcm, 'energy').ravel() for prop in properties])
            feats1 = np.hstack([greycoprops(glcm, 'homogeneity').ravel() for prop in properties])
            feats2 = np.hstack([greycoprops(glcm, 'dissimilarity').ravel() for prop in properties])
            feats3 = np.hstack([greycoprops(glcm, 'correlation').ravel() for prop in properties])
            feats4 = np.hstack([greycoprops(glcm, 'contrast').ravel() for prop in properties])

            k = np.mean(feats)
            l = np.mean(feats1)
            m = np.mean(feats2)
            n = np.mean(feats3)
            o = np.mean(feats4)
            ar = []
            ar.append(k)
            ar.append(l)
            ar.append(m)
            ar.append(n)
            ar.append(o)
            arr = []
            test_val = np.array(ar)
            arr.append(test_val)

            import pandas as pd
            a = pd.read_csv(staticpath1 + "staticfeatures.csv")
            attributes = a.values[1:, 0:5]
            labels = a.values[1:, 5]

            rf = RandomForestClassifier(n_estimators=100)
            rf.fit(attributes, labels)
            pred = rf.predict(arr)
            print("Hi")
            print(pred, pred[0][1])
            return render_template("Doctor/prediction_image.html", data=pred[0])

        return render_template("Doctor/prediction_image.html")
    else:
        return redirect('/')


# ---------------------------------------------symptoms------------------------------------------


@app.route("/add_symptoms", methods=['get','post'])
def add_symptoms():
    if session['lg']=='lin':
        session['head']="Select Your Symptoms "
        if request.method=="POST":
            val=request.form.getlist('symp')
            if len(val)>0:
                symp=",".join(val)
                from pred import Disease
                ds=Disease()
                print("hi")
                # ds = diseases_prediction()
                pred=ds.predictDisease(symp)
                session['prediction'] = pred
                session['symptoms'] = symp
                print("Result--------------------------")
                print("Symptoms  ",symp)
                print("Disease  ", pred)
                specialization={
                    "Fungal infection": "Dermatology",
                    "Allergy":"Allergist and Clinical Immunologist",
                    "Diabetes":"Endocrinologist",
                    "Bronchial Asthma":"Pulmonologist",
                    "Hypertension ":"Cardiology",
                    "Migraine":"Neurology",
                    "Malaria":"General Physician/ Internal Medicine",
                    "Chicken pox":"General Physician/ Internal Medicine",
                    "Drug Reaction":"General Physician/ Internal Medicine",
                    "Dengue":"General Physician/ Internal Medicine",
                    "Typhoid":"General Physician/ Internal Medicine",
                    "Common Cold":"General Physician/ Internal Medicine",
                    "Jaundice":"General Physician/ Internal Medicine",
                    "Pneumonia":"Pulmonology/ Respiratory Medicine",
                    "Heart attack":"Cardiology",
                    "VaricoseD veins":"Pain Management",
                    "Gastroenteritis":"Endocrinology ",
                    "GERD":"Endocrinology ",

                }
                try:
                    category=specialization[pred]
                    print("To consult", category)
                except:
                    category="General Physician/ Internal Medicine"

                db=Db()
                session['head']="View Result"

                # res = db.select("select * from doctor  where specialization='" + category + "'")
                symptoms = ["Itching", "Skin Rash", "Nodal Skin Eruptions", "Continuous Sneezing", "Shivering",
                            "Chills", "Joint Pain", "Stomach Pain", "Acidity", "Vomiting", "Fatigue", "Anxiety",
                            "High Fever", "Weight Loss", "Restlessness", "Cough", "Breathlessness", "Sweating",
                            "Dehydration", "Indigestion"]

                return render_template("doctor/select_symptoms.html", p=pred, data=symptoms, ln=len(symptoms))
            else:
                return "<script>alert('Please choose symptoms');window.location='/add_symptoms'</script>"
        symptoms=["Itching", "Skin Rash", "Nodal Skin Eruptions", "Continuous Sneezing","Shivering", "Chills", "Joint Pain", "Stomach Pain","Acidity","Vomiting","Fatigue","Anxiety","High Fever","Weight Loss","Restlessness","Cough","Breathlessness","Sweating","Dehydration","Indigestion"]
        return render_template("doctor/select_symptoms.html", data=symptoms, ln=len(symptoms))
    return redirect('/')

# tlist("symp")






#######################################                     ANDROID

@app.route('/and_login', methods=['post'])
def and_login():
    username=request.form['usr']
    password=request.form['psw']
    db=Db()
    res=db.selectOne("select * from login where username='"+username+"' and password='"+password+"'")
    if res is None:
        return jsonify(status="invalid")
    else:
        type=res['usertype']
        if type=="user":
            return jsonify(status="ok", lid=res['login_id'],type=res['usertype'])
        else:
            return jsonify(status="no")

@app.route('/and_register' , methods=['post'])
def and_register():
    name=request.form['nam']
    email=request.form['em']
    phone=request.form['ph']
    age=request.form['ag']
    gender=request.form['gnd']
    password=request.form['psw']
    db=Db()
    lid=db.insert("INSERT INTO login (username, password, usertype) VALUES('"+email+"', '"+password+"', 'user')")
    db.insert("INSERT INTO user (user_id,name,email,phone,age,gender) VALUES('"+str(lid)+"','"+name+"','"+email+"','"+phone+"','"+age+"','"+gender+"')")
    return jsonify(status="ok")

@app.route('/and_view_profile' ,methods=['post'])
def and_view_profile():
    lid=request.form['lid']
    db=Db()
    res=db.selectOne("select * from user where user_id='"+lid+"'")
    print(res)
    return jsonify(status="ok",name=res['name'],email=res['email'],phone=res['phone'],age=res['age'],gender=res['gender'])

@app.route('/and_view_doc', methods=['post'])
def and_view_doc():
    db=Db()
    res=db.select("select * from doctor ")
    print(res)
    return jsonify(status="ok",data=res)

@app.route('/and_view_sche', methods=['post'])
def and_view_sche():
    did=request.form['did']
    db=Db()
    res=db.select("select * from schedule where schedule.doctor_id='"+did+"' ")
    print(res)
    return jsonify(status="ok",data=res)




########################################### chat android ####################################


@app.route('/add_chat',methods=['post'])
def add_chat():
    lid = request.form['lid']
    toid = request.form['toid']
    message = request.form['message']
    db=Db()
    q2="insert into chat(date,time,from_id,to_id,message)values(curdate(),curtime(),'"+lid+"','"+toid+"','"+message+"')"
    res = db.insert(q2)
    res1 = {}
    res1['status'] = "Inserted"
    return demjson.encode(res1)

@app.route('/view_chat',methods=['post'])
def view_chat():
    lid = request.form['lid']
    toid = request.form['toid']
    lastid = request.form['lastid']
    print("aaaaaaaaaaaaa",lid,toid,lastid)
    db = Db()
    q2="select chat.* from chat where chat_id>'"+lastid+"' and ((from_id='"+lid+"' and to_id='"+toid+"') or (from_id='"+toid+"' and to_id='"+lid+"'))"
    res = db.select(q2)
    print(res)
    res1 = {}
    res1['status'] = "ok"
    res1['data'] = res
    return demjson.encode(res1)
# @app.route('/view_staff',methods=['post'])
# def view_chatcouncillor():
#     lid = request.form['lid']
#     print(lid)
#     qry = db.selectOne("select * from student,course where student.stud_course_id=course.course_id and student.stud_id='" + str(lid) + "'")
#     print(qry)
#     cid = qry['stud_course_id']
#     y = qry['batch']
#     q = db.select("select * from subect_alloc,staff,subject,suballoctocourse where  suballoctocourse.suballoccourseid=subect_alloc.csuballocid and suballoctocourse.ssubid=subject.sub_id and staff.Staff_id=subect_alloc.staff_name and suballoctocourse.scid='"+str(cid)+"' group by staff.Staff_id ")
#     # print(q, cid)
#     res1 = {}
#     res1['status'] = "ok"
#     res1['data'] = q
#     return demjson.encode(res1)



######################################################################################################


@app.route('/and_review', methods=['post'])
def and_review():
    id=request.form['id']
    did=request.form['did']
    re=request.form['re']
    db = Db()
    db.insert("insert into review VALUES ('',curdate(),'"+id+"','"+did+"','"+re+"')")
    return jsonify(status="ok")

@app.route('/and_feedback', methods=['post'])
def and_feedback():
    id=request.form['id']
    fee=request.form['fee']
    db = Db()
    db.insert("insert into feedback VALUES ('','"+id+"',curdate(),'"+fee+"')")
    return jsonify(status="ok")

@app.route('/and_view_booking',methods=['post'])
def and_view_booking():
    bn=request.form['bn']
    acn=request.form['acn']
    ifsc=request.form['ifsc']
    did=request.form['sid']
    id=request.form['id']
    db=Db()
    ses=db.selectOne("select * from bank where bank_name='"+bn+"' and account_no='"+acn+"' and ifsc_no='"+ifsc+"'")
    if ses is None:
        return jsonify(status="no")
    else:
        if float(ses['balance']) < 100:
            return jsonify(status="insuff")
        else:
            # res=db.selectOne("select max(token_no)+1 as tkn from appointment where appoint_id=1")
            res=db.selectOne("select max(token_no)+1 as tkn from appointment where sched_id='"+did+"'")
            if res is not None:

                res=db.insert("insert into appointment VALUES ('','"+id+"','"+did+"','"+str(res['tkn'])+"')")
                db.insert("insert into payment VALUES ('','" +str(res) +"',100)")
                db.update("update bank set balance=balance+'100' where bank_id='1'")
                db.update("update bank set balance=balance-'100' where bank_id='"+str(ses['bank_id'])+"'")
                return jsonify(status="ok")

@app.route('/and_prediction_image',methods=['post'])
def and_prediction_image():
    img=request.files['pic']
    lid=request.form['id']
    db=Db()
    date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    p=img.save(r"C:\Users\LENOVO\PycharmProjects\aiskin\static\pic\\" + date + '.jpg')
    path="/static/pic/"+date+'.jpg'
    import numpy as np
    from skimage import io, color, img_as_ubyte
    # from DBConnection import Db
    from skimage.feature import greycomatrix, greycoprops
    from sklearn.metrics.cluster import entropy
    #
    rgbImg = io.imread(r"C:\Users\LENOVO\PycharmProjects\aiskin\static\pic\\" + date + '.jpg')
    grayImg = img_as_ubyte(color.rgb2gray(rgbImg))

    distances = [1, 2, 3]
    angles = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4]
    properties = ['energy', 'homogeneity', 'dissimilarity', 'correlation', 'contrast']

    glcm = greycomatrix(grayImg,
                        distances=distances,
                        angles=angles,
                        symmetric=True,
                        normed=True)

    feats = np.hstack([greycoprops(glcm, 'energy').ravel() for prop in properties])
    feats1 = np.hstack([greycoprops(glcm, 'homogeneity').ravel() for prop in properties])
    feats2 = np.hstack([greycoprops(glcm, 'dissimilarity').ravel() for prop in properties])
    feats3 = np.hstack([greycoprops(glcm, 'correlation').ravel() for prop in properties])
    feats4 = np.hstack([greycoprops(glcm, 'contrast').ravel() for prop in properties])

    k = np.mean(feats)
    l = np.mean(feats1)
    m = np.mean(feats2)
    n = np.mean(feats3)
    o = np.mean(feats4)
    ar = []
    ar.append(k)
    ar.append(l)
    ar.append(m)
    ar.append(n)
    ar.append(o)
    arr = []
    test_val = np.array(ar)
    arr.append(test_val)

    import pandas as pd
    a = pd.read_csv(staticpath1 + "staticfeatures.csv")
    attributes = a.values[1:, 0:5]
    labels = a.values[1:, 5]

    rf = RandomForestClassifier(n_estimators=100)
    rf.fit(attributes, labels)
    pred = rf.predict(arr)
    print(pred, pred[0][1])
    if pred[0]=='Acne and Rosacea':
        return jsonify(status="ok",rslt="Acne and Rosacea")
    elif pred[0]=='Actinic Keratosis':
        return jsonify(status="ok",rslt="Actinic Keratosis")
    elif pred[0]=='Atopic Dermatitis':
        return jsonify(status="ok",rslt="Atopic Dermatitis")
    else:
        return jsonify(status="ok",rslt="Bullous Disease")




# --------------------------------------------------Predict Symptoms-----------------------------



@app.route("/and_symptoms", methods=['post'])
def and_symptoms():
    f1=request.form['f1']
    f2=request.form['f2']
    f3=request.form['f3']
    f4=request.form['f4']
    f5=request.form['f5']
    f6=request.form['f6']
    f7=request.form['f7']
    f8=request.form['f8']
    f9=request.form['f9']
    f10=request.form['f10']
    f11=request.form['f11']
    f12=request.form['f12']
    f13=request.form['f13']
    f14=request.form['f14']
    f15=request.form['f15']
    f16=request.form['f16']
    f17=request.form['f17']
    f18=request.form['f18']
    f19=request.form['f19']
    f20=request.form['f20']

    val=[]
    if f1=="1":
        val.append("Itching")
    if f2=="1":
        val.append("Skin Rash")
    if f3=="1":
        val.append("Nodal Skin Eruptions")
    if f4=="1":
        val.append("Continous Sneezing")
    if f5=="1":
        val.append("Shivering")
    if f6=="1":
        val.append("Chills")
    if f7=="1":
        val.append("Joint Pain")
    if f8=="1":
        val.append("Stomach Pain")
    if f9=="1":
        val.append("Acidity")
    if f10=="1":
        val.append("Vomiting")
    if f11=="1":
        val.append("Fatigue")
    if f12=="1":
        val.append("Anxiety")
    if f13=="1":
        val.append("High Fever")
    if f14=="1":
        val.append("Weight Loss")
    if f15=="1":
        val.append("Restlessness")
    if f16=="1":
        val.append("Cough")
    if f17=="1":
        val.append("Breathlessness")
    if f18=="1":
        val.append("Sweating")
    if f19=="1":
        val.append("Dehydration")
    if f20=="1":
        val.append("Indijestion")


    if len(val)>0:
        symp=",".join(val)
        from pred import Disease
        ds=Disease()
        print("hi")
        # ds = diseases_prediction()
        pred=ds.predictDisease(symp)
        session['prediction'] = pred
        session['symptoms'] = symp
        print("Result--------------------------")
        print("Symptoms  ",symp)
        print("Disease  ", pred)
        specialization={
            "Fungal infection": "Dermatology",
            "Allergy":"Allergist and Clinical Immunologist",
            "Diabetes":"Endocrinologist",
            "Bronchial Asthma":"Pulmonologist",
            "Hypertension ":"Cardiology",
            "Migraine":"Neurology",
            "Malaria":"General Physician/ Internal Medicine",
            "Chicken pox":"General Physician/ Internal Medicine",
            "Drug Reaction":"General Physician/ Internal Medicine",
            "Dengue":"General Physician/ Internal Medicine",
            "Typhoid":"General Physician/ Internal Medicine",
            "Common Cold":"General Physician/ Internal Medicine",
            "Jaundice":"General Physician/ Internal Medicine",
            "Pneumonia":"Pulmonology/ Respiratory Medicine",
            "Heart attack":"Cardiology",
            "VaricoseD veins":"Pain Management",
            "Gastroenteritis":"Endocrinology ",
            "GERD":"Endocrinology ",
        }
        try:
            category=specialization[pred]
            print("To consult", category)
        except:
            category="General Physician/ Internal Medicine"
        return jsonify(status="ok", p=pred, c=category)





if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

