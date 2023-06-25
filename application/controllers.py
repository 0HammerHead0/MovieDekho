from flask import Flask, request,render_template,redirect,url_for
from flask import current_app as app
from application.models import SHOWS,VENUES,USERS,USERS_SHOWS,UserShowRate
import statistics
import os
import datetime
from .database import db
import matplotlib
matplotlib.use('Agg')
from werkzeug.security import generate_password_hash, check_password_hash
import matplotlib.pyplot as plt
from sqlalchemy import or_ ,and_
current_dir=os.getcwd()
from flask_login import LoginManager,UserMixin,login_user, login_required

login_manager=LoginManager(app)
@login_manager.user_loader
def load_user(user_id):
    return USERS.query.get(int(user_id))

@app.route("/",methods=["GET","POST","DELETE"])
def home():
    if request.method=='GET':
        return render_template("user_login.html")
    elif request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        if not username or not password:
            body="The fields cannot be left empty"
            link="home"
            return redirect(url_for('trans',body=body,link=link))
        existing_user=USERS.query.filter_by(username=username).first()
        if existing_user:
            user=USERS.query.filter_by(username=username).first()
            if(password==user.password):
                login_user(user)
                return redirect(url_for('user_dash',username=user.username))
            body="Password doesn't match"
            link="home"
            return redirect(url_for('trans',body=body,link=link))
        return redirect(url_for('user_register'))
    else:
        print("error check")

@app.route("/summary",methods=["GET","POST"])
def summary():
    if request.method=='GET':
        shows=SHOWS.query.all()
        if shows:
            label=[]
            vals=[]
            for show in shows:
                label.append(show.name)
                vals.append(show.user_rating)
            img_path=os.path.join(current_dir,'static\\images\\user_rate.png')
            fig, ax = plt.subplots()
            fig.set_facecolor('#72D3D1')
            ax.set_facecolor('#72D3D1')
            ax.bar(label,vals,color="#003F36")
            axes_color='#000000'
            plt.ylabel('User Rating(0-5)',color=axes_color)
            for spine in ax.spines.values():
                spine.set_color(axes_color)
            plt.tick_params(axis='x', colors=axes_color)
            plt.tick_params(axis='y', colors=axes_color)
            plt.savefig(img_path)
            label=[]
            vals=[]
            for show in shows:
                label.append(show.name)
                if show.tot_cap>0:
                    vals.append((show.tot_cap-show.rem_cap)/show.tot_cap)
                else:
                    vals.append(0)
            img_path=os.path.join(current_dir,'static\\images\\pop.png')
            fig, ax = plt.subplots()
            fig.set_facecolor('#72D3D1')
            ax.set_facecolor('#72D3D1')
            ax.bar(label,vals,color="#003F36")
            axes_color='#000000'
            plt.ylabel('User Rating(0-5)',color=axes_color)
            for spine in ax.spines.values():
                spine.set_color(axes_color)
            plt.tick_params(axis='x', colors=axes_color)
            plt.tick_params(axis='y', colors=axes_color)
            plt.savefig(img_path)
        venues=VENUES.query.all()
        if venues:
            for venue in venues:
                l=[]
                v=[]
                for show in venue.shows:
                    l.append(show.name)
                    v.append(show.user_rating)
                dir='static\\images\\{img_name}.png'.format(img_name=venue.name)
                img_path=os.path.join(current_dir,dir)
                fig, ax = plt.subplots()
                fig.set_facecolor('#72D3D1')
                ax.set_facecolor('#72D3D1')
                ax.bar(l,v,color="#003F36",width=0.8)
                axes_color='#000000'
                plt.ylabel('Venue {} Rating(0-5)'.format(venue.name),color=axes_color)
                for spine in ax.spines.values():
                    spine.set_color(axes_color)
                plt.tick_params(axis='x', colors=axes_color)
                plt.tick_params(axis='y', colors=axes_color)
                plt.savefig(img_path)
        return render_template("summary.html",venues=venues,shows=shows)
    elif request.method==' POST':
        return ""
    else:
        return "error check"
    
@app.route("/user_dash/<username>",methods=["GET","POST"])
def user_dash(username):
    if request.method=='GET':
        venues=VENUES.query.all()
        user=USERS.query.filter_by(username=username).first()
        sorted_shows=SHOWS.query.order_by(SHOWS.user_rating.desc()).limit(5).all()
        x=5-len(sorted_shows)
        y=["https://media.istockphoto.com/id/915697084/photo/concept-of-reserved-seats.jpg?b=1&s=170667a&w=0&k=20&c=TxTJtGan1OAnc_7LfKoUM_OyDiKzZQqyMCfSGM2M8UE="]*x
        lis=[]
        for i in sorted_shows:
            lis.append(str(i.img))
        lis+=y
        img0=lis[0]
        img1=lis[1]
        img2=lis[2]
        img3=lis[3]
        img4=lis[4]
        return render_template("user_dash.html",user=user,venues=venues,img0=img0,img1=img1,img2=img2,img3=img3,img4=img4)
    elif request.method=="POST":
        location=request.form['location']
        keyword=request.form['search']
        rating=request.form['rating']
        start_time=request.form['start_time']
        end_time=request.form['end_time']
        return redirect(url_for('search_res',keyword=keyword.strip(),username=username,rating=rating,location=location,start_time=start_time,end_time=end_time))
    else:
        return("error check")

@app.route("/search_res",methods=['GET','POST'])
def search_res():
    keyword=request.args.get('keyword')
    username=request.args.get('username')
    location=request.args.get('location')
    rating=request.args.get('rating')
    start_t=request.args.get('start_time')
    print(start_t,"heloooooooooooooooooooooooooooooooooo")
    end_t=request.args.get('end_time')
    venues=VENUES.query.all()
    user=USERS.query.filter_by(username=username).first()
    # print(max(datetime.datetime.strptime(time_str,'%H:%M:%S').time(),datetime.datetime.strptime(tim_str,'%H:%M:%S').time()))
    if request.method=="GET":
        if location==None or location=="0":
            shows=SHOWS.query.all()
        else:
            shows = SHOWS.query.filter(SHOWS.VID == location).all()
        show_list=[]
        if keyword!="":
            for show in shows:
                if rating!="":
                    if ((str(keyword).lower() in str(show.name).lower()) and (float(rating)<=show.rating or float(rating)<=show.user_rating)) or ((str(keyword).lower() in str(show.tags).lower())  and (float(rating)<=show.rating or float(rating)<=show.user_rating)): 
                        show_list.append(show)
                else:
                    if (str(keyword).lower() in str(show.name).lower()) or (str(keyword).lower() in str(show.tags).lower()) : 
                        show_list.append(show)
            if start_t!="" and end_t!="":
                temp=[]
                for show in show_list:
                    if show.start_time!="" and show.end_time!="":
                        print(start_t,end_t)
                        print(datetime.datetime.strptime(str(show.start_time),'%H:%M:%S').time())
                        if datetime.datetime.strptime(str(show.start_time),'%H:%M:%S').time() >= datetime.datetime.strptime(start_t,'%H:%M').time() and  datetime.datetime.strptime(str(show.end_time),'%H:%M:%S').time() <= datetime.datetime.strptime(end_t,'%H:%M').time() :
                            temp.append(show)
                show_list=temp
            return render_template('search_res.html',user=user,show_list=show_list,venues=venues)
        elif rating!="":
            for show in shows:
                if (float(rating)<=show.rating or float(rating)<=show.user_rating): 
                        show_list.append(show)
            if start_t!="" and end_t!="":
                temp=[]
                for show in show_list:
                    if show.start_time!="" and show.end_time!="":
                        print(start_t,end_t)
                        print(datetime.datetime.strptime(str(show.start_time),'%H:%M:%S').time())
                        if datetime.datetime.strptime(str(show.start_time),'%H:%M:%S').time() >= datetime.datetime.strptime(start_t,'%H:%M').time() and  datetime.datetime.strptime(str(show.end_time),'%H:%M:%S').time() <= datetime.datetime.strptime(end_t,'%H:%M').time() :
                            temp.append(show)
                show_list=temp
            return render_template('search_res.html',user=user,show_list=show_list,venues=venues)
        if start_t!="" and end_t!="":
            temp=[]
            for show in shows:
                if show.start_time!="" and show.end_time!="":
                    print(start_t,end_t)
                    print(datetime.datetime.strptime(str(show.start_time),'%H:%M:%S').time())
                    if datetime.datetime.strptime(str(show.start_time),'%H:%M:%S').time() >= datetime.datetime.strptime(start_t,'%H:%M').time() and  datetime.datetime.strptime(str(show.end_time),'%H:%M:%S').time() <= datetime.datetime.strptime(end_t,'%H:%M').time() :
                        temp.append(show)
            shows=temp
        return render_template('search_res.html',user=user,show_list=shows,venues=venues)
    elif request.method=="POST":
        #need to take data again from form of search_res.html, previously it was from  dash
        location=request.form['location']
        keyword=request.form['search']
        rating=request.form['rating']
        start_time=request.form['start_time']
        end_time=request.form['end_time']
        return redirect(url_for('search_res',keyword=keyword.strip(),username=username,rating=rating,location=location,start_time=start_time,end_time=end_time))
    else:
        return("error check")

@app.route("/user_all_bookings/<username>",methods=["GET","POST"])
def user_all_bookings(username):
    if request.method=='GET':
        user=USERS.query.filter_by(username=username).first()
        shows=user.visits
        for i in shows:
            print(i.name)
        user_rates=UserShowRate.query.filter_by(users_id=user.ID).order_by(UserShowRate.shows_id).all()
        # shows=user_rates=db.session.query(USERS_SHOWS).filter_by(users_id=user.ID)
        return render_template("user_all_bookings.html",user=user,shows=shows,user_rates=user_rates,zip=zip)
    elif request.method=="POST":
        return ""
    else:
        print("error check")

@app.route("/rating/<user_id>/<show_id>",methods=["GET","POST"])
def rating(user_id,show_id):
    user=USERS.query.filter_by(ID=user_id).first()
    show=SHOWS.query.filter_by(ID=show_id).first()
    if request.method=='GET':
        return render_template("rating.html",user=user,show=show)
    elif request.method=="POST":
        shows=user.visits
        for key,value in request.form.items():
            if key.startswith('rate'):
                rate=request.form['rate']
                user_show=UserShowRate.query.filter_by(users_id=user.ID,shows_id=show.ID).first()
                if user_show:
                    user_show.rating = rate
                else:
                    db.session.add(UserShowRate(users_id=user.ID,shows_id=show.ID,rating=rate))
        rows=UserShowRate.query.filter_by(shows_id=show.ID).all()
        show.user_rating=round(statistics.mean([int(i.rating) for i in rows]),1)
        db.session.commit()
        user_rates=UserShowRate.query.filter_by(users_id=user.ID).order_by(UserShowRate.shows_id).all()
        return render_template("user_all_bookings.html",user=user,shows=shows,user_rates=user_rates,zip=zip)
    else:
        return ("error check")
    
@app.route("/user_new_booking/<username>/<show_id>",methods=["GET","POST"])
def user_new_booking(username,show_id):
    if request.method=='GET':
        user=USERS.query.filter_by(username=username).first()
        show=SHOWS.query.filter_by(ID=show_id).first()
        return render_template("user_new_booking.html",user=user,show=show)
    elif request.method=="POST":
        number=request.form['number']
        show=SHOWS.query.filter_by(ID=show_id).first()
        total=int(show.price)*int(number)
        if int(show.rem_cap)<int(number):
            body="Not enough seats left!"
            return redirect(url_for('no_seat',username=username,show_id=show_id,body=body))
        return redirect(url_for('user_new_booking_total',username=username,show_id=show_id,total=total,number=number))
    else:   
        return ("error check")
    
@app.route("/user_new_booking/<username>/<show_id>/total",methods=["GET","POST"])
def user_new_booking_total(username,show_id):
    if request.method=='GET':
        total = request.args.get('total')
        number = request.args.get('number')
        user=USERS.query.filter_by(username=username).first()
        show=SHOWS.query.filter_by(ID=show_id).first()
        return render_template("user_new_booking_total.html",user=user,show=show,total=total,number=number)
    elif request.method=="POST":
        number = request.args.get('number')
        show=SHOWS.query.filter_by(ID=show_id).first()
        show.rem_cap=int(show.rem_cap)-int(number)
        user=USERS.query.filter_by(username=username).first()
        user.visits.append(show)
        user_show=UserShowRate.query.filter_by(users_id=user.ID,shows_id=show.ID).first()
        if user_show:
            user_show.seats+=int(number)
        else:
            db.session.add(UserShowRate(users_id=user.ID,shows_id=show.ID,seats=int(number)))
        db.session.commit()
        return redirect(url_for('user_dash',username=username))
    else:   
        return ("error check")

@app.route("/no_seat",methods=["GET","POST"])
def no_seat():
    body = request.args.get('body')
    username=request.args.get('username')
    show_id=request.args.get('show_id')
    if request.method=='GET':
        return render_template('trans.html',title="Try Again!",body=body)
    else:
        return redirect(url_for('user_new_booking',username=username,show_id=show_id))

@app.route("/admin_login",methods=["GET","POST"])
def admin_login():
    username_admin="admin"
    password_admin="admin"
    if request.method=='GET':
        return render_template("admin_login.html")
    elif request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        if username==username_admin and password==password_admin:
            return redirect(url_for('admin_dash'))
        elif not username or not password:
            body="The fields cannot be left empty"
            link="admin_login"
            return redirect(url_for('trans', body=body, link=link))
        else:
            body="Password doesn't match"
            link="admin_login"
            return redirect(url_for('trans',body=body,link=link))
    else:   
        return ("error check")
    
@app.route("/admin_dash",methods=["GET","POST"])
def admin_dash():
    if request.method=='GET':
        venues=VENUES.query.all()
        return render_template("admin_dash.html",venues=venues)
    elif request.method=="POST":
        return "hello"
    else:   
        return ("error check")

@app.route("/del_venue/<venue_id>",methods=["GET","POST"])
def del_venue(venue_id):
    if request.method=='GET':
        venue=VENUES.query.filter_by(ID=venue_id).first()
        shows=SHOWS.query.filter_by(VID=venue_id).all()
        for show in shows:
            db.session.query(USERS_SHOWS).filter_by(shows_id=show.ID).delete()
            db.session.delete(show)
        db.session.delete(venue)
        db.session.commit()
        return redirect(url_for('admin_dash'))
    else:
        return("error check")  
      
@app.route("/edit_venue/<venue_id>",methods=["GET","POST"])
def edit_venue(venue_id):
    if request.method=='GET':
        title="Edit the venue"
        return render_template("create_venue.html",title=title)
    elif request.method=="POST":
        venue=VENUES.query.filter_by(ID=venue_id).first()
        if request.form['name'] != "":
            venue.name=request.form['name']
        if request.form['location'] != "":
            venue.place=request.form['location']
        if request.form['capacity'] !="":
            venue.capacity=request.form['capacity']
        db.session.commit()
        return redirect(url_for('admin_dash'))
    else:
        return ("error check")
    
@app.route("/delete_show/<show_id>",methods=["GET","POST","DELETE"])
def del_show(show_id):
    if request.method=='GET':
        show=SHOWS.query.filter_by(ID=show_id).first()
        db.session.query(USERS_SHOWS).filter_by(shows_id=show_id).delete()
        db.session.delete(show)
        db.session.commit()
        return redirect(url_for('admin_dash'))
    else:
        return ("error check")
    
@app.route("/edit_show/<venue_id>/<show_id>",methods=["GET","POST"])
def edit_show(show_id,venue_id):
    if request.method=='GET':
        venue=VENUES.query.filter_by(ID=venue_id).first()
        title="Edit the show"
        return render_template("create_show.html",venue=venue,title=title)
    elif request.method=="POST":
        show=SHOWS.query.filter_by(ID=show_id).first()
        if request.form['name'] !="":
            show.name=request.form['name']
        if request.form['rating'] != "":
            show.rating=request.form['rating']
        if request.form['start_time'] != "":
            show.start_time=datetime.datetime.strptime(request.form['start_time']+":00",'%H:%M:%S').time()
        if request.form['end_time'] != "":
            show.end_time=datetime.datetime.strptime(request.form['end_time']+":00",'%H:%M:%S').time()
        if request.form['date'] != "":
            show.date=request.form['date']
        if request.form['tags'] != "":
            show.tags=request.form['tags']
        if request.form['price'] != "":
            show.price=int(request.form['price'])
        if request.form['capacity'] !="":
            show.rem_cap=int(request.form['capacity'])
            show.tot_cap=int(request.form['capacity'])
        if request.form['img']!="":
            show.img=request.form['img']
        db.session.commit()
        return redirect(url_for('admin_dash'))
    else:
        return ("error check")

@app.route("/create_show/<venue_id>",methods=["GET","POST"])
def create_show(venue_id):
    if request.method=='GET':
        venue=VENUES.query.filter_by(ID=venue_id).first()
        title="Create a new show"
        return render_template("create_show.html",title=title,venue=venue)
    elif request.method=="POST":
        venue=VENUES.query.filter_by(ID=venue_id).first()
        name=request.form['name']
        rating=request.form['rating']
        if rating=="":
            rating=0
        else:
            try:
                rating=rating
            except:
                return redirect(url_for('value_error',venue_id=venue_id))
        start_time=request.form['start_time']+":00"
        end_time=request.form['end_time']+":00"
        if start_time==":00" :
            start_time="00:00:00"
        if end_time==":00" :
            end_time="00:00:00"
        start_time=datetime.datetime.strptime(str(start_time),'%H:%M:%S').time()
        end_time=datetime.datetime.strptime(str(end_time),'%H:%M:%S').time()
        date=request.form['date']
        if date=="" :
            date=str(datetime.datetime.now().date())
        tags=request.form['tags']
        price=request.form['price']
        if price=="":
            price=0
        else:
            try:
                price=int(price)
            except:
                return redirect(url_for('value_error',venue_id=venue_id))
        capacity=request.form['capacity']
        if capacity=="":
            capacity=0
        else:
            try:
                capacity=int(capacity)
            except:
                return redirect(url_for('value_error',venue_id=venue_id))
        img=request.form['img']
        if img=="":
            img="https://media.istockphoto.com/id/915697084/photo/concept-of-reserved-seats.jpg?b=1&s=170667a&w=0&k=20&c=TxTJtGan1OAnc_7LfKoUM_OyDiKzZQqyMCfSGM2M8UE="
        db.session.add(SHOWS(name=name,rating=rating,tags=tags,price=price,start_time=start_time,end_time=end_time,VID=venue.ID,rem_cap=capacity,rated=1,img=img,tot_cap=capacity,date=date))
        db.session.commit()
        return redirect(url_for('admin_dash'))
    else:   
        return ("error check")
    
@app.route("/create_venue",methods=["GET","POST"])
def create_venue():
    if request.method=='GET':
        title="Create a new venue-"
        return render_template("create_venue.html",title=title)
    elif request.method=="POST":
        name=request.form['name']
        location=request.form['location']
        capacity=request.form['capacity']
        db.session.add(VENUES(name=name,place=location,capacity=capacity))
        db.session.commit()
        return redirect(url_for('admin_dash'))
    else:
        return ("error check")

@app.route("/value_error",methods=["GET","POST"])
def value_error():
    venue_id=request.args.get('venue_id')
    if request.method=='GET':
        return render_template('trans.html',title="Try Again!",body="Please check the value type entered")
    else:
        return redirect(url_for('create_show',venue_id=venue_id))

@app.route("/user_register",methods=["GET","POST","DELETE"])
def user_register():
    if request.method=='GET':
        return render_template("user_register.html")
    elif request.method=="POST":
        name=request.form['name']
        username=request.form['username']
        password=request.form['password']
        if not username or not password or not name:
            body="The fields cannot be left empty"
            link="user_register"
            return redirect(url_for('trans', body=body, link=link))
        user=USERS.query.filter_by(username=username).first()
        if user:
            body="Already an existing user!"
            link="user_register"
            return redirect(url_for('trans',body=body,link=link))
        else:
            db.session.add(USERS(name=name,username=username,password=password))
            db.session.commit()           
            return redirect(url_for('user_dash',username=username))
    else:
        return("error check")

@app.route("/trans/<link>",methods=["GET","POST"])
def trans(link):
    body = request.args.get('body')
    if request.method=='GET':
        return render_template('trans.html',title="Try Again!",body=body)
    else:
        return redirect(url_for(link))

@app.route('/go_back',methods=["GET","POST"])
def go_back():
    return redirect(request.referrer)