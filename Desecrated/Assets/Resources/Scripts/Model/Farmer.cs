using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

[RequireComponent(typeof(NavMeshAgent))]
public class Farmer : MonoBehaviour, Clock.ITickable {

	public List<FarmerPOI> poi=new List<FarmerPOI>();

	public FarmerPOI goal;
	public bool atGoal;
	public float stoppingDistance=.2f;
	public Globals globals;

	public void Start(){
		setUpGlobals();

		goal=poi[0];
		setDest();

		globals.CLOCK.subscribe(this);
	}

	private void setUpGlobals(){
		GameObject globalsObj=GameObject.FindWithTag("Globals");
		globals=globalsObj.GetComponent<Globals>();
	}

	private void setDest(){
		NavMeshAgent agent = GetComponent<NavMeshAgent>();
        agent.destination = goal.gameObject.transform.position;
	}

	public void onTick(){
		float distToGoal=(goal.gameObject.transform.position-gameObject.transform.position).magnitude;
		Debug.Log(distToGoal);
		atGoal=distToGoal<stoppingDistance;

		if (atGoal){
			Debug.Log("Got to "+goal.name);
			int oldIndex=poi.IndexOf(goal);
			int newIndex=oldIndex+1;
			if (newIndex>=poi.Count){
				newIndex=0;
			}
			goal=poi[newIndex];
			setDest();
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
