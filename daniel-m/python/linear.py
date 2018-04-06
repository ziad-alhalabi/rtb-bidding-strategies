from DansEvaluateStrategy import evaluateStrategy
from DansDataProcessing import getData
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor

# File Paths
TRAIN_PATH = "we_data/train.csv"
VALIDATION_PATH = "we_data/test.csv"

def main():
	# xgboost: 81 clicks when base bid is 63
    X, Y, X_test, Y_test = getData()
    print("----------------XGBRegressor start----------------")
    xgb = XGBRegressor(max_depth=10, learning_rate=0.08, n_estimators=100, silent=True, objective='reg:linear', booster='gbtree', n_jobs=1, nthread=None, gamma=0, min_child_weight=1, max_delta_step=0, subsample=1, colsample_bytree=1, colsample_bylevel=1, reg_alpha=0, reg_lambda=1, scale_pos_weight=1, base_score=0.5, random_state=0, seed=None, missing=None)
    xgb.fit(X,Y)
    pred = xgb.predict(X_test)
    print("----------------XGBRegressor evaluation----------------")
    evaluateStrategy(pred)
    print("----------------XGBRegressor complete----------------")
	
    print(" ")
    
    print("----------------RandomForestRegressor start----------------")	
    randomf = RandomForestRegressor(n_estimators=64, oob_score=False, random_state=0)
    randomf.fit(X,Y)
    pred = randomf.predict(X_test)
    print("----------------RandomForestRegressor evaluation----------------")		
    evaluateStrategy(pred)	
    print("----------------RandomForestRegressor complete----------------")	

if __name__ == "__main__":
    main()