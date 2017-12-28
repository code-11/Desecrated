using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Clock : MonoBehaviour {

	private float lastTickTime;
	private float numTicks=0;
	public float tickDuration=100; 
	private IList<ITickable> events=new List<ITickable>();

	private int TICKS_PER_HOUR=100;
	private int HOURS_PER_DAY=10;
	private int DAYS_PER_MONTH=10;
	private int MONTH_PER_YEAR=10;

	//100 ticks in an hour, 10 hours in a day, 10 days in a month, 10 months in a year.

	public interface ITickable{
		void onTick();
		void onHour();
		void onDay();
		void onMonth();
		void onYear();
	}

	public class DebugTickable : ITickable{
		public void onTick(){
			Debug.Log("Tick");
		}
		public void onHour(){
			Debug.Log("Hour");
		}
		public void onDay(){}
		public void onMonth(){}
		public void onYear(){}
	}

	// Use this for initialization
	void Start () {
		lastTickTime=0;
	}

	public void subscribe(ITickable evt){
		events.Add(evt);
	}
	
	private void callOnTicks(){
		foreach(ITickable evt in events){
			evt.onTick();
		}
	} 

	private void callOnHours(){
		foreach(ITickable evt in events){
			evt.onHour();
		}
	} 

	private void callOnDays(){
		foreach(ITickable evt in events){
			evt.onDay();
		}
	} 

	private void callOnMonths(){
		foreach(ITickable evt in events){
			evt.onMonth();
		}
	} 

	private void callOnYears(){
		foreach(ITickable evt in events){
			evt.onYear();
		}
	}

	// Update is called once per frame
	void Update () {
		if (Time.timeSinceLevelLoad-lastTickTime>tickDuration){
			lastTickTime=Time.timeSinceLevelLoad;
			numTicks+=1;

			callOnTicks();

			if (numTicks % TICKS_PER_HOUR==0){
				//On hour edge trigger
				callOnHours();
			} 
		}
	}
}
