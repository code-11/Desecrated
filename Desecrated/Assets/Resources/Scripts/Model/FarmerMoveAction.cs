using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FarmerMoveAction : FarmerAction {
	private FarmerPOI moveGoal;
	private float stoppingDistance=.2f;
	private GameObject parent;

	public FarmerMoveAction(FarmerPOI poi,GameObject parent){
		this.moveGoal=poi;
		this.parent=parent;
	}

	public override bool isDelay(){
		return false;
	}

	public override void onStart(){
		setDest();
	}

	public override bool isFinished(int elapsedTicks){
		float distToGoal=(moveGoal.gameObject.transform.position-parent.gameObject.transform.position).magnitude;
		return distToGoal<stoppingDistance;
	}

	private void setDest(){
		UnityEngine.AI.NavMeshAgent agent = parent.GetComponent<UnityEngine.AI.NavMeshAgent>();
        agent.destination = moveGoal.gameObject.transform.position;
	}
}
