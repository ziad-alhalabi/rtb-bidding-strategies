from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
from DansEvaluateStrategy import ortb_evaluateStrategy
from DansDataProcessing import getData

# File Paths
TRAIN_PATH = "we_data/train.csv"
VALIDATION_PATH = "we_data/test.csv"

def main():
    X, Y, X_test, Y_test = getData()
    print("----------------RandomForestRegressor start----------------")
    randomf = RandomForestRegressor(n_estimators=64, oob_score=False, random_state=0)
    randomf.fit(X,Y)
    preds = randomf.predict(X_test)
    print("----------------RandomForestRegressor evaluation (ortb 1)----------------")	
    ortb_evaluateStrategy(preds,1)
    print("----------------RandomForestRegressor evaluation (ortb 2)----------------")	
    ortb_evaluateStrategy(preds,2)	
    print("----------------RandomForestRegressor complete----------------")		
	
    print(" ")
	
    print("----------------AdaBoostRegressor start----------------")
    ab = AdaBoostRegressor()
    ab.fit(X,Y)
    preds = ab.predict(X_test)
    print("----------------AdaBoostRegressor evaluation (ortb 1)----------------")	
    ortb_evaluateStrategy(preds,1)
    print("----------------AdaBoostRegressor evaluation (ortb 2)----------------")	
    ortb_evaluateStrategy(preds,2)	
    print("----------------AdaBoostRegressor start----------------")

if __name__ == "__main__":
    main()