from flask import jsonify,Flask,url_for,render_template,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask_login import LoginManager, UserMixin , login_user ,logout_user, login_required
import base64
import json
from werkzeug.security import generate_password_hash,check_password_hash
from flask_mail import Mail,Message
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import current_user
from livereload import server,Server
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT']= 0
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)
app.secret_key= "wutyeihdhhasbnk"
login_manager = LoginManager()
login_manager.init_app(app)
mail = Mail(app)
from array import *
@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

def send_reset_email(user):
    token = get_reset_token(user)
    msg = Message('Password Reset Request',
                  sender='MAIL',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    user = User.query.filter_by(email='MAIL').first()
    send_reset_email(user)
    
    flash('An email has been sent with instructions to reset your password.', 'info')
    return redirect('/login')
    

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
            user_id = s.loads(token)['user_id']
    except:
            user = None
    user = User.query.get(user_id)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect('/')
    else:
      return redirect(url_for('forgot',user=user.id))
@app.route('/resetform/<user>')
def resetform(user):
    return render_template('forgot_password.html',user=user)

@app.route('/resetpass/<user>',methods=['POST'])
def resetpass(user):
     hashed_password = generate_password_hash(request.form['password'])
     user_change=User.query.filter_by(id=user).first()
     user_change.password_hash = hashed_password
     db.session.commit()
     flash('Your password has been updated! You are now able to log in', 'success')
     return redirect('/')

class User(UserMixin,db.Model):
    id =  db.Column(db.Integer,primary_key=True)
    password_hash = db.Column(db.String(30))
    username = db.Column(db.String(30),unique=True)
    email = db.Column(db.String(255),nullable=False,unique=True)

@login_manager.user_loader
def load_user(user_id):
   return User.query.get(int(user_id))

def set_password(self,password):
    self.password_hash =generate_password_hash(password)

def check_password(self,password):
    return check_password_hash(self.password_hash,password)



@app.route('/home')
@login_required
def home():
    return render_template('Graph.html')
    
    
@app.route('/')
def login():
    return render_template('login.html')
    
@app.route('/view')
@login_required
def profile():
    return render_template('view.html')
    
@app.route('/forgotpass')
def forgot(user):
    return render_template('forgot_password.html',user=user)
    
@app.route('/model')
@login_required
def predict():
    return render_template('Graph.html')

@app.route('/', methods=['POST'])    
def login_post():
    if request.method == 'POST':
     pwd = request.form['password']
     user1 = User.query.all()
     for user in user1: 
      if(check_password(user,pwd)):
       login_user(user)
       db.session.commit()
       return redirect(url_for('home')); 
     flash("Invalid Credentials")
     return redirect(url_for("login"))

@app.route('/logout')
@login_required
def logout():
      logout_user()
      flash("Logged out")
      return render_template("login.html") 


@app.route('/viewinput',methods = ['POST'])
def modelrun(): 
    #saving basic model  
  
   import os
   if request.method == 'POST':
    graph = request.files['input']
    graph.save(os.path.join("PATH_TO_DIR","graph.txt"))
    f="PATH_TO_DIR/graph.txt"
    from communities.algorithms import louvain_method,girvan_newman
    from communities.visualization import draw_communities
    import networkx as nx
    import matplotlib.pyplot as plt
    import csv
    import sys
    import numpy as np


    def buildG(G, file_, delimiter_):
            reader = csv.reader(open(file_), delimiter=delimiter_)
            for line in reader:
                    G.add_edge(int(line[0]),int(line[1]))
    G = nx.Graph()  
    print(G)
    buildG(G, f, ' ')
    nx.draw(G,pos=nx.spring_layout(G))
    plt.savefig('../static/plotgraph.png')
    #matrix to array
    S= np.array(nx.to_numpy_matrix(G,dtype=int))
    print(S)
    plt.clf()
    plt.cla()
    plt.close()

    #louvain    
    communities, _ = louvain_method(S)
    draw_communities(S, communities,False,'../static/louvain.png')
    print("communities")
    plt.clf()
    plt.cla()
    plt.close()

    #girvan
    import community as girvan_newman
    import matplotlib.cm as cm
    L=G
    partition = girvan_newman.best_partition(L)


    # draw the graph
    pos = nx.spring_layout(L)
    cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
    nx.draw_networkx_nodes(L, pos, partition.keys(), node_size=40,
    cmap=cmap, node_color=list(partition.values()))
    nx.draw_networkx_edges(L, pos, alpha=0.5)
    plt.savefig('../static/girvan.png') 
    plt.clf()
    plt.cla()
    plt.close()

    #visualization
    #Highest_degree
    com = set(partition.values())
    c_dict = {c: [l for l,i in partition.items() if i==c ] for c in com}
    highest_degree ={l: max(i, key=lambda x:G.degree(x)) for l,i in c_dict.items()}
    a = []
    for i in range(0,len(highest_degree)):
       a.append([])
       for j in range(0,2):
               a[i].append([])

    for i in range(0,len(highest_degree)):
        a[i][0]=(highest_degree[i])
        a[i][1]=(G.degree(highest_degree[i]))
    length=[]
    for i in range(0,len(highest_degree)):
        length.append(i)
    
    f=[]
    i=0
    y=0
    #total no of communities
    for i in partition:
      if partition[i] not in f:
        f.append(partition[i])
        y=y+1   
    #print("Total No of Communities: ", y)      
    #each community size
    import numpy as np
    l = np.zeros((y,), dtype=int)
    for i in partition:
      k = partition[i]
      l[k]=l[k]+1     

    for i in range(0,y):
    #print("Community ", i+1," Size: ")
      print(l[i])  
    
    #elements in each community
    k=len(partition)#no of partitions
    g=[]
    for i in range(0,y):
       g.append(i)#list of communities
    
    m=[]#community stored as list of lists
    for x in range(0,y):  
     print("Community: ",x+1)
     q=[]
     for j in partition.keys():  
        if(partition[j]==x):
           q.append(j)
     m.append(q)

    #generate bar graph
    height = l
    bars = range(len(l))
    y_pos = np.arange(len(bars))

    # Create bars
    plt.bar(y_pos, height)

    # Create names on the x-axis
    plt.xticks(y_pos, bars)

    plt.xlabel('Communities')
    plt.ylabel('No. of nodes')
    plt.savefig('../static/bargraph.png') 
    plt.clf()
    plt.cla()
    plt.close()
    
    
    
    #calculating radius, diameter,center, periphery for each community and image
    d=[]
    r=[]
    c=[]
    p=[]

    for i in range(0,len(highest_degree)):
        d.append([])
    for i in range(0,len(highest_degree)):
        r.append([])
    for i in range(0,len(highest_degree)):
        c.append([])
    for i in range(0,len(highest_degree)):
        p.append([])  
    count=0                                            
    
    for i in range(0,len(highest_degree)):
     L= G.copy()
     f='PATH_TO_DIR/graph.txt'
     def removeG(L, file_, delimiter_):
            reader = csv.reader(open(file_), delimiter=delimiter_)
            for line in reader:
                if partition[int(line[0])]!=i:
                 if partition[int(line[1])]!=i and L.has_edge(int(line[0]),int(line[1])):  
                    L.remove_edge(int(line[0]),int(line[1]))
                    L.remove_node(int(line[0]))
                    L.remove_node(int(line[1]))
                if partition[int(line[0])]!=i and L.has_node(int(line[0])):
                    L.remove_node(int(line[0]))
                if partition[int(line[1])]!=i  and L.has_node(int(line[1])):
                    L.remove_node(int(line[1]))
    
     removeG(L,f,' ')
     ecc = nx.eccentricity(L,v=None ,sp=None)
     k=nx.diameter(L,e=ecc)
     print(k)
     d[i].append(k)
     r[i].append(nx.radius(L,e=ecc))
     for k in nx.center(L,e=ecc):
        c[i].append(k)
     for k in nx.periphery(L,e=ecc):
        p[i].append(k)
     nx.draw_networkx(L, with_labels = True)
     f='../static/community'+str(count)+'.png'
     count=count+1
     plt.savefig(f)
     plt.clf()
     plt.cla()
     plt.close()
         
    return render_template("view.html",y=y,l=l,partition=partition,m=m,g=g,a=a,length=length,count=count,d=d,p=p,r=r,c=c)
   
if __name__ == "__main__":
   app.run(debug=True,port=35729)    



