from flask import Flask, render_template, request
import pandas as pd
import pygal

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

@app.route('/displaygraph', methods=['GET', 'POST'])
def displaygraph():
    x_axis=[]
    marking_len=len(marks)
    for i in range(marking_len):
        x_axis.append(i+1)        
    graph = pygal.Line()
    graph.title = 'Performance Graph (SEM vs SGPA)'
    graph.x_labels = x_axis
    graph.add('Progress', marks)
    graph_data = graph.render_data_uri()
    if(marks[0] ==0 and marks[1]==0):
        rem=['Diploma Student', 'Diploma Student', 'Initial']
        pivot=3
        piv=2
    else:    
        rem=['Initial']
        pivot=1
        piv=0
    for comp in range(len(marks)):
        if(pivot<marking_len):
            sem_ind=marks.index(marks[pivot])
            if(marks[pivot]>marks[piv]):
                dif=marks[pivot]-marks[piv]
                rem.append("Good. Improvement of {} compared to Sem {}".format(round(dif,2), piv+1))
            elif(marks[pivot]==marks[piv]):
                rem.append("No difference")
            else:
                diff=marks[piv]-marks[pivot]
                rem.append("Poor. Detoriated by {} compared to Sem {}".format(round(diff,2), piv+1))
        pivot=pivot+1
        piv=piv+1


    df1={'Sem': x_axis, 'SGPA': marks, 'Remarks': rem}   
    df1 = pd.DataFrame(df1, columns=['Sem', 'SGPA', 'Remarks'])  
    df1.index+=1 

    
    if(marks[0] ==0 and marks[1]==0):
        total_sems = 6
        total_pointer_sum = 60
    else:    
        total_sems=8
        total_pointer_sum=80
    
    total_pointer=10

    dummy=[]

    mk=marking_len
    if(marks[0] ==0 and marks[1]==0):
        mk=mk-2
    else:
        mk=mk

    scored=sum(marks)/mk
    remaining_sems=total_sems-mk
    if request.method == 'POST':
        desired_pointer=request.form['desper']
        desired_pointer=float(desired_pointer)
        desired_score=desired_pointer*total_sems

        to_score=desired_score-sum(marks)
        if(remaining_sems!=0):
            actual_score=to_score/remaining_sems
            max_pointer_sum=remaining_sems*total_pointer
            max_pointer=(sum(marks)+max_pointer_sum)/total_sems    
            if(actual_score>10):
                dummy.append("Maximum you can score is: {}".format(round(max_pointer,2)))    
            else:
                dummy.append("Score Minimum {} in each of the remaining semesters. Good Luck".format(round(actual_score,2)))    
        else:
            dummy.append("You have Completed your course, Your CGPA is {}".format(round(scored,2)))        
        return render_template('graphs.html', graph_data=graph_data, marks=marks, df1=df1.to_dict(orient='records'), dummy=dummy)
    return render_template('graphs.html', graph_data=graph_data, marks=marks, df1=df1.to_dict(orient='records'), dummy=dummy)


if __name__ == '__main__':
    app.run()

