using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Squirrel : MonoBehaviour, Clock.ITickable {

	private Vector3 goal;
	private bool hasGoal=false;
	private int ambitiousness=10;
	private int speed=4;
	private int ticksSinceLastChange=0;
	private int ticksToGoalChange=5;

	public void Update(){
		if(hasGoal){
			float step = speed * Time.deltaTime;
			transform.position = Vector3.MoveTowards(transform.position, goal, step);
		}
	}

	public void onTick(){
		if((!hasGoal) || (ticksSinceLastChange>=ticksToGoalChange)){
			//In the next pass I need to find the point but then raycast down from above to get the terrain point at that point
			//Or perhaps I can access the terrain height value directly somehow.
			Vector3 direction=Random.insideUnitCircle.normalized;
			direction=new Vector3(direction.x,0,direction.y);
			Debug.Log("Setting Squirrel goal "+direction);
			Vector3 position=transform.position+direction*ambitiousness;
			goal=position;
			hasGoal=true;
			ticksSinceLastChange=0;
		}
		ticksSinceLastChange+=1;
	}
	public	void onHour(){}
	public 	void onDay(){}
	public	void onMonth(){}
	public 	void onYear(){}
	
}
