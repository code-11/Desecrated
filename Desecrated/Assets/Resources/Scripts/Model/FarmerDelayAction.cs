using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FarmerDelayAction: FarmerAction{
	public int delayTicks=10;

	public FarmerDelayAction(int delayTicks){
		this.delayTicks=delayTicks;
	}

	public override void onStart(){}

	public override bool isDelay(){
		return true;
	}

	public override bool isFinished(int elapsedTicks){
		return elapsedTicks>delayTicks;
	}
}
