using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SquirrelWarren : MonoBehaviour, Clock.ITickable {

	public int numDesiredSquirrel=4;
	public GameObject spawnLocation;
	public GameObject squirrelPrefab;
	List<Squirrel> members=new List<Squirrel>();
	private int interSpawnTickDuration=10;
	private int ticksSinceLastSpawn;
	public Globals globals;


	public void Start(){
		ticksSinceLastSpawn=interSpawnTickDuration;
		globals.CLOCK.subscribe(this);
	}

	public void onTick(){
		if ((members.Count<numDesiredSquirrel) && (ticksSinceLastSpawn>=interSpawnTickDuration)){
			//Spawning a new squirrel
			Debug.Log("Spawning a new squirrel");
 			GameObject squirrelObj=Instantiate(squirrelPrefab, spawnLocation.transform.position, Quaternion.identity);
 			Squirrel newSquirrel=squirrelObj.GetComponent<Squirrel>();
 			globals.CLOCK.subscribe(newSquirrel);
 			members.Add(newSquirrel);

 			ticksSinceLastSpawn=0;
		}else{
			ticksSinceLastSpawn+=1;
		}
	}
	public	void onHour(){}
	public 	void onDay(){}
	public	void onMonth(){}
	public 	void onYear(){}
}
