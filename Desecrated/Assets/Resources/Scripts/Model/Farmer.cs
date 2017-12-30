using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

[RequireComponent(typeof(NavMeshAgent))]
public class Farmer : MonoBehaviour, Clock.ITickable {

	public List<FarmerAction> poi=new List<FarmerPOI>();

	public Globals globals;

	public void Start(){
		setUpGlobals();

		globals.CLOCK.subscribe(this);
	}

	private void setUpGlobals(){
		GameObject globalsObj=GameObject.FindWithTag("Globals");
		globals=globalsObj.GetComponent<Globals>();
	}

	public void onTick(){
		
		// if (atGoal){
		// 	Debug.Log("Got to "+goal.name);
		// 	int oldIndex=poi.IndexOf(goal);
		// 	int newIndex=oldIndex+1;
		// 	if (newIndex>=poi.Count){
		// 		newIndex=0;
		// 	}
		// 	goal=poi[newIndex];
		// 	setDest();
		// }
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
