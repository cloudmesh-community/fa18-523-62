import pandas as pd
from textblob import TextBlob
#from sklearn import model_selection
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
data3= pd.read_csv("Consolidated.csv")

#Create a dictionary to map Hashtags to team name.
dic = {'AFCB':'Bournemouth',
'AFC':	'Arsenal',
'arsenalfc':	'Arsenal',
'gunners':	'Arsenal',
'coyg':	'Arsenal',
'BHAFC':	'Brighton',
'brightonandhovealbion':	'Brighton',
'Clarets':	'Burnley',
'BurnleyFC':	'Burnley',
'cardiffcity':	'Cardiff',
'cardiffcityfc':	'Cardiff',
'CFC':	'Chelsea',
'chelseafc':	'Chelsea',
'stamfordbridge':	'Chelsea',
'CPFC':	'Crystal Palace',
'crystalpalacefc':	'Crystal Palace',
'EFC':	'Everton',
'evertonfc':	'Everton',
'FulhamFC':	'Fulham',
'HTAFC':	'Huddersfield',
'LCFC':	'Leicester',
'leicestercity':	'Leicester',
'LFC':	'Liverpool',
'liverpoolfc':	'Liverpool',
'thekop':	'Liverpool',
'MCFC':	'Man City',
'mancity':	'Man City',
'manchestercity':	'Man City',
'MUFC':	'Man United',
'MUTD':	'Man United',
'MANU':	'Man United',
'reddevils':	'Man United',
'manutd':	'Man United',
'ggmu':	'Man United',
'NUFC':	'Newcastle',
'newcastleunitedFC':	'Newcastle',
'SaintsFC':	'Southampton',
'southamptonFC':	'Southampton',
'COYS':	'Tottenham',
'TottenhamHotspur':	'Tottenham',
'TottenhamHotspurs':	'Tottenham',
'comeonyouspurs':	'Tottenham',
'Thfc':	'Tottenham',
'WatfordFC':	'Watford',
'WHUFC':	'West Ham',
'wwfc':	'Wolves',
'Wolverhamptonfc':	'Wolves',
'WolverhamptonWanderers':	'Wolves',
'wolvesfc':	'Wolves',
'westhamunited': 	'West Ham'}

data3.replace({"used_hashtag": dic}, inplace=True)

###############################################################

odds_data= pd.read_csv("soccerData.csv")
main_data= data3
main_data['sentiment']=0
for i in range(main_data.shape[0]):
    blob = TextBlob(main_data.iloc[i,5])
    main_data.iloc[i,8] = blob.sentiment.polarity

main_data['dateid'] = (main_data['dateid']).astype(int)
final_data = main_data.loc[main_data['dateid'] < 20180818].groupby(['used_hashtag'])[["sentiment"]].mean()
final_data.reset_index(level=0, inplace=True)
final_data['Gameweek']=1
#j=2
cutdateids = [20180818,20180825,20180901,20180915,20180922,20180929,20181006,20181020,20181027,20181103,20181110,20181124,20181201]
for j in range(1,len(cutdateids)):
    temp_df = main_data.loc[(main_data['dateid'] < cutdateids[j]) & (main_data['dateid'] >= cutdateids[j-1])].groupby(['used_hashtag'])[["sentiment"]].mean()
    temp_df.reset_index(level=0, inplace=True)
    temp_df['Gameweek']=j+1
    final_data=final_data.append(temp_df)
    j+=1

odds_data['homesentiment']=0
odds_data['awaysentiment']=0
for gw in range(1,13):
    for team in list(set(final_data['used_hashtag'])):
        #df.loc[(df['Gameweek']==gw) & ((df['HomeTeam']==team) | (df['AwayTeam']==team)),'homesentiment'] = df1.loc[(df1['Gameweek']==gw) & (df1['used_hashtag']==team),'sentiment'].values[0]
        odds_data.loc[(odds_data['Gameweek']==gw) & (odds_data['HomeTeam']==team),'homesentiment'] = final_data.loc[(final_data['Gameweek']==gw) & (final_data['used_hashtag']==team),'sentiment'].values[0]
        odds_data.loc[(odds_data['Gameweek']==gw) & (odds_data['AwayTeam']==team),'awaysentiment'] = final_data.loc[(final_data['Gameweek']==gw) & (final_data['used_hashtag']==team),'sentiment'].values[0]

########### Creating the cumsum dictionary
odds_data['goals_hm_cm']=0
odds_data['goals_away_cm']=0
odds_data['shots_hm_cm']=0
odds_data['shots_away_cm']=0
odds_data['shots_target_hm_cm']=0
odds_data['shots_target_away_cm']=0
odds_data['fouls_hm_cm']=0
odds_data['fouls_away_cm']=0
odds_data['corners_hm_cm']=0
odds_data['corners_away_cm']=0
odds_data['yellow_hm_cm']=0
odds_data['yellow_away_cm']=0
odds_data['red_hm_cm']=0
odds_data['red_away_cm']=0
cm_goals={1:{},2:{},3:{},4:{},5:{},6:{},7:{},8:{},9:{},10:{},11:{},12:{},13:{}}
cm_shots={1:{},2:{},3:{},4:{},5:{},6:{},7:{},8:{},9:{},10:{},11:{},12:{},13:{}}
cm_shots_target={1:{},2:{},3:{},4:{},5:{},6:{},7:{},8:{},9:{},10:{},11:{},12:{},13:{}}
cm_fouls={1:{},2:{},3:{},4:{},5:{},6:{},7:{},8:{},9:{},10:{},11:{},12:{},13:{}}
cm_corners={1:{},2:{},3:{},4:{},5:{},6:{},7:{},8:{},9:{},10:{},11:{},12:{},13:{}}
cm_yellow={1:{},2:{},3:{},4:{},5:{},6:{},7:{},8:{},9:{},10:{},11:{},12:{},13:{}}
cm_red={1:{},2:{},3:{},4:{},5:{},6:{},7:{},8:{},9:{},10:{},11:{},12:{},13:{}}
for i in range(odds_data.shape[0]):
    #for team in list(set(final_data['used_hashtag'])):
        gw=odds_data.loc[i,'Gameweek']
        if gw==1:
            #goals
            cm_goals[gw].update({odds_data.loc[i,'HomeTeam'] : odds_data.loc[i,'goals_hm']})
            cm_goals[gw].update({odds_data.loc[i,'AwayTeam'] : odds_data.loc[i,'goals_away']})
            odds_data.loc[i,'goals_hm_cm']=0
            odds_data.loc[i,'goals_away_cm']=0
            #shots
            cm_shots[gw].update({odds_data.loc[i,'HomeTeam'] : odds_data.loc[i,'shots_hm']})
            cm_shots[gw].update({odds_data.loc[i,'AwayTeam'] : odds_data.loc[i,'shots_away']})
            odds_data.loc[i,'shots_hm_cm']=0
            odds_data.loc[i,'shots_away_cm']=0
            #shots_target
            cm_shots_target[gw].update({odds_data.loc[i,'HomeTeam'] : odds_data.loc[i,'shots_target_hm']})
            cm_shots_target[gw].update({odds_data.loc[i,'AwayTeam'] : odds_data.loc[i,'shots_target_away']})
            odds_data.loc[i,'shots_target_hm_cm']=0
            odds_data.loc[i,'shots_target_away_cm']=0
			   #fouls
            cm_fouls[gw].update({odds_data.loc[i,'HomeTeam'] : odds_data.loc[i,'fouls_hm']})
            cm_fouls[gw].update({odds_data.loc[i,'AwayTeam'] : odds_data.loc[i,'fouls_away']})
            odds_data.loc[i,'fouls_hm_cm']=0
            odds_data.loc[i,'fouls_away_cm']=0
            #corners
            cm_corners[gw].update({odds_data.loc[i,'HomeTeam'] : odds_data.loc[i,'corners_hm']})
            cm_corners[gw].update({odds_data.loc[i,'AwayTeam'] : odds_data.loc[i,'corners_away']})
            odds_data.loc[i,'corners_hm_cm']=0
            odds_data.loc[i,'corners_away_cm']=0
            #yellow
            cm_yellow[gw].update({odds_data.loc[i,'HomeTeam'] : odds_data.loc[i,'yellow_hm']})
            cm_yellow[gw].update({odds_data.loc[i,'AwayTeam'] : odds_data.loc[i,'yellow_away']})
            odds_data.loc[i,'yellow_hm_cm']=0
            odds_data.loc[i,'yellow_away_cm']=0
            #red
            cm_red[gw].update({odds_data.loc[i,'HomeTeam'] : odds_data.loc[i,'red_hm']})
            cm_red[gw].update({odds_data.loc[i,'AwayTeam'] : odds_data.loc[i,'red_away']})
            odds_data.loc[i,'red_hm_cm']=0
            odds_data.loc[i,'red_away_cm']=0            
        else:
            
            cm_goals[gw].update({odds_data.loc[i,'HomeTeam'] : cm_goals[gw-1][odds_data.loc[i,'HomeTeam']] + odds_data.loc[i,'goals_hm']})
            cm_goals[gw].update({odds_data.loc[i,'AwayTeam'] : cm_goals[gw-1][odds_data.loc[i,'AwayTeam']] + odds_data.loc[i,'goals_away']})            
            odds_data.loc[i,'goals_hm_cm']=cm_goals[gw-1][odds_data.loc[i,'HomeTeam']]
            odds_data.loc[i,'goals_away_cm']=cm_goals[gw-1][odds_data.loc[i,'AwayTeam']]
            #shots
            cm_shots[gw].update({odds_data.loc[i,'HomeTeam'] : cm_shots[gw-1][odds_data.loc[i,'HomeTeam']] + odds_data.loc[i,'shots_hm']})
            cm_shots[gw].update({odds_data.loc[i,'AwayTeam'] : cm_shots[gw-1][odds_data.loc[i,'AwayTeam']] + odds_data.loc[i,'shots_away']})            
            odds_data.loc[i,'shots_hm_cm']=cm_shots[gw-1][odds_data.loc[i,'HomeTeam']]
            odds_data.loc[i,'shots_away_cm']=cm_shots[gw-1][odds_data.loc[i,'AwayTeam']]
            #shots_target
            cm_shots_target[gw].update({odds_data.loc[i,'HomeTeam'] : cm_shots_target[gw-1][odds_data.loc[i,'HomeTeam']] + odds_data.loc[i,'shots_target_hm']})
            cm_shots_target[gw].update({odds_data.loc[i,'AwayTeam'] : cm_shots_target[gw-1][odds_data.loc[i,'AwayTeam']] + odds_data.loc[i,'shots_target_away']})            
            odds_data.loc[i,'shots_target_hm_cm']=cm_shots_target[gw-1][odds_data.loc[i,'HomeTeam']]
            odds_data.loc[i,'shots_target_away_cm']=cm_shots_target[gw-1][odds_data.loc[i,'AwayTeam']]
            #fouls
            cm_fouls[gw].update({odds_data.loc[i,'HomeTeam'] : cm_fouls[gw-1][odds_data.loc[i,'HomeTeam']] + odds_data.loc[i,'fouls_hm']})
            cm_fouls[gw].update({odds_data.loc[i,'AwayTeam'] : cm_fouls[gw-1][odds_data.loc[i,'AwayTeam']] + odds_data.loc[i,'fouls_away']})            
            odds_data.loc[i,'fouls_hm_cm']=cm_fouls[gw-1][odds_data.loc[i,'HomeTeam']]
            odds_data.loc[i,'fouls_away_cm']=cm_fouls[gw-1][odds_data.loc[i,'AwayTeam']]
            #corners
            cm_corners[gw].update({odds_data.loc[i,'HomeTeam'] : cm_corners[gw-1][odds_data.loc[i,'HomeTeam']] + odds_data.loc[i,'corners_hm']})
            cm_corners[gw].update({odds_data.loc[i,'AwayTeam'] : cm_corners[gw-1][odds_data.loc[i,'AwayTeam']] + odds_data.loc[i,'corners_away']})            
            odds_data.loc[i,'corners_hm_cm']=cm_corners[gw-1][odds_data.loc[i,'HomeTeam']]
            odds_data.loc[i,'corners_away_cm']=cm_corners[gw-1][odds_data.loc[i,'AwayTeam']]
            #yellow
            cm_yellow[gw].update({odds_data.loc[i,'HomeTeam'] : cm_yellow[gw-1][odds_data.loc[i,'HomeTeam']] + odds_data.loc[i,'yellow_hm']})
            cm_yellow[gw].update({odds_data.loc[i,'AwayTeam'] : cm_yellow[gw-1][odds_data.loc[i,'AwayTeam']] + odds_data.loc[i,'yellow_away']})            
            odds_data.loc[i,'yellow_hm_cm']=cm_yellow[gw-1][odds_data.loc[i,'HomeTeam']]
            odds_data.loc[i,'yellow_away_cm']=cm_yellow[gw-1][odds_data.loc[i,'AwayTeam']]
            #red
            cm_red[gw].update({odds_data.loc[i,'HomeTeam'] : cm_red[gw-1][odds_data.loc[i,'HomeTeam']] + odds_data.loc[i,'red_hm']})
            cm_red[gw].update({odds_data.loc[i,'AwayTeam'] : cm_red[gw-1][odds_data.loc[i,'AwayTeam']] + odds_data.loc[i,'red_away']})            
            odds_data.loc[i,'red_hm_cm']=cm_red[gw-1][odds_data.loc[i,'HomeTeam']]
            odds_data.loc[i,'red_away_cm']=cm_red[gw-1][odds_data.loc[i,'AwayTeam']]
 
odds_data['goals_hm_cm'] = odds_data['goals_hm_cm'].divide(odds_data['Gameweek']-1, fill_value =1)
odds_data['goals_away_cm'] = odds_data['goals_away_cm'].divide(odds_data['Gameweek']-1, fill_value =1)
odds_data['shots_hm_cm'] = odds_data['shots_hm_cm'].divide(odds_data['Gameweek']-1, fill_value =1)
odds_data['shots_away_cm'] = odds_data['shots_away_cm'].divide(odds_data['Gameweek']-1, fill_value =1)
odds_data['shots_target_hm_cm'] = odds_data['shots_target_hm_cm'].divide(odds_data['Gameweek']-1, fill_value =1)
odds_data['shots_target_away_cm'] = odds_data['shots_target_away_cm'].divide(odds_data['Gameweek']-1, fill_value =1)
odds_data['fouls_hm_cm'] = odds_data['fouls_hm_cm'].divide(odds_data['Gameweek']-1, fill_value =1)
odds_data['fouls_away_cm'] = odds_data['fouls_away_cm'].divide(odds_data['Gameweek']-1, fill_value =1)
odds_data['corners_hm_cm'] = odds_data['corners_hm_cm'].divide(odds_data['Gameweek']-1, fill_value =1)
odds_data['corners_away_cm'] = odds_data['corners_away_cm'].divide(odds_data['Gameweek']-1, fill_value =1)
odds_data['yellow_hm_cm'] = odds_data['yellow_hm_cm'].divide(odds_data['Gameweek']-1, fill_value =1)
odds_data['red_hm_cm'] = odds_data['red_hm_cm'].divide(odds_data['Gameweek']-1, fill_value =1)
odds_data['red_away_cm'] = odds_data['red_away_cm'].divide(odds_data['Gameweek']-1, fill_value =1)

final_df=odds_data

del final_df['goals_hm']
del final_df['goals_away']
del final_df['shots_hm']
del final_df['shots_away']
del final_df['shots_target_hm']
del final_df['shots_target_away']
del final_df['fouls_hm']
del final_df['fouls_away']
del final_df['corners_hm']
del final_df['corners_away']
del final_df['yellow_hm']
del final_df['red_hm']
del final_df['red_away']
del final_df['Div']

final_df = final_df.dropna()
final_df = final_df.reset_index(drop=True)

del final_df['HomeTeam']
del final_df['AwayTeam']
del final_df['Date']


###################### Create train and test datasets


train = final_df.loc[final_df['Gameweek'] < 10 ,:]
test = final_df.loc[final_df['Gameweek'] == 10,:]


Y=train['result']
Ytest=test['result']
del train['result']
del test['result']
X=train
Xtest=test

X = X.astype(float)
Xtest = Xtest.astype(float)

############# Dataset without twitter sentiments ######################

X2 = X
Xtest2 = Xtest
del X2['homesentiment']
del X2['awaysentiment']
del Xtest2['homesentiment']
del Xtest2['awaysentiment']

############### RANDOM FOREST #######################################
seed = 7
num_trees = 100
max_features = 13
max_depth=13
model_RF = RandomForestClassifier(n_estimators=num_trees, max_features=max_features,max_depth=max_depth,class_weight="balanced")
model_RF.fit(X2,Y)
y_pred_RF=model_RF.predict(Xtest2)
accuracy_RF = accuracy_score(Ytest, y_pred_RF)*100
print("\nPrediction of Random forest without twittersentiment: ",y_pred_RF)
print("\nAccuracy of prediction using Random forest without twittersentiment: ",accuracy_RF)


model_RF = RandomForestClassifier(n_estimators=num_trees, max_features=max_features,max_depth=max_depth,class_weight="balanced")
model_RF.fit(X,Y)
y_pred_RF=model_RF.predict(Xtest)
accuracy_RF = accuracy_score(Ytest, y_pred_RF)*100
print("\nPrediction of Random forest with twittersentiment: ",y_pred_RF)
print("\nAccuracy of prediction using Random forest with twittersentiment: ",accuracy_RF)


############### XG boost ########################################

# fit model no training data
model_xgb = XGBClassifier(max_depth= 3)
model_xgb.fit(X2, Y)
# make predictions for test data
y_pred_XGB = model_xgb.predict(Xtest2)
# evaluate predictions
accuracy_XGB = accuracy_score(Ytest, y_pred_XGB) * 100

print("\nPrediction of XG boost without twittersentiment: ",y_pred_XGB)
print("\nAccuracy of prediction using XG boost without twittersentiment: ",accuracy_XGB)


# fit model no training data
model_xgb = XGBClassifier(max_depth= 3)
model_xgb.fit(X, Y)
# make predictions for test data
y_pred_XGB = model_xgb.predict(Xtest)
# evaluate predictions
accuracy_XGB = accuracy_score(Ytest, y_pred_XGB) * 100

print("\nPrediction of XG boost  with twittersentiment: ",y_pred_XGB)
print("\nAccuracy of prediction using XG boost  with twittersentiment: ",accuracy_XGB)


###################    Logistic regression   #################################

model_logreg = LogisticRegression(C=1e5, solver='lbfgs', multi_class='multinomial')
# Create an instance of Logistic Regression Classifier and fit the data.
model_logreg.fit(X2, Y)
# make predictions for test data
y_pred_logreg = model_logreg.predict(Xtest2)
# evaluate predictions
accuracy_logreg = accuracy_score(Ytest, y_pred_logreg) * 100
print("\nPrediction using multinomial logistic regression without twittersentiment: ",y_pred_logreg)
print("\nAccuracy of prediction using multinomial logistic regression  without twittersentiment: ",accuracy_logreg)


model_logreg = LogisticRegression(C=1e5, solver='lbfgs', multi_class='multinomial')
# Create an instance of Logistic Regression Classifier and fit the data.
model_logreg.fit(X, Y)
# make predictions for test data
y_pred_logreg = model_logreg.predict(Xtest)
# evaluate predictions
accuracy_logreg = accuracy_score(Ytest, y_pred_logreg) * 100
print("\nPrediction using multinomial logistic regression  with twittersentiment: ",y_pred_logreg)
print("\nAccuracy of prediction using multinomial logistic regression  with twittersentiment: ",accuracy_logreg)

