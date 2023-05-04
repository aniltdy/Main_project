from flask import *
from src.dbconnection import *
import os
from werkzeug.utils import secure_filename




from stegano import lsb

# secret = lsb.hide("./tests/sample-files/Lenna.png", "Hello World")
# secret.save("./Lenna-secret.png")
# clear_message = lsb.reveal("./Lenna-secret.png")


app=Flask(__name__)

app.secret_key = "27254254"
import functools

def login_required(func):
    @functools.wraps(func)
    def secure_function():
        if "lid" not in session:
            return render_template('login_index.html')
        return func()

    return secure_function


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/')
def log():
    return render_template('login_index.html')


@app.route('/login',methods=['post'])
def login():
    uname = request.form['textfield']
    password = request.form['textfield2']
    qry="SELECT * FROM `login`WHERE `username`=%s AND `password`=%s"
    val=(uname,password)
    r=selectone(qry,val)
    if r is None:
        return '''<script>alert("invalid");window.location="/"</script>'''
    elif r ['type'] =='admin':
        session['lid'] = r['lid']
        return '''<script>alert("logined");window.location="/adminhome"</script>'''
    elif r ['type'] =='leader':
        session['lid'] = r['lid']

        return redirect('leaderhome')
    elif r ['type'] =='member':
        session['lid'] = r['lid']

        return redirect('memberhome')

    else:
        return '''<script>alert("invalid");window.location="/"</script>'''






@app.route('/adminhome',methods=['get','post'])
@login_required
def adminhome():
    return render_template("admin_index.html")



@app.route('/mnagemember',methods=['get','post'])
@login_required
def mnagemember():
    qry="SELECT *FROM `member`"
    res=selectall(qry)
    return render_template("managemember.html",val=res)



@app.route('/addmember',methods=['get','post'])
@login_required
def addmember():
    return render_template("addmember.html")



@app.route('/deletemem',methods=['get','post'])
@login_required
def deletemem():
    id=request.args.get('id')
    qry="delete from member where lid=%s"
    iud(qry,id)
    qr="delete from login where lid=%s"
    iud(qr,id)
    return '''<script>alert("deleted");window.location="mnagemember#about"</script>'''


@app.route('/addmem',methods=['post'])
@login_required
def addmem():
    fname = request.form['textfield']
    lname = request.form['textfield2']
    place = request.form['textfield3']
    post = request.form['textfield4']
    pin = request.form['textfield5']
    phone = request.form['textfield6']
    email = request.form['textfield7']
    username = request.form['textfield8']
    password = request.form['textfield9']
    qry="INSERT INTO `login` VALUES(NULL,%s,%s,'member')"
    val=(username,password)
    id=iud(qry,val)
    qr="INSERT INTO `member` VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s)"
    va=(fname,lname,place,post,pin,phone,email,str(id))
    iud(qr,va)
    return '''<script>alert("success");window.location="mnagemember#about"</script>'''




@app.route('/editmember',methods=['get','post'])
@login_required
def editmember():
    id=request.args.get('id')
    session['mid']=id
    qry="select * from member where tid=%s"
    res=selectone(qry,id)
    return render_template("editmember.html",val=res)



@app.route('/editmemb',methods=['post'])
@login_required
def editmemb():
    fname = request.form['textfield']
    lname = request.form['textfield2']
    place = request.form['textfield3']
    post = request.form['textfield4']
    pin = request.form['textfield5']
    phone = request.form['textfield6']
    email = request.form['textfield7']
    qr="UPDATE `member` SET `fname`=%s,`lname`=%s,`place`=%s,`post`=%s,`pin`=%s,`phone`=%s,`email`=%s WHERE `tid`=%s"
    va=(fname,lname,place,post,pin,phone,email,session['mid'])
    iud(qr,va)
    return '''<script>alert("success");window.location="mnagemember#about"</script>'''


@app.route('/mnageleader',methods=['get','post'])
@login_required
def mnageleader():
    qry="SELECT *FROM `leader`"
    res=selectall(qry)
    return render_template("manageleader.html",val=res)



@app.route('/addleader',methods=['get','post'])
@login_required
def addleader():
    return render_template("addleader.html")


@app.route('/addlead',methods=['post'])
@login_required
def addlead():
    fname = request.form['textfield']
    lname = request.form['textfield2']
    place = request.form['textfield3']
    post = request.form['textfield4']
    pin = request.form['textfield5']
    phone = request.form['textfield6']
    email = request.form['textfield7']
    username = request.form['textfield8']
    password = request.form['textfield9']
    qry="INSERT INTO `login` VALUES(NULL,%s,%s,'leader')"
    val=(username,password)
    id=iud(qry,val)
    qr="INSERT INTO `leader` VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s)"
    va=(fname,lname,place,post,pin,phone,email,str(id))
    iud(qr,va)
    return '''<script>alert("success");window.location="mnageleader#about"</script>'''

@app.route('/editldr',methods=['get','post'])
@login_required
def editldr():
    id=request.args.get('id')
    session['llid']=id
    qry="select * from leader where tid=%s"
    res=selectone(qry,id)
    return render_template("editleader.html",val=res)


@app.route('/editleader',methods=['post'])
@login_required
def editleader():
    fname = request.form['textfield']
    lname = request.form['textfield2']
    place = request.form['textfield3']
    post = request.form['textfield4']
    pin = request.form['textfield5']
    phone = request.form['textfield6']
    email = request.form['textfield7']
    qr="UPDATE `leader` SET `fname`=%s,`lname`=%s,`place`=%s,`post`=%s,`pin`=%s,`phone`=%s,`email`=%s WHERE `tid`=%s"
    va=(fname,lname,place,post,pin,phone,email,session['llid'])
    iud(qr,va)
    return '''<script>alert("success");window.location="mnageleader#about"</script>'''


@app.route('/deletel',methods=['get','post'])
@login_required
def deletel():
    id=request.args.get('id')
    qry="delete from leader where lid=%s"
    iud(qry,id)
    qr="delete from login where lid=%s"
    iud(qr,id)
    return '''<script>alert("deleted");window.location="mnageleader#about"</script>'''


@app.route('/mangework',methods=['get','post'])
@login_required
def mangework():
    qry="SELECT *FROM `work`"
    res=selectall(qry)
    return render_template("managework.html",val=res)



@app.route('/addwork',methods=['get','post'])
@login_required
def addwork():
    return render_template("addwork.html")

@app.route('/addwrk',methods=['post'])
@login_required
def addwrk():
    work = request.form['textfield']
    desc = request.form['textfield2']
    msg=request.form['msg']
    qp = request.files['file']
    fname = secure_filename(qp.filename)
    # qp.save('static/work/' + fname)
    qp.save('static/sample/'+fname)
    qp = lsb.hide(r'static/sample/'+fname, msg)
    qp.save('static/work/'+fname)
    qr="INSERT INTO `work` VALUES(NULL,%s,%s,curdate(),%s)"
    va=(work,desc,fname)
    iud(qr,va)
    return '''<script>alert("success");window.location="mangework#about"</script>'''




@app.route('/deletework',methods=['post','get'])
@login_required
def deletework():
    id=request.args.get('id')
    qr="DELETE FROM  `work` WHERE wwid=%s"

    iud(qr,id)
    return '''<script>alert("Deleted");window.location="mangework#about"</script>'''


@app.route('/assignedwork',methods=['get','post'])
@login_required
def assignedwork():
    qry="SELECT *FROM `work` JOIN `assign` ON work.wwid=assign.wid JOIN leader ON assign.lid=leader.lid "
    res=selectall(qry)
    return render_template("assignworktoleader.html",val=res)

@app.route('/assignwork',methods=['get','post'])
@login_required
def assignwork():
    qry="select * from work"
    r=selectall(qry)
    qr="select * from leader"
    res=selectall(qr)
    return render_template("assigntoleader.html",v=r,val=res)

@app.route('/assignworkkk',methods=['get','post'])
@login_required
def assignworkkk():
    work=request.form['select']
    leader=request.form['select2']
    qry="insert into assign values(null,%s,%s,curdate(),'pending',1)"
    val=(work,leader)
    iud(qry,val)
    return '''<script>alert("success");window.location="assignedwork#about"</script>'''
# ======================================adminhome end================================================

# leaderhome=============================================

@app.route('/leaderhome',methods=['get','post'])
@login_required
def leaderhome():
    return render_template("leader/leaderhome.html")

@app.route('/assignedworkviw',methods=['get','post'])
@login_required
def assignedworkviw():
    qry="SELECT *FROM `work` JOIN `assign` ON work.wwid=assign.wid WHERE assign.lid=%s"
    res=selectall2(qry,session['lid'])
    for i in res:
        clear_message = lsb.reveal("static/work/"+i['image'])
        i['msg']=clear_message
    # print(res)
    # clear_message = lsb.reveal("../static/work")
    # print(clear_message)
    return render_template("leader/viewassign.html",val=res)


@app.route('/allocatetoteammember',methods=['get','post'])
@login_required
def allocatetoteammember():
    id=request.args.get('id')
    session['wid']=id
    qry="SELECT * FROM member"
    res=selectall(qry)
    return render_template("leader/assignmember.html",val=res)

@app.route('/assignworkkkmember',methods=['get','post'])
@login_required
def assignworkkkmember():
    member=request.form['select2']
    qp = request.files['file']
    qp = request.files['file']
    msg=request.form['msg']
    fname = secure_filename(qp.filename)
    # qp.save('static/work/' + fname)
    qp = lsb.hide('static/work/' + fname,msg)
    qp.save('static/work/' + fname)
    qr="update assign set status='Allocated'where wid=%s"
    iud(qr,session['wid'])
    qry="insert into assign values(null,%s,%s,curdate(),'pending',%s)"
    val=(session['wid'],member,fname)
    iud(qry,val)
    return '''<script>alert("success");window.location="assignedworkviw#about"</script>'''



@app.route('/viewrep',methods=['get','post'])
@login_required
def viewrep():
    qry="SELECT *FROM member"
    res=selectall(qry)
    return render_template("leader/viewreport.html",val=res)


@app.route('/viewrepp',methods=['get','post'])
@login_required
def viewrepp():
    name=request.form['select']
    qry="SELECT *FROM member"
    res=selectall(qry)
    qr="SELECT * FROM `report` WHERE lid=%s"
    v=(name)
    r=selectall2(qr,v)

    return render_template("leader/viewreport.html",val=res,val1=r)


# ==================memberhome
@app.route('/memberhome',methods=['get','post'])
@login_required
def memberhome():
    return render_template("member/memberhome.html")

@app.route('/addrep',methods=['get','post'])
@login_required
def addrep():
    return render_template("member/addreport.html")

@app.route('/addrepp',methods=['get','post'])
@login_required
def addrepp():
    title = request.form['textfield']
    qp = request.files['file']
    fname = secure_filename(qp.filename)
    qp.save('static/report/' + fname)
    qry = "insert into report values(null,%s,%s,%s,curdate())"
    val = (title,fname,session['lid'])
    iud(qry, val)
    return '''<script>alert("success");window.location="memberhome#about"</script>'''




@app.route('/viewassignw',methods=['get','post'])
@login_required
def viewassignw():
    qry="SELECT `work`.work,`work`.`description`,`assign`.* FROM `work` JOIN `assign` ON `work`.wwid=`assign`.wid WHERE `assign`.lid=%s"
    res=selectall2(qry,session['lid'])
    for i in res:
        clear_message = lsb.reveal("static/work/" + i['image'])
        i['msg'] = clear_message


    return render_template("member/viewassign.html",val=res)

@app.route('/updatework',methods=['get','post'])
@login_required
def updatework():
    id=request.args.get('id')
    session['awid']=id
    return render_template("member/updatework.html")

@app.route('/updateworkkk',methods=['get','post'])
@login_required
def updateworkkk():
    status=request.form['textfield']
    qry="UPDATE assign SET STATUS=%s WHERE aid=%s"
    val=(status,session['awid'])
    iud(qry,val)
    return '''<script>alert("updated");window.location="memberhome#about"</script>'''


app.run(debug=True)