from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)




@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html')    


@app.route('/marks', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/getdetails', methods=['GET', 'POST'])
def getdetails():
    global name
    if request.method == 'POST':
        name = request.form['name']
        sems = request.form['sems']
        sems=int(sems)
        return render_template('new.html', n=name, s=sems)
    return render_template('index.html')
    return name

@app.route('/getmarks', methods=['GET', 'POST'])
def getmarks():
    remarks=[]
    global marks
    if request.method == 'POST':
        marks = list(map(float,(request.form['sgpa']).split()))
        marklen=len(marks)
        for i in range(marklen):
            if(marks[i]<6 and marks[i]>=4.8):
                remarks.append("Uh, Oh! You got to work hard")
            elif(marks[i]>=6 and marks[i]<7):
                remarks.append("Satisfactory")
            elif(marks[i]>=7 and marks[i]<8):
                remarks.append("Well Done")
            elif(marks[i]>=8 and marks[i]<9):
                remarks.append("Impressive")
            elif(marks[i]>=9):
                remarks.append("Incredible")
            elif(marks[i]==0):
                remarks.append("Diploma Student")     
        
        df={'SGPA': marks,
        'Remarks': remarks
        }
        df = pd.DataFrame(df, columns=['SGPA','Remarks'])  
        df.index+=1

        if(marks[0] ==0 and marks[1]==0):
            marklen = marklen-2

        cgpa = round((sum(marks)/marklen),2)
        if(marks[0] ==0 and marks[1]==0):
            best = max(marks[2:])
        else:    
            best = max(marks)

        bi = marks.index(best)+1
        
        if(marks[0] ==0 and marks[1]==0):
            low = min(marks[2:])  
        else:
            low = min(marks) 

        li = marks.index(low)+1 
        if(cgpa<7):
            per=round((7.1*(cgpa)+12),2)
        else:
            per=round((7.4*(cgpa)+12),2)                        
        return render_template('results.html', df=df.to_dict(orient='records'), cgpa=cgpa, best=best, low=low, bi=bi, li=li, per=per, name=name)    
    return render_template('getmarks.html')
    return marks
if __name__ == '__main__':
    app.run()

