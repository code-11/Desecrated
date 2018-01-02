using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public abstract class FarmerAction {

	public class NullAction: FarmerAction{
		public override void onStart(){}
		public override bool isDelay(){return false;}
		public override bool isFinished(int elapsed){
			return true;
		}
	}

	private int elapsedTicks=0;

	public bool isMove(){
		return !isDelay();
	}
	public bool isFinished(){
		if(isFinished(elapsedTicks)){
			return true;
		}else{
			elapsedTicks+=1;	
			return false;
		}
		
	}

	public abstract bool isFinished(int elapsedTicks);

	public abstract bool isDelay();

	public abstract void onStart();
}

