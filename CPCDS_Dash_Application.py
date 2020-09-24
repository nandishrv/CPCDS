import pandas as pd 
import plotly
import plotly.express as px 
import plotly.graph_objects as go
from csv import reader

import dash
import dash_core_components as dcc 
import dash_html_components as html 
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

#from flask import Flask, redirect, url_for
#from flask_dance.contrib.google import make_google_blueprint, google


cpcds_data=[]
with open(r"D://CPCDS//CPCDS_Claims.csv", 'r') as read_obj:
    csv_reader = reader(read_obj)
    for row in csv_reader:
        if row[89] =='':
            row[89] = "Without Diagnosis description"
        if row[95] =='':
            row[95] = "Without Procedure description"      
        # row variable is a list that represents a row in csv
        cpcds_data+= [[row[2],row[12],row[18],row[48],row[51],row[52],row[89],row[95]],]
        #break;
df=pd.DataFrame(cpcds_data)
new_header = df.iloc[0] #grab the first row for the header
df = df[1:] #take the data less the header row
df.columns = new_header
read_obj.close()
print(new_header)

print("CSV file read done")


#chunks = pd.read_csv(r"\\192.168.6.8\Data_Science\CPCDS Project\CPCDS_Claims.csv", chunksize=10000)
#df = pd.concat(chunks)
#chunks = pd.read_csv(r"D:\CPCDS\CPCDS-compressed.csv", chunksize=1000)
#df = pd.concat(chunks)


#df = pd.read_csv(r"D:\CPCDS\CPCDS_Claims.csv", nrows=4000)
#df['year']=pd.DatetimeIndex(df['Claim paid date']).year

df['Claim paid date'] = pd.to_datetime(df['Claim paid date']).dt.strftime("%Y-%m-%d")

print("Data Cleanup Done")
claim_paid_date = sorted(list(dict.fromkeys(df['Claim paid date'])))
print("claim_paid_date listed")
df_row, df_col = df.shape
df_sum_set=()
for j in [3,4,5]:
    df_sum=0
    for i in range(0,df_row):
        df_sum+=float(df.iat[i,j])
    df_sum_set+=(df_sum,)
print("df sum done")
'''    
# Yearly_Payout
claim_paid_date= sorted(list(dict.fromkeys(df['Claim paid date'])))
#print(claim_paid_date)
payout_yearly_set=[]
for i in claim_paid_date:
    df_filter=df[df['Claim paid date']==i]
    claims=len(df_filter)
    cashless_yearly=(df_filter['Claim total allowed amount'].sum(axis=0, skipna=True))
    reimbursement_yearly=(df_filter['Member reimbursement'].sum(axis=0, skipna=True))
    payout_yearly=(df_filter['Claim payment amount'].sum(axis=0, skipna=True))       
    payout_yearly_set+=[[i,claims,cashless_yearly,reimbursement_yearly,payout_yearly],]
    #print(payout_yearly_set)
yearly_payout=pd.DataFrame(payout_yearly_set, columns=['Claim paid date', 'claims','cashless_yearly','reimbursement_yearly','payout_yearly'])
#print(yearly_payout)

# Yearly_Payout(Admission_Mode)
inpatient_admission_code=sorted(list(dict.fromkeys(df['Claim source inpatient admission code'])))
admission_mode_header=['Claim paid date']
admission_mode_header.extend(inpatient_admission_code)
#print(admission_mode_header)
payout_admission=[]
for i in claim_paid_date:
    df_admisssion=df[df['Claim paid date']==i]
    payout_admission_yearly=[i,]
    for j in inpatient_admission_code:        
        df_admission_code=df_admisssion[df_admisssion['Claim source inpatient admission code']==j]
        payout_admission_yearly+=[df_admission_code['Claim payment amount'].sum(axis=0, skipna=True),]
    payout_admission+=[payout_admission_yearly,]
admission_mode_yearly_payout=pd.DataFrame(payout_admission, columns=admission_mode_header)
#print(admission_mode_yearly_payout)

# Yearly_Payout(Claim_type)
claim_type=sorted(list(dict.fromkeys(df['Claim type'])))
claim_type_header=['Claim paid date']
claim_type_header.extend(claim_type)
payout_claim_type=[]
for i in claim_paid_date:
    df_claim=df[df['Claim paid date']==i]
    payout_claim_type_yearly=[i,]
    for k in claim_type:
        df_claim_type=df_claim[df_claim['Claim type']==k]
        payout_claim_type_yearly+=[df_claim_type['Claim payment amount'].sum(axis=0, skipna=True),]
    payout_claim_type+=[payout_claim_type_yearly,]
claim_type_yearly_payout=pd.DataFrame(payout_claim_type, columns=claim_type_header)
#print(claim_type_yearly_payout)
'''
# Payout(Diagnosis description)
diagnosis_description = sorted(list(dict.fromkeys(df['Diagnosis description'])))
payout_diagnosis_description_set=[]
print(diagnosis_description)
for m in diagnosis_description:
    df_filter=df[df['Diagnosis description']==m]
    claims=len(df_filter)
    nrow, ncol = df_filter.shape
    cashless = 0
    reimbursement = 0
    payout = 0
    for i in range(0,nrow):  
        cashless+= float(df_filter.iat[i,3])
        reimbursement+=float(df_filter.iat[i,4])
        payout+=float(df_filter.iat[i,5])
    payout_diagnosis_description_set+=[[m,claims,cashless,reimbursement,payout],]
    #print(payout_yearly_set)
diagnosis_description_payout=pd.DataFrame(payout_diagnosis_description_set, columns=['diagnosis_description', 'claims','cashless','reimbursement','total_payout'])
diagnosis_description_payout.sort_values(by=['total_payout'], inplace=True, ascending=False)
#print(diagnosis_description_payout)
print("diagnosis_description_Done")
'''
# Payout(Procedure description)
procedure_description = (list(dict.fromkeys(df['Procedure description'])))
payout_procedure_description_set=[]
#print(procedure_description)
for n in procedure_description:
    df_filter=df[df['Procedure description']==n]
    claims=len(df_filter)
    cashless_procedure_description=(df_filter['Claim total allowed amount'].sum(axis=0, skipna=True))
    reimbursement_procedure_description=(df_filter['Member reimbursement'].sum(axis=0, skipna=True))
    payout_procedure_description=(df_filter['Claim payment amount'].sum(axis=0, skipna=True))       
    payout_procedure_description_set+=[[n,claims,cashless_procedure_description,reimbursement_procedure_description,payout_procedure_description],]
    #print(payout_yearly_set)
procedure_description_payout=pd.DataFrame(payout_procedure_description_set, columns=['procedure_description', 'claims','cashless','reimbursement','total_payout'])
procedure_description_payout.sort_values(by=['total_payout'], inplace=True, ascending=False)
#print(diagnosis_description_payout)

# Yearly_Payout_Progress
claim_paid_date = sorted(list(dict.fromkeys(df['Claim paid date'])))
#print(claim_paid_date)
payout_yearly_set=[]
cashless=0
reimbursement=0
payout=0
for i in claim_paid_date:
    df_filter=df[df['year']==i]
    claims=len(df_filter)
    cashless+=(df_filter['Claim total allowed amount'].sum(axis=0, skipna=True))
    reimbursement+=(df_filter['Member reimbursement'].sum(axis=0, skipna=True))
    payout+=(df_filter['Claim payment amount'].sum(axis=0, skipna=True))       
    payout_yearly_set+=[[i,claims,cashless,reimbursement,payout],]
    #print(payout_yearly_set)
daily_payout_progress=pd.DataFrame(payout_yearly_set, columns=['Claim paid date', 'claims','cashless','reimbursement','payout'])
#print(yearly_payout)
'''
#=======================================================================================================
# Payout_Progress_with_Diagnosis_Description
#diagnosis_description = sorted(list(dict.fromkeys(df['Diagnosis description'])))
payout_progress_header=['Claim paid date']
payout_progress_header.extend(diagnosis_description)
progress_data_frame=[]

print(len(diagnosis_description))
print(len(claim_paid_date))


iter=1
for i in claim_paid_date: 
    dff1= df[(df['Claim paid date']==i)] 
    payout_data=[]
    payout_data+=[i,]
    
    for j in diagnosis_description:
        #df_filter=df[(df['Claim paid date']==i) & (df['Diagnosis description']==j)]  
            
        df_filter= dff1[(dff1['Diagnosis description']==j)] 
        dff1 = dff1[dff1['Diagnosis description'] != j]  
        row, col = df_filter.shape
        payout = 0
        for k in range(0, row):
            payout += float(df_filter.iat[k,5])
        #payout=df_filter['Claim payment amount'].sum(axis=0, skipna=True)
        payout_data+=[payout,]
    progress_data_frame+=[payout_data,]
    per=100*iter/len(claim_paid_date)
    print("{0}/{1}-------{2}%".format(iter,len(claim_paid_date),per)) 
    iter+=1 
payout_progress=pd.DataFrame(progress_data_frame, columns=payout_progress_header)
payout_progress1=payout_progress
print("Progress Report Part Done")

row, col = payout_progress.shape
#print(payout_progress.shape)
#print(payout_progress.iat[0,1])

for i in range(1,row):
    for j in range(1,col):
       payout_progress.iat[i,j]= payout_progress.iat[i,j]+payout_progress.iat[i-1,j]
    per=100*i/(row-1)
    print("{0}/{1}-------{2}%".format(i,row-1,per))
print("Progress Report Done")
#=======================================================================================================
'''
# Write Text Report
report_header_list=['Yearly_Payout','Yearly_Payout(Admission_Mode)','Yearly_Payout(Claim_type)','Payout(Diagnosis description)','Payout(Procedure description)','payout_progress1','payout_progress']
report_list=[yearly_payout,admission_mode_yearly_payout,claim_type_yearly_payout,diagnosis_description_payout,procedure_description_payout,payout_progress1,payout_progress]
report_file=open(r'D:\CPCDS.txt','w')
i=1
for i in range(7):
    report_file.write('\n-----------------------------------------------------------------------------------------------\n')
    report_file.write(report_header_list[i])
    report_file.write('\n-----------------------------------------------------------------------------------------------\n')
    report_file.write(report_list[i].to_string(header=True,index=False))
    report_file.write('\n')
report_file.close()
'''
print("Done")

# Dash Application

external_stylesheets = [dbc.themes.BOOTSTRAP]
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    html.H1('CPCDS Data Analysis', style={'border-radius':'10px','background-color': 'DarkBlue','color':'white','display':'inline-block',
                                          'width':'100%','text-align':'center','padding-top':'20px','padding-bottom':'20px'}),
    
    html.H3(['Total Claims',html.Br(),len(df),'+'], style={'border-radius':'10px','background-color': 'DodgerBlue','color':'white',
                                                           'display':'inline-block','width':'20%','height':'100px','text-align':'center',
                                                           'margin-right':'3%','margin-left':'5%','padding-top':'5px',}),

    html.H3(['Cashless',html.Br(),'$ ',int(df_sum_set[0]),'+'], style={'border-radius':'10px','background-color': 'DodgerBlue','color':'white',
                                                                   'display':'inline-block','width':'20%','height':'100px','text-align':'center',
                                                                   'margin-right':'3%','padding-top':'5px',}),

    html.H3(['Reimbursement',html.Br(),'$ ',int(df_sum_set[1]),'+'], style={'border-radius':'10px','background-color': 'DodgerBlue','color':'white',
                                                                        'display':'inline-block','width':'20%','height':'100px','text-align':'center',
                                                                        'margin-right':'3%','padding-top':'5px',}),
    
    html.H3(['Total Claims Amount',html.Br(),'$ ',int(df_sum_set[2]),'+'], style={'border-radius':'10px','background-color': 'DodgerBlue','color':'white',
                                                                              'display':'inline-block','width':'22%','height':'100px','text-align':'center',
                                                                              'margin-right':'3%','padding-top':'5px',}),
    
    html.Div([
        dcc.Dropdown(id='my_dropdown',
            options=[
                    {'label':'Claim Source Inpatient Admission', 'value':'Claim source inpatient admission code'},
                    {'label':'Claim Type', 'value':'Claim type'},        
                    ],
            optionHeight=35,
            value='Claim source inpatient admission code',
            disabled=False,
            multi=False,
            searchable=True,
            search_value='',
            placeholder='Please select...',
            clearable=True,
            style={'width':"90%",'margin-left':'3%'},
                    ),   

        dcc.Graph(id='our_graph')],
    style={'width': '30%', 'display': 'inline-block'}),


    html.Div([
        dcc.Dropdown(id='diagnosis_description',
            options=[{'label': x, 'value': x} for x in diagnosis_description
                    ],
            optionHeight=35,
            value=diagnosis_description_payout['diagnosis_description'][:3],
            disabled=False,
            multi=True,
            searchable=True,
            search_value='',
            placeholder='Please select...',
            clearable=True,
            style={'width':"90%",'margin-left':'5%'},
                    ),   

        dcc.Graph(id='line_graph')],
    style={'width': '70%', 'display': 'inline-block'}
        ),  
            
           
  
])
                      
             
@app.callback(
    Output(component_id='our_graph', component_property='figure'),
    [Input(component_id='my_dropdown', component_property='value')]
)

def plot_pie_chart(column_chosen):
    df1=df
    fig=px.pie(df1, names=column_chosen, title=column_chosen)
    fig.update_traces(textposition='inside', textinfo='percent+label',)    
    return fig

@app.callback(
    Output(component_id='line_graph', component_property='figure'),
    [Input(component_id='diagnosis_description', component_property='value')]
)

def plot_line_chart(column_chosen):
    df2=payout_progress

    fig = go.Figure()
    for i in column_chosen:
        fig.add_trace(go.Scatter(x=df2['Claim paid date'], y=df2[i],
                        mode='lines',
                        name=i))
    fig.layout.plot_bgcolor = 'white'
    fig.layout.title = 'Claim Paid Amount'
    fig.layout.yaxis.gridcolor = 'lightgrey'
    fig.layout.xaxis.gridcolor = 'lightgrey'
    fig.update_xaxes(showline=True, linewidth=2, linecolor='lightgrey', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='lightgrey', mirror=True)
    fig.layout.xaxis.title='Claim Paid Date'
    fig.layout.yaxis.title='Claim Paid Amount'
    #fig.show()
    return fig


if __name__ == '__main__':
    #app.run_server(debug=True)
    #server.run(host="192.168.43.39", port=80)
    server.run(host="127.0.0.1", port=8050)
    