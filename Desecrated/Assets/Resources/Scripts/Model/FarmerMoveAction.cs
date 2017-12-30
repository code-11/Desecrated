using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FarmerMoveAction : FarmerAction {
	private FarmerPOI moveGoal;
	private float stoppingDistance=.2f;

	public override bool isDelay(){
		return false;
	}

	public override void onStart(){
		setDest();
	}

	public abstract bool isFinished(int elapsedTicks){
		float distToGoal=(goal.gameObject.transform.position-gameObject.transform.position).magnitude;
		return distToGoal<stoppingDistance;
	}

	private void setDest(){
		NavMeshAgent agent = GetComponent<NavMeshAgent>();
        agent.destination = moveGoal.gameObject.transform.position;
	}
}
