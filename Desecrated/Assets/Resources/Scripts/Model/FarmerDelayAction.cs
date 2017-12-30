using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public abstract class FarmerDelayAction: FarmerAction{
	private int delayTicks=10;

	public override void onStart(){}

	public override bool isDelay(){
		return true;
	}

	public override bool isFinished(int elapsedTicks){
		return elapsedTicks>delayTicks;
	}
}
