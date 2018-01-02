using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

[RequireComponent(typeof(NavMeshAgent))]
public class Farmer : MonoBehaviour, Clock.ITickable {

	public FarmerPOI home;
	public List<FarmerPOI> plots;
	public List<FarmerPOI> supplySheds;

	public List<FarmerAction> actions=new List<FarmerAction>();
	private int curActionIndex=0;
	public Globals globals;

	public void Start(){
		setUpGlobals();
		createActions();
		globals.CLOCK.subscribe(this);
	}

	private void setUpGlobals(){
		GameObject globalsObj=GameObject.FindWithTag("Globals");
		globals=globalsObj.GetComponent<Globals>();
	}

	private void createActions(){
		List<FarmerAction> tempActions=new List<FarmerAction>();

		FarmerAction dudAction=new FarmerAction.NullAction();
		tempActions.Add(dudAction);

		FarmerAction homeAction=new FarmerMoveAction(home,gameObject);
		tempActions.Add(homeAction);
		FarmerAction delayAction=new FarmerDelayAction(2);
		tempActions.Add(delayAction);

		foreach(FarmerPOI plot in plots){
			FarmerAction moveAction=new FarmerMoveAction(plot,gameObject);
			tempActions.Add(moveAction);
			FarmerAction delayAction2=new FarmerDelayAction(2);
			tempActions.Add(delayAction2);
		}

		FarmerAction homeAction2=new FarmerMoveAction(home,gameObject);
		tempActions.Add(homeAction2);
		FarmerAction delayAction3=new FarmerDelayAction(2);
		tempActions.Add(delayAction3);

		actions=tempActions;
	}

	public void onTick(){
		FarmerAction curAction = actions[curActionIndex];
		if(curAction.isFinished()){
			curActionIndex+=1;
			if (curActionIndex>=actions.Count){
				curActionIndex=0;
			}
			FarmerAction nextAction= actions[curActionIndex];
			nextAction.onStart();
		}
	}

	public	void onHour(){}
	public 	void onDay(){}
	public	void onMonth(){}
	public 	void onYear(){}

	public string getName(){
		return "Farmer";
	}
	
	public string provideActivity(){
		int choice= Random.Range(0,3);
		if (choice==0){
			return "Field";
		}else if (choice==1){
			return "Shed";
		}else if (choice==2){
			return "House";
		}else{
			return "Broken";
		}
	}
}
