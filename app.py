from flask import Flask, render_template, request
import json
import requests
import random
import base64

app = Flask(__name__)
@app.route('/', methods=['GET','POST'])
def main():
    
    if request.method=='POST':
        
        title=str(request.form['title'])
        description=str(request.form['description'])
        param_dict = {"SearchText":title, "PageNo":1, "NoOfRecordsPerPage":1000, "OrderBy":"UpdatedOn", "SortOrder":"DESC", "IsResumeSearch": True, "Filters":[] }
        PARAMS = json.dumps(param_dict)
        headers={'Content-type':'application/json', 'Accept':'application/json'}
        p = requests.post(url = 'https://psgqaapiservice.azurewebsites.net/GlobalDbAdvancedSearch/', data=PARAMS, headers=headers)
        candidates=p.json()
        
        candidate_list=[]
        candidate_data=''
        
        if len(candidates['appViewList'])>5:
            candidate_list = random.sample(range(0, min([len(candidates['appViewList']),1000])), 5)
        else:
            candidate_list = [i for i in range(len(candidates['appViewList']))]

        for i in candidate_list:
            name = candidates['appViewList'][i]['Document']['FirstName'] + ' ' + candidates['appViewList'][i]['Document']['LastName']
            email = candidates['appViewList'][i]['Document']['Email']
            resume = candidates['appViewList'][i]['Document']['ResumePath']
            if not resume:
                continue
            
            ENCODING = 'utf-8'
            base64_resume_object = base64.b64encode(requests.get(resume).content)
            base64_resume_string = base64_resume_object.decode(ENCODING)
            candidate_http_request_data = {'JobOrderId':34892,'ClientJONumber':'111229','EndClientJONumber':None,'SubAccountId':602,'SubAccountDetails':None,'Location':'Pune, Pune, Maharashtra, India','Type':None,'BillRate':None,'MaxBillRate':None,'PayRate':None,'MaxPayRate':None,'ContractLength':None,'MarkupRate':None,'JobFunction':'jolit','JobSubFunction':'jolsfsoftdev','JobIndustry':'indit','JobOrderDate':'2021-03-08T08:00:00','JobBandLevel':'jbnd0','AssignedTo':'3a86217a-19ef-4a10-87c9-3a60c4e2e9ce','IsShared':False,'InternalNotes':None,'Status':'joactive','InternalQAAuditor':None,'TimeLimit':0,'Burden':0.0,'Priority':1,'NoOfOpenings':5,'MaxSubmits':0,'PSGGoalSubmits':0,'IsReopened':False,'ClientJODate':'2021-03-05T08:00:00','IsDeleted':False,'CreatedBy':'3a86217a-19ef-4a10-87c9-3a60c4e2e9ce','CreatedOn':'2021-03-08T06:44:16.953','UpdatedBy':None,'UpdatedOn':None,'ClosedOn':None,'ClosedBy':None,'IsAtsFetched':False,'City':'Pune','State':'MH','Country':'IN','PostalCode':None,'Skills':'C#, SQL.','FolderGroupId':None,'SubAccountName':None,'AssignedToName':None,'AccountId':293,'AccountName':None,'HoursRemaining':None,'AnnualWage':0.0,'DirectHirePercentage':0.0,'CandidateDetails':None,'JobOrderUsers':None,'IsRequestToVerify':False,'PublishOnCareersPage':False,'PublishedBy':None,'LatestPublishDate':None,'CareersPageTitle':None,'CareersPageDescription':None,'CareersPageSkills':None,'JobOrderDateStartOfDay':'2021-03-08T00:00:00','AllowJobsOnCP':False,'PreferredJobTerm':'Permanent','ShortDescription':None,'ShortTitle':None,'GeographyCordinates':None,'Address':'Pune','CareersPageTemplate':None,'ClientInfo':None,'EndClient':'Thinkbridge','EnableAutomatedCandEngagement':False,'AllowJOTemplateConfig':False,'SourcingIntelligence':None,'HireEventDate':'2021-03-15T07:00:00','HireEventStartTime':'00:00:00','HireEventEndTime':'12:00:00','CurrencyCode':'INR','IsSponsored':False,'CandidateCount':0,'TotalCandidateSS':0,'EmploymentSchedule':'Full Time','JOLink':None,'FinalRate':None,'ActualSubmit':1.0,'AbJobOrderDate':'2021-03-08T00:00:00','AbClientJODate':'2021-03-05T00:00:00','AbJobOrderDateStartOfDay':'2021-03-07T00:00:00','TodayCandidateCount':0,'TodayJOWorkedBy':None,'ActualTimeToSubmit':4356.67,'ActualTimeToFirstSubmit':4356.67,'PooledCandidateCount':0,'GroupPoolCandidateCount':None,'ModernHireRequisitionId':None,'UseJOTempConfig':False,'IsDefaultJO':False,'EmailBox':None,'AllowJobsOnIndeed':False,'IsIndeedRequestToVerify':False,'PublishOnIndeed':False,'LatestIndeedPublishDate':None,'IsForIndeed':False,'IsForCareerPage':False,'JobStatusMsg':None,'IsPreQualConfigured':False,'IsStateWideJO':None,'PayRateType':None,'PublishCompanyName':None,'TagValue':None,'CutOffScore':None,'IsRequestToVerifyOnJobVite':False,'IsForJobVite':False,'JobviteAttachmentKey':None,'JobviteOrderId':None,'JobviteOrderStatus':None,'PublishOnJobVite':False,'PublishDateOnJobVite':None,'PublishedByOnJobVite':None,'RetryCountForJobVite':0,'TimezoneDateTime':'2021-03-07T22:44:16.953','Timezone':'Pacific Standard Time'}
            candidate_http_request_data['Title'] = title
            candidate_http_request_data['Description'] = description
            data={}
            data['jobOrder'] = json.dumps(candidate_http_request_data)
            data['fileContentInBase64Stringformat'] = base64_resume_string
            PARAMS = json.dumps(data, indent=2)
            headers={'Content-type':'application/json', 'Accept':'application/json'}
            p = requests.post(url = 'https://psg-inboundlead-parser.azurewebsites.net/api/GetTheRankingScore', data = PARAMS,headers = headers)
        
            joined_name='_'.join(name.split())
            candidate_data = candidate_data + joined_name + ' ' + email + ' '
        
        candidates=[i for i in candidate_data.split()]
        if len(candidates)<10:
            for i in range(len(candidates),10):
                candidates.append('Nil')
        a1=candidates[0]
        a2=candidates[1]
        b1=candidates[2]
        b2=candidates[3]
        c1=candidates[4]
        c2=candidates[5]
        d1=candidates[6]
        d2=candidates[7]
        e1=candidates[8]
        e2=candidates[9]
        return render_template('result.html', a1=a1, a2=a2, b1=b1, b2=b2, c1=c1, c2=c2, d1=d1, d2=d2, e1=e1, e2=e2)
    
    return render_template('index.html')

if __name__=='__main__':
	app.run(debug=True)